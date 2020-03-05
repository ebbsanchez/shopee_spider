from django.urls import path, include
from . import views


app_name = 'shopee_spider'

urlpatterns = [
    path('', views.index, name='index'),
    path('following_items', views.show_followering_items, name="following_items"),
	path('abandoned_items', views.show_abandoned_items, name="abandoned_items"),
	# actions
    path('abandened/<int:item_id>', views.make_item_abandoned, name="abandoned"),
    path('following/<int:item_id>', views.make_item_following, name="following"),

]
