from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def products_page(request):
    return render(request, 'all_products.html')
