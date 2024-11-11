from django.urls import path
from . import views
from .views import update_booking

urlpatterns=[
    path('',views.home,name='home'),

    path('register/', views.Register_user, name='register'),

    path('login/',views.loginUser,name='login'),

    path('pictures/',views.pictures,name='pictures'),

    path('bookings/create/',views.create_booking,name='create_booking'),

    path('bookings/',views.view_bookings,name='view_bookings'),

    path('bookings/update/<int:booking_id>/',views.update_booking,name='update_booking'),

    path('bookings/delete/<int:booking_id>/',views.delete_booking,name='delete_booking'),

    path('checkout/', views.checkout, name='checkout'),

    path('add_to_cart/<int:id>/', views.add_to_cart, name='addtocart'),

    path('view', views.view, name='view'),

    path('success/', views.success, name='success'),

    path('cancel/', views.cancel, name='cancel'),

    path('empty_cart/',views.cart_empty_view,name='cart_empty_view')

]
