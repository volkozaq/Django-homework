from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from books.models import Book


def index_view(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books_objects = Book.objects.all()
    books= [{'id': b.id, 'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in books_objects]
    context = {'books': books}
    print(context)
    return render(request, template, context)

def pub_date_view(request, pub_date):
    template = 'books/books_list.html'

    book_objects = Book.objects.all()
    books= [{'id': b.id, 'name': b.name, 'author': b.author, 'pub_date': b.pub_date} for b in book_objects]
    print(books)
    pub_dates = Book.objects.values('pub_date').distinct()
    print(pub_dates)
    p_dates = []
    for p in pub_dates:
        p_dates.append(p['pub_date'])
    print(p_dates)
    p_dates = sorted(p_dates)
    print(p_dates)
    index = 0
    for i, p_d in enumerate(p_dates):
        if str(p_d) == str(pub_date):
            index = i

    try:
        next_date = p_dates[index+1]
        print(f'Next is {next_date}')
    except IndexError:
        next_date = None

    if index != 0:
        prev_date = p_dates[index-1]
    else:
        prev_date = None
    books_by_date = []
    for b in books:
        if str(b['pub_date']) == str(pub_date):
            books_by_date.append(b)
    print(books_by_date)
    paginator = Paginator(books_by_date, 10)
    context = {'books': books_by_date,
               'next': next_date,
               'prev': prev_date
               }
    return render(request, template, context)

