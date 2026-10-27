from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/', views.room_list, name='room_list'), 
    path('book/', views.book_room, name='book_room'),
    path('approve/', views.approve_bookings, name='approve_bookings'),
    path('approve/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]