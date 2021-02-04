# Create your tests here.
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Writer, Article

WRITER_NAMES = [
    "Fernando Pessoa",
    "ß∂åß∂•ªåß∂ª˜˜™˜˜˜åºßª∂",
    "≤∂≥åß∂øç∂¢∞¡™ªº∂∆",
    "¨ÎÍ¨ÓÅÍ·°Î‡",
]
CORRECT_PAYLOADS = [
    {"status": True, "edited_by": 1},
    {"status": False, "edited_by": 1},
]
WRONG_PAYLOADS = [
    {"name": "Test"},
    {"id": 2},
    {"status": True},
    {"edited_by": 1},
    {"asd": True},
    {},
]


class DashboardPageTests(TestCase):
    def test_dashboard_page_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/dashboard.html")


class ArticleCreatePageTests(TestCase):
    def test_article_create_page_status_code(self):
        response = self.client.get("/article/")
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("article_create"))
        self.assertEquals(response.status_code, 302)


class ArticleApprovalPageTests(TestCase):
    # def test_article_approval_page_status_code(self):
    #     response = self.client.get("article-approval")
    #     self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("article_approval"))
        self.assertEquals(response.status_code, 302)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('article_approval'))
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'blog/approval.html')


class ArticleEditedPageTests(TestCase):
    # def test_article_edited_page_status_code(self):
    #     response = self.client.get("article-edited")
    #     self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse("article_edited"))
        self.assertEquals(response.status_code, 302)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('article_edited'))
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'blog/edited.html')


class WriterTests(TestCase):
    def setUp(self):
        for name in WRITER_NAMES:
            User.objects.create(username=name, password="123")

    def test_name_content(self):
        for name in WRITER_NAMES:
            writer = Writer.objects.get(name=name)
            expected_object_name = name
            self.assertEquals(f"{writer.name}", expected_object_name)


class ApprovalTests(TestCase):
    def setUp(self):
        for name in WRITER_NAMES:
            User.objects.create(username=name, password="123")
        for writer in Writer.objects.all():
            Article.objects.create(
                title=f"title - {writer.name}",
                content="Hello",
                written_by=writer,
            )

    def test_api(self):
        articles = Article.objects.all()
        for article in articles:
            url = f"/article/{article.id}/update_article/"
            print("\n===== CORRECT_PAYLOADS =====")
            for cp in CORRECT_PAYLOADS:
                # Correct request
                print("\n========== Using PUT method")
                response = self.client.put(
                    url, data=json.dumps(cp), content_type="application/json"
                )
                print(cp)
                print(f"{response.status_code} == 200")
                self.assertEquals(response.status_code, 200)

                # ========== Using POST method. Not correct
                print("\n========== Using POST method. Not correct")
                response = self.client.post(
                    url, data=json.dumps(cp), content_type="application/json"
                )
                print(cp)
                print(f"{response.status_code} == 405")
                self.assertEquals(response.status_code, 405)

                # ========== Using GET method. Not correct
                print("\n========== Using GET method. Not correct")
                response = self.client.get(url)
                print(cp)
                print(f"{response.status_code} == 405")
                self.assertEquals(response.status_code, 405)
            # Using wrong payloads
            print("\n===== WRONG_PAYLOADS =====")
            for wp in WRONG_PAYLOADS:
                print("\n========== Using PUT method")
                response = self.client.put(
                    url, data=json.dumps(wp), content_type="application/json"
                )
                print(wp)
                print(f"{response.status_code} == 200")
                self.assertNotEquals(response.status_code, 200)

                # ========== Using POST method. Not correct
                print("\n========== Using POST method. Not correct")
                response = self.client.post(
                    url, data=json.dumps(wp), content_type="application/json"
                )
                print(wp)
                print(f"{response.status_code} == 405")
                self.assertEquals(response.status_code, 405)

                # ========== Using GET method. Not correct
                print("\n========== Using GET method. Not correct")
                response = self.client.get(url)
                print(wp)
                print(f"{response.status_code} == 405")
                self.assertEquals(response.status_code, 405)
