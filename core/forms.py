from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, initial='student', widget=forms.Select(attrs={'class': 'form-select'}))
    roll_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. 2026CS101'}))
    room_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. 302'}))
    hostel_block = forms.CharField(required=False, initial='Block A', widget=forms.TextInput(attrs={'placeholder': 'e.g. Block A'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '+91 9876543210'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['roll_number', 'room_number', 'hostel_block', 'phone', 'emergency_contact', 'bio']
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'hostel_block': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'category', 'priority', 'room_number', 'hostel_block', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of problem'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 302'}),
            'hostel_block': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Block A'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed explanation of the complaint...'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement Title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Details of notice...'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MessMenuForm(forms.ModelForm):
    class Meta:
        model = MessMenu
        fields = ['day', 'meal_type', 'items', 'timing']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'items': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Paneer Butter Masala, Roti, Rice, Dal'}),
            'timing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 7:30 AM - 9:30 AM'}),
        }


class MessReviewForm(forms.ModelForm):
    class Meta:
        model = MessReview
        fields = ['rating', 'meal_type', 'comments']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your feedback on meal quality, hygiene, or service...'}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'category', 'description', 'contact_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures & Algorithms Textbook'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Edition, condition, or terms for borrowing'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone / WhatsApp / Hostel Room'}),
        }


class LostAndFoundForm(forms.ModelForm):
    class Meta:
        model = LostAndFound
        fields = ['item_type', 'title', 'category', 'location', 'date_event', 'contact_info', 'description']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Black Leather Wallet / Boat Earbuds'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Electronics, ID Card, Clothing, Keys'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mess Hall Table 4 or Library 2nd Floor'}),
            'date_event': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone / WhatsApp number'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Distinctive marks, color, brand, or details'}),
        }
