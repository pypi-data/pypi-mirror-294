import logging
import os
import sys
import time

from ctools import call

clog, flog = None, None

neglect_keywords = [
  "OPTIONS",
  '/scheduleInfo/list',
  '/sys/get_sys_state',
  '/scheduleInfo/tmpList',
  '/sys/getSysLog',
  '/downloadManage/static_file',
  '/downloadManage/static_images'
]


# 文件日志
@call.once
def _file_log(sys_log_path: str = './', log_level: int = logging.INFO, mixin: bool = False) -> logging:
  try:
    os.mkdir(sys_log_path)
  except Exception:
    pass
  log_file = sys_log_path + os.path.sep + "log-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + ".log"
  if mixin:
    handlers = [logging.FileHandler(filename=log_file, encoding='utf-8'), logging.StreamHandler()]
  else:
    handlers = [logging.FileHandler(filename=log_file, encoding='utf-8')]
  logging.basicConfig(level=log_level,
                      format='%(asctime)s-%(levelname)s-%(thread)d-%(module)s(%(funcName)s:%(lineno)d) %(message)s',
                      datefmt='%Y%m%d%H%M%S',
                      handlers=handlers)
  logger = logging.getLogger('ck-flog')
  return logger


# 控制台日志
@call.once
def _console_log(log_level: int = logging.INFO) -> logging:
  handler = logging.StreamHandler()
  logging.basicConfig(level=log_level,
                      format='%(asctime)s-%(levelname)s-%(thread)d-%(module)s(%(funcName)s:%(lineno)d) %(message)s',
                      datefmt='%Y%m%d%H%M%S',
                      handlers=[handler])
  logger = logging.getLogger('ck-clog')
  return logger


class GlobalLogger(object):
  def __init__(self, logger):
    sys.stdout = self
    sys.stderr = self
    self.log = logger

  def write(self, message):
    if message == '\n': return
    global neglect_keywords
    for neglect_keyword in neglect_keywords:
      if neglect_keyword in message: return
    self.log.info(message)

  def flush(self):
    pass


@call.init
def _init_log() -> None:
  global flog, clog
  flog = _file_log(sys_log_path='~/ck-py-log/', mixin=True, log_level=logging.INFO)
  clog = _console_log()
  GlobalLogger(flog)
