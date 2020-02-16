from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Item
from .scripts import shopee

# Create your views here.


def index(request):

    if request.method == "POST":
        new_items = shopee.getitems()
        Item.objects.all().update(updated=False)
        for new_item in new_items:
            item, created = Item.objects.get_or_create(
                itemid=new_item['itemid'])
            if new_item['price'] == None:
                print("[*] Get price None.. skipping")
                continue
            elif created:
                item.name = new_item['name']
                item.item_status = new_item['item_status']
                item.image = new_item['image']
                item.images = new_item['images']
                item.price = new_item['price']
                item.price_min = new_item['price_min']
                item.price_max = new_item['price_max']
                item.currency = new_item['currency']
                item.abandoned = False
                item.updated = True
            elif not created and (  # something_changed()
                    item.name != new_item['name'] or
                    item.item_status != new_item['item_status'] or
                    item.image != new_item['image'] or
                    item.images != new_item['images'] or
                    item.price != new_item['price'] or
                    item.price_min != new_item['price_min'] or
                    item.price_max != new_item['price_max'] or
                    item.currency != new_item['currency']):
                item.abandoned = False
                item.updated = True
                item.name = new_item['name']
                item.item_status = new_item['item_status']
                item.image = new_item['image']
                item.images = new_item['images']
                item.price = new_item['price']
                item.price_min = new_item['price_min']
                item.price_max = new_item['price_max']
                item.currency = new_item['currency']
            else:  # old item
                pass

            item.save()
            return HttpResponseRedirect(reverse('shopee_spider:index'))
    items = Item.objects.all()
    context = {
        'items': items,
        'items_counts': len(items)
    }
    return render(request, 'shopee/index.html', context)


def item_abandoned(request, item_id):
    item = Item.objects.get(id=item_id)
    item.abandoned = True
    item.save()
    return HttpResponseRedirect(reverse('shopee_spider:index'))


def item_following(request, item_id):
    item = Item.objects.get(id=item_id)
    item.following = True
    item.save()
    return HttpResponseRedirect(reverse('shopee_spider:index'))
