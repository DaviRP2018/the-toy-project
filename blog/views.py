from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, F, Case, When
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView

from blog.models import Article


class DashboardView(TemplateView):
    template_name = "blog/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.values("written_by__name").annotate(
            written_count=Count(F("written_by")),
            written_count_last_thirty=Count(
                Case(
                    When(
                        created_at__gt=timezone.now() - timedelta(days=30),
                        then=1
                    )
                )
            ),
        )
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ["title", "content"]
    template_name = "blog/article_form.html"

    def get_success_url(self):
        return reverse("dashboard")

    def form_valid(self, form):
        http_response = super().form_valid(form)
        self.object.written_by = self.request.user.writer
        self.object.save(update_fields=["written_by"])
        return http_response


class ArticleApproval(PermissionRequiredMixin, TemplateView):
    template_name = "blog/approval.html"
    permission_denied_message = "You need to be an editor do access this page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.all()
        return context

    def has_permission(self):
        if not isinstance(self.request.user, AnonymousUser):
            return self.request.user.writer.is_editor
        return False


class ArticleEdited(PermissionRequiredMixin, TemplateView):
    template_name = "blog/edited.html"
    permission_denied_message = "You need to be an editor do access this page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.all()
        return context

    def has_permission(self):
        if not isinstance(self.request.user, AnonymousUser):
            return self.request.user.writer.is_editor
        return False
