from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds initial sample data for HostelMate application'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Create Warden / Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Hostel',
                'last_name': 'Warden',
                'email': 'warden@hostel.edu',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
        
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.role = 'admin'
        admin_profile.hostel_block = 'Block A'
        admin_profile.phone = '+91 9876500000'
        admin_profile.save()

        # 2. Create Student Users
        students_data = [
            {'username': 'student1', 'first': 'Rahul', 'last': 'Sharma', 'roll': '2026CS101', 'room': '302', 'block': 'Block A', 'phone': '+91 9876543210'},
            {'username': 'student2', 'first': 'Ananya', 'last': 'Patel', 'roll': '2026EC204', 'room': '104', 'block': 'Block B', 'phone': '+91 9876543211'},
            {'username': 'student3', 'first': 'Vikram', 'last': 'Singh', 'roll': '2026ME310', 'room': '215', 'block': 'Block A', 'phone': '+91 9876543212'},
        ]

        student_objs = []
        for sdata in students_data:
            user, s_created = User.objects.get_or_create(
                username=sdata['username'],
                defaults={
                    'first_name': sdata['first'],
                    'last_name': sdata['last'],
                    'email': f"{sdata['username']}@student.edu"
                }
            )
            if s_created:
                user.set_password('student123')
                user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'student'
            profile.roll_number = sdata['roll']
            profile.room_number = sdata['room']
            profile.hostel_block = sdata['block']
            profile.phone = sdata['phone']
            profile.save()
            student_objs.append(user)

        # 3. Create Announcements
        Announcement.objects.get_or_create(
            title="Hostel Night & Cultural Fest 2026 Registration",
            defaults={
                'content': "Annual Hostel Night will be held on Oct 25th. Registrations for music, drama, and dance events are open now at the Warden Office!",
                'category': 'event',
                'is_pinned': True,
                'created_by': admin_user
            }
        )

        Announcement.objects.get_or_create(
            title="Scheduled Water Tank Maintenance on Wednesday",
            defaults={
                'content': "Water supply in Block A & B will be suspended between 2:00 PM to 4:00 PM on Wednesday for overhead tank cleaning.",
                'category': 'maintenance',
                'is_pinned': False,
                'created_by': admin_user
            }
        )

        Announcement.objects.get_or_create(
            title="Strict Gate Entry Timings & Curfew Notice",
            defaults={
                'content': "All residents are reminded that main gate entry closes at 10:00 PM. Late entry requires prior written approval from the Warden.",
                'category': 'urgent',
                'is_pinned': False,
                'created_by': admin_user
            }
        )

        # 4. Weekly Mess Menu
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        sample_menus = {
            'breakfast': ('Puri Bhaji, Tea & Coffee, Banana, Omelette', '7:30 AM - 9:30 AM'),
            'lunch': ('Paneer Butter Masala, Dal Tadka, Jeera Rice, Chapati, Salad', '12:30 PM - 2:30 PM'),
            'snacks': ('Samosa / Poha, Mint Chutney, Masala Tea', '5:00 PM - 6:00 PM'),
            'dinner': ('Mix Veg Curry, Dal Makhani, Phulka, Rice, Gulab Jamun', '7:30 PM - 9:30 PM')
        }

        for day in days:
            for mtype, (items, timing) in sample_menus.items():
                MessMenu.objects.get_or_create(
                    day=day,
                    meal_type=mtype,
                    defaults={'items': items, 'timing': timing}
                )

        # 5. Complaints
        s1 = student_objs[0]
        s2 = student_objs[1]
        s3 = student_objs[2]

        Complaint.objects.get_or_create(
            title="Leaking Pipe in Room 302 Washroom",
            defaults={
                'student': s1,
                'category': 'plumbing',
                'description': 'The pipe under the washbasin in room 302 is constantly dripping water.',
                'room_number': '302',
                'hostel_block': 'Block A',
                'priority': 'high',
                'status': 'pending'
            }
        )

        Complaint.objects.get_or_create(
            title="Wi-Fi Signal Weak on 1st Floor Corridor",
            defaults={
                'student': s2,
                'category': 'wifi',
                'description': 'Wi-Fi disconnects repeatedly near room 104 in Block B.',
                'room_number': '104',
                'hostel_block': 'Block B',
                'priority': 'medium',
                'status': 'in_progress',
                'admin_remarks': 'IT network technician dispatched to inspect Access Point B-102.'
            }
        )

        Complaint.objects.get_or_create(
            title="Faulty Tube Light Replacement",
            defaults={
                'student': s3,
                'category': 'electrical',
                'description': 'Study table tube light flickers and creates noise.',
                'room_number': '215',
                'hostel_block': 'Block A',
                'priority': 'low',
                'status': 'resolved',
                'admin_remarks': 'Replaced tube light bulb with new LED tube light on Monday.'
            }
        )

        # 6. Mess Reviews
        MessReview.objects.get_or_create(
            student=s1,
            meal_type='lunch',
            defaults={'rating': 5, 'comments': 'Paneer dish was fresh and delicious today! Great improvement.'}
        )
        MessReview.objects.get_or_create(
            student=s2,
            meal_type='breakfast',
            defaults={'rating': 4, 'comments': 'Puri bhaji was tasty, tea could be a bit warmer.'}
        )

        # 7. Shared Resources
        Resource.objects.get_or_create(
            title="CLRS Introduction to Algorithms (4th Edition)",
            defaults={
                'category': 'book',
                'description': 'Hardcover algorithms textbook in mint condition. Available for CS semester exams.',
                'contact_info': 'Rahul Sharma (Room 302) • +91 9876543210',
                'uploader': s1,
                'is_available': True
            }
        )

        Resource.objects.get_or_create(
            title="Scientific Calculator Casio fx-991EX",
            defaults={
                'category': 'electronics',
                'description': 'Solar powered non-programmable scientific calculator for engineering math.',
                'contact_info': 'Ananya Patel (Room 104) • +91 9876543211',
                'uploader': s2,
                'is_available': True
            }
        )

        # 8. Lost & Found Items
        LostAndFound.objects.get_or_create(
            title="Found: Blue Boat Airdopes Earbuds Case",
            defaults={
                'item_type': 'found',
                'category': 'Electronics',
                'description': 'Found near Table 6 in Mess Hall during lunch hours. Please verify serial number to claim.',
                'location': 'Mess Hall Table 6',
                'date_event': date.today() - timedelta(days=1),
                'contact_info': 'Vikram Singh • Room 215',
                'status': 'open',
                'reported_by': s3
            }
        )

        LostAndFound.objects.get_or_create(
            title="Lost: Black Leather Wallet with Student ID",
            defaults={
                'item_type': 'lost',
                'category': 'Personal Belongings',
                'description': 'Lost black Tommy Hilfiger wallet containing college ID card and library card.',
                'location': 'Between Block A and Basketball Court',
                'date_event': date.today() - timedelta(days=2),
                'contact_info': 'Rahul Sharma • +91 9876543210',
                'status': 'open',
                'reported_by': s1
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with initial sample records!"))
