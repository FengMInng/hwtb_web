#coding=utf-8
from django.contrib import admin

# Register your models here.
from .models import Question,Choice

admin.site.register(Question)

admin.site.register(Choice)

