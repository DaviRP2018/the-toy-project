from datetime import timedelta

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count, F, Case, When
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from blog.forms import WriterForm
from blog.models import Article, Writer
from blog.serializers import ArticleSerializer


class DashboardView(TemplateView):
    template_name = "blog/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.values(
            "written_by__name"
        ).annotate(
            written_count=Count(F("written_by")),
            written_count_last_thirty=Count(
                Case(
                    When(
                        created_at__gt=timezone.now() - timedelta(days=30),
                        then=1,
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


class WriterCreate(CreateView):
    model = Writer
    form_class = WriterForm
    template_name = "blog/writer_form.html"

    def get_success_url(self):
        return reverse("dashboard")

    def form_valid(self, form):
        http_response = super().form_valid(form)
        writer = Writer.objects.get(user_id=self.object.id)
        if "is_editor" in self.request.POST:
            writer.is_editor = True
            writer.save(update_fields=["is_editor"])
        return http_response


class ArticleApproval(PermissionRequiredMixin, TemplateView):
    template_name = "blog/approval.html"
    permission_denied_message = "You need to be an editor do access this page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.order_by("id")
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
        context["articles"] = Article.objects.filter(
            edited_by=self.request.user.writer
        ).order_by("id")
        return context

    def has_permission(self):
        if not isinstance(self.request.user, AnonymousUser):
            return self.request.user.writer.is_editor
        return False


class UpdateArticle(viewsets.ViewSet):
    @action(detail=True, methods=["PUT"])
    def update_article(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        serializer = ArticleSerializer(data=request.data, instance=article)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateWriter(viewsets.ViewSet):
#     @action(detail=True, methods=["POST"])
#     def create_writer(self, request):
#         serializer = WriterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
