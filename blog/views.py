from datetime import timedelta

from django.db.models import Count, F, Case, When
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView

from blog.models import Article


class DashboardView(TemplateView):
    template_name = "blog/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["writers"] = Article.objects.values("written_by").annotate(
            written_count=Count(F("written_by")),
            written_count_last_thirty=Count(Case(When(
                created_at__lt=timezone.now() - timedelta(days=30),
                then=1
            )))
        )
        return context


class ArticleCreate(CreateView):
    model = Article
    fields = ["title", "content"]

    def get_success_url(self):
        return reverse("dashboard")


class ArticleApproval(TemplateView):
    template_name = "blog/approval.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.all()
        return context


class ArticleEdited(TemplateView):
    template_name = "blog/edited.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.all()
        return context
