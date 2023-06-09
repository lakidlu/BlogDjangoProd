import datetime

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Summary, Connections, Exchanges
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import requests
import json


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.object.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.2).order_by('-rank')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


def post_share(request, post_id):
    # Pobranie posta na podstawie jego identyfikatora
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Formularz zostal wyslany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Weryfikacja pól formularza zakończyła siępowodzeniem...
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"', format(cd['name'],
                                                                     cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez: {}: {}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
            # Więc można wysłać maila
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)  # trzy posty na kazdej stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # jezeli zmienna page nie jest liczba calkowita
        # wowczas pobierana jest pierwsza strona wynikow
        posts = paginator.page(1)
    except EmptyPage:
        # jezeli zmienna page ma wartosc wieksza niz numer ostatniej strony
        # wynikow wtedy pobierana jest ostatnia strona wynikow.
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Lista aktywnych komentarzy dla danego posta
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # Komentarz opublikowany
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Utworzenie obiektu comment: jeszcze jednak nie zapisujemy go w bazie danych
            new_comment = comment_form.save(commit=False)
            # Przypisanie komentarza do bieżącego posta
            new_comment.post = post
            # Zapisanie komentarza wbazie danych
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids) \
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
        .order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/details.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})


def production_view(request):
    URL = "https://www.pse.pl/transmissionMapService"
    page = requests.get(URL)

    datas = json.loads(page.text)

    current_data = Summary()
    try:
        if request.method == "GET" or request.method == "POST":
            current_data.status = datas['status']
            current_data.czas = datetime.datetime.now()
            current_data.timestamp = datas['timestamp']
            current_data.PV = datas['data']['podsumowanie']['PV']
            current_data.cieplne = datas['data']['podsumowanie']['cieplne']
            current_data.czestotliwosc = datas['data']['podsumowanie']['czestotliwosc']
            current_data.generacja = datas['data']['podsumowanie']['generacja']
            current_data.inne = datas['data']['podsumowanie']['inne']
            current_data.wiatrowe = datas['data']['podsumowanie']['wiatrowe']
            current_data.wodne = datas['data']['podsumowanie']['wodne']
            current_data.zapotrzebowanie = datas['data']['podsumowanie']['zapotrzebowanie']
    except:
        pass


    return render(request,
                  'blog/production.html',
                  {'current_data': current_data,
                   }
                  )

def exchange_view(request):
    URL = "https://www.pse.pl/transmissionMapService"
    page = requests.get(URL)
    datas = json.loads(page.text)
    connections_data_se = Connections()
    connections_data_cz = Connections()
    connections_data_de = Connections()
    connections_data_sk = Connections()
    connections_data_ua = Connections()
    connections_data_lt = Connections()
    exchanges_data = Exchanges()
    eksport, importt = exchanges_calculation(datas)
    saldo = eksport + importt

    try:
        if request.method == "GET" or request.method == "POST":
            exchanges_data.timestamp = datas['timestamp']
            exchanges_data.czas = datetime.datetime.now()
            exchanges_data.eksport = abs(eksport)
            exchanges_data.importt = importt
            exchanges_data.saldo = saldo

            connections_data_se.wartosc = datas['data']['przesyly'][0]['wartosc']
            connections_data_se.wartosc_plan = datas['data']['przesyly'][0]['wartosc_plan']
            connections_data_cz.wartosc = datas['data']['przesyly'][2]['wartosc']
            connections_data_cz.wartosc_plan = datas['data']['przesyly'][2]['wartosc_plan']
            connections_data_de.wartosc = datas['data']['przesyly'][1]['wartosc']
            connections_data_de.wartosc_plan = datas['data']['przesyly'][1]['wartosc_plan']
            connections_data_sk.wartosc = datas['data']['przesyly'][3]['wartosc']
            connections_data_sk.wartosc_plan = datas['data']['przesyly'][3]['wartosc_plan']
            connections_data_ua.wartosc = datas['data']['przesyly'][4]['wartosc']
            connections_data_ua.wartosc_plan = datas['data']['przesyly'][4]['wartosc_plan']
            connections_data_lt.wartosc = datas['data']['przesyly'][5]['wartosc']
            connections_data_lt.wartosc_plan = datas['data']['przesyly'][5]['wartosc_plan']
    except:
        pass


    return render(request,
                  'blog/exchange.html',
                  {'connections_data_se': connections_data_se,
                   'connections_data_cz': connections_data_cz,
                   'connections_data_de': connections_data_de,
                   'connections_data_sk': connections_data_sk,
                   'connections_data_ua': connections_data_ua,
                   'connections_data_lt': connections_data_lt,
                   'exchanges_data': exchanges_data,
                   }
                  )


def exchanges_calculation(datas):
    eksport, importt = 0, 0
    for _ in datas['data']['przesyly']:
        if _['wartosc'] > 0:
            importt += _['wartosc']
        elif _['wartosc'] <= 0:
            eksport += _['wartosc']

    return eksport, importt
