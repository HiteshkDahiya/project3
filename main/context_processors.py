from .models import WishlistModel
from .models import CartModel

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = WishlistModel.objects.filter(user=request.user).count()
    return {'total_wis': count}


def cartlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartModel.objects.filter(user=request.user).count()
    return {'total_cis': count}