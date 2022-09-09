# Easy-TongjiAPI

> 项目仍处于测试状态，功能开发尚未完成，敬请注意

## 项目简介



本项目是同济大学教务系统的信息查询、课表操作、成绩查询等学生教务API的封装，以及登录教务系统等辅助功能的实现。

作者相信，借助本项目，任何一个有python基础的人都可以轻松完成换课、查询成绩等操作；而对那些对python较为熟练的人来说，使用本工具可以让他们如虎添翼，轻松完成自动查成绩、抢课、监视扩课等操作。

**在使用本工具时，请负起责任心。1系统不是你的后花园，请不要对1系统发出过量的请求。**

> 忘了那烦人的Cookie、headers和乱七八糟的接口和格式吧!

### 本项目是：

- 一个任何人都可以轻松使用的Python包
- 一个封装了基本教务功能API接口的工具
- 一个使你不用再去浏览器复制cookies的好帮手

### 本项目不是：

- 抢课工具
- 可以黑入一系统的神奇软件
- 技术力很强的作品



## 安装

### 环境要求

对所有用户，都需要3.0以上的Python环境。

- 对于Windows用户，只需拥有**Python 3.6及以上**的环境即可。在Powershell / cmd / 终端输入`python --version`查看你的版本。若你的Python版本小于3.6，则你需要拥有生成工具。

    - 你可以安装Visual Studio生成工具：[官方链接](https://visualstudio.microsoft.com/zh-hans/downloads/#build-tools-for-visual-studio-2022)

    - 若你有Conda工具，也可以使用 `conda install libpython m2w64-toolchain -c msys2` 来安装生成工具。

- 对于Linux、Unix和Mac用户，需要拥有生成工具（gcc）。大多数发行版都会随附生成工具，在控制台输入 `gcc --version` 查看自己是否已经安装gcc。

### 安装过程

```python
pip install easyTongjiapi
```

对Linux、Unix和Mac用户，可能需要使用 `pip3` 而不是 `pip`。 

