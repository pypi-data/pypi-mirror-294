import logging
import os
import time


# 文件日志
def flog(base_work_path: str = './', log_level: int = logging.INFO, mixin: bool = False) -> logging:
  try:
    os.mkdir(base_work_path + ".logs")
  except Exception:
    pass
  log_file = base_work_path + ".logs" + os.path.sep + "log-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + ".ck"
  if mixin:
    handlers = [logging.FileHandler(filename=log_file, encoding='utf-8'), logging.StreamHandler()]
  else:
    handlers = [logging.FileHandler(filename=log_file, encoding='utf-8')]
  logging.basicConfig(level=log_level,
                      format='%(asctime)s-%(levelname)s-%(thread)d-%(funcName)s-%(lineno)d - %(message)s',
                      handlers=handlers)
  return logging.getLogger("ck-flog")


# 控制台日志
def clog(log_level: int = logging.INFO) -> logging:
  logging.basicConfig(level=log_level,
                      format='%(asctime)s-%(levelname)s-%(thread)d-%(funcName)s-%(lineno)d - %(message)s',
                      handlers=[logging.StreamHandler()])
  return logging.getLogger("ck-clog")
