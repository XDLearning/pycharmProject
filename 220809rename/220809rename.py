# -*- coding: UTF8 -*-
"""
@Project        ：pythonProject 
@File           ：220809rename.py
@Author         ：Di Xu
@Date           ：2022/8/9 16:21
@Description    : 批量文档重命名程序
"""
import os

# 1.获取路径下所有旧的文件名
path = 'name'
folder_list = os.listdir(path)
print("="*50)
print(folder_list)
print("-"*50)
# 2.旧的文件名改成新的文件名
# 创建循环
n = 0
for i in folder_list:
    # 输入要添加的内容
    print("要修改的文件名为：%s" % i)
    content_tag = input("请输入文件的内容标签，如latex，beamer：")
    style_tag = input("请输入文件的类型标签编号，1.手册，2.教材，3.其他：")
    # is_tag = input("请输入文件的功能类型编号，0.未阅读，1.已阅读：")

    # 数字标签和类型对应
    if style_tag == '1':
        style_tag = '手册'
    elif style_tag == '2':
        style_tag = '教材'
    else:
        style_tag = '其他'

    # 新的文件名
    old_name = path + os.sep + i
    show_name = content_tag + '_' + style_tag + '_' + '0_' + i
    newname = path + os.sep + show_name
    os.rename(old_name, newname)
    n += 1
    print("%d : %s ==> %s" % (n, i, show_name))
    print("-"*50)
