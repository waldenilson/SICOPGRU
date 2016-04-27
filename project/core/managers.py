#coding:utf-8
from django.db import models

class UserActiveManager(models.Manager):
	def get_query_set(self):
		qs = super(UserActiveManager, self).get_query_set()
		qs = qs.filter(is_active=True)
		return qs