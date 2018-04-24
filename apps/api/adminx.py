#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin
from .models import Job, Question, Option


class JobAdmin(object):
    list_display = ["name", ]


class QuestionAdmin(object):
    list_display = ["question_content", "job_id"]
    search_fields = ['question_content', ]
    list_filter = ['job_id']



class OptionAdmin(object):
    list_display = ['answer_a', 'answer_b', 'answer_c', 'question_id']



xadmin.site.register(Job, JobAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(Option, OptionAdmin)
