from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from django.views import View
from django.db.models import Count
# Create your views here.
from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_tags = Tag.objects.annotate(tag_count=Count("quote")).order_by("-tag_count")[:10]
    return render(request, 'quotes/index.html', context={"top_tags": top_tags, "quotes": quotes_on_page})



def author_detail(request, id):
  author = Author.objects.get(pk=id)
  return render(request, 'quotes/author_detail.html', context={'author': author})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        author_form = AuthorForm(request.POST)

        if form.is_valid():
            author_name = request.POST.get('author')
            author, created = Author.objects.get_or_create(fullname=author_name, defaults={'user': request.user})

            quote = form.save(commit=False)
            quote.user = request.user
            quote.author = author
            quote.save()

            tags = form.cleaned_data['tags']
            new_tags = request.POST.get('new_tags')
            if new_tags:
                new_tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in new_tags.split(',')]
                quote.tags.add(*new_tag_objects)
            quote.tags.add(*tags)
            return redirect("/")
    else:
        form = QuoteForm()
        author_form = AuthorForm()

    return render(request, "quotes/add_quote.html", {"form": form, 'author_form': author_form})


@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)

    if request.user.is_authenticated and quote.user == request.user:
        quote.delete()
        return redirect('/')
    else:
        return JsonResponse({'message': 'Your access was not authorized or Quote does not exist.'}, status=401)


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = AuthorForm()

    return render(request, "quotes/add_author.html", {"form": form})

class TagQuotesView(View):
    template_name = 'quotes/tag_quotes.html'
    quotes_per_page = 10

    def get(self, request, *args, **kwargs):
        tag_name = kwargs['tag_name']
        top_tags = Tag.objects.annotate(tag_count=Count("quote")).order_by("-tag_count")[:10]
        tag = get_object_or_404(Tag, name=tag_name)
        quotes_with_tag = get_list_or_404(Quote.objects.filter(tags=tag))

        paginator = Paginator(quotes_with_tag, self.quotes_per_page)
        page = request.GET.get('page')

        try:
            quotes_per_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            quotes_per_page = paginator.page(1)

        context = {
            'tag_name': tag_name,
            'quotes_with_tag': quotes_per_page,
            "top_tags": top_tags
        }

        return render(request, self.template_name, context)















# @login_required
# def authors(request):
#     author = Author.objects.filter(user=request.user).all()
#     return render(request, 'quotes/base.html', context={"author": author})
#
# @login_required
# def upload(request):
#     form = AuthorForm(instance=Author())
#     if request.method == 'POST':
#         form = AuthorForm(request.POST)
#         if form.is_valid():
#             auth = form.save(commit=False)
#             auth.user = request.user
#             auth.save()
#             return redirect('quotes:base')
#     return render(request, 'quotes/upload.html', {'form': form})










# def upload(request):
#     form = AuthorForm(instance=Author())
#     if request.method == "POST":
#         form = AuthorForm(request.POST, request.FILES, instance=Author())
#         if form.is_valid():
#             # Прив'язуємо користувача і його фотографії, щоб він бачив лише свої фотографії
#             pic = form.save(commit=False)
#             pic.user = request.user
#             pic.save()
#             return redirect(to="app_photo:pictures")
#     return render(request, 'app_photo/upload.html', context={"form": form})




# @login_required
# def edit(request, pic_id):
#     if request.method == "POST":
#         desc = request.POST.get('description')
#         Author.objects.filter(pk=pic_id, user=request.user).update(description=desc)
#         return redirect(to="app_photo:pictures")
#     pic = Author.objects.filter(pk=pic_id, user=request.user).first()
#     return render(request, 'app_photo/edit_desc.html', context={"pic": pic})
#
# @login_required
# def remove(request, pic_id):
#     pic = Author.objects.filter(pk=pic_id, user=request.user)
#     file_path: Path = settings.MEDIA_ROOT / str(pic.first().path)
#     if file_path.exists():
#         file_path.unlink()
#         pic.delete()
#         print('Нарешті ти видалив цю фігню')
#     else:
#         print('Ця фігня настільки жахлива, що я її навіть видалити не можу. Викинь її або я викину тебе!')
#     return redirect(to="app_photo:pictures")