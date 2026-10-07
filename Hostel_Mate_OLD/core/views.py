from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Q
from datetime import datetime
from django.contrib.auth.models import User

from .models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound
from .forms import (
    UserRegisterForm, ProfileUpdateForm, ComplaintForm, AnnouncementForm,
    MessMenuForm, MessReviewForm, ResourceForm, LostAndFoundForm
)

def get_or_create_profile(user):
    """Utility to ensure UserProfile exists for every user."""
    profile, created = UserProfile.objects.get_or_create(user=user)
    if user.is_superuser and profile.role != 'admin':
        profile.role = 'admin'
        profile.save()
    return profile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            role = form.cleaned_data.get('role', 'student')
            roll_number = form.cleaned_data.get('roll_number', '')
            room_number = form.cleaned_data.get('room_number', '')
            hostel_block = form.cleaned_data.get('hostel_block', 'Block A')
            phone = form.cleaned_data.get('phone', '')

            UserProfile.objects.create(
                user=user,
                role=role,
                roll_number=roll_number,
                room_number=room_number,
                hostel_block=hostel_block,
                phone=phone
            )
            
            login(request, user)
            messages.success(request, f"Welcome to HostelMate, {user.username}! Account created successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegisterForm()
    
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            get_or_create_profile(user)
            messages.success(request, f"Logged in successfully as {user.username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)
    
    if profile.is_admin():
        # Admin / Warden Analytics
        total_students = UserProfile.objects.filter(role='student').count()
        total_complaints = Complaint.objects.count()
        pending_complaints = Complaint.objects.filter(status='pending').count()
        in_progress_complaints = Complaint.objects.filter(status='in_progress').count()
        resolved_complaints = Complaint.objects.filter(status='resolved').count()
        total_resources = Resource.objects.filter(is_available=True).count()
        open_lost_found = LostAndFound.objects.filter(status='open').count()
        
        avg_rating = MessReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0.0

        recent_complaints = Complaint.objects.all().select_related('student')[:5]
        recent_announcements = Announcement.objects.all()[:4]
        
        context = {
            'profile': profile,
            'is_admin_dashboard': True,
            'total_students': total_students,
            'total_complaints': total_complaints,
            'pending_complaints': pending_complaints,
            'in_progress_complaints': in_progress_complaints,
            'resolved_complaints': resolved_complaints,
            'total_resources': total_resources,
            'open_lost_found': open_lost_found,
            'avg_rating': round(avg_rating, 1),
            'recent_complaints': recent_complaints,
            'recent_announcements': recent_announcements,
        }
        return render(request, 'core/dashboard_admin.html', context)
    else:
        # Student Dashboard
        today_day = datetime.now().strftime('%A') # e.g. Monday
        my_complaints = Complaint.objects.filter(student=request.user)[:5]
        pinned_announcements = Announcement.objects.filter(is_pinned=True)[:3]
        latest_announcements = Announcement.objects.filter(is_pinned=False)[:4]
        today_mess_menu = MessMenu.objects.filter(day=today_day)
        recent_resources = Resource.objects.filter(is_available=True)[:4]
        recent_lost_found = LostAndFound.objects.filter(status='open')[:4]
        
        context = {
            'profile': profile,
            'is_admin_dashboard': False,
            'today_day': today_day,
            'my_complaints': my_complaints,
            'pinned_announcements': pinned_announcements,
            'latest_announcements': latest_announcements,
            'today_mess_menu': today_mess_menu,
            'recent_resources': recent_resources,
            'recent_lost_found': recent_lost_found,
        }
        return render(request, 'core/dashboard_student.html', context)

# --- PROFILE VIEWS ---

@login_required
def profile_view(request):
    profile = get_or_create_profile(request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if form.is_valid():
            form.save()
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            messages.success(request, "Your profile details have been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'core/profile.html', {
        'profile': profile,
        'form': form
    })

# --- ANNOUNCEMENTS ---

@login_required
def announcements_list(request):
    profile = get_or_create_profile(request.user)
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    announcements = Announcement.objects.all()
    if query:
        announcements = announcements.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category:
        announcements = announcements.filter(category=category)
        
    form = AnnouncementForm()
    return render(request, 'core/announcements.html', {
        'profile': profile,
        'announcements': announcements,
        'form': form,
        'query': query,
        'selected_category': category
    })

@login_required
def announcement_create(request):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('announcements')
        
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "Announcement posted successfully!")
        else:
            messages.error(request, "Failed to post announcement. Check inputs.")
    return redirect('announcements')

@login_required
def announcement_delete(request, pk):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied.")
        return redirect('announcements')
        
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, "Announcement deleted successfully.")
    return redirect('announcements')

