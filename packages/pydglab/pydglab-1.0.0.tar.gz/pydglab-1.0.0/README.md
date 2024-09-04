# DGLAB-python-driver

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydglab) ![GitHub Release](https://img.shields.io/github/v/release/shilapi/dglab-python-driver)
![PyPI - Version](https://img.shields.io/pypi/v/pydglab)
![GitHub last commit](https://img.shields.io/github/last-commit/shilapi/dglab-python-driver)
[![CodeFactor](https://www.codefactor.io/repository/github/shilapi/dglab-python-driver/badge)](https://www.codefactor.io/repository/github/shilapi/dglab-python-driver)
![PyPI - License](https://img.shields.io/pypi/l/pydglab) 

 PyDGLAB - A Third-party DGLAB Python Driver

 一个第三方的郊狼驱动器。

## 特性

- 采用蓝牙直接连接郊狼设备
- 采用asyncio实现
- 易上手，相比于去看官方文档那真是简简又单单啊

## 开始之前

> ⚠️ **CAUTION**
> 
> **本模块的使用可能伴随着人身安全风险，请确保您在使用前知道自己在做什么。作者对使用本模块造成的一切损失概不负责。**
> 
> **The use of this module may be accompanied by personal safety risks, please make sure you know what you're doing before using it. The author is not responsible for any losses caused by the use of this module.**

## 快速上手

**注意：郊狼2.0与3.0的使用方式并不相同！！！**

### 安装

```bash
pip install pydglab
```

### 实例化并开启连接

#### 对于郊狼2.0

```python
import asyncio
import pydglab
from pydglab import model_v2

async def _():
    dglab_instance = pydglab.dglab()
    await dglab_instance.create()
    # Do whatever u want here

asyncio.run(_())
```

#### 对于郊狼3.0

```python
import asyncio
import pydglab
from pydglab import model_v3

async def _():
    dglab_instance = pydglab.dglab_v3()
    await dglab_instance.create()
    # Do whatever u want here

asyncio.run(_())
```

## 文档

 请查阅demo_v2.py或demo_v3.py（取决于你所连接的设备是郊狼2.0还是3.0）来获取更多信息。

 由于作者懒得写独立的文档了，因此关于模块的调用问题，请查阅内嵌的文档字符串(DocStrings)。

 目前已支持郊狼2.0与3.0！

