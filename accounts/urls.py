from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # auth_views olarak import ediyoruz
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),  # Ana sayfa
    path('register/', views.register_view, name='register'),  # Kayıt olma URL'si
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma URL'si
    path('login/', views.login_view, name='login'),  # Giriş yapma URL'si
    path('merhaba/', views.merhaba, name='merhaba'),  # Merhaba URL'si
    path('password_reset/', views.send_reset_email, name='password_reset'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('admin/', admin.site.urls),
]
urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('reservation/<int:parking_id>/', views.make_reservation, name='make_reservation'),
    path('review/<int:reservation_id>/', views.leave_review, name='leave_review'),
]

