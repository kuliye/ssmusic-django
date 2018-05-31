from  django.shortcuts import redirect
def login_check(func):
    def login_check_func(request,*args,**kwargs):
        if request.session.has_key('userid'):
            return func(request,*args,**kwargs)
        else:
            red=redirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_check_func