# --- COMPLAINTS ---

@login_required
def complaints_list(request):
    profile = get_or_create_profile(request.user)
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    query = request.GET.get('q', '')

    if profile.is_admin():
        complaints = Complaint.objects.all().select_related('student')
    else:
        complaints = Complaint.objects.filter(student=request.user)

    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category_filter:
        complaints = complaints.filter(category=category_filter)
    if query:
        complaints = complaints.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(room_number__icontains=query))

    form = ComplaintForm(initial={
        'room_number': profile.room_number or '',
        'hostel_block': profile.hostel_block or 'Block A'
    })

    return render(request, 'core/complaints.html', {
        'profile': profile,
        'complaints': complaints,
        'form': form,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'query': query
    })

@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()
            messages.success(request, "Complaint submitted successfully! Warden will review it shortly.")
        else:
            messages.error(request, "Failed to submit complaint. Check your input.")
    return redirect('complaints')

@login_required
def complaint_detail(request, pk):
    profile = get_or_create_profile(request.user)
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permissions
    if not profile.is_admin() and complaint.student != request.user:
        messages.error(request, "Permission denied.")
        return redirect('complaints')
        
    return render(request, 'core/complaint_detail.html', {
        'profile': profile,
        'complaint': complaint
    })

@login_required
def complaint_update_status(request, pk):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied.")
        return redirect('complaints')
        
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        admin_remarks = request.POST.get('admin_remarks', '')
        
        if new_status in dict(Complaint.STATUS_CHOICES):
            complaint.status = new_status
            complaint.admin_remarks = admin_remarks
            complaint.save()
            messages.success(request, f"Complaint #{complaint.id} status updated to {complaint.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")
            
    return redirect('complaint_detail', pk=pk)

# --- MESS SERVICES & REVIEWS ---

@login_required
def mess_menu_view(request):
    profile = get_or_create_profile(request.user)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    active_day = request.GET.get('day', datetime.now().strftime('%A'))
    if active_day not in days:
        active_day = 'Monday'
        
    menus = MessMenu.objects.filter(day=active_day)
    reviews = MessReview.objects.all().select_related('student')[:15]
    avg_rating = MessReview.objects.aggregate(Avg('rating'))['rating__avg'] or 0.0

    review_form = MessReviewForm()
    menu_form = MessMenuForm(initial={'day': active_day})

    return render(request, 'core/mess_menu.html', {
        'profile': profile,
        'days': days,
        'active_day': active_day,
        'menus': menus,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_form': review_form,
        'menu_form': menu_form,
    })

@login_required
def mess_menu_update(request):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied.")
        return redirect('mess_menu')
        
    if request.method == 'POST':
        day = request.POST.get('day')
        meal_type = request.POST.get('meal_type')
        items = request.POST.get('items')
        timing = request.POST.get('timing', '')
        
        if day and meal_type and items:
            mess_menu, created = MessMenu.objects.get_or_create(
                day=day,
                meal_type=meal_type,
                defaults={'items': items, 'timing': timing}
            )
            if not created:
                mess_menu.items = items
                mess_menu.timing = timing
                mess_menu.save()
            messages.success(request, f"Mess menu updated for {day} ({meal_type.title()}).")
        else:
            messages.error(request, "Please fill in all required fields.")
            
    return redirect(f"/mess/?day={request.POST.get('day', 'Monday')}")

@login_required
def mess_review_create(request):
    if request.method == 'POST':
        form = MessReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.save()
            messages.success(request, "Thank you! Your mess review has been submitted.")
        else:
            messages.error(request, "Invalid review input.")
    return redirect('mess_menu')

# --- RESOURCE SHARING ---

@login_required
def resources_list(request):
    profile = get_or_create_profile(request.user)
    category_filter = request.GET.get('category', '')
    query = request.GET.get('q', '')

    resources = Resource.objects.all().select_related('uploader')
    if category_filter:
        resources = resources.filter(category=category_filter)
    if query:
        resources = resources.filter(Q(title__icontains=query) | Q(description__icontains=query))

    form = ResourceForm()
    return render(request, 'core/resources.html', {
        'profile': profile,
        'resources': resources,
        'form': form,
        'category_filter': category_filter,
        'query': query
    })

