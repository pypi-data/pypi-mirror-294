#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2024/9/5 10:39'

import signal
import sys
import time
from threading import Thread, Lock

from kafka import KafkaProducer, errors, KafkaConsumer
from kafka.producer.future import FutureRecordMetadata

from ctools import thread_pool
from ctools.cjson import dumps

"""
import time

from ctools import thread_pool
from ctools.ckafka import CKafka

c = CKafka(kafka_url='192.168.3.160:9094', secure=True)

def send_msg():
  while True:
    time.sleep(3)
    c.send_msg('test', 'test')

thread_pool.submit(send_msg)
c.get_msg('test')
"""

class CKafka:

  def __init__(self, kafka_url: str = '127.0.0.1:9092', secure: bool = False, username: str = 'client', password: str = 'hylink_user_password', consumer_group: str = 'ck-py-kafka-consumer'):
    self.consumer: KafkaConsumer = None
    self.producer: KafkaProducer = None
    self.start_consumer = False
    self.consumer_callback = {"topic_key": []}
    self.consumer_group = consumer_group
    self.kafka_url = kafka_url
    self.init_producer = False
    self.init_consumer = False
    self.secure = secure
    self.username = username
    self.password = password
    self.locker = Lock()
    self.quited = False

  def _create_producer(self) -> KafkaProducer:
    print("[ Producer ] Connecting to Kafka brokers")
    for i in range(0, 6):
      try:
        if self.secure:
          self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_url,
            sasl_plain_username=self.username,
            sasl_plain_password=self.password,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='PLAIN',
            value_serializer=lambda x: dumps(x).encode('utf-8'))
        else:
          self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_url,
            value_serializer=lambda x: dumps(x).encode('utf-8'))
        print("[ Producer ] Connected to Kafka...")
        self.init_producer = True
        return self.producer
      except errors.NoBrokersAvailable:
        print("[ Producer ] Waiting for brokers to become available...")
        time.sleep(3)
    raise RuntimeError("[ Producer ] Failed to connect to brokers within 60 seconds")

  def _create_consumer(self) -> KafkaProducer:
    print("[ Consumer ] Connecting to Kafka brokers")
    for i in range(0, 6):
      try:
        if self.secure:
          self.consumer = KafkaConsumer(
            group_id=self.consumer_group,
            bootstrap_servers=self.kafka_url,
            sasl_plain_username=self.username,
            sasl_plain_password=self.password,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='PLAIN',
            value_deserializer=lambda x: x.decode('utf-8'))
        else:
          self.consumer = KafkaProducer(
            bootstrap_servers=self.kafka_url,
            value_deserializer=lambda x: x.decode('utf-8'))
        print("[ Consumer ] Connected to Kafka...")
        self.init_consumer = True
        return self.consumer
      except errors.NoBrokersAvailable:
        print("[ Consumer ] Waiting for brokers to become available...")
        time.sleep(3)
    raise RuntimeError("[ Consumer ] Failed to connect to brokers within 60 seconds")

  # FutureRecordMetadata 可以添加回调, 来监听是否发送成功
  # r.add_callback(lambda x: print(x))
  # r.get() 可以同步获取结果
  def send_msg(self, topic, msg, key: str=None, partition:int=None) -> FutureRecordMetadata:
    if self.quited: return None
    if not self.init_producer:
      with self.locker:
        if not self.init_producer:
          self._create_producer()
    return self.producer.send(topic=topic, value=msg, key=None if key is None else key.encode('utf-8'), partition=partition)

  def get_msg(self, topics: str, callBack=print):
    if not self.init_consumer:
      with self.locker:
        if not self.init_consumer:
          self._create_consumer()
    for topic in topics.split(','):
      if topic not in self.consumer_callback.keys():
        self.consumer_callback[topic] = []
        self.consumer.subscribe(self.consumer_callback.keys())
      self.consumer_callback[topic].append(callBack)
    if not self.start_consumer:
      t = Thread(target=self._start_consumer_poll)
      t.start()

  def _start_consumer_poll(self):
    self.start_consumer = True
    for msg in self.consumer:
      if self.quited: break
      taskList = []
      funcList = []
      begin_time = time.time()
      for func in self.consumer_callback[msg.topic]:
        if self.quited: break
        f = thread_pool.submit(func, (msg, ))
        taskList.append(f)
        funcList.append(func.__name__)
      for f in taskList:
        if self.quited: break
        f.result()
      end_time = time.time()
      if end_time - begin_time > 1: print(f"kafka consume too slow!!! {funcList} time cost: ", f'{round(end_time - begin_time, 2)}s')
      taskList.clear()
      funcList.clear()

  def shutdown(self):
    self.quited = True
    try: self.consumer.close()
    except Exception: pass
    try: self.producer.close()
    except Exception: pass
    thread_pool.shutdown(wait=True)

