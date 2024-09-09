from django.test import TestCase
from django.urls import reverse
from articles.models import Article
from django.test import Client


class TestArticlesView(TestCase):
    def setUp(self):
        self.client = Client()
        self.articles_url = reverse("articles")
        Article.objects.create(
            title="First Article", content="This is the first article.", author="Author 1"
        )
        Article.objects.create(
            title="Second Article", content="This is the second article.", author="Author 2"
        )

    def test_create_article(self):
        data = {
            "title": "Test Article",
            "content": "This is a test article.",
            "author": "Test Author",
        }
        response = self.client.post(self.articles_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.articles_url)
        article = Article.objects.get(title="Test Article")
        self.assertEqual(article.content, "This is a test article.")
        self.assertEqual(article.author, "Test Author")

    def test_get_all_articles(self):
        response = self.client.get(self.articles_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["articles"]), 2)

    def test_search_articles_by_title(self):
        response = self.client.get(self.articles_url, {"q": "First"})
        self.assertEqual(response.status_code, 200)
        articles = response.context["articles"]
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "First Article")

    def test_search_articles_by_content(self):
        response = self.client.get(self.articles_url, {"q": "second"})
        self.assertEqual(response.status_code, 200)
        articles = response.context["articles"]
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].content, "This is the second article.")
