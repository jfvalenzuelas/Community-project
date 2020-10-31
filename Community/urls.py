"""Community URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from community_main import views as community_views
from market import views as market_views
from wall import views as wall_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', community_views.signup_user, name="signup_user"),
    path('login/', community_views.login_user, name="login_user"),
    path('logout/', community_views.logout_user, name="logout_user"),

    #Community_Main
    path('', community_views.home, name="community_home"),
    path('profile', community_views.profile, name="community_profile"),

    #Market
    path('market/', market_views.home, name="market_home"),
    path('market/new-post', market_views.new_post, name="new_post"),
    path('market/view-post/<int:product_pk>', market_views.view_post, name="view_post"),
    path('market/edit-post/<int:product_pk>', market_views.edit_post, name="edit_post"),
    path('market/delete-post/<int:product_pk>', market_views.delete_post, name="delete_post"),
    path('market/sold-product/<int:product_pk>', market_views.sold_product, name="sold_product"),

    #Wall
    path('wall/', wall_views.home, name="wall_home"),
    path('wall/new-post', wall_views.new_post, name="new_wall_post"),
    path('wall/view-post/<int:post_pk>', wall_views.view_post, name="view_wall_post"),
    path('wall/edit-post/<int:post_pk>', wall_views.delete_post, name="delete_wall_post"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
