from django.shortcuts import redirect

def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'doctor':
            return view_func(request, *args, **kwargs)
        return redirect('/login/')
    return wrapper