@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.uploader = request.user
            res.save()
            messages.success(request, "Resource shared successfully with hostel mates!")
        else:
            messages.error(request, "Error sharing resource.")
    return redirect('resources')

@login_required
def resource_toggle_status(request, pk):
    profile = get_or_create_profile(request.user)
    resource = get_object_or_404(Resource, pk=pk)
    
    if resource.uploader != request.user and not profile.is_admin():
        messages.error(request, "Permission denied.")
        return redirect('resources')
        
    resource.is_available = not resource.is_available
    resource.save()
    status_str = "Available" if resource.is_available else "Borrowed / Unavailable"
    messages.success(request, f"Resource state changed to '{status_str}'.")
    return redirect('resources')

@login_required
def resource_delete(request, pk):
    profile = get_or_create_profile(request.user)
    resource = get_object_or_404(Resource, pk=pk)
    
    if resource.uploader != request.user and not profile.is_admin():
        messages.error(request, "Permission denied.")
        return redirect('resources')
        
    resource.delete()
    messages.success(request, "Resource removed.")
    return redirect('resources')

# --- LOST AND FOUND ---

@login_required
def lost_found_list(request):
    profile = get_or_create_profile(request.user)
    type_filter = request.GET.get('type', '')
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')

    items = LostAndFound.objects.all().select_related('reported_by')
    if type_filter:
        items = items.filter(item_type=type_filter)
    if status_filter:
        items = items.filter(status=status_filter)
    if query:
        items = items.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query))

    form = LostAndFoundForm()
    return render(request, 'core/lost_found.html', {
        'profile': profile,
        'items': items,
        'form': form,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'query': query
    })

@login_required
def lost_found_create(request):
    if request.method == 'POST':
        form = LostAndFoundForm(request.POST)
        if form.is_valid():
            lf_item = form.save(commit=False)
            lf_item.reported_by = request.user
            lf_item.save()
            messages.success(request, f"Item reported as {lf_item.get_item_type_display()} successfully!")
        else:
            messages.error(request, "Error submitting Lost & Found report.")
    return redirect('lost_found')

@login_required
def lost_found_toggle_status(request, pk):
    profile = get_or_create_profile(request.user)
    item = get_object_or_404(LostAndFound, pk=pk)
    
    if item.reported_by != request.user and not profile.is_admin():
        messages.error(request, "Permission denied.")
        return redirect('lost_found')
        
    item.status = 'resolved' if item.status == 'open' else 'open'
    item.save()
    messages.success(request, f"Item marked as {item.get_status_display()}.")
    return redirect('lost_found')

@login_required
def lost_found_delete(request, pk):
    profile = get_or_create_profile(request.user)
    item = get_object_or_404(LostAndFound, pk=pk)
    
    if item.reported_by != request.user and not profile.is_admin():
        messages.error(request, "Permission denied.")
        return redirect('lost_found')
        
    item.delete()
    messages.success(request, "Item deleted.")
    return redirect('lost_found')

# --- ADMIN STUDENT & ROOM MANAGEMENT ---

@login_required
def admin_students_list(request):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('dashboard')
        
    query = request.GET.get('q', '')
    block_filter = request.GET.get('block', '')
    
    students = UserProfile.objects.select_related('user').all()
    if query:
        students = students.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(room_number__icontains=query)
        )
    if block_filter:
        students = students.filter(hostel_block=block_filter)
        
    return render(request, 'core/admin_students.html', {
        'profile': profile,
        'students': students,
        'query': query,
        'block_filter': block_filter
    })

@login_required
def admin_student_edit(request, pk):
    profile = get_or_create_profile(request.user)
    if not profile.is_admin():
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    target_profile = get_object_or_404(UserProfile, pk=pk)
    
    if request.method == 'POST':
        target_profile.roll_number = request.POST.get('roll_number', '')
        target_profile.room_number = request.POST.get('room_number', '')
        target_profile.hostel_block = request.POST.get('hostel_block', 'Block A')
        target_profile.phone = request.POST.get('phone', '')
        new_role = request.POST.get('role', 'student')
        target_profile.role = new_role
        target_profile.save()
        
        messages.success(request, f"Updated student details for {target_profile.user.username}.")
        return redirect('admin_students')
        
    return render(request, 'core/admin_student_edit.html', {
        'profile': profile,
        'target_profile': target_profile
    })
