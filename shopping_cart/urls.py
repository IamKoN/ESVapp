from django.conf.urls import url

from . import views

app_name = 'shopping_cart'

urlpatterns = [
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', views.order_details, name="order_summary"),
    url(r'^success/$', views.success, name='purchase_success'),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction_records,
        name='update_records')
]