from django.contrib import admin
from .models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'roll_number', 'room_number', 'hostel_block', 'phone')
    list_filter = ('role', 'hostel_block')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'roll_number', 'room_number')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_pinned', 'created_by', 'created_at')
    list_filter = ('category', 'is_pinned')
    search_fields = ('title', 'content')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'category', 'room_number', 'priority', 'status', 'created_at')
    list_filter = ('status', 'category', 'priority', 'hostel_block')
    search_fields = ('title', 'description', 'student__username', 'room_number')

@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ('day', 'meal_type', 'items', 'timing')
    list_filter = ('day', 'meal_type')

@admin.register(MessReview)
class MessReviewAdmin(admin.ModelAdmin):
    list_display = ('student', 'rating', 'meal_type', 'created_at')
    list_filter = ('rating', 'meal_type')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploader', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')

@admin.register(LostAndFound)
class LostAndFoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'location', 'status', 'reported_by', 'created_at')
    list_filter = ('item_type', 'status')
    search_fields = ('title', 'description', 'location')
