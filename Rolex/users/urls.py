from django.urls import path
from .views import *
from users.models import CustomLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name="users/Login.html"),name='login'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
         name='password_reset'),
    path('profile/',profile,name='profile'),
    path('logout/',CustomLogoutView.as_view(template_name="users/logout.html"),name='logout'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('add-to-basket/',cart_view,name='basket-view'),
    path('add-to-basket/<int:product_id>',add_to_basket,name='add-to-basket'),
    path('increase_quantity/<int:item_id>',increase_quantity,name='increase_quantity'),
    path('decrease-quantity/<int:item_id>',decrease_quantity,name='decrease_quantity'),
    path('remove_item/<int:item_id>',remove_item,name='remove_item'),
    path('process_order/',process_order,name='process_order'),
    path('order_cancel/',cancel_order,name='cancel_order'),
    path('order_confirmation/',confirm_order,name='order_confirmation'),
    path('order_success/<int:order_id>',order_success,name='order_success'),
    path('order_history/',history_orders,name='history_orders'),
]