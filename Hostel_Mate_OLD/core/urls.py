from django.urls import path
from . import views

urlpatterns = [
    # Auth & Dashboards
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Announcements
    path('announcements/', views.announcements_list, name='announcements'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/delete/<int:pk>/', views.announcement_delete, name='announcement_delete'),

    # Complaints
    path('complaints/', views.complaints_list, name='complaints'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaints/<int:pk>/status/', views.complaint_update_status, name='complaint_update_status'),

    # Mess Menu & Feedback
    path('mess/', views.mess_menu_view, name='mess_menu'),
    path('mess/update/', views.mess_menu_update, name='mess_menu_update'),
    path('mess/review/', views.mess_review_create, name='mess_review_create'),

    # Resources
    path('resources/', views.resources_list, name='resources'),
    path('resources/create/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/toggle/', views.resource_toggle_status, name='resource_toggle_status'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),

    # Lost & Found
    path('lost-found/', views.lost_found_list, name='lost_found'),
    path('lost-found/create/', views.lost_found_create, name='lost_found_create'),
    path('lost-found/<int:pk>/toggle/', views.lost_found_toggle_status, name='lost_found_toggle_status'),
    path('lost-found/<int:pk>/delete/', views.lost_found_delete, name='lost_found_delete'),

    # Admin Management
    path('admin-students/', views.admin_students_list, name='admin_students'),
    path('admin-students/<int:pk>/edit/', views.admin_student_edit, name='admin_student_edit'),
]
