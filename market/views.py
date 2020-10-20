from django.shortcuts import render, redirect, get_object_or_404
from .models import MarketPost, ImageAlbum, Image, MarketProduct, MarketCategory

from .forms import MarketPostForm

# Create your views here.
def home(request):
    market_posts = MarketPost.objects.filter(product__sold=False)

    return render(request, 'market/home.html', {'market_posts':market_posts})

def new_post(request):
    if request.method == 'POST':
         # create a form instance and populate it with data from the request:
        form = MarketPostForm(request.POST)

        if form.is_valid():
            print(form['category'].data)
            # Create a new Image Album
            album = ImageAlbum()
            album.save()

            # Get selected Category
            category = MarketCategory.objects.get(title=form['category'].data.capitalize())

            # Create a new Market Product
            market_product = MarketProduct(name=form['name'].data, description=form['description'].data, price=form['price'].data, album=album, category=category)
            market_product.save()

            # Create a new Market Post
            market_post = MarketPost(title=form['title'].data, product=market_product)
            market_post.save()

            return redirect('home')
        else:
            return render(request, 'market/new-post.html', {'form':form})
    else:
        form = MarketPostForm()

        return render(request, 'market/new-post.html', {'form':form})

def view_post(request, post_pk):
    market_post = get_object_or_404(MarketPost, pk=post_pk)
    market_product = get_object_or_404(MarketProduct, pk=market_post.product)
    product_category = get_object_or_404(MarketCategory, pk=market_product.category.id)

    return render(request, 'market/view-post.html', {'market_post':market_post, 'market_product':market_product, 'product_category':product_category})

def delete_post(request, post_pk):
    market_post = get_object_or_404(MarketPost, pk=post_pk)
    market_product = get_object_or_404(MarketProduct, pk=market_post.id)
    product_album = get_object_or_404(ImageAlbum, pk=market_product.album.id)

    if request.method == 'POST':
        product_album.delete()

        return redirect('home')
