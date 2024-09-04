# 安装环境
基础环境安装
``` 
conda create --name quantguard python=3.10.6
conda activate quantguard

```
安装poetry包管理工具

```
pip install poetry

# 解决 poetry publish 问题
pip install urllib3==1.26.6
```

安装项目依赖
```
poetry install
```

开发过程中安装具体某个包
```
poetry add xxx包名
```

启动项目

本地测试
```
请在config目录下创建settings.local.yml填写自己的配置
```
启动
```
quantguard server
```

生成环境安装
```
pip install quantguard==0.1.24 -i https://pypi.Python.org/simple 
```