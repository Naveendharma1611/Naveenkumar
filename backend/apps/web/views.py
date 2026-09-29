"""Server-rendered HTML pages. Every view reads straight from the Django ORM."""
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.blog.models import BlogCategory, BlogPost, Tag
from apps.certificates.models import Certificate
from apps.learning.models import Bookmark, InterviewQuestion, Lesson, LessonNote, Progress, StudyCategory
from apps.portfolio.models import Achievement, Education, Experience, Skill
from apps.projects.models import Project
from apps.quizzes.models import Quiz, QuizAttempt

from .forms import AccountForm, ContactForm, RegisterForm


def page_of(request, qs, per_page=12):
    return Paginator(qs, per_page).get_page(request.GET.get("page"))


# ---------- Portfolio ----------

def home(request):
    return render(request, "web/home.html", {
        "skills": Skill.objects.filter(is_published=True, is_featured=True)[:12],
        "projects": Project.objects.published().filter(is_featured=True).prefetch_related("technologies")[:6],
        "posts": BlogPost.objects.published()[:3],
        "stats": [
            ("Projects", Project.objects.published().count()),
            ("Certificates", Certificate.objects.published().count()),
            ("Lessons", Lesson.objects.published().count()),
            ("Quizzes", Quiz.objects.published().count()),
        ],
    })


def about(request):
    return render(request, "web/about.html", {
        "education": Education.objects.all(),
        "achievements": Achievement.objects.all(),
    })


def skills(request):
    return render(request, "web/skills.html", {"skills": Skill.objects.filter(is_published=True)})


def experience(request):
    return render(request, "web/experience.html", {
        "jobs": Experience.objects.filter(is_published=True),
        "education": Education.objects.all(),
    })


def resume(request):
    return render(request, "web/resume.html", {
        "jobs": Experience.objects.filter(is_published=True),
        "education": Education.objects.all(),
        "skills": Skill.objects.filter(is_published=True),
        "certificates": Certificate.objects.published(),
        "achievements": Achievement.objects.all(),
    })


def projects(request):
    qs = Project.objects.published().prefetch_related("technologies")
    if cat := request.GET.get("category"):
        qs = qs.filter(category=cat)
    if q := request.GET.get("q", "").strip():
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(technologies__name__icontains=q)).distinct()
    return render(request, "web/projects.html", {
        "page": page_of(request, qs), "categories": Project.Category.choices, "q": q,
    })


PROJECT_SECTIONS = [
    ("problem_statement", "Problem statement"), ("objective", "Objective"), ("dataset", "Dataset"),
    ("architecture", "Architecture"), ("data_flow", "Data flow"), ("algorithm", "Algorithm"),
    ("implementation", "Implementation"), ("model_training", "Model training"), ("evaluation", "Evaluation"),
    ("results", "Results"), ("future_improvements", "Future improvements"), ("documentation", "Documentation"),
]


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.published().prefetch_related("technologies", "images", "videos", "code_snippets"), slug=slug
    )
    sections = [(label, getattr(project, field)) for field, label in PROJECT_SECTIONS if getattr(project, field)]
    return render(request, "web/project_detail.html", {"project": project, "sections": sections})


def certifications(request):
    return render(request, "web/certifications.html", {"certificates": Certificate.objects.published()})


def certificate(request, credential_id):
    cert = get_object_or_404(Certificate.objects.published(), credential_id=credential_id)
    return render(request, "web/certificate.html", {"cert": cert})


# ---------- Blog ----------

