from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordResetForm
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Products, ProductImage, ProductReview


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sua conta foi criada! Faça log in.')
            return redirect('users:login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Sua conta foi Atualizada!')
            return redirect('products:product_list')  

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('products:product_list')  
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html', {'form': form})


@login_required 
def myreviews(request):
    user_reviews = ProductReview.objects.filter(author=request.user).select_related('product')  
    return render(request, 'my_reviews.html', {'reviews': user_reviews})


@login_required  
def mylisting(request):
    products_list = Products.objects.filter()  
    return render(request, 'users/user_listings.html', {'products_list': products_list})


def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                from_email=settings.DEFAULT_FROM_EMAIL,
            )
            messages.success(request, 'Um e-mail com instruções para redefinir sua senha foi enviado.')
            return redirect('users:login')
        else:
            messages.error(request, 'Por favor, insira um e-mail válido.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'reset.html', {'form': form})

# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes