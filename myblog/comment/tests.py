from django.test import TestCase

# Create your tests here.
from .models import Comment

rock = Comment.objects.create(article="1", author='爸爸', body='啥啊,这是', created_time='2019-08-25')
# blues = Comment.objects.create(article="1", author='爸爸', body='啥啊,这是', created_time='2019-08-25')
Comment.objects.create(article="1", author='儿子', body='好啊', created_time='2019-08-25', reply_to='爸爸', parent='爸爸')
Comment.objects.create(name="Pop Rock", parent=rock)