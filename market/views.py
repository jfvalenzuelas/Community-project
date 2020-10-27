from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse
from .models import Product, Image, Category
from django.contrib.auth.models import User
from .forms import ProductForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    products_list = []
    products = Product.objects.filter(sold=False)
    for product in products:
        thumbnail = Image.objects.filter(product=product)[0]
        product_data = {
            "product": product,
            "thumbnail": thumbnail
        }
        products_list.append(product_data)

    return render(request, 'market/home.html', {'products_list':products_list})

@login_required
def new_post(request):
    if request.method == 'POST':
         # create a form instance and populate it with data from the request.
        form = ProductForm(request.POST)

        if form.is_valid():
            # Get selected Category
            category = Category.objects.get(pk=form['category'].data)

            # Create a new Market Product
            product = Product(title=form['title'].data, description=form['description'].data, price=form['price'].data, category=category, created_by=request.user)
            product.save()

            length = request.POST.get('length')

            for file_num in range(0, int(length)):
                Image.objects.create(
                    product = product,
                    image = request.FILES.get(f'image{file_num}')
                )
            data = {
                "message": "Product was published successfully",
                "redirect": reverse('market_home')
            }
            return JsonResponse({'data': data}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = ProductForm()

        return render(request, 'market/new-post.html', {'form':form})

def view_post(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    product_category = get_object_or_404(Category, pk=product.category.id)
    photos = Image.objects.filter(product=product).order_by('id')

    return render(request, 'market/view-post.html', {
        'product':product, 
        'product_category':product_category,
        'photos': photos
    })

def edit_post(request, product_pk):
    if request.method == 'GET':
        # process GET method
        product = get_object_or_404(Product, pk=product_pk)
        product_category = get_object_or_404(Category, pk=product.category.id)
        photos = Image.objects.filter(product=product).order_by('id')

        formContext = {
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'category': product.category
        }

        form = ProductForm(formContext)

        return render(request, 'market/edit-post.html', {
            'form': form,
            'product': product
        })

    else:
        # process POST method
        product = get_object_or_404(Product, pk=product_pk)
        form = ProductForm(request.POST or None, instance=product)

        if form.is_valid():
            form.save()

            data = {
                "message": "Product was edited successfully",
                "redirect": reverse('community_profile')
            }
            return JsonResponse({'data': data}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({'error': form.errors}, status=400)

def delete_post(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        product.delete()

        return redirect('community_profile')

def sold_product(request, product_pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_pk)
        product.sold = not product.sold
        product.save()

        if (product.sold):
            data = {
                "message": "Product marked as sold",
                "sold": product.sold
            }
        else:
            data = {
                "message": "Product marked as available",
                "sold": product.sold
            }

        return JsonResponse(data, status=200)
