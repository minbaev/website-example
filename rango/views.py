from django.shortcuts import render, reverse, redirect

from django.http import HttpResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required 
from test import test_cookie
from rango.handlers import visitor_cookie_handler

from registration.backends.simple.views import RegistrationView
from django.template.defaultfilters import slugify
from test.test_sax import start

def index (request):
    
        
    print "method---->", request.method, request.user
    print "COOKIES--->", request.session.get('visits')
#     print "COOKIES Visits--->", request.COOKIES.get('visits')
    print "COOKIES Last-visit--->", request.session.get('last_visit')
    
    print "SESSION--->", request.session 
    
    request.session.set_test_cookie()

    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:6]
    pages_list = Page.objects.order_by('-views')[:3]
    context_dict['most_liked_categories'] = category_list
    context_dict['most_viewed_pages'] = pages_list
#     if request.method == 'POST':
#         context_dict['post_message'] = 'Category added!'

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response =  render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    print "method---->", request.method, request.user
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session.get('visits')
    
    response = render(request, 'rango/about.html', context_dict)


    return response

def show_category(request, category_name_slug):
    print "method---->", request.method, request.user
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        number_of_views = category.views
        number_of_views = number_of_views+1
        category.views = number_of_views
        category.save()
        
        pages = Page.objects.filter(category=category).order_by('-views')
         
        context_dict['category'] = category
        context_dict['pages'] = pages
        context_dict['query'] = category.name
        
        pages_from_search = []
        if request.method == 'POST':
            query = request.POST.get('query')
            if query:
                context_dict['query'] = query
                
                pages_from_search = run_query(query.strip())
                for page in pages_from_search:
                    page["page_slug"]=slugify(page["name"])
        
        
        context_dict["pages_from_search"] = pages_from_search
        
        
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context_dict)

@login_required 
def add_category(request):
    print "method---->", request.method, request.user

    form = CategoryForm()
    
    if request.method =='POST':
        form = CategoryForm(request.POST)
        print"input data---->", request.POST['name']
        
        if form.is_valid():
            form.save(commit=True)
            
            return index(request)
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})
    

@login_required 
def add_page(request):
    catid = None
    page_title = None
    page_url = None
    context_dict = {}
    print "CALLED--->", request.method
    if request.method == 'GET':
        print "CATID--->",request.GET.get('catid')
        catid = request.GET.get('catid')
        page_title = request.GET.get('page_title')
        page_url = request.GET.get('page_url')
        
        if catid:
        
            page = Page.objects.get_or_create(category_id=int(catid), title=page_title)
            print "GET_OR_CREATE--->", page[1]
            if page[1]:
                page[0].url = page_url
                page[0].save()
            
                    
            
            
            pages = Page.objects.filter(category_id=int(catid)).order_by('-views')
            context_dict['pages'] = pages
            print "PAGES--->", pages
    
    response = render(request, 'rango/pages.html', context_dict)
    return response

class MyRegistrationView(RegistrationView):
  
    def get_success_url(self, user):
        return '/rango/register_profile/'

def account_settings(request):
    response = render(request, 'rango/account_settings.html', {})
    return response

# def change_profile_website(request):
#     context_dict = {}
#     print "USERNAME--->", request.user.id
# 
#     
#         
#     if request.method == 'POST':
#         profile = UserProfile.objects.get(user_id=request.user.id)
# #         pic = request.POST.get('pic')
#         
#         profile.website = request.POST.get("website")
#         profile.save()
#         return render(request, 'rango/account_settings.html', {})
# 
#             
#     else:
#         return render(request, 'rango/change_website.html', {})
# 
# def change_profile_picture(request):
#     context_dict = {}
#     print "USERNAME--->", request.user.id
# 
#     
#         
#     if request.method == 'POST':
#         profile = UserProfile.objects.get(user_id=request.user.id)
# #         pic = request.POST.get('pic')
#         if 'picture' in request.FILES:
#             profile.picture = request.FILES.get('picture')
#         profile.save()
#         return render(request, 'rango/account_settings.html', {})
# 
#             
#     else:
#         return render(request, 'rango/change_picture.html', {})
    



# from registration.signals import user_registered
# 
# def user_registered_callback(sender,user,request,**kwargs):
#     print "CALLBACK CALLED"
#     profile = UserProfile(user_id=request.user.id)
#     
#     profile.website = request.POST.get("website")
#     if "picture" in request.FILES:
#         profile.picture = request.FILES.get("picture")
#     profile.save()
#     
# user_registered.connect(user_registered_callback)

from rango.bing_search import run_query



def track_page(request):
    page_id = None
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        print "PAGE_ID--->", page_id
        page = Page.objects.get(id=page_id)
        page.views = page.views+1
        page.save()
        
        return HttpResponseRedirect(page.url)
    return HttpResponseRedirect(reverse('rango:index'))

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('rango:index')
        else:
            print(form.errors)
    
    context_dict = {"form": form}
    response = render(request, 'rango/profile_registration.html', context_dict)
    return response    

@login_required
def profile(request, username):
    context_dict={}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect("rango/index")
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website,'picture': userprofile.picture})
    
    if request.user.username == username:
        if request.method =="POST":
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if form.is_valid():
                form.save(commit=True)
                return redirect('rango:profile', user.username)
            else:
                print(form.errors)
    context_dict['userprofile'] = userprofile
    context_dict['selecteduser'] = user
    context_dict['form'] = form    
    response = render(request, 'rango/profile.html', context_dict)
    return response
    
@login_required
def list_profiles(request):
    userprofile_list = UserProfile.objects.all()
    print "Username--->", UserProfile.objects.get(user=request.user).user.username
    print "Username--->", request.user.username
    
    return render (request, 'rango/list_profiles.html',
                   {'userprofile_list' : userprofile_list})
    
    
@login_required 
def like_category(request):
    cat_id=None
    if request.method == "GET":
        cat_id = request.GET.get('category_id')
        my_likes=0
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                my_likes = cat.likes + 1
                cat.likes = my_likes
                cat.save()
    return HttpResponse(my_likes)

def get_category_list(max_length=0, start_with=""):
    cats=[]
    if start_with:
        if start_with=="":
            cats = Category.objects.all()
            return cats
        cats = Category.objects.filter(name__istartswith=start_with)
    
    if max_length > 0:
        if max_length < len(cats):
            cats = cats[:max_length]
    
    return cats
def get_suggested_category(request):
    cats = []
    start_with=""
    context_dict = {}
    if request.method =="GET":
        start_with = request.GET.get('suggestion')
        print "QUERY--->", start_with, "|"   

        cats = get_category_list(10, start_with) 
        print "CATS--->", cats              
        
    context_dict['cats'] = cats
    response = render(request, 'rango/cats.html', context_dict )
    return response

def display_all_categories(request):
    cats=[]
    if request.method == 'GET':
        cats = Category.objects.all()
    
    response = render(request, 'rango/cats.html', {'cats':cats})
    return response
           
                
                  
            