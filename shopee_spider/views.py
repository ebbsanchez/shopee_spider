from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Item
from .scripts import shopee

# Create your views here.


def index(request):
    none_price_count = 0
    Item.objects.all().update(updated=False)
    all_new_items = []
    if request.method == "POST":
        new_items = shopee.getitems()
        all_new_items += new_items
        Item.objects.all().update(updated=False)
        for new_item in new_items:
            item, created = Item.objects.get_or_create(
                itemid=new_item['itemid'])
            if new_item['price'] == None:
                none_price_count += 1
                continue
            elif created:
                item.shopid = new_item['shopid']
                item.name = new_item['name']
                item.item_status = new_item['item_status']
                item.image = new_item['image']
                item.images = new_item['images']
                item.price = new_item['price'] / 100000
                item.price_min = new_item['price_min']
                item.price_max = new_item['price_max']
                item.currency = new_item['currency']
                item.abandoned = False
                item.updated = True
            elif not created and (  # something_changed()
                    item.shopid != new_item['shopid'] or
                    item.name != new_item['name'] or
                    item.item_status != new_item['item_status'] or
                    item.image != new_item['image'] or
                    item.images != new_item['images'] or
                    item.price != new_item['price']/100000 or
                    item.price_min != new_item['price_min'] or
                    item.price_max != new_item['price_max'] or
                    item.currency != new_item['currency']):
                item.abandoned = False
                item.updated = True
                item.shopid = new_item['shopid']
                item.name = new_item['name']
                item.item_status = new_item['item_status']
                item.image = new_item['image']
                item.images = new_item['images']
                item.price = new_item['price']/100000
                item.price_min = new_item['price_min']
                item.price_max = new_item['price_max']
                item.currency = new_item['currency']
            else:  # old item
                pass

            item.save()
        print("[*] Get {} None price".format(str(none_price_count)))
        return HttpResponseRedirect(reverse('shopee_spider:index'))

    items = Item.objects.all()

    context = {
        'items': items,
        'items_counts': len(items)
    }

    if all_new_items != None:
        context['new_items'] = all_new_items

    return render(request, 'shopee/index.html', context)


def show_followering_items(requests):
    items = Item.objects.filter(following=True)
    context = {
        "items": items,
    }
    return render(requests, "shopee/index_with_filter.html", context)


def show_abandoned_items(requests):
    items = Item.objects.filter(abandoned=True)
    context = {
        "items": items,
    }
    return render(requests, "shopee/index_with_filter.html", context)
    return


# def show_eye_on_items(requests):
#     return


# actions
def make_item_abandoned(request, item_id):
    item = Item.objects.get(id=item_id)
    item.abandoned = not item.abandoned
    item.save()
    return HttpResponseRedirect(reverse('shopee_spider:index'))


def make_item_following(request, item_id):
    item = Item.objects.get(id=item_id)
    item.following = not item.following
    item.save()
    return HttpResponseRedirect(reverse('shopee_spider:index'))


def following_list(request):
    return


def abandoned_list(request):
    return
