from setuptools import setup, find_packages

setup(
  name="gomyck-tools",
  version="1.0.1",
  author="gomyck",
  author_email="hao474798383@163.com",
  description="A ctools for python development by hao474798383",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://blog.gomyck.com",
  packages=["ctools"],  # 自动发现并包含包内所有模块
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.8",  # 指定最低 Python 版本
  install_requires=[        # 你的包依赖的其他包
    "jsonpickle>=3.2.2",
    "SQLAlchemy>=2.0.32",
    "chardet>=5.2.0",
    "psycopg2-binary>=2.9.9",
    "croniter>=3.0.3",
    "pyautogui>=0.9.54",
    "gmssl>=3.2.2",
    "psutil>=6.0.0"
  ],
)

# 安装依赖, 并生成构建包
# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel

# 构建之前要删除 build dist egg 三个目录
# twine upload dist/*