def blog(request):
    qs = BlogPost.objects.published().select_related("category")
    if cat := request.GET.get("category"):
        qs = qs.filter(category__slug=cat)
    if tag := request.GET.get("tag"):
        qs = qs.filter(tags__slug=tag)
    if q := request.GET.get("q", "").strip():
        qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(content__icontains=q))
    return render(request, "web/blog.html", {
        "page": page_of(request, qs.distinct(), 9), "categories": BlogCategory.objects.all(),
        "tags": Tag.objects.all(), "q": q,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost.objects.published().select_related("category", "author"), slug=slug)
    return render(request, "web/blog_detail.html", {"post": post})


# ---------- Learning ----------

def study_materials(request):
    categories = StudyCategory.objects.filter(is_published=True).annotate(
        lesson_count=Count("lessons", filter=Q(lessons__is_published=True), distinct=True)
    )
    return render(request, "web/study_materials.html", {"categories": categories})


def study_category(request, category):
    cat = get_object_or_404(StudyCategory, slug=category, is_published=True)
    courses = cat.courses.published().prefetch_related("materials")
    lessons = Lesson.objects.published().filter(category=cat)
    done = set()
    if request.user.is_authenticated:
        done = set(Progress.objects.filter(user=request.user, lesson__category=cat).values_list("lesson_id", flat=True))
    by_course = {}
    for lesson in lessons:
        by_course.setdefault(lesson.course_id, []).append(lesson)
    return render(request, "web/study_category.html", {
        "category": cat, "done": done, "total": len(lessons),
        "courses": [(c, by_course.get(c.id, [])) for c in courses],
    })


def lesson(request, category, lesson):
    obj = get_object_or_404(
        Lesson.objects.published().select_related("course", "category"), category__slug=category, slug=lesson
    )
    user = request.user
    if request.method == "POST":
        if not user.is_authenticated:
            return redirect(f"/login/?next={request.path}")
        action = request.POST.get("action")
        if action == "bookmark":
            bm, created = Bookmark.objects.get_or_create(user=user, lesson=obj)
            if not created:
                bm.delete()
        elif action == "complete":
            pr, created = Progress.objects.get_or_create(user=user, lesson=obj)
            if not created:
                pr.delete()
        elif action == "note":
            LessonNote.objects.update_or_create(user=user, lesson=obj, defaults={"content": request.POST.get("content", "")[:20000]})
            messages.success(request, "Note saved.")
        return redirect(request.path)

    siblings = list(Lesson.objects.published().filter(course=obj.course).values("slug", "title"))
    idx = next(i for i, s in enumerate(siblings) if s["slug"] == obj.slug)
    ctx = {
        "lesson": obj,
        "materials": obj.materials.all(),
        "prev": siblings[idx - 1] if idx > 0 else None,
        "next": siblings[idx + 1] if idx + 1 < len(siblings) else None,
    }
    if user.is_authenticated:
        ctx["bookmarked"] = Bookmark.objects.filter(user=user, lesson=obj).exists()
        ctx["completed"] = Progress.objects.filter(user=user, lesson=obj).exists()
        ctx["note"] = LessonNote.objects.filter(user=user, lesson=obj).values_list("content", flat=True).first() or ""
    return render(request, "web/lesson.html", ctx)


def interview(request):
    categories = StudyCategory.objects.filter(is_published=True).annotate(
        q_count=Count("interview_questions", filter=Q(interview_questions__is_published=True))
    ).filter(q_count__gt=0)
    return render(request, "web/interview.html", {"categories": categories})


def interview_category(request, category):
    cat = get_object_or_404(StudyCategory, slug=category, is_published=True)
    qs = cat.interview_questions.published()
    if diff := request.GET.get("difficulty"):
        qs = qs.filter(difficulty=diff)
    return render(request, "web/interview_category.html", {
        "category": cat, "questions": qs, "difficulties": InterviewQuestion.Difficulty.choices,
    })


def practice(request):
    quizzes = Quiz.objects.published().select_related("category").annotate(q_count=Count("questions"))
    return render(request, "web/practice.html", {"quizzes": quizzes})


def quiz(request, slug):
    obj = get_object_or_404(Quiz.objects.published(), slug=slug)
    questions = list(obj.questions.all())
    ctx = {"quiz": obj, "questions": questions}
    if request.method == "POST":
        answers, results, score, max_score = {}, [], 0, 0
        for q in questions:
            answer = request.POST.get(f"q{q.id}", "").strip()
            answers[str(q.id)] = answer
            ok = q.grade(answer)
            if ok is not None:
                max_score += q.points
                score += q.points if ok else 0
            chosen = q.options[int(answer)] if q.type == "MCQ" and answer.isdigit() and int(answer) < len(q.options) else answer
            results.append({"q": q, "answer": chosen, "ok": ok})
        percent = round(score * 100 / max_score) if max_score else 0
        if request.user.is_authenticated:
            QuizAttempt.objects.create(
                user=request.user, quiz=obj, submitted_at=timezone.now(), answers=answers, score=score,
                max_score=max_score, percent=percent, timed_out=request.POST.get("timed_out") == "1",
            )
        ctx.update(results=results, score=score, max_score=max_score, percent=percent)
    if obj.show_leaderboard:
        ctx["leaderboard"] = (QuizAttempt.objects.filter(quiz=obj, submitted_at__isnull=False)
                              .select_related("user").order_by("-percent", "submitted_at")[:10])
    return render(request, "web/quiz.html", ctx)


# ---------- Contact & search ----------

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "")).split(",")[0].strip()
        key = f"contact:{ip}"
        if cache.get(key, 0) >= 5:
            messages.error(request, "Too many messages. Please try again later.")
        else:
            cache.set(key, cache.get(key, 0) + 1, 3600)
            msg = form.save(commit=False)
            msg.ip_address = ip or None
            msg.user_agent = request.META.get("HTTP_USER_AGENT", "")[:300]
            msg.save()
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect("contact")
    return render(request, "web/contact.html", {"form": form})


