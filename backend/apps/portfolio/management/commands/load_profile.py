"""Loads Naveen Kumar's resume into the portfolio: profile, skills, education, experience and projects.

Run once per database:  python manage.py load_profile
It replaces the demo skills and sample projects. After that, edit everything in the Django admin
(re-running this command would overwrite those admin edits for the items below).
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.portfolio.models import Education, Experience, SiteProfile, Skill
from apps.projects.models import Project, Technology

PROFILE = {
    "full_name": "Naveen Kumar",
    "headline": "Python Developer | Data Science | AI/ML | Data Analytics",
    "tagline": "MCA graduate building machine learning models, data analytics solutions "
               "and Django web applications with Python.",
    "short_bio": "MCA graduate with hands-on knowledge of Python, Data Science, Machine Learning, SQL, "
                 "Django and Data Analytics.",
    "about": (
        "MCA graduate with hands-on knowledge of **Python, Data Science, Machine Learning, SQL, Django** "
        "and **Data Analytics**.\n\n"
        "I completed Python with Data Science training and developed practical projects involving machine "
        "learning, data analysis, web development and AI applications.\n\n"
        "I'm familiar with NumPy, Pandas, Matplotlib, Seaborn, Scikit-learn, TensorFlow, Django, REST APIs, "
        "MySQL/PostgreSQL, Power BI and Git."
    ),
    "professional_goals": "Transitioning toward software development, data analytics and AI/ML roles "
                          "through technical training and project development.",
    "technical_interests": "Python Development\nData Science\nMachine Learning & Deep Learning\n"
                           "Data Analytics & Dashboards\nGenerative AI (LLMs, RAG, LangChain)",
    "hero_badges": "Python,Data Science,Machine Learning,Deep Learning,SQL,Django,Power BI,GenAI",
    "email": "naveendharma1611@gmail.com",
    "phone": "+91 93608 30290",
    "location": "Coimbatore, Tamil Nadu, India",
    "linkedin_url": "https://www.linkedin.com/in/naveendharma1611",
    "github_url": "https://github.com/naveendharma1611",
}

C = Skill.Category
SKILLS = {
    C.PROGRAMMING: ["Python", "SQL", "C", "JavaScript", "HTML", "CSS"],
    C.DATA_SCIENCE: ["NumPy", "Pandas", "Matplotlib", "Seaborn", "Scikit-learn", "Statistics", "EDA",
                     "Data Cleaning", "Data Visualization"],
    C.MACHINE_LEARNING: ["Regression", "Classification", "Clustering", "Decision Trees", "Random Forest", "SVM",
                         "KNN", "Naive Bayes", "PCA", "Model Evaluation", "Hyperparameter Tuning"],
    C.DEEP_LEARNING: ["TensorFlow", "Keras", "CNN", "Neural Networks", "ReLU", "Pooling", "Dropout",
                      "Model Training"],
    C.GENAI: ["LLM Concepts", "Transformers", "RAG", "Embeddings", "Vector Search", "LangChain", "LangGraph"],
    C.WEB: ["Django", "Django ORM", "Django Templates", "Django REST Framework", "REST API", "CRUD",
            "Authentication", "HTML5", "CSS3", "React/Next.js fundamentals"],
    C.DATABASE: ["MySQL", "PostgreSQL", "SQLite"],
    C.TOOLS: ["Git", "GitHub", "Jupyter Notebook", "Google Colab", "VS Code", "PyCharm", "Anaconda", "Postman",
              "Docker"],
    C.ANALYTICS: ["Power BI", "Microsoft Excel", "Dashboard Development"],
}
FEATURED_SKILLS = {"Python", "SQL", "NumPy", "Pandas", "Scikit-learn", "TensorFlow", "Keras", "Django",
                   "Django REST Framework", "PostgreSQL", "Power BI", "LangChain"}

EDUCATION = [
    {"degree": "Master of Computer Applications (MCA)", "institution": "Bharathiar University",
     "end_year": 2024, "score": "72% (up to 2nd semester)"},
    {"degree": "Bachelor of Science (B.Sc.)", "institution": "Kongunadu Arts and Science College",
     "location": "Coimbatore", "end_year": 2022, "score": "65%"},
    {"degree": "Higher Secondary Certificate (HSC)", "institution": "Sankar Ponnar Higher Secondary School",
     "location": "Palani", "end_year": 2019, "score": "64%"},
    {"degree": "Secondary School Leaving Certificate (SSLC)", "institution": "Sankar Ponnar Higher Secondary School",
     "location": "Palani", "end_year": 2017, "score": "87%"},
]

EXPERIENCE = [
    {
        "role": "Process Executive", "organization": "Cognizant", "type": Experience.Type.JOB,
        "description": (
            "- Followed organizational processes, documentation standards and productivity requirements.\n"
            "- Developed professional experience in communication, teamwork, problem-solving and process "
            "management.\n"
            "- Currently transitioning toward software development, data analytics and AI/ML roles through "
            "technical training and project development."
        ),
    },
]

PROJECTS = [
    {
        "slug": "diabetes-prediction-system", "title": "Diabetes Prediction System", "category": Project.Category.ML,
        "summary": "Machine learning system that predicts diabetes from patient-related features.",
        "objective": "Predict whether a patient is likely to have diabetes based on patient-related features.",
        "implementation": "- Performed data preprocessing and exploratory data analysis (EDA)\n"
                          "- Prepared features for modelling\n"
                          "- Trained classification models with Scikit-learn\n"
                          "- Evaluated model performance using appropriate metrics",
        "algorithm": "Classification algorithms (Scikit-learn)",
        "pipeline_steps": ["Patient Data", "Preprocessing", "EDA", "Feature Preparation", "Model Training",
                           "Evaluation"],
        "technologies": ["Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning"],
    },
    {
        "slug": "cnn-image-classification-cat-vs-dog", "title": "CNN Image Classification — Cat vs Dog",
        "category": Project.Category.DL,
        "summary": "Convolutional neural network that classifies cat and dog images, built with TensorFlow/Keras.",
        "objective": "Classify images as cat or dog using a Convolutional Neural Network.",
        "implementation": "- Implemented image resizing and normalization\n"
                          "- Built the CNN with Conv2D, ReLU, MaxPooling, Flatten, Dense and Dropout layers\n"
                          "- Applied image augmentation to improve model generalization",
        "model_training": "Trained and evaluated the model using TensorFlow/Keras.",
        "pipeline_steps": ["Images", "Resize & Normalize", "Augmentation", "Conv2D + ReLU", "MaxPooling",
                           "Flatten + Dense", "Dropout", "Evaluation"],
        "technologies": ["Python", "TensorFlow", "Keras", "CNN"],
    },
    {
        "slug": "ai-resume-screening-system", "title": "AI Resume Screening System", "category": Project.Category.AI,
        "summary": "NLP-based system concept that analyses resumes against job requirements for candidate matching.",
        "objective": "Automatically analyse resumes against job requirements to support screening and "
                     "candidate matching.",
        "implementation": "- Used text preprocessing and NLP techniques to extract relevant skills\n"
                          "- Compared extracted skills with job requirements\n"
                          "- Designed the system to support automated resume screening and candidate matching",
        "pipeline_steps": ["Resumes + Job Description", "Text Preprocessing", "Skill Extraction (NLP)",
                           "Skill Comparison", "Candidate Matching"],
        "technologies": ["Python", "NLP", "Machine Learning"],
    },
    {
        "slug": "job-scraping-data-analysis-system", "title": "Job Scraping & Data Analysis System",
        "category": Project.Category.ANALYTICS,
        "summary": "Web-scraping workflow that collects job listings, cleans them with Pandas and stores them in SQL.",
        "objective": "Collect job data from the web and prepare it for analytics and dashboard visualization.",
        "implementation": "- Collected job information using web scraping (BeautifulSoup, Selenium)\n"
                          "- Processed the data with Python\n"
                          "- Cleaned and analysed it with Pandas\n"
                          "- Stored the structured data in SQL",
        "future_improvements": "Dashboard visualization and further analytics on the collected job data.",
        "pipeline_steps": ["Scrape (BeautifulSoup / Selenium)", "Process (Python)", "Clean & Analyse (Pandas)",
                           "Store (SQL)", "Dashboard"],
        "technologies": ["Python", "BeautifulSoup", "Selenium", "Pandas", "SQL"],
    },
    {
        "slug": "django-full-stack-portfolio", "title": "Django Full-Stack Portfolio",
        "category": Project.Category.DJANGO,
        "summary": "Personal portfolio application built with Django, PostgreSQL and an HTML/CSS/JavaScript "
                   "frontend (in progress).",
        "objective": "Present profile, skills, education, projects and professional information in one "
                     "full-stack application.",
        "implementation": "- Django views, URLs, templates, models and ORM with database integration\n"
                          "- REST API concepts and modern frontend technologies\n"
                          "- Sections for profile, skills, education, projects and professional information",
        "pipeline_steps": ["Django Models", "ORM + PostgreSQL", "REST API", "HTML / CSS / JS Frontend"],
        "technologies": ["Python", "Django", "HTML", "CSS", "JavaScript", "PostgreSQL"],
    },
]


class Command(BaseCommand):
    help = "Load Naveen Kumar's resume (profile, skills, education, experience, projects) into the portfolio."

    @transaction.atomic
    def handle(self, *args, **options):
        profile = SiteProfile.load()
        for field, value in PROFILE.items():
            setattr(profile, field, value)
        profile.save()

        keep = set()
        for category, names in SKILLS.items():
            for order, name in enumerate(names):
                skill, _ = Skill.objects.update_or_create(
                    name=name, category=category,
                    defaults={"order": order, "is_featured": name in FEATURED_SKILLS, "is_published": True},
                )
                keep.add(skill.pk)
        removed_skills, _ = Skill.objects.exclude(pk__in=keep).delete()

        Education.objects.all().delete()
        for order, row in enumerate(EDUCATION):
            Education.objects.create(order=order, **row)

        Experience.objects.all().delete()
        for order, row in enumerate(EXPERIENCE):
            Experience.objects.create(order=order, is_published=True, **row)

        removed_samples, _ = Project.objects.filter(is_sample=True).delete()
        for order, spec in enumerate(PROJECTS):
            spec = dict(spec)
            tech_names = spec.pop("technologies")
            project, _ = Project.objects.update_or_create(
                slug=spec.pop("slug"),
                defaults={**spec, "order": order, "is_published": True, "is_featured": True, "is_sample": False},
            )
            project.technologies.set(Technology.objects.get_or_create(name=n)[0] for n in tech_names)

        self.stdout.write(self.style.SUCCESS(
            f"Profile saved; {len(keep)} skills ({removed_skills} demo skills removed); "
            f"{len(EDUCATION)} education; {len(EXPERIENCE)} experience; {len(PROJECTS)} projects "
            f"({removed_samples} sample rows removed)."
        ))
