FastKit: FastFlyer 框架配套开发工具包
-------------------------------------

|License| |Verison|

[TOC]

项目介绍
--------

FastKit 是 Python 开发工具包，集成了 增强 HTTP 请求、MySQL、Redis
等通用方法。

.. image:: fastkit/static/logo.png
   :alt: FastKit

项目依赖
--------

python版本：\ ``>3, <4``

安装方法
--------

使用下面的命令直接安装最新版本

.. code:: shell

   pip3 install fastkit --index-url https://mirrors.cloud.tencent.com/pypi/simple/

注：若安装报错，可以 case by case 解决，或者提供报错截图。

功能说明
--------

``注：功能将持续更新，使用请查阅功能配套说明文档。``

| \| **功能** \| **说明文档** \| **备注**
| \|------------------------------------------------------------|---------------------------------------------
  \| **日志打印** \| `fastkit/logging <fastkit/logging>`__ \|
  同时支持本地\ ``Console``\ 、文件日志打印
| \| **HTTP请求** \| `fastkit/httpx <fastkit/httpx>`__ \|
  提供\ ``HTTP``\ 状态码对象和\ ``HTTP``\ 增强型客户端等功能 \|
  **配置中心** \| `fastkit/configure <fastkit/configure>`__ \|
  鹅厂内部版本特有，开源版本已剔除
| \| **服务发现** \| `fastkit/discovery <fastkit/discovery>`__ \|
  鹅厂内部版本特有，开源版本已剔除
| \| **监控告警** \| `fastkit/monitor <fastkit/monitor>`__ \|
  鹅厂内部版本特有，开源版本已剔除
| \| **数据缓存** \| `fastkit/cache <fastkit/cache>`__ \|
  对接\ ``Redis``\ 和\ ``Cacheout``\ 组件
| \| **数据存储** \| `fastkit/database <fastkit/database>`__ \| 基于
  ``SQLAlchemy``\ 和 ``Dataset``
  封装，同时提供\ ``ORM``\ 和\ ``SQL``\ 使用模式
| \| **消息队列** \| `fastkit/message <fastkit/message>`__ \|
  对接\ ``kafka``\ 组件，提供生产者和消费者模型
| \| **基础功能** \| `fastkit/utils <fastkit/utils>`__ \|
  提供字符串格式化等各种工具函数

开发规范&建议
-------------

-  推荐插件或设置：

   -  懒人三套：\ ``Python``\ 、\ ``autoDocstring``\ 、\ ``yapf``\ ，建议开启保存自动格式化代码设置
   -  懒人进阶：安装\ ``Copilot``\ 插件，自动猜想代码

.. |License| image:: fastkit/static/License-icon.svg
.. |Verison| image:: fastkit/static/Python-3.6.8+-icon.svg
