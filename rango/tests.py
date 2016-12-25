from django.test import TestCase
from django.core.urlresolvers import reverse
from rango.models import Category


        
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=-1,likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)
        
    def test_slug_line_creation(self):
        cat = Category(name=" Random Category String")
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories")
        self.assertQuerysetEqual(response.context['most_liked_categories'], []) 
    
    def test_index_view_with_categories(self):
        add_cat('test',1,1)
        add_cat('temp', 1,1)
        add_cat('txt',1,1)
        add_cat('fortran rocks',1,1)
        
        response = self.client.get(reverse('rango:index'))
                                   
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'fortran rocks')
        
        num_cat = len(response.context['most_liked_categories'])
        self.assertEqual(num_cat, 4)
        
        
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c    