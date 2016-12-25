'''
Created on Dec 12, 2016

@author: minbaev
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    python_pages = [
        {"title":"Official Python Tutorial",
         "url":"http://docs.python.org/2/tutorial/",
         "views":100},
        {"title":"How To Think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/",
         "views":200},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/",
         "views":5}
    ]
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views":30},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/",
         "views":150},
        {"title":"How To Tango With Django",
         "url":"http://www.tangowithdjango.com/",
         "views":10}
    ]
    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/",
         "views":0},
        {"title":"Flask",
         "url":"http://flask.pocoo.org",
         "views":300}
    ]
    
    categories_dict = {
        "Python":{"pages":python_pages,"views":128,"likes":64},
        "Django":{"pages":django_pages,"views":64,"likes":32},
        "Other Frameworks":{"pages":other_pages,"views":32,"likes":16}
    }
    
    for cat, cat_data in categories_dict.iteritems():
        c = add_category(cat,cat_data["views"], cat_data["likes"])
        print(c)
        print(cat)
        for page in cat_data["pages"]:
            add_page(c, page['title'],page['url'],page['views'])
    
    #Print out categories
    for cat in Category.objects.all():
        for page in Page.objects.filter(category = cat):
            print("- {0} - {1}".format(str(cat), str(page)))
        
    
def add_page(cat, title, url, views=0):
    
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p
    
def add_category(name, views, likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes )[0]
    c.save()
    return c

# Start execution
if __name__ =='__main__':
    print('Starting Rango population script')
    populate()
    
