#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@date: 2013-01-06
@author: shell.xu
'''
from distutils.core import setup

version = '2.0'
description = 'scheme interrupter written by python'
long_description = ' scheme interrupter written by python.\
  * tail recursion\
  * execute freeze/resume\
  * a little debuger'

setup(
    name='schemepy', version=version,
    description=description, long_description=long_description,
    author='Shell.E.Xu', author_email='shell909090@gmail.com',
    scripts=['scheme'], packages=['schemepy',])
