# 数据库课程设计

### 前言

* 这个是数据库课程安排的大作业，然后做的很粗糙没有考虑的太细致。

* 关于界面的设计参考了这个项目的内容（ https://github.com/zaevi/StudentsManager ）

* 学生宿舍管理系统，使用PyQt5编写，用了pymysql操作mysql库

###  配置

#### 文件

| 文件名    | 作用                                  |
| --------- | ------------------------------------- |
| init.pyw  | 程序入口                              |
| public.py | 存放公共变量                          |
| mainUI.py | 主窗口封装类                          |
| sql.py    | 封装数据库操作                        |
| UI        | UI界面（用Qtdesigner设计，PYUIC生成） |
| Ccontrol  | 学生、宿舍、舍管（类和管理类的封装）  |
| sushe.sql | 建立数据库的语句                      |

  #### 平台

* Python3.X
* PyQt5
* QtDesigner
* pymysql
* mysql

### 系统主要功能界面介绍

* 学生管理界面：

![img](https://i.loli.net/2020/11/23/YzcZmvU4yVsFNha.jpg) 

​                               修改界面：	                                       新建界面：					                       多属性搜索界面：

![img](https://i.loli.net/2020/11/23/snaClodGi1fTNcw.png)

单属性搜索：

![img](https://i.loli.net/2020/11/23/qkh1ZaAxlRV8GOu.jpg) 



* 宿舍管理界面：

![img](https://i.loli.net/2020/11/23/Qg7NmM2v1WtdEYh.jpg) 

​                                       修改界面：	                               多属性搜索界面：	            	  新建界面：		

![img](https://i.loli.net/2020/11/23/UiCqPQE2WNaeSHp.png)

单属性搜索：

![img](https://i.loli.net/2020/11/23/GiWgbmIdvafxjRC.jpg) 



* 宿管管理界面：

![img](https://i.loli.net/2020/11/23/sKT1QGgNoM8i9jd.jpg) 



修改界面：                                            高级搜索：                                          添加界面：

![img](https://i.loli.net/2020/11/23/34EGqU615Klo9sW.png) 

单属性搜索：

![img](https://i.loli.net/2020/11/23/uDcO3veJMTN7Gsf.jpg) 