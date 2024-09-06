from functools import wraps

from bottle import request


class PageInfo:
  def __init__(self, page_size, page_index):
    self.page_size = page_size
    self.page_index = page_index


class FormDataParams:
  def __init__(self, data, files):
    self.data = data
    self.files = files

class DictWrapper(dict):
  def __getattr__(self, key):
    return self.get(key)

  def __setattr__(self, key, value):
    self[key] = value

def parameter_handler():
  def return_func(func):
    @wraps(func)
    def decorated(*args, **kwargs):
      if request.method == 'GET':
        queryStr = request.query.decode('utf-8')
        pageInfo = PageInfo(
          page_size=10 if request.headers.get('page_size') is None else int(request.headers.get('page_size')),
          page_index=1 if request.headers.get('page_index') is None else int(request.headers.get('page_index'))
        )
        try:
          return func(params=queryStr, *args, **kwargs)
        except TypeError:
          return func(params=queryStr, pageInfo=pageInfo, *args, **kwargs)
      elif request.method == 'POST':
        content_type = request.get_header('content-type')
        if content_type == 'application/json':
          params = request.json
          return func(params=DictWrapper(params), *args, **kwargs)
        elif content_type and 'multipart/form-data' in content_type:
          form_data = request.forms.decode()
          form_files = request.files.decode()
          params = FormDataParams(data=DictWrapper(form_data), files=form_files)
          return func(params=params, *args, **kwargs)
        else:
          params = request.query.decode('utf-8')
          return func(params=params, *args, **kwargs)
      else:
        return func(*args, **kwargs)

    return decorated

  return return_func
