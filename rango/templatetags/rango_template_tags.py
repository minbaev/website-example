'''
Created on Dec 14, 2016

@author: minbaev
'''
from django import template
from rango.models import Category
from django.template.defaultfilters import slugify


register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return{'cats': Category.objects.all,
           'act_cat': cat}

@register.inclusion_tag('rango/category.html')
def slugify_name(name=None):
    slug = slugify(name)
    return {'slugified_name': slug}