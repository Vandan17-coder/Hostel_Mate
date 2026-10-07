import click
from datetime import date, timedelta
from app.extensions import db
from app.models import User, UserProfile, Announcement, Complaint, MessMenu, MessReview, Resource, LostAndFound

def register_commands(app):
    @app.cli.command('seed')
    def seed_data():
        """Seeds initial sample data for HostelMate application."""
        click.echo("Starting database seeding...")

        # 1. Create Warden / Admin User
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                first_name='Hostel',
                last_name='Warden',
                email='warden@hostel.edu',
                is_staff=True,
                is_superuser=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.flush()

        admin_profile = UserProfile.query.filter_by(user_id=admin_user.id).first()
        if not admin_profile:
            admin_profile = UserProfile(
                user_id=admin_user.id,
                role='admin',
                hostel_block='Block A',
                phone='+91 9876500000'
            )
            db.session.add(admin_profile)
        else:
            admin_profile.role = 'admin'

        # 2. Create Student Users
        students_data = [
            {'username': 'student1', 'first': 'Rahul', 'last': 'Sharma', 'roll': '2026CS101', 'room': '302', 'block': 'Block A', 'phone': '+91 9876543210'},
            {'username': 'student2', 'first': 'Ananya', 'last': 'Patel', 'roll': '2026EC204', 'room': '104', 'block': 'Block B', 'phone': '+91 9876543211'},
            {'username': 'student3', 'first': 'Vikram', 'last': 'Singh', 'roll': '2026ME310', 'room': '215', 'block': 'Block A', 'phone': '+91 9876543212'},
        ]

        student_objs = []
        for sdata in students_data:
            user = User.query.filter_by(username=sdata['username']).first()
            if not user:
                user = User(
                    username=sdata['username'],
                    first_name=sdata['first'],
                    last_name=sdata['last'],
                    email=f"{sdata['username']}@student.edu"
                )
                user.set_password('student123')
                db.session.add(user)
                db.session.flush()

            profile = UserProfile.query.filter_by(user_id=user.id).first()
            if not profile:
                profile = UserProfile(
                    user_id=user.id,
                    role='student',
                    roll_number=sdata['roll'],
                    room_number=sdata['room'],
                    hostel_block=sdata['block'],
                    phone=sdata['phone']
                )
                db.session.add(profile)
            student_objs.append(user)

        # 3. Create Announcements
        if not Announcement.query.filter_by(title="Hostel Night & Cultural Fest 2026 Registration").first():
            db.session.add(Announcement(
                title="Hostel Night & Cultural Fest 2026 Registration",
                content="Annual Hostel Night will be held on Oct 25th. Registrations for music, drama, and dance events are open now at the Warden Office!",
                category='event',
                is_pinned=True,
                created_by_id=admin_user.id
            ))

        if not Announcement.query.filter_by(title="Scheduled Water Tank Maintenance on Wednesday").first():
            db.session.add(Announcement(
                title="Scheduled Water Tank Maintenance on Wednesday",
                content="Water supply in Block A & B will be suspended between 2:00 PM to 4:00 PM on Wednesday for overhead tank cleaning.",
                category='maintenance',
                is_pinned=False,
                created_by_id=admin_user.id
            ))

        if not Announcement.query.filter_by(title="Strict Gate Entry Timings & Curfew Notice").first():
            db.session.add(Announcement(
                title="Strict Gate Entry Timings & Curfew Notice",
                content="All residents are reminded that main gate entry closes at 10:00 PM. Late entry requires prior written approval from the Warden.",
                category='urgent',
                is_pinned=False,
                created_by_id=admin_user.id
            ))

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
                if not MessMenu.query.filter_by(day=day, meal_type=mtype).first():
                    db.session.add(MessMenu(
                        day=day,
                        meal_type=mtype,
                        items=items,
                        timing=timing
                    ))

        # 5. Complaints
        s1 = student_objs[0]
        s2 = student_objs[1]
        s3 = student_objs[2]

        if not Complaint.query.filter_by(title="Leaking Pipe in Room 302 Washroom").first():
            db.session.add(Complaint(
                student_id=s1.id,
                title="Leaking Pipe in Room 302 Washroom",
                category='plumbing',
                description='The pipe under the washbasin in room 302 is constantly dripping water.',
                room_number='302',
                hostel_block='Block A',
                priority='high',
                status='pending'
            ))

        if not Complaint.query.filter_by(title="Wi-Fi Signal Weak on 1st Floor Corridor").first():
            db.session.add(Complaint(
                student_id=s2.id,
                title="Wi-Fi Signal Weak on 1st Floor Corridor",
                category='wifi',
                description='Wi-Fi disconnects repeatedly near room 104 in Block B.',
                room_number='104',
                hostel_block='Block B',
                priority='medium',
                status='in_progress',
                admin_remarks='IT network technician dispatched to inspect Access Point B-102.'
            ))

        if not Complaint.query.filter_by(title="Faulty Tube Light Replacement").first():
            db.session.add(Complaint(
                student_id=s3.id,
                title="Faulty Tube Light Replacement",
                category='electrical',
                description='Study table tube light flickers and creates noise.',
                room_number='215',
                hostel_block='Block A',
                priority='low',
                status='resolved',
                admin_remarks='Replaced tube light bulb with new LED tube light on Monday.'
            ))

        # 6. Mess Reviews
        if not MessReview.query.filter_by(student_id=s1.id, meal_type='lunch').first():
            db.session.add(MessReview(
                student_id=s1.id,
                meal_type='lunch',
                rating=5,
                comments='Paneer dish was fresh and delicious today! Great improvement.'
            ))

        if not MessReview.query.filter_by(student_id=s2.id, meal_type='breakfast').first():
            db.session.add(MessReview(
                student_id=s2.id,
                meal_type='breakfast',
                rating=4,
                comments='Puri bhaji was tasty, tea could be a bit warmer.'
            ))

        # 7. Shared Resources
        if not Resource.query.filter_by(title="CLRS Introduction to Algorithms (4th Edition)").first():
            db.session.add(Resource(
                title="CLRS Introduction to Algorithms (4th Edition)",
                category='book',
                description='Hardcover algorithms textbook in mint condition. Available for CS semester exams.',
                contact_info='Rahul Sharma (Room 302) • +91 9876543210',
                uploader_id=s1.id,
                is_available=True
            ))

        if not Resource.query.filter_by(title="Scientific Calculator Casio fx-991EX").first():
            db.session.add(Resource(
                title="Scientific Calculator Casio fx-991EX",
                category='electronics',
                description='Solar powered non-programmable scientific calculator for engineering math.',
                contact_info='Ananya Patel (Room 104) • +91 9876543211',
                uploader_id=s2.id,
                is_available=True
            ))

        # 8. Lost & Found Items
        if not LostAndFound.query.filter_by(title="Found: Blue Boat Airdopes Earbuds Case").first():
            db.session.add(LostAndFound(
                item_type='found',
                title="Found: Blue Boat Airdopes Earbuds Case",
                category='Electronics',
                description='Found near Table 6 in Mess Hall during lunch hours. Please verify serial number to claim.',
                location='Mess Hall Table 6',
                date_event=date.today() - timedelta(days=1),
                contact_info='Vikram Singh • Room 215',
                status='open',
                reported_by_id=s3.id
            ))

        if not LostAndFound.query.filter_by(title="Lost: Black Leather Wallet with Student ID").first():
            db.session.add(LostAndFound(
                item_type='lost',
                title="Lost: Black Leather Wallet with Student ID",
                category='Personal Belongings',
                description='Lost black Tommy Hilfiger wallet containing college ID card and library card.',
                location='Between Block A and Basketball Court',
                date_event=date.today() - timedelta(days=2),
                contact_info='Rahul Sharma • +91 9876543210',
                status='open',
                reported_by_id=s1.id
            ))

        db.session.commit()
        click.echo(click.style("Database seeded successfully with initial sample records!", fg='green'))
