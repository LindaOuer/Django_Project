from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_user(viewFunction):
    # Example of a decorator: It tests if a user is not authenticated it redirects to the login page otherwise it runs the view
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return viewFunction(request, *args, **kwargs)
    return wrapper


def allowed_users(allowed=[]):
    def decorator(viewFunction):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()
            # print(group)
            for g in group:
                if g.name in allowed:
                    return viewFunction(request, *args, **kwargs)
                else:
                    return HttpResponse('Access denied')
        return wrapper
    return decorator
