from django.contrib import admin

# Register your models here.


from .models import User, Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('count', 'title', 'question_type', )
    list_filter = ('count', 'title', 'question_type', )
    list_per_age = 10  # 分页
    search_fields = ('count', 'title', 'question_type', )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_content', 'answer_type', )
    list_filter = ('answer_content', 'answer_type', )
    list_per_age = 10  # 分页
    search_fields = ('answer_content', 'answer_type', )


# @admin.register(AnswerRecord)
# class AnswerRecordAdmin(admin.ModelAdmin):
#     list_display = ('answer',)
#     list_filter = ('answer',)
#     list_per_age = 10  # 分页
#     search_fields = ('answer',)
