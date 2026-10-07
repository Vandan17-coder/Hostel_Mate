from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Hostel Admin / Warden'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    hostel_block = models.CharField(max_length=50, blank=True, null=True, default='Block A')
    phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Announcement(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General Notice'),
        ('urgent', 'Urgent / Important'),
        ('maintenance', 'Maintenance Work'),
        ('event', 'Hostel Event'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_pinned = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class Complaint(models.Model):
    CATEGORY_CHOICES = (
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('cleanliness', 'Cleanliness & Hygiene'),
        ('wifi', 'Wi-Fi & Internet'),
        ('furniture', 'Furniture & Carpentry'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    room_number = models.CharField(max_length=20)
    hostel_block = models.CharField(max_length=50, default='Block A')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.username} ({self.get_status_display()})"


class MessMenu(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    MEAL_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Evening Snacks'),
        ('dinner', 'Dinner'),
    )
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=15, choices=MEAL_CHOICES)
    items = models.TextField(help_text="Menu items, e.g., Paneer Masala, Butter Roti, Rice, Dal")
    timing = models.CharField(max_length=50, blank=True, help_text="e.g. 7:30 AM - 9:30 AM")

    class Meta:
        unique_together = ('day', 'meal_type')
        ordering = ['id']

    def __str__(self):
        return f"{self.day} - {self.get_meal_type_display()}"


class MessReview(models.Model):
    MEAL_CHOICES = (
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Evening Snacks'),
        ('dinner', 'Dinner'),
        ('general', 'General Mess Quality'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mess_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    meal_type = models.CharField(max_length=15, choices=MEAL_CHOICES, default='general')
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.student.username} - {self.rating}/5 stars"


class Resource(models.Model):
    CATEGORY_CHOICES = (
        ('book', 'Books & Notes'),
        ('electronics', 'Electronics & Accessories'),
        ('sports', 'Sports Goods'),
        ('lab', 'Lab & Study Tools'),
        ('other', 'Other Utility'),
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='book')
    description = models.TextField()
    contact_info = models.CharField(max_length=100, help_text="Phone number or WhatsApp")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class LostAndFound(models.Model):
    TYPE_CHOICES = (
        ('lost', 'Lost Item'),
        ('found', 'Found Item'),
    )
    STATUS_CHOICES = (
        ('open', 'Open / Searching'),
        ('resolved', 'Claimed / Resolved'),
    )
    item_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='Personal Belongings')
    description = models.TextField()
    location = models.CharField(max_length=150, help_text="Where it was lost/found")
    date_event = models.DateField(help_text="Date item was lost or found")
    contact_info = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_and_found_items')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_item_type_display()}] {self.title}"
