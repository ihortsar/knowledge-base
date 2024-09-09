from django.shortcuts import render
from django.views import View
from .models import Article
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q


def add_article(request):
    """
    Render the 'Add Article' form page.

    Args:
        request: HTTP request object.

    Returns:
        Response: Rendered HTML template for the 'Add Article' page.
    """
    return render(request, "html/add_article.html")


def agb(request):
    """
    Render the 'AGB' page.

    Args:
        request: HTTP request object.

    Returns:
        Response: Rendered HTML template for the AGB page.
    """
    return render(request, "html/agb.html")


def imprint(request):
    return render(request, "html/imprint.html")


class Articles(View):
    """
    Handles both GET and POST requests for managing articles.
    
    GET request: Displays articles (filtered or all).
    POST request: Creates a new article.
    """
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new article.

        Args:
            request: HTTP request object containing the form data.

        Returns:
            Response: Redirects to the articles list page after successful creation.
        """
        
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.POST.get("author")

        Article.objects.create(title=title, content=content, author=author)
        return redirect(reverse("articles"))

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to fetch and display articles.

        Args:
            request: HTTP request object containing query parameters.

        Returns:
            Response: Rendered HTML template with filtered articles if a query is provided,
                      or all articles if no query is given.
        """
        query = request.GET.get("q", "")
        if query:
            articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        else:
            articles = Article.objects.all().order_by("title")
        return render(request, "html/find_article.html", {"articles": articles})
