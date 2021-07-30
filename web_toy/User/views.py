from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import LoginForm

# Create your views here.
# def home(request):
#     user_id = request.session.get('user')
#     if user_id:
#         user = User.objects.get(pk = user_id)
#         return HttpResponse(user.username)
#     return HttpResponse('Home')
def home(request):
    user_id = request.session.get('user')
    
    if user_id:
        user = User.objects.get(pk = user_id)
    
    return render(request, 'home.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['re_password']

        res_data = {}
        if not(username and password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != re_password:
            res_data['error'] = '비밀번호를 확인해주세요'
        else:
            user = User(
                username = username,
                password = make_password(password)
            )
            user.save()

        return render(request, 'register.html', res_data)
    
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#     elif request.method == 'POST':
#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
        
#         res_data = {}
#         if not(username and password):
#             res_data['error'] = '모든 값을 입력해야합니다.'
#         else:
#             user = User.objects.get(username = username)
#             if check_password(password, user.password):
#                 request.session['user'] = user.id
#                 return redirect('/')
#             else:
#                 res_data['error'] = '사용자 이름 혹은 비밀번호를 확인해주세요.'
        
#         return render(request, 'login.html', res_data)
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # session
            request.session['user'] = form.user_id
            return redirect('/')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form' : form})


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')

