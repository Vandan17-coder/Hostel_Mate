import unittest
from app import create_app
from app.extensions import db
from app.models import User, UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

class HostelMateFlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed test admin
        self.admin_user = User(username='admin', first_name='Hostel', last_name='Warden', email='admin@hostel.edu', is_superuser=True)
        self.admin_user.set_password('admin123')
        db.session.add(self.admin_user)
        db.session.flush()
        self.admin_profile = UserProfile(user_id=self.admin_user.id, role='admin', hostel_block='Block A', room_number='W-01')
        db.session.add(self.admin_profile)

        # Seed test student
        self.student_user = User(username='student1', first_name='Rahul', last_name='Sharma', email='student1@hostel.edu')
        self.student_user.set_password('student123')
        db.session.add(self.student_user)
        db.session.flush()
        self.student_profile = UserProfile(user_id=self.student_user.id, role='student', hostel_block='Block A', room_number='302', roll_number='2026CS101')
        db.session.add(self.student_profile)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_student(self):
        self.client.get('/logout', follow_redirects=True)
        return self.client.post('/login', data={'username': 'student1', 'password': 'student123'}, follow_redirects=True)

    def login_admin(self):
        self.client.get('/logout', follow_redirects=True)
        return self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

    # 1. AUTHENTICATION TESTS
    def test_password_hashing(self):
        self.assertTrue(self.student_user.check_password('student123'))
        self.assertFalse(self.student_user.check_password('wrongpass'))
        self.assertNotEqual(self.student_user.password_hash, 'student123')

    def test_student_login_and_logout(self):
        response = self.login_student()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, Rahul', response.data)

        # Logout
        logout_res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(logout_res.status_code, 200)
        self.assertIn(b'Sign In', logout_res.data)

    def test_invalid_login(self):
        self.client.get('/logout', follow_redirects=True)
        response = self.client.post('/login', data={'username': 'student1', 'password': 'wrongpassword'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_registration(self):
        self.client.get('/logout', follow_redirects=True)
        reg_data = {
            'username': 'newstudent',
            'first_name': 'Aarav',
            'last_name': 'Mehta',
            'email': 'aarav@hostel.edu',
            'role': 'student',
            'roll_number': '2026CS500',
            'room_number': '401',
            'hostel_block': 'Block B',
            'phone': '+91 9999988888',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        res = self.client.post('/register', data=reg_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Welcome back, Aarav', res.data)
        created = User.query.filter_by(username='newstudent').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.profile.room_number, '401')

    # 2. DASHBOARD & ROLE ACCESS TESTS
    def test_admin_dashboard(self):
        self.login_admin()
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Hostel Administration Dashboard', res.data)
        self.assertIn(b'Registered Students', res.data)

    def test_role_protection_for_admin_routes(self):
        self.login_student()
        # Student trying to access admin students roster
        res = self.client.get('/admin-students', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Access denied', res.data)

    # 3. ANNOUNCEMENTS
    def test_announcements_flow(self):
        self.login_admin()
        # Create announcement
        res = self.client.post('/announcements/create', data={
            'title': 'Test Water Tank Cleaning',
            'category': 'maintenance',
            'content': 'Water supply cutoff tomorrow 2-4 PM.',
            'is_pinned': 'y'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Test Water Tank Cleaning', res.data)

        ann = Announcement.query.filter_by(title='Test Water Tank Cleaning').first()
        self.assertIsNotNone(ann)
        self.assertTrue(ann.is_pinned)

        # Delete announcement
        del_res = self.client.post(f'/announcements/delete/{ann.id}', follow_redirects=True)
        self.assertEqual(del_res.status_code, 200)
        self.assertIsNone(Announcement.query.filter_by(title='Test Water Tank Cleaning').first())

    # 4. COMPLAINTS FLOW
    def test_complaints_lifecycle(self):
        self.login_student()
        # Submit complaint
        res = self.client.post('/complaints/create', data={
            'title': 'Broken Tap in Bathroom',
            'category': 'plumbing',
            'priority': 'high',
            'room_number': '302',
            'hostel_block': 'Block A',
            'description': 'Water leaking from the main tap continuously.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Complaint submitted successfully', res.data)

        complaint = Complaint.query.filter_by(title='Broken Tap in Bathroom').first()
        self.assertIsNotNone(complaint)
        self.assertEqual(complaint.status, 'pending')

        # Admin logs in and updates status
        self.login_admin()
        status_res = self.client.post(f'/complaints/{complaint.id}/status', data={
            'status': 'in_progress',
            'admin_remarks': 'Plumber assigned.'
        }, follow_redirects=True)
        self.assertEqual(status_res.status_code, 200)
        self.assertIn(b'Plumber assigned', status_res.data)

        updated = Complaint.query.get(complaint.id)
        self.assertEqual(updated.status, 'in_progress')

    # 5. MESS MENU & REVIEWS
    def test_mess_menu_and_reviews(self):
        self.login_admin()
        # Admin updates menu
        res = self.client.post('/mess/update', data={
            'day': 'Monday',
            'meal_type': 'lunch',
            'items': 'Paneer Makhani, Naan, Jeera Rice, Dal',
            'timing': '12:30 PM - 2:30 PM'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Paneer Makhani', res.data)

        # Student submits review
        self.login_student()
        rev_res = self.client.post('/mess/review', data={
            'rating': 5,
            'meal_type': 'lunch',
            'comments': 'Delicious meal today!'
        }, follow_redirects=True)
        self.assertEqual(rev_res.status_code, 200)
        self.assertIn(b'Delicious meal today!', rev_res.data)

    # 6. RESOURCES SHARING
    def test_resources_flow(self):
        self.login_student()
        # Post resource
        res = self.client.post('/resources/create', data={
            'title': 'Operating System Concepts (Silberschatz)',
            'category': 'book',
            'description': 'Standard dinosaur textbook in good condition.',
            'contact_info': 'Rahul • 302'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Operating System Concepts', res.data)

        item = Resource.query.filter_by(title='Operating System Concepts (Silberschatz)').first()
        self.assertTrue(item.is_available)

        # Toggle availability
        toggle_res = self.client.get(f'/resources/{item.id}/toggle', follow_redirects=True)
        self.assertEqual(toggle_res.status_code, 200)
        item_updated = Resource.query.get(item.id)
        self.assertFalse(item_updated.is_available)

    # 7. LOST AND FOUND
    def test_lost_and_found_flow(self):
        self.login_student()
        # Report lost item
        res = self.client.post('/lost-found/create', data={
            'item_type': 'lost',
            'title': 'Casio Watch with Silver Dial',
            'category': 'Personal Belongings',
            'location': 'Near Gym / Common Room',
            'date_event': '2026-10-05',
            'contact_info': '+91 9876543210',
            'description': 'Silver dial metallic wrist watch.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Casio Watch with Silver Dial', res.data)

        lf = LostAndFound.query.filter_by(title='Casio Watch with Silver Dial').first()
        self.assertEqual(lf.status, 'open')

        # Toggle claimed
        self.client.get(f'/lost-found/{lf.id}/toggle', follow_redirects=True)
        lf_updated = LostAndFound.query.get(lf.id)
        self.assertEqual(lf_updated.status, 'resolved')

    # 8. ADMIN STUDENT ROSTER EDIT
    def test_admin_student_edit(self):
        self.login_admin()
        res = self.client.post(f'/admin-students/{self.student_profile.id}/edit', data={
            'role': 'student',
            'roll_number': '2026CS101-EDITED',
            'room_number': '305-A',
            'hostel_block': 'Block B',
            'phone': '+91 1234567890'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        prof = UserProfile.query.get(self.student_profile.id)
        self.assertEqual(prof.room_number, '305-A')
        self.assertEqual(prof.hostel_block, 'Block B')

if __name__ == '__main__':
    unittest.main()
