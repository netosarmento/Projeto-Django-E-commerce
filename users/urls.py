from django.urls import path, reverse_lazy
from .views import register,profile,myreviews,mylisting, login_view, password_reset_view
from django.contrib.auth import views as auth_views

app_name= 'users'
urlpatterns = [
     path('', register,name="register"),
     path('profile/',profile,name="profile"),
     path('myreviews/',myreviews,name="myreviews"),
     path('listing/',mylisting,name="listing"),
     path('login/', login_view,name='login'),
     path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
     # Rotas para redefinição de senha
     path('passwordreset/', password_reset_view,name='password_reset'),
     
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='registration/password_reset_confirm.html',
         success_url=reverse_lazy('users:password_reset_complete')
     ),
     name='password_reset_confirm'),
    
    path(
    'reset/done/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ),
    name='password_reset_complete'),
]
# Developed by: Tech Norte Soluções
# Instagram: norte_dev
# MEI instagram: @tech.nortesolucoes