from django.contrib import admin
from market.models import MarketProduct, MarketCategory, MarketPost, Image, ImageAlbum
# Register your models here.
class MarketPostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(MarketCategory)
admin.site.register(Image)
admin.site.register(ImageAlbum)
admin.site.register(MarketProduct)
admin.site.register(MarketPost, MarketPostAdmin)