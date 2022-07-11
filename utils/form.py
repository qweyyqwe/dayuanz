# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : form.py
# @Software: PyCharm
"""
链接————————————————————
https://blog.csdn.net/weixin_35757704/article/details/117084841
常用参数——————————————————
CharField：用来接收字符串、文本等任何格式的输入。
参数：
max_length：这个字段值的最大长度。
min_length：这个字段值的最小长度。
required：这个字段是否是必须的。默认是必须的。
error_messages：在某个条件验证失败的时候，给出错误信息。


验证类——————————————————————
EmailField：接收邮件格式，会自动验证邮件是否合法。
FloatField：接收浮点类型，并且如果验证通过后，会将这个字段的值转换为浮点类型。
IntegerField：接收整形，并且验证通过后，会将这个字段的值转换为整形。
URLField：接收url格式的字符串。

"""

from django import forms


class FormTestForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
