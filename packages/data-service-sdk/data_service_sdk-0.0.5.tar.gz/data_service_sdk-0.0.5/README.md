# data-service-sdk

## Getting started

### 构建

```
修改 config -> version.py 的版本 +1

pip install build

打包，  命令将生成一个 dist 目录
python -m build

本地安装
pip install .\dist\data-service-sdk-0.0.1-py3-none-any.whl

# 上传 pip 包到 pypi
twine upload --repository pypi dist/*

# 上传 pip 包到 test pypi
twine upload --repository testpypi dist/*

# 从pypi 下载
pip install -i https://pypi.org/simple/ data-service-sdk

从pypi 更新
pip install -i https://pypi.org/simple/ -U data-service-sdk

# 从测试 pypi 下载
pip install -i https://test.pypi.org/simple/ data-service-sdk

# 从测试 pypi 更新
pip install -i https://test.pypi.org/simple/ -U data-service-sdk
```

