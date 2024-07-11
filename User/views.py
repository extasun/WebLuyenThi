from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .form import SignUpForm
from django.contrib.auth import authenticate, login, logout
from .models import StudentUser
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    def get(self, request):
        return render(request, 'homepage/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            error_message = 'Vui lòng nhập đủ thông tin!'
            context = {'username': username, 'error_message': error_message}
            return render(request, 'homepage/login.html', context)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            request.session['id'] = user.id
            request.session['full_name'] = user.first_name + ' ' + user.last_name
            return redirect('/')
        else:
            error_message = 'Tài khoản không tồn tại hoặc mật khẩu sai!'
            context = {'username': username, 'error_message': error_message}
            return render(request, 'homepage/login.html', context)

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'homepage/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            # Tạo một user mới
            user = StudentUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            
            # Đăng nhập ngay sau khi đăng ký
            login(request, user)
            
            # Chuyển hướng đến trang chủ hoặc trang đã đăng ký thành công
            return redirect('/')
        
        # Nếu form không hợp lệ, render lại form với các thông tin lỗi
        return render(request, 'homepage/signup.html', {'form': form})

class LogoutView(LoginRequiredMixin, View):
    login_url = '/Userlogin/'
    def get(self, request):
        username = request.session.get('username', '')
        error_message = 'Đăng xuất thành công!'
        context = {'username': username, 'error_message': error_message}
        logout(request)
        
        # Xóa session
        request.session.flush()
        
        return redirect('core:index')
