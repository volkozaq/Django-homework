from operator import itemgetter

from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'

    phone_objects = Phone.objects.all()
    phones = [{'id': p.id, 'name': p.name, 'price': p.price, 'image': p.image,
               'release_date': p.release_date, 'lte_exists': p.lte_exists, 'slug': p.slug} for p in phone_objects]
    sort = request.GET.get('sort', 'id')
    if sort == 'name':
        phones = sorted(phones, key=itemgetter('name'))
    elif sort == 'min_price':
        phones = sorted(phones, key=itemgetter('price'))
    elif sort == 'max_price':
        phones = sorted(phones, key=itemgetter('price'), reverse=True)
    else:
        phones = sorted(phones, key=itemgetter('id'))
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_objects = Phone.objects.filter(slug = slug)
    phone = [{'id': p.id, 'name': p.name, 'price': p.price, 'image': p.image,
               'release_date': p.release_date, 'lte_exists': p.lte_exists, 'slug': p.slug} for p in phone_objects]
    context = {'phone': phone[0]}
    return render(request, template, context)
