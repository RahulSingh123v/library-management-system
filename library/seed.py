import os
import sys

def seed_database():
    try:
        from django.contrib.auth.models import User, Group
        from library.models import Category, Book
        
        # 1. Create Default Groups if they don't exist
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        member_group, _ = Group.objects.get_or_create(name='Member')

        # 2. Create Default Users
        # Create Superuser / Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@libraryos.com',
                password='adminpassword123',
                first_name='System',
                last_name='Admin'
            )
            admin_user.groups.add(admin_group)
            sys.stderr.write("Seeded superuser: admin / adminpassword123\n")
            
        # Create Regular Member
        if not User.objects.filter(username='member').exists():
            member_user = User.objects.create_user(
                username='member',
                email='member@libraryos.com',
                password='memberpassword123',
                first_name='Jane',
                last_name='Doe'
            )
            member_user.groups.add(member_group)
            sys.stderr.write("Seeded member: member / memberpassword123\n")

        # 3. Create Categories if none exist
        if Category.objects.count() == 0:
            cs_cat = Category.objects.create(name='Computer Science')
            fiction_cat = Category.objects.create(name='Fiction')
            science_cat = Category.objects.create(name='Science')
            history_cat = Category.objects.create(name='History')
            sys.stderr.write("Seeded categories.\n")
        else:
            cs_cat = Category.objects.filter(name='Computer Science').first()
            fiction_cat = Category.objects.filter(name='Fiction').first()
            science_cat = Category.objects.filter(name='Science').first()
            history_cat = Category.objects.filter(name='History').first()

        # 4. Create Books if none exist
        if Book.objects.count() == 0:
            # CS Books
            Book.objects.create(
                title="Clean Code: A Handbook of Agile Software Craftsmanship",
                author="Robert C. Martin",
                isbn="9780132350884",
                category=cs_cat,
                description="Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. Every year, countless hours and significant resources are lost because of poorly written code. But it doesn't have to be that way.",
                total_copies=5,
                available_copies=5
            )
            Book.objects.create(
                title="The Pragmatic Programmer",
                author="David Thomas & Andrew Hunt",
                isbn="9780135957059",
                category=cs_cat,
                description="The Pragmatic Programmer is one of the most significant books in software development. Topics range from personal responsibility and career development to architectural techniques.",
                total_copies=3,
                available_copies=3
            )
            
            # Fiction Books
            Book.objects.create(
                title="1984",
                author="George Orwell",
                isbn="9780451524935",
                category=fiction_cat,
                description="Winston Smith reins in his rebellion against Big Brother, who controls every aspect of people's lives. A masterpiece of dystopian fiction.",
                total_copies=4,
                available_copies=4
            )
            Book.objects.create(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                isbn="9780061120084",
                category=fiction_cat,
                description="The memorable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it, by Harper Lee.",
                total_copies=6,
                available_copies=6
            )
            
            # Science Books
            Book.objects.create(
                title="A Brief History of Time",
                author="Stephen Hawking",
                isbn="9780553380163",
                category=science_cat,
                description="A landmark volume in science writing by one of the great minds of our time, Stephen Hawking.",
                total_copies=3,
                available_copies=3
            )

            # History Books
            Book.objects.create(
                title="Sapiens: A Brief History of Humankind",
                author="Yuval Noah Harari",
                isbn="9780062316097",
                category=history_cat,
                description="100,000 years ago, at least six human species inhabited the earth. Today there is just one. Us. Homo sapiens. How did our species succeed in the battle for dominance?",
                total_copies=4,
                available_copies=4
            )
            sys.stderr.write("Seeded books successfully.\n")

    except Exception as e:
        sys.stderr.write(f"Database seeding failed: {str(e)}\n")
