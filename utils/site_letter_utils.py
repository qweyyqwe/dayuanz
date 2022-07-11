# -*- coding: utf-8 -*-
# @Time    : 2021/11/22
# @File    : utils.py
# @Software: PyCharm


from site_letter.models import SendMail


def set_mass_send_site_mail(user):
    """
    获取用户为读取的群发站内信

    将未添加到sitemail中的群发内容添加进去
    1、获取所有的群发站内信数据---只获取用户注册之后的群发站内信消息
    2、获取需要添加站内信的数据id
    3、添加站内信数据
    :return:
    """
    # [1, 2, 3, 4]
    site_mail_type = SendMail.objects.filter(site_mail_type=0, send_time__gte=user.date_joined).values_list(
        'content_id', flat=True)
    # [1, 2, ]
    user_all_site_mail = SendMail.objects.filter(user=user).values_list('content_id', flat=True)
    # 获取需要添加站内信的数据id
    need_add_id = list(set(site_mail_type) - set(user_all_site_mail))
    for content_id in need_add_id:
        # 添加站内信数据
        site_mail = SendMail.objects.create(content_id=content_id, user=user)
        site_mail.save()
