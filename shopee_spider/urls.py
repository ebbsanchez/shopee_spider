from django.urls import path, include
from . import views


app_name = 'shopee_spider'

urlpatterns = [
    path('', views.index, name='index'),
    path('abandened/<int:item_id>', views.item_abandoned, name="abandoned"),
    path('following/<int:item_id>', views.item_following, name="following")
]
