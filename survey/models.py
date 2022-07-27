from django.db import models

# Create your models here.
from django.utils import timezone

from child.models import User


class Question(models.Model):
    """
    问题表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=68, verbose_name="第N期问卷调查   /1.1")
    count = models.TextField(verbose_name="题目内容")
    status = models.IntegerField(verbose_name="状态0存在/   1删除", default=0)
    question_type = models.IntegerField(verbose_name="类型0单选|     1多选|    2判断|    3问答|", default=-1)

    class Meta:
        db_table = 'survey_question'

    def __str__(self):
        return "第{}期问卷调查".format(self.title)


class Answer(models.Model):
    """
    可选答案/回答
    """
    questionid = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题id")
    right_wrong = models.BooleanField(verbose_name="对错", default=True)
    answer_type = models.CharField(max_length=10, null=True, blank=True, verbose_name="选项类型/ A/B/C")
    answer_content = models.CharField(max_length=168, verbose_name="选项内容")

    class Meta:
        db_table = 'survey_answer'


# class AnswerRecord(models.Model):
#     """
#     记录用户回答
#     """
#     userid = models.ForeignKey(User, on_delete=models.CASCADE)
#     questionid = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="问题id")
#     answer = models.TextField(verbose_name="用户回答")
#
#     class Meta:
#         db_table = 'survey_answerrecord'


# #0、添加问题的人
# 1、问题内容   '2108班级谁的年龄最小'
# 2、问题类型    1
# #3、创建时间
# #4、问题状态
#
#
# #0、关联的问题id   AXXX BXXX CXXX DXXX
# 1、选项名称
# 2、选项内容
# 3、是否正确
