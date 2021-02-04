"""the_toy_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers

from blog.views import (
    DashboardView,
    ArticleCreate,
    ArticleApproval,
    ArticleEdited,
    UpdateArticle, WriterCreate,
)
from the_toy_project.views import logout_writer

router = routers.DefaultRouter()
router.register(r"article", UpdateArticle, basename="update_article")

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout", logout_writer, name="logout_writer"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("writer/", WriterCreate.as_view(), name="writer_create"),
    path("article/", ArticleCreate.as_view(), name="article_create"),
    path(
        "article-approval", ArticleApproval.as_view(), name="article_approval"
    ),
    path("article-edited", ArticleEdited.as_view(), name="article_edited"),
]

urlpatterns += router.urls
