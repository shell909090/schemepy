# 简述 #

schemepy是使用python写的支持尾递归的scheme解释器。

# scheme #

scheme是通常的执行入口。执行.cdp文件时按照coredump文件加载，执行.scc文件时会按照编译后内容加载，其他扩展名按照scheme源文件加载。不加任何参数时进入交互模式。

## 参数 ##

* -c: 编译文件
* -d: 调试模式
* -h: 帮助
* -i: 格式化文件
* -n: 禁用coredump
* -p: 显示解析树

## 编译 ##

编译会将.scm文件编译为.scc文件。编译后的文件主要包括解析树，载入.scc可以避免再次解析。

## 格式化 ##

格式化会读入文件并按照格式重新打印出来。

# break #

一个简单的例子，描述了中断/再执行模式是如何工作的。

# 授权 #

    Copyright (C) 2012 Shell Xu

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
