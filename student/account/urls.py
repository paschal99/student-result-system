
from django.urls import path
from .views import *

urlpatterns = [

     path('signup', register_user, name='registration'),
     path('', index, name='index'),
     path('login/', login_user, name='login'),
     path('programs/', list_programs, name='list_programs'),
     path('subject/', list_subject, name='list_subject'),
     path('dashboard/', dashboard, name= 'dashboard'),
     path('register_program/', register_program, name='register_program'),
     path('registerStudent/', register_student, name='registerStudent'),
     path('entermarks/', enter_student_marks, name='entermarks'),
     path('view_all_mrks/', view_all_marks,name='view_marks'),
     path('logout/', logout_user, name='logout'),
     path('edit_marks/<int:marks_id>/', edit_marks, name='edit_marks'),
     path('search_student/', search_students, name='search_students'),
     path('register_subject/', register_subject, name='register_subject'),
     path('register_grade/', register_grade, name='register_grade'),
     path('change_password/', change_password, name='change_password'),
]
