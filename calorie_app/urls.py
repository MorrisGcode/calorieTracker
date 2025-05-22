from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.calorie_tracker_view, name='calorie_tracker'),
    path('remove/<int:item_id>/', views.remove_food_item, name='remove_food_item'),
    path('reset/', views.reset_calories, name='reset_calories'),
]