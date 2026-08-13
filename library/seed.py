import os
import sys
import urllib.request
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def download_cover_image(isbn):
    try:
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        # Limit timeout to 5 seconds to prevent long startup delays
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read()
            # Open Library returns a tiny 1x1 blank image if not found, check size
            if len(content) > 1000:
                temp_file = NamedTemporaryFile(delete=True)
                temp_file.write(content)
                temp_file.flush()
                return temp_file
    except Exception as e:
        sys.stderr.write(f"Failed to fetch cover for {isbn}: {str(e)}\n")
    return None

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
            # Helper to create book and seed its cover
            def create_book_with_cover(title, author, isbn, category, description, total_copies):
                book = Book.objects.create(
                    title=title,
                    author=author,
                    isbn=isbn,
                    category=category,
                    description=description,
                    total_copies=total_copies,
                    available_copies=total_copies
                )
                img_file = download_cover_image(isbn)
                if img_file:
                    book.cover_image.save(f"{isbn}.jpg", File(img_file))
                    sys.stderr.write(f"Attached cover image to book: '{title}'\n")
                return book

            # CS Books
            create_book_with_cover(
                title="Clean Code: A Handbook of Agile Software Craftsmanship",
                author="Robert C. Martin",
                isbn="9780132350884",
                category=cs_cat,
                description="Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. Every year, countless hours and significant resources are lost because of poorly written code. But it doesn't have to be that way.",
                total_copies=5
            )
            create_book_with_cover(
                title="The Pragmatic Programmer",
                author="David Thomas & Andrew Hunt",
                isbn="9780135957059",
                category=cs_cat,
                description="The Pragmatic Programmer is one of the most significant books in software development. Topics range from personal responsibility and career development to architectural techniques.",
                total_copies=3
            )
            
            # Fiction Books
            create_book_with_cover(
                title="1984",
                author="George Orwell",
                isbn="9780451524935",
                category=fiction_cat,
                description="Winston Smith reins in his rebellion against Big Brother, who controls every aspect of people's lives. A masterpiece of dystopian fiction.",
                total_copies=4
            )
            create_book_with_cover(
                title="To Kill a Mockingbird",
                author="Harper Lee",
                isbn="9780061120084",
                category=fiction_cat,
                description="The memorable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it, by Harper Lee.",
                total_copies=6
            )
            
            # Science Books
            create_book_with_cover(
                title="A Brief History of Time",
                author="Stephen Hawking",
                isbn="9780553380163",
                category=science_cat,
                description="A landmark volume in science writing by one of the great minds of our time, Stephen Hawking.",
                total_copies=3
            )

            # History Books
            create_book_with_cover(
                title="Sapiens: A Brief History of Humankind",
                author="Yuval Noah Harari",
                isbn="9780062316097",
                category=history_cat,
                description="100,000 years ago, at least six human species inhabited the earth. Today there is just one. Us. Homo sapiens. How did our species succeed in the battle for dominance?",
                total_copies=4
            )
            sys.stderr.write("Seeded books successfully.\n")

        # 5. Fallback/Retroactive seeding: download cover image for any existing books missing one
        for book in Book.objects.filter(cover_image=''):
            img_file = download_cover_image(book.isbn)
            if img_file:
                book.cover_image.save(f"{book.isbn}.jpg", File(img_file))
                sys.stderr.write(f"Updated cover image for existing book: '{book.title}'\n")

    except Exception as e:
        sys.stderr.write(f"Database seeding failed: {str(e)}\n")
