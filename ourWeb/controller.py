from ourWeb.models import ProdOrder,Order 

def post_update_prod_price(prod):
    prods =  ProdOrder.objects.filter( prod=prod )
    orders = Order.objects.filter(
                id__in = prods.filter(
                                order__status=Order.IN_PROCESS
                            ).values('order').distinct())
    for o in orders:
        o.update_total()
