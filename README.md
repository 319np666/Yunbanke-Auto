# Yunbanke-auto

云班课作业互评（python3+selenium）

github项目地址：https://github.com/xingjiahui/Yunbanke-auto

# 项目介绍

## 功能

1. 自动登录、进入课程
2. 统计互评作业总数、需要互评数目
3. 根据自定义的评分值对作业进行互评

## 使用须知

- 需要python3环境
- 仅供学习参考使用，任何商业用途后果自负

## 语言库

- python 3.8
- selenium 3.141.0
- pyyaml 5.3.1

# 使用该项目

## 安装库

- pip install selenium
- pip install pyyaml

## 安装浏览器驱动

1. 教程：[Chrome驱动](https://plushine.cn/22094.html#%E6%B5%8F%E8%A7%88%E5%99%A8%E5%8F%8A%E9%A9%B1%E5%8A%A8)
2. 浏览器推荐：Chrome，新版Edge（未做测试）

## 配置文件

1. 下载项目后，解压缩

2. 打开项目，找到 `userData.yml` 文件：

   <img src="https://cdn.jsdelivr.net/gh/xingjiahui/CDN@latest/2020/10/22/1370c4972332f9e384ad9caeb6a36305.png" width="70%"/>

   注意：老师姓名和课程名称要与云班课中一致

## 运行项目

- 运行 `index.py` 文件即可开始互评项目：

  <img src="https://cdn.jsdelivr.net/gh/xingjiahui/CDN@latest/2020/10/22/fa03e7028e0a87e8e121c5b1bb2794ce.png" width="70%"/>

  注意：程序未进行异常处理，运行本项目前请确保配置文件填写正确

- 配置文件正确填写依然报错，请联系作者