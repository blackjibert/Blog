## 基于python3和django3.0的博客网站
## 修改  {% load staicfiles %}
{% load staticfiles %} and {% load adminstatic %} were deprecated in Django 2.1, and removed in Django 3.0.

If you have any of the following in your template:

    {% load staticfiles %}
    {% load static from staticfiles %}
    {% load adminstatic %}
You should replace the tag with simply:

    {% load static %}
### 参考：https://stackoverflow.com/questions/55929472/django-templatesyntaxerror-staticfiles-is-not-a-registered-tag-library