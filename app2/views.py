from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .serializers import BlogSerializer
from .models import Blog
from rest_framework import viewsets

# Create your views here.

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.session.get('username'):
        return redirect('home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    request.session['username'] = user.username
                    response = redirect('home')
                    response.set_cookie('user_logged_in', 'true', max_age=3600)  # Set cookie on login
                    return response
        else:
            initial = {'username': '', 'password': ''}
            form = AuthenticationForm(initial=initial)

        return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.session.get('username'):
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            initial = {'username': '', 'password1': '', 'password2': ''}
            form = UserCreationForm(initial=initial)

        return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('user_logged_in')  # Remove cookie on logout
    request.session.pop('username', None)
    return response

def blog(request):
    if request.session.get('username'):
        return render(request, 'blog.html')
    else:
        return render(request, 'login.html')

def post(request):
    if 'user_logged_in' in request.COOKIES:
        context={
            'username': request.COOKIES.get('user_logged_in'),
        }
    return render(request, 'post.html',context)

def some_view(request):
    # Example of retrieving a cookie value
    user_logged_in = request.COOKIES.get('user_logged_in', 'false')
    return HttpResponse(f'User Logged In: {user_logged_in}')
