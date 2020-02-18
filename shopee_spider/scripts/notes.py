"{}/{}-{}.{}.{}".format('https://shopee.tw',new_items[0]['name'].replace(' ','-'),'i',new_items[0]['shopid'], new_items[0]['itemid'])

SHELL:
item.url = "{}/{}-{}.{}.{}".format('https://shopee.tw',item.name.replace(' ','-'),'i',item.shopid, item.itemid)

* "Accept", "application/json"

* 可以撈JSON+LD
<script type="application/ld+json">
    { 
   "@context":"http://schema.org",
   "@type":"Product",
   "name":"【eYe攝影】現貨 馬歇爾 Marshall Stockwell II 二代 可攜式 藍牙音響 無線喇叭 藍芽音箱 手提",
   "description":"",
   "url":"https://shopee.tw/【eYe攝影】現貨-馬歇爾-Marshall-Stockwell-II-二代-可攜式-藍牙音響-無線喇叭-藍芽音箱-手提-i.2739654.2800358164",
   "productID":"2800358164",
   "image":"https://cf.shopee.tw/file/abffb596b0acf0de92865611b615acd9",
   "brand":"Marshall 馬歇爾",
   "offers":{ 
      "@type":"AggregateOffer",
      "lowPrice":"7990.00",
      "highPrice":"8500.00",
      "priceCurrency":"TWD",
      "availability":"http://schema.org/InStock"
   },
   "aggregateRating":{ 
      "@type":"AggregateRating",
      "bestRating":5,
      "worstRating":1,
      "ratingCount":"6",
      "ratingValue":"4.83"
   }
}
</script>
<script>
function showBody() {
    document && document.body && (document.body.style.visibility = "visible")
}
var SHORT_URL_MAX_LENGTH = 256,
    pathname = location && location.pathname;
if ("/" !== pathname && pathname.length < SHORT_URL_MAX_LENGTH && "" === location.hash && -1 === pathname.indexOf("-") && 0 === pathname.lastIndexOf("/")) {
    document && document.body && (document.body.style.visibility = "hidden"), setTimeout(showBody, 5e3);
    var xhr = new XMLHttpRequest;
    xhr.open("GET", "/api/v0/is_short_url/?path=" + pathname.replace("/", "")), xhr.setRequestHeader("Content-Type", "application/json"), xhr.setRequestHeader("Accept", "application/json"), xhr.onreadystatechange = function() {
        if (4 === this.readyState)
            if (200 === this.status)
                if (JSON.parse(this.responseText).error) showBody();
                else {
                    var e = document.createElement("a");
                    e.href = location.href, e.search += "?" === e.search[0] ? "&__classic__=1" : "?__classic__=1", location.href = e.href
                }
        else showBody()
    }, xhr.send()
}
</script>



# def testlen(keyword,s):
#     biggest = 0
#     for item in s.items:
#         title_len = len(str(item[keyword]))
#         if title_len > biggest:
#             biggest=title_len
#             bname=item[keyword]
#     print('format: {}'.format(type(s.items[0][keyword])))
#     print("""item[{keyword}] max_length = {max_length}
# {keyword}: {name}""".format(keyword=keyword, max_length=biggest, name=bname))


# def r(nameOfModule):
#     import importlib
#     importlib.reload(nameOfModule)

# :authority: shopee.tw
# :method: GET
# :path: /api/v2/search_items/?by=relevancy&keyword=marshall%20stockwell&limit=50&newest=0&order=desc&page_type=search&version=2
# :scheme: https
# accept: */*
# accept-encoding: gzip, deflate, br
# accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6
# cookie: _gcl_au=1.1.2098345466.1581707635; _med=refer; csrftoken=oMs1RLrqT8FlYliqyOyn860UYB2244kX; __BWfp=c1581707636071x709c604a3; SPC_IA=-1; SPC_EC=-; SPC_U=-; REC_T_ID=2560c43c-4f5e-11ea-be85-d094668e4ae3; SPC_F=dvDwxMitnpbVXIBW3QN9P76h7T0JOuU9; REC_T_ID=256f68e6-4f5e-11ea-b272-b4969130c480; SPC_SI=tirs2imqpt8xwfw4yjws9c3bvk5drbc6; _ga=GA1.2.500498420.1581707637; _gid=GA1.2.1868143270.1581707637; language=zhHant; SPC_R_T_ID="x93tuSqAwzZN+Sq7dMzsKI7SSSOC+7t1OhyRThEsAsUj6kdG1db0P9WmrvLCc8pdzDlBy/B0Ztnsag879GpMsJD/uw605eQe5apinM5KgFw="; SPC_T_IV="0t8Yv2q0adXaFHTU73KVbw=="; SPC_R_T_IV="0t8Yv2q0adXaFHTU73KVbw=="; SPC_T_ID="x93tuSqAwzZN+Sq7dMzsKI7SSSOC+7t1OhyRThEsAsUj6kdG1db0P9WmrvLCc8pdzDlBy/B0Ztnsag879GpMsJD/uw605eQe5apinM5KgFw="
# if-none-match-: 55b03-ef0ab7fbbf9e315b43ebfee7ed98cf45
# referer: https://shopee.tw/search?keyword=marshall%20stockwell&page=0
# sec-fetch-dest: empty
# sec-fetch-mode: cors
# sec-fetch-site: same-origin
# user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36
# x-api-source: pc
# x-requested-with: XMLHttpRequest


# attr=[
#     itemid
#     # welcome_package_info
#     # liked
#     # recommendation_info
#     # bundle_deal_info
#     # price_max_before_discount
#     image
#     # is_cc_installment_payment_eligible
#     # shopid
#     # can_use_wholesale
#     # group_buy_info
#     # reference_item_id
#     currency
#     # raw_discount
#     # show_free_shipping
#     # video_info_list
#     # ads_keyword
#     # collection_id
#     images
#     # match_type
#     # price_before_discount
#     # is_category_failed
#     # show_discount
#     # cmt_count
#     # view_count
#     # display_name
#     # catid
#     # json_data
#     # upcoming_flash_sale
#     # is_official_shop
#     # brand
#     price_min
#     # liked_count
#     # can_use_bundle_deal
#     # show_official_shop_label
#     # coin_earn_label
#     # price_min_before_discount
#     # cb_option
#     # sold
#     # deduction_info
#     # stock
#     # status
#     price_max
#     # add_on_deal_info
#     # is_group_buy_item
#     # flash_sale
#     price
#     # shop_location
#     # item_rating
#     # show_official_shop_label_in_title
#     # tier_variations
#     # is_adult
#     # discount
#     # flag
#     # is_non_cc_installment_payment_eligible
#     # has_lowest_price_guarantee
#     # has_group_buy_stock
#     # preview_info
#     # welcome_package_type
#     name
#     # distance
#     # adsid
#     # ctime
#     # wholesale_tier_list
#     # show_shopee_verified_label
#     # campaignid
#     # show_official_shop_label_in_normal_position
#     item_status
#     # shopee_verified
#     # hidden_price_display
#     # size_chart
#     # item_type
#     # shipping_icon_type
#     # campaign_stock
#     # label_ids
#     # service_by_shopee_flag
#     # badge_icon_type
#     # historical_sold
#     # transparent_background_image
# ]
