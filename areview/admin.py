from django.contrib import admin

# Register your models here.
from .models import Review, Asin,Post


class ReviewTexture(admin.ModelAdmin):
    model=Review
    list_display = ('asin','page_number', 'review_text', 'pub_date', 'review_header', 'review_rating', 'review_author')
    list_filter = ['pub_date', 'review_rating']
    search_fields = ['review_text']

class AsinRegister(admin.ModelAdmin):
    model=Asin
    list_display=['name']
    search_fields = ['name']

admin.site.register(Review, ReviewTexture)
admin.site.register(Asin, AsinRegister)
admin.site.register(Post)
