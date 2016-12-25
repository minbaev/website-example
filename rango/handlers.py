'''
Created on Dec 18, 2016

@author: minbaev
'''
from datetime import datetime



def visitor_cookie_handler(request):
#     visits = int(request.COOKIES.get('visits', '1'))
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    print "TIME--->", str(datetime.now())
    
#     last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    print "LAST_VISIT_COOKIE--->", last_visit_cookie

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    print "LAST_VISIT_COOKIE--->", last_visit_cookie[:7]
    
    if (datetime.now()-last_visit_time).total_seconds() > 5:
        visits = visits + 1
#         response.set_cookie('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
#         response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie
    
#     response.set_cookie('visits', visits)
    request.session['visits'] = visits
    
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val