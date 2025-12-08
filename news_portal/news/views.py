# news/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Article, Tag, Bookmark

User = get_user_model()


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        qs = Article.objects.all()

        # Якщо користувач не авторизований – показуємо лише публічні
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)

        # Пошук
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(body__icontains=q)
            )

        # Сортування
        order = self.request.GET.get('order')
        if order == 'author':
            qs = qs.order_by('author__username', '-created_at')
        elif order == 'tag':
            # Сортування по тегам — спірне, але для завдання достатньо
            qs = qs.order_by('tags__name', '-created_at').distinct()
        else:
            # за датою публікації (за замовчуванням, від нових до старих)
            qs = qs.order_by('-created_at')

        # Фільтр по конкретному тегу (якщо треба)
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tags'] = Tag.objects.all()
        ctx['current_order'] = self.request.GET.get('order', 'date')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CommentForm


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = super().get_object(queryset)

        # Якщо стаття не public і користувач не авторизований – 403/redirect
        if not article.is_public and not self.request.user.is_authenticated:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Увійдіть, щоб читати цю статтю.")

        return article

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        article = ctx['article']
        ctx['comments'] = article.comments.filter(is_approved=True)
        ctx['form'] = CommentForm()

        if self.request.user.is_authenticated:
            ctx['is_bookmarked'] = Bookmark.objects.filter(
                user=self.request.user,
                article=article
            ).exists()
        else:
            ctx['is_bookmarked'] = False

        return ctx

    def post(self, request, *args, **kwargs):
        # Обробка створення коментаря
        self.object = self.get_object()
        if not request.user.is_authenticated:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Потрібно увійти, щоб коментувати.")

        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.article = self.object
            form.save()
            return redirect('news:article_detail', slug=self.object.slug)

        ctx = self.get_context_data()
        ctx['form'] = form
        return self.render_to_response(ctx)