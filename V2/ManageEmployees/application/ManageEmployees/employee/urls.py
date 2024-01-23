from django.urls import path
from .views import *

urlpatterns = [
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    #test à supprimer
    path('rh/', rh_dashboard, name='welcome'),
    #___ Admin
    path('listEmployees/', listEmployees, name='listEmployees'),  
    path('deleteEmployee/<int:employee_id>/', deleteEmployee, name='deleteEmployee'),
    path('updateEmployee/<int:employee_id>/', updateEmployee, name='updateEmployee'),
    path('filter-employees/<str:position>/', filter_employees, name='filter_employees'),

    #___ AllEmployees
    path('create_profile/', create_profile, name='create_profile'),

]