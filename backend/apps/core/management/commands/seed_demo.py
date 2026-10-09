"""Seeds structure and clearly-marked sample content. Safe to run repeatedly.

Creates: site profile placeholder, study categories (empty - add lessons in the admin), skills
(without proficiency claims), blog categories, and five SAMPLE projects flagged `is_sample=True`.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.blog.models import BlogCategory
from apps.learning.models import StudyCategory
from apps.portfolio.models import SiteProfile, Skill
from apps.projects.models import Project, Technology

STUDY_CATEGORIES = [
    ("Python", "python"), ("C", "code"), ("C++", "code"), ("SQL", "database"), ("NumPy", "grid"),
    ("Pandas", "table"), ("Matplotlib", "chart"), ("Seaborn", "chart"), ("Statistics", "sigma"),
    ("Machine Learning", "brain"), ("Deep Learning", "network"), ("Power BI", "dashboard"), ("Excel", "sheet"),
    ("Django", "server"), ("FastAPI", "zap"), ("Data Science", "flask"), ("Generative AI", "sparkles"),
    ("Agentic AI", "bot"),
]

# Names that would otherwise slugify to the same value ("C" and "C++" -> "c").
CATEGORY_SLUGS = {"C++": "cpp"}

SKILLS = {
    Skill.Category.PROGRAMMING: ["Python", "C", "C++"],
    Skill.Category.DATA_SCIENCE: ["NumPy", "Pandas", "Matplotlib", "Seaborn", "Scikit-learn"],
    Skill.Category.MACHINE_LEARNING: ["Regression", "Classification", "Clustering", "Model Evaluation"],
    Skill.Category.DEEP_LEARNING: ["TensorFlow", "Keras", "CNN", "ANN"],
    Skill.Category.DATABASE: ["SQL", "MySQL", "PostgreSQL"],
    Skill.Category.WEB: ["HTML", "CSS", "JavaScript", "Django", "REST API"],
    Skill.Category.ANALYTICS: ["Excel", "Power BI"],
    Skill.Category.GENAI: ["LLM", "RAG", "LangChain", "LangGraph", "Prompt Engineering"],
    Skill.Category.AGENTIC_AI: ["AI Agents", "Tool Calling"],
    Skill.Category.TOOLS: ["Git/GitHub", "Docker", "AWS"],
}
FEATURED_SKILLS = {"Python", "Pandas", "Scikit-learn", "SQL", "Django", "TensorFlow", "LangChain", "Power BI"}

ML_PIPELINE = [
    "Dataset", "Data Cleaning", "EDA", "Feature Engineering", "Train/Test Split", "Model Training", "Evaluation",
    "Prediction",
]

SAMPLE_NOTE = "\n\n> **Sample project** - placeholder content. Replace it with your own work in the admin."

SAMPLE_PROJECTS = [
    {
        "title": "Diabetes Prediction",
        "category": Project.Category.ML,
        "summary": "Sample: classification model that predicts diabetes risk from diagnostic measurements.",
        "tech": ["Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning"],
        "problem_statement": "Early detection of diabetes helps patients get timely care. "
        "This sample project shows how a classifier could flag at-risk patients from routine measurements.",
        "objective": "Build and evaluate a classification model on a public diabetes dataset.",
        "dataset": "Describe the dataset you used here (source, licence, rows, features).",
        "algorithm": "Describe the algorithms you compared (e.g. Logistic Regression, Random Forest).",
        "pipeline": ML_PIPELINE,
        "code": ("Train a baseline model", "from sklearn.linear_model import LogisticRegression\n"
                 "from sklearn.model_selection import train_test_split\n\n"
                 "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n"
                 "model = LogisticRegression(max_iter=1000).fit(X_train, y_train)\n"
                 "print(model.score(X_test, y_test))"),
    },
    {
        "title": "AI Resume Screening",
        "category": Project.Category.AI,
        "summary": "Sample: NLP pipeline that ranks resumes against a job description.",
        "tech": ["Python", "NLP", "Machine Learning"],
        "problem_statement": "Recruiters spend a long time on first-pass resume screening.",
        "objective": "Rank resumes by relevance to a job description using text similarity.",
        "pipeline": ["Resumes", "Text Extraction", "Cleaning", "Vectorisation", "Similarity Scoring", "Ranking"],
    },
    {
        "title": "Student Chatbot",
        "category": Project.Category.GENAI,
        "summary": "Sample: chatbot that answers student questions from course data.",
        "tech": ["Python", "AI", "SQL", "NLP"],
        "problem_statement": "Students repeatedly ask the same questions about courses and schedules.",
        "objective": "Answer common questions automatically using course data stored in SQL.",
        "pipeline": ["User Question", "Intent Detection", "SQL Lookup", "Response Generation", "Answer"],
    },
    {
        "title": "Data Analytics Dashboard",
        "category": Project.Category.ANALYTICS,
        "summary": "Sample: interactive dashboard summarising sales KPIs.",
        "tech": ["Python", "Pandas", "Power BI", "SQL"],
        "problem_statement": "Business teams need a single view of key metrics.",
        "objective": "Clean raw data with Pandas and build an interactive Power BI dashboard.",
        "pipeline": ["Raw Data", "SQL Extraction", "Pandas Cleaning", "Data Model", "Power BI Dashboard"],
    },
    {
        "title": "Django Student Management System",
        "category": Project.Category.DJANGO,
        "summary": "Sample: web app to manage students, courses and attendance.",
        "tech": ["Python", "Django", "PostgreSQL", "HTML", "CSS", "JavaScript"],
        "problem_statement": "Institutions track student records in scattered spreadsheets.",
        "objective": "Provide a secure web app for student, course and attendance management.",
        "pipeline": ["Browser", "Django Views", "ORM", "PostgreSQL", "Templates", "Response"],
    },
]


class Command(BaseCommand):
    help = "Seed study categories, skills and clearly marked sample projects."

    @transaction.atomic
    def handle(self, *args, **options):
        profile = SiteProfile.load()
        if profile.full_name in ("Your Name", "", None):
            profile.full_name = "Naveenkumar"
            profile.save(update_fields=["full_name"])

        for order, (name, icon) in enumerate(STUDY_CATEGORIES):
            defaults = {"icon": icon, "order": order}
            if name in CATEGORY_SLUGS:
                defaults["slug"] = CATEGORY_SLUGS[name]
            StudyCategory.objects.get_or_create(name=name, defaults=defaults)

        # Demo skills and sample projects are only for an empty database, so real
        # content (e.g. from `manage.py load_profile`) is never mixed with demo data.
        seed_skills = not Skill.objects.exists()
        seed_projects = not Project.objects.exists()

        for category, names in SKILLS.items() if seed_skills else ():
            for order, name in enumerate(names):
                Skill.objects.get_or_create(
                    name=name, category=category,
                    defaults={"order": order, "is_featured": name in FEATURED_SKILLS, "icon": name.lower()},
                )

        for name in ["Python", "AI", "Machine Learning", "Data Science", "Django", "GenAI", "Career", "Projects",
                     "Tutorials"]:
            BlogCategory.objects.get_or_create(name=name)

        created = 0
        for order, spec in enumerate(SAMPLE_PROJECTS if seed_projects else ()):
            if Project.objects.filter(title=spec["title"]).exists():
                continue
            project = Project.objects.create(
                title=spec["title"],
                category=spec["category"],
                summary=spec["summary"],
                problem_statement=spec["problem_statement"] + SAMPLE_NOTE,
                objective=spec["objective"],
                dataset=spec.get("dataset", ""),
                algorithm=spec.get("algorithm", ""),
                pipeline_steps=spec["pipeline"],
                is_sample=True,
                is_published=True,
                is_featured=order < 3,
                order=order,
            )
            project.technologies.set([Technology.objects.get_or_create(name=t)[0] for t in spec["tech"]])
            if "code" in spec:
                title, code = spec["code"]
                project.code_snippets.create(title=title, code=code, language="python")
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(STUDY_CATEGORIES)} study categories, {Skill.objects.count()} skills, "
            f"{created} new sample projects."
        ))
