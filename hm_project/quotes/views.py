from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
from .forms import AuthorForm
from .models import Author
# Create your views here.
from .utils import get_mongodb

def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

@login_required
def authors(request):
    author = Author.objects.filter(user=request.user).all()
    return render(request, 'quotes/base.html', context={"author": author})

@login_required
def upload(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            auth = form.save(commit=False)
            auth.user = request.user
            auth.save()
            return redirect('quotes:base')
    return render(request, 'quotes/upload.html', {'form': form})
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