from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

class HostelMateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Admin User
        self.admin_user = User.objects.create_superuser(username='testadmin', password='password123', email='admin@test.com')
        self.admin_profile, _ = UserProfile.objects.get_or_create(user=self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.save()

        
        # Student User
        self.student_user = User.objects.create_user(username='teststudent', password='password123', email='student@test.com')
        self.student_profile, _ = UserProfile.objects.get_or_create(
            user=self.student_user,
            defaults={'role': 'student', 'roll_number': '2026CS99', 'room_number': '404', 'hostel_block': 'Block A'}
        )

    def test_login_and_dashboard(self):
        # Test Student Login & Dashboard
        response = self.client.post('/login/', {'username': 'teststudent', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Overview')

    def test_admin_dashboard(self):
        # Test Admin Login & Dashboard
        self.client.post('/login/', {'username': 'testadmin', 'password': 'password123'})
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hostel Administration Dashboard')

    def test_complaint_lifecycle(self):
        # Student creates complaint
        self.client.post('/login/', {'username': 'teststudent', 'password': 'password123'})
        response = self.client.post('/complaints/create/', {
            'title': 'Test Broken Fan',
            'category': 'electrical',
            'priority': 'high',
            'room_number': '404',
            'hostel_block': 'Block A',
            'description': 'Fan speed regulator is broken.'
        })
        self.assertEqual(response.status_code, 302)
        
        complaint = Complaint.objects.get(title='Test Broken Fan')
        self.assertEqual(complaint.status, 'pending')

        # Logout student and login as admin to update status
        self.client.logout()
        self.client.login(username='testadmin', password='password123')
        response = self.client.post(f'/complaints/{complaint.id}/status/', {
            'status': 'resolved',
            'admin_remarks': 'Regulator replaced by electrician.'
        })

        self.assertEqual(response.status_code, 302)
        
        complaint.refresh_from_db()
        self.assertEqual(complaint.status, 'resolved')
        self.assertEqual(complaint.admin_remarks, 'Regulator replaced by electrician.')

    def test_resource_sharing(self):
        self.client.post('/login/', {'username': 'teststudent', 'password': 'password123'})
        response = self.client.post('/resources/create/', {
            'title': 'Python Programming Handbook',
            'category': 'book',
            'description': 'Comprehensive python guide for lab exercises.',
            'contact_info': 'Room 404'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resource.objects.filter(title='Python Programming Handbook').exists())
