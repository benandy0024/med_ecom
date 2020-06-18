
from django.urls import path,reverse_lazy
from .views import register_page,login_page,AccountHomeView,UserUpdateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from products.views import UserProductHistoryView
urlpatterns = [
      path('',AccountHomeView.as_view(),name='account'),
    path('details', UserUpdateView.as_view(), name='user-update'),
      path('register', register_page, name='register'),
   path('login', login_page,name='login'),
path('logout/', LogoutView.as_view(), name='logout'),
    #user history
path('history/product', UserProductHistoryView.as_view(), name='history'),
    #password management
path(r'password/change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('accounts:password_change_done')
    ), name='password_change'),

path(r'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
     ),



path(r'password/reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'),
path(r'password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
path(r'password/reset/\
        (?P<uidb64>[0-9A-Za-z_\-]+)/\
        (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

path(r'password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

]

