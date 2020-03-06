from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Item
from .scripts.shopee import shopeeSpider


def index(request):
    Item.objects.all().update(updated=False)
    if request.method == "POST":
        try:
            new_item_count, updated_item_count = run_spider(
            request, request.POST['search_keyword'])
        except TypeError as e:
            print(e)
            messages.warning(request, "Spider got wrong. Please check console")
            return HttpResponseRedirect(reverse("shopee_spider:index"))
        messages.info(request, "{} new item Added. {} old items updated.".format(
            new_item_count, updated_item_count
        ))
        return HttpResponseRedirect(reverse('shopee_spider:index'))

    items = Item.objects.all()

    context = {
        'items': items,
        'items_counts': len(items)
    }

    return render(request, 'shopee/index.html', context)


def show_followering_items(request):
    items = Item.objects.filter(following=True)
    context = {
        "items": items,
    }
    return render(request, "shopee/index_with_filter.html", context)


def show_abandoned_items(request):
    items = Item.objects.filter(abandoned=True)
    context = {
        "items": items,
    }
    return render(request, "shopee/index_with_filter.html", context)
    return


def test(request):

    if request.method == "POST":
        data = request.POST.get('search_keyword', '')
        messages.info(request, data)
        if data == '':
            messages.warning(request, "You can't pass empty keyword.")
        return HttpResponseRedirect(reverse('shopee_spider:test'))
    return render(request, "shopee/test.html")


# def show_eye_on_items(requests):
#     return

# actions_views


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


# Functions
def run_spider(request, keyword, limit=9999):

    new_items_count = 0
    updated_items_count = 0

    Item.objects.all().update(updated=False)

    # SPIDER
    spider = shopeeSpider()
    
    new_items = spider.search(keyword=keyword, limit=limit)
    for new_item in new_items:
        item, created = Item.objects.get_or_create(
            itemid=new_item['itemid'])

        if created:
            new_items_count += 1
            item = save_data(item, new_item)
        elif not created and (  # something_changed()
                item.name != new_item['name'] or
                item.item_status != new_item['item_status'] or
                item.image != new_item['image'] or
                item.images != new_item['images'] or
                item.price != new_item['price']):
            updated_items_count += 1
            item = save_data(item, new_item)
        else:  # old item
            pass
        item.save()
    return new_items_count, updated_items_count


def save_data(item, new_item):
    item.itemid = new_item['itemid']
    item.shopid = new_item['shopid']
    item.name = new_item['name']
    item.brand = new_item['brand']
    item.item_status = new_item['item_status']
    item.image = new_item['image']
    item.images = new_item['images']
    item.price = new_item['price']
    item.price_min = new_item['price_min']
    item.price_max = new_item['price_max']
    item.currency = new_item['currency']
    item.stock = new_item['stock']
    item.view_count = new_item['view_count']
    item.liked_count = new_item['liked_count']
    item.url = new_item['url']

    # Many to many relationship
    # item.tag = new_item['tag_name']

    item.updated = True
    return item
