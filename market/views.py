from django.shortcuts import render, redirect, get_object_or_404
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
         # create a form instance and populate it with data from the request:
        form = ProductForm(request.POST)

        if form.is_valid():
            # Get selected Category
            category = Category.objects.get(title=form['category'].data.capitalize())

            # Create a new Market Product
            product = Product(title=form['title'].data, description=form['description'].data, price=form['price'].data, category=category, created_by=request.user)
            product.save()

            length = request.POST.get('length')

            for file_num in range(0, int(length)):
                Image.objects.create(
                    product = product,
                    image = request.FILES.get(f'image{file_num}')
                )

            return redirect('market_home')
        else:
            return render(request, 'market/new-post.html', {
                'form':form
            })
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

def delete_post(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'POST':
        product.delete()

        return redirect('market_home')