def search(request):
    q = request.GET.get("q", "").strip()
    results = []
    if len(q) >= 2:
        results = [
            ("Projects", [(p.title, p.summary, f"/projects/{p.slug}/")
                          for p in Project.objects.published().filter(Q(title__icontains=q) | Q(summary__icontains=q))[:10]]),
            ("Lessons", [(l.title, l.summary, f"/study-materials/{l.category.slug}/{l.slug}/")
                         for l in Lesson.objects.published().select_related("category")
                         .filter(Q(title__icontains=q) | Q(content__icontains=q))[:10]]),
            ("Blog", [(b.title, b.excerpt, f"/blog/{b.slug}/")
                      for b in BlogPost.objects.published().filter(Q(title__icontains=q) | Q(content__icontains=q))[:10]]),
            ("Interview questions", [(i.question[:120], "", f"/interview/{i.category.slug}/#q{i.id}")
                                     for i in InterviewQuestion.objects.published().select_related("category")
                                     .filter(question__icontains=q)[:10]]),
        ]
        results = [(label, items) for label, items in results if items]
    return render(request, "web/search.html", {"q": q, "results": results})


# ---------- Accounts ----------

def register(request):
    if request.user.is_authenticated:
        return redirect("student")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Welcome! Your account is ready.")
        return redirect("student")
    return render(request, "web/form_page.html", {"form": form, "title": "Create account", "button": "Register",
                                                  "alt": ("Already have an account?", "/login/", "Log in")})


@login_required
def account(request):
    form = AccountForm(instance=request.user)
    pw_form = PasswordChangeForm(request.user)
    if request.method == "POST":
        if request.POST.get("action") == "password":
            pw_form = PasswordChangeForm(request.user, request.POST)
            if pw_form.is_valid():
                update_session_auth_hash(request, pw_form.save())
                messages.success(request, "Password changed.")
                return redirect("account")
        else:
            form = AccountForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated.")
                return redirect("account")
    return render(request, "web/account.html", {"form": form, "pw_form": pw_form})


@login_required
def student(request):
    user = request.user
    done = set(Progress.objects.filter(user=user).values_list("lesson_id", flat=True))
    categories = StudyCategory.objects.filter(is_published=True).annotate(
        total=Count("lessons", filter=Q(lessons__is_published=True), distinct=True)
    ).filter(total__gt=0)
    per_lesson = dict(Lesson.objects.published().filter(id__in=done).values_list("id", "category_id"))
    progress = []
    for c in categories:
        n = sum(1 for cid in per_lesson.values() if cid == c.id)
        progress.append({"category": c, "done": n, "total": c.total, "percent": round(n * 100 / c.total)})
    return render(request, "web/student.html", {
        "progress": progress,
        "completed": len(done),
        "bookmarks": Bookmark.objects.filter(user=user).select_related("lesson__category")[:20],
        "attempts": QuizAttempt.objects.filter(user=user, submitted_at__isnull=False).select_related("quiz")[:20],
    })
