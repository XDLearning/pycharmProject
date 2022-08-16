# -*- coding: UTF8 -*-
"""
@Project        ：pycharmProject 
@File           ：220814urllib_test.py
@Author         ：Di Xu
@Date           ：2022/8/14 22:01
@Description    : The test for package urllib.
"""
import urllib.request

# 1. 模拟浏览器请求过程，并输出网页html源代码
# response = urllib.request.urlopen('https://www.python.org')
# print(response.read().decode('utf-8'))

# 2. Network-response headers；
# form means imitating forms.
# data = bytes(urllib.parse.urlencode({'name': 'germey'}), encoding='utf-8')
# response = urllib.request.urlopen('https://httpbin.org/post', data=data)
# print(response.read().decode('utf-8'))
# print(type(response))

# 3. Request class
request = urllib.request.Request('https://python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
