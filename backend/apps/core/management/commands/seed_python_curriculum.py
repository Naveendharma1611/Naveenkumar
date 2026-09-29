from django.core.management.base import BaseCommand
import subprocess
import sys
import os

class Command(BaseCommand):
    help = "Seeds the complete Python syllabus, courses, lessons, 25 interview questions, and HTML study notes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Running Python curriculum generator and seeder..."))
        from generate_study_html_and_seed import generate_html_notes, seed_database
        
        html_content = generate_html_notes()
        
        # Served by Django at /study/python-complete-study-notes.html (see apps/web/urls.py)
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        notes_path = os.path.join(backend_dir, "apps", "web", "study", "python-complete-study-notes.html")
        os.makedirs(os.path.dirname(notes_path), exist_ok=True)
        with open(notes_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        seed_database()
        self.stdout.write(self.style.SUCCESS("Successfully seeded Python courses, lessons, interview questions, and HTML notes!"))
