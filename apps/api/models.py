from django.db import models

# Create your models here.

class Job(models.Model):
    name = models.CharField(max_length=10, verbose_name='从事的职业')


    class Meta:
        verbose_name = '岗位列表'
        verbose_name_plural = verbose_name


class Question(models.Model):
    question_content = models.CharField(max_length=100, verbose_name='问题')
    job_id = models.ForeignKey(Job, verbose_name='所属岗位', default='')


    class Meta:
        verbose_name = '测试问题'
        verbose_name_plural = verbose_name

class Option(models.Model):
    answer_a = models.CharField(max_length=20, verbose_name='答案A')
    answer_b = models.CharField(max_length=20, verbose_name='答案B')
    answer_c = models.CharField(max_length=20, verbose_name='答案C')
    question_id = models.ForeignKey(Question, verbose_name='所属问题', default='')


    class Meta:
        verbose_name = '测试选项'
        verbose_name_plural = verbose_name


