import json
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserData, CartModel, ProductModel, WishlistModel, UserProductModel, SideImage, ItemVariant, PurchaseHistory
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Home View
def home(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if "login" in request.POST:
                username = request.POST["username"]
                password = request.POST["password"]
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    print('logging in...')
                    items = ProductModel.objects.all()
                    for item in items:
                        user_id = user.id
                        item_id = item.id
                        try:
                            obj = UserProductModel.objects.get(user_id=user_id, item_id=item_id)
                        except UserProductModel.DoesNotExist:
                            obj = UserProductModel.objects.create(user_id=user_id, item_id=item_id)
                            obj.save()
                    user_product = UserProductModel.objects.all()
                    messages.success(request, "Login successful!")
                    print("Items of this User are created")
                    user_id = user.id
                    return render(request, "main/home.html",
                                  {'client': True, 'user_product': user_product, 'user_id': user_id})

                else:
                    messages.error(request, "Invalid username or password.")
                    return render(request, 'main/home.html', {'log_in': True})



            elif "signup" in request.POST:
                username = request.POST["new_username"]
                email = request.POST["email"]
                password = request.POST["new_password"]
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already taken.")
                    return render(request, 'main/home.html', {'sign_in': True})
                else:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    messages.success(request, "Account created! You can log in now.")
                    return render(request, 'main/home.html', {'log_in': True})

        products = ProductModel.objects.all()
        sports_products = [p for p in products if p.item_brand == 'campus-sports'][:5]
        walking_products = [p for p in products if p.item_brand == 'campus-walking'][:5]
        sneakers_products = [p for p in products if p.item_brand == 'campus-sneakers'][:5]
        return render(request, 'main/home.html', {'client': False, 'products': products, "sports_products":sports_products
                       , 'walking_products':walking_products, 'sneakers_products':sneakers_products})
    else:
        products = ProductModel.objects.all()
        user_products = UserProductModel.objects.all()
        can_edit = request.user.has_perm('main.change_productmodel')
        user_id = request.user.id
        sports_products = [p for p in products if p.item_brand == 'campus-sports'][:5]
        walking_products = [p for p in products if p.item_brand == 'campus-walking'][:5]
        sneakers_products = [p for p in products if p.item_brand == 'campus-sneakers'][:5]
        for product in products:
            if product.discount:
                product.final_price = product.item_price - ((product.item_price * product.discount) / 100)
        return render(request, 'main/home.html', {'client': True, 'user_products': user_products,
                       'user_id': user_id, 'can_edit': can_edit, 'products': products, "sports_products":sports_products
                       , 'walking_products':walking_products, 'sneakers_products':sneakers_products})

# Log_out View
def log_out(request):
    logout(request)
    print("I am logging out..")
    return redirect('/')

# Show and Edit profile View
def profile_data(request):
    user = request.user
    try:
        profile = UserData.objects.get(username=user.username)
        if request.method == 'POST':
            profile.username = request.POST['username']
            profile.first_name = request.POST['first_name']
            profile.last_name = request.POST['last_name']
            profile.email = request.POST['email']
            profile.phone_number = request.POST['phone_number']
            profile.address = request.POST['address']
            profile.pin_code = request.POST['pin_code']
            if profile.phone_number == '':
                profile.phone_number = None
            if profile.pin_code == '':
                profile.pin_code = None
            profile.save()
            user.username = profile.username
            user.email = profile.email
            user.save()
            return redirect('/')
        return render(request, 'main/edit_profile.html', {'profile': profile})
    except UserData.DoesNotExist:
        if request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            pin_code = request.POST['pin_code']
            if phone_number == '':
                phone_number = None
            if pin_code == '':
                pin_code = None
            profile = UserData.objects.create(username=username, first_name=first_name, last_name=last_name,
                                              email=email,
                                              phone_number=phone_number, address=address, pin_code=pin_code)
            profile.save()
            user.username = profile.username
            user.email = profile.email
            user.save()
            return redirect('/')
        return render(request, 'main/edit_profile.html')

# Show men's shoes
def men_shoes(request):
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = ProductModel.objects.all().order_by('item_price')
    elif sort == 'price_desc':
        products = ProductModel.objects.all().order_by('-item_price')
    elif sort == 'discount_desc':
        products = ProductModel.objects.all().order_by('-discount')
    elif sort == 'is_bestSeller':
        products = ProductModel.objects.filter(is_bestSeller= True)
    elif sort == 'is_newArrival':
        products = ProductModel.objects.filter(is_newArrival=True)
    else:
        products = ProductModel.objects.all()
    itemCount = -5
    for product in products:
        itemCount += 1
        if product.discount:
            product.final_price = product.item_price - ((product.item_price * product.discount) / 100)

    images = SideImage.objects.all()
    second_images = {}
    for product in products:
        matching = [img.item_image.url for img in images if img.item_id == product.id]
        if len(matching) >= 2:
            second_images[product.id] = matching[1]
    return render(request, 'main/men.html',{'products':products, 'second_images':second_images, 'available_sizes': [6, 7, 8, 9, 10], 'itemCount': itemCount})


def check_pincode(request, pin):
    url = f"https://api.postalpincode.in/pincode/{pin}"
    response = requests.get(url)
    data = response.json()

    if data[0]['Status'] == 'Success' and data[0]['PostOffice']:
        post_office = data[0]['PostOffice'][0]
        area = post_office['Name']
        district = post_office['District']
        state = post_office['State']
        message1 = "Pincode is valid."
        message2 = f"Area: {area}, District: {district}, State: {state}"
        return JsonResponse({'status': 'success', 'message1': message1, 'message2': message2})
    else:
        return JsonResponse({'status': 'fail','message1': 'Invalid pincode','message2': ''})

# Show women's shoes
def women_shoes(request):
    return render(request, 'main/women.html')

#Add Cart Data
def toggle_cartlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if "cart" in request.POST:
                item_quantity = request.POST["item_quantity"]
                user_id = request.POST['user_id']
                item_id = request.POST['item_id']
                item_size = request.POST['item_size']
                print(item_quantity, user_id, item_id, item_size)
                print('hello django')

                try:
                    obj = CartModel.objects.get(user_id=user_id, item_id=item_id, item_size=item_size)
                    obj.delete()
                    total_count = CartModel.objects.filter(user=request.user).count()
                    return JsonResponse(
                        {'status': 'removed', 'message': 'Item removed from cart!', 'type':'warning', 'total_count': total_count})

                except CartModel.DoesNotExist:
                    item = CartModel.objects.create(item_quantity=item_quantity, user_id=user_id, item_id=item_id, item_size=item_size)
                    item.save()
                    total_count = CartModel.objects.filter(user=request.user).count()
                    return JsonResponse({'status': 'success', 'message': 'Added to Cart','type':'success', 'total_count': total_count})
    else:
        return JsonResponse({'status': 'danger', 'message': 'First Login to Save'})

# Show Cart Data
def show_cart_data(request):
    if not request.user.is_authenticated:
        messages.error(request, 'First Login to access Cart Items!')
        return redirect('/')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            new_quantity = int(data.get('quantity'))

            # Get product for the current user only
            product = CartModel.objects.get(id=product_id, user=request.user)

            # Update quantity
            product.item_quantity = new_quantity
            product.save()

            # Calculate new total for this product and entire cart
            cart_items = CartModel.objects.filter(user=request.user)
            for item in cart_items:
                if item.item.discount:
                    item.final_price = item.item.item_price - ((item.item.item_price * item.item.discount) / 100)
                else:
                    item.final_price = item.item.item_price
                item.total_price = item.final_price * item.item_quantity
                print(item.total_price)
            cart_total = sum(item.total_price for item in cart_items)
            if product.item.discount:
                final_price = product.item.item_price - ((product.item.item_price * product.item.discount) / 100)
            else:
                final_price = product.item.item_price

            item_total = final_price * product.item_quantity

            print(cart_total)

            return JsonResponse({
                'success': True,
                'item_total': item_total,
                'cart_total': cart_total
            })

        except CartModel.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        cart_items = CartModel.objects.filter(user=request.user)
        user_id = request.user.id
        for item in cart_items:
            if item.item.discount:
                item.final_price = item.item.item_price - ((item.item.item_price * item.item.discount) / 100)
            else:
                item.final_price = item.item.item_price
            item.total_price = item.final_price * item.item_quantity
        cart_total = sum(item.total_price for item in cart_items)
        print(cart_total)
        if cart_total < 1:
            return render(request, 'main/show_cart_data.html',
                          {'cart_items': cart_items, 'cart_total': cart_total, 'user_id': user_id, 'client': True, })
        item_ids = [str(item.item.id) for item in cart_items]
        data = {
            "amount": int(cart_total * 100),
            "currency": "USD",
            "payment_capture": 1,
        }
        payment = client.order.create(data=data)
        return render(request, 'main/show_cart_data.html',
                      {'cart_items': cart_items, 'cart_total': cart_total, 'user_id': user_id, 'client': True, "payment": payment,
                       "razorpay_key": settings.RAZORPAY_KEY_ID, "item_ids": item_ids,})

# Delete Cart Data
def delete_cart_data(request, id):
    if request.method == 'POST':  # Make sure it handles only POST requests
        try:
            item = CartModel.objects.get(id=id)  # Find the cart item by ID
            item.delete()  # Delete the cart item from the database
            total_count = CartModel.objects.filter(user=request.user).count()
            cart_items = CartModel.objects.filter(user=request.user)
            cart_total = sum(item.item.item_price * item.item_quantity for item in cart_items)
            return JsonResponse({'status': 'success', 'message': 'Item removed from Cart!', 'total_count': total_count, 'cart_total': cart_total})  # Respond with success
        except CartModel.DoesNotExist:  # If the item doesn't exist, handle the error
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)  # Respond with error
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)  # Handle other request methods


# Add WishList Data
def toggle_wishlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if "wish" in request.POST:
                user_id = request.POST['user_id']
                item_id = request.POST['item_id']
                print(user_id, item_id)
                print('hello django')

                try:
                    obj = WishlistModel.objects.get(user_id=user_id, item_id=item_id)
                    obj.delete()
                    total_count = WishlistModel.objects.filter(user=request.user).count()
                    return JsonResponse(
                        {'status': 'removed', 'message': 'Item removed from wish', 'type': 'warning',
                         'total_count': total_count})


                except WishlistModel.DoesNotExist:
                    item = WishlistModel.objects.create(user_id=user_id, item_id=item_id)
                    item.save()
                    total_count = WishlistModel.objects.filter(user=request.user).count()
                    return JsonResponse({'status': 'success', 'message': 'Added to wishlist', 'total_count': total_count})

# Show Wish List Data
def show_wish_data(request):
    if not request.user.is_authenticated:
        messages.error(request, 'First Login to access Wishlist!')
        return redirect('/')
    else:
        wish_items = WishlistModel.objects.filter(user=request.user)
        for item in wish_items:
            if item.item.discount:
                item.final_price = item.item.item_price - ((item.item.item_price * item.item.discount) / 100)
            else:
                item.final_price = item.item.item_price
        user_id = request.user.id
        return render(request, 'main/show_wish_data.html',
                      {'wish_items': wish_items, 'user_id': user_id, 'client': True})

# Delete Wishlist Data
def delete_wish_data(request, id):
    try:
        item = WishlistModel.objects.get(id=id)
        item.delete()
        total_count = WishlistModel.objects.filter(user=request.user).count()
        return JsonResponse({'status': 'success', 'message': 'Item deleted successfully', 'total_count': total_count})
    except WishlistModel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'})





# Add Item in product list as a admin
def add_item(request):
    if request.method == 'POST':
        item_brand = request.POST['item_brand']
        item_image = request.FILES['item_image']
        item_name = request.POST['item_name']
        item_total = request.POST['item_total']
        item_price = request.POST['item_price']
        items = ProductModel.objects.all()
        for item in items:
            if item.item_name == item_name:
                messages.error(request, 'Item name is already available')
                return redirect('/add_item')

        item = ProductModel.objects.create(item_brand=item_brand, item_image=item_image, item_name=item_name,
                                           item_total=item_total, item_price=item_price)
        item.save()
        messages.success(request, 'Item is created')
        return redirect('/add_item')

    return render(request, 'main/add_item.html')

# Add images for item
def add_images(request, id):
    product = ProductModel.objects.get(id=id)
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item_name = request.POST['item_name']
        item_image = request.FILES['item_image']
        try:
            item = SideImage.objects.get(item_name=item_name)
            messages.info(request, 'this image is already added')
            return redirect(f'/add_images/{id}')
        except SideImage.DoesNotExist:
            item = SideImage.objects.create(item_image=item_image, item_name=item_name, item_id=item_id)
            messages.success(request, 'Item_image saved successfully!')
            return redirect(f'/add_images/{id}')
    return render(request, 'main/add_images.html', {'product': product})

# Add Variant for item
def add_variants(request, id):
    product = ProductModel.objects.get(id=id)
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item_name = request.POST['item_name']
        item_image = request.FILES['item_image']
        try:
            item = ItemVariant.objects.get(item_name=item_name)
            messages.info(request, 'this variant is already added')
            return redirect(f'/add_variants/{id}')
        except ItemVariant.DoesNotExist:
            item = ItemVariant.objects.create(item_image=item_image, item_name=item_name, item_id=item_id)
            messages.success(request, 'variant saved successfully!')
            return redirect(f'/add_variants/{id}')
    return render(request, 'main/add_variants.html', {'product': product})


# Delete an Item in product list as a admin
def delete_item(request, id):
    item = ProductModel.objects.get(id=id)
    item.delete()
    return redirect('/')

# Edit an Item in product list as a admin
def edit_item(request, id):
    product = ProductModel.objects.get(id=id)
    if request.method == 'POST':
        # product.item_image = request.FILES['item_image']
        product.item_name = request.POST['item_name']
        product.item_total = request.POST['item_total']
        product.item_price = request.POST['item_price']
        product.is_bestSeller = 'is_bestSeller' in request.POST
        product.is_newArrival = 'is_newArrival' in request.POST
        product.is_size6 = 'is_size6' in request.POST
        product.is_size7 = 'is_size7' in request.POST
        product.is_size8 = 'is_size8' in request.POST
        product.is_size9 = 'is_size9' in request.POST
        product.is_size10 = 'is_size10' in request.POST
        product.save()
        messages.success(request, 'Item updated successfully!!')
        return redirect('/')
    return render(request, 'main/edit_item.html', {'product': product})

# Show full details of an item
def show_detail(request, id):
    product = ProductModel.objects.get(id=id)
    if product.discount:
        product.final_price = product.item_price - ((product.item_price * product.discount) / 100)

    images = SideImage.objects.all()
    variants = ItemVariant.objects.all()
    user_id = request.user.id
    print(product.id)
    print(user_id)
    item_ids = [str(product.id)]
    data = {
        "amount": int(product.final_price * 100),
        "currency": "USD",
        "payment_capture": 1,
    }
    payment = client.order.create(data=data)
    return render(request, 'main/item_detail.html',
                  {'user_id': user_id, 'client': True, 'product': product, 'images': images, 'variants': variants, 'available_sizes': [6, 7, 8, 9, 10],
                   "payment": payment, "razorpay_key": settings.RAZORPAY_KEY_ID, "item_ids": item_ids,})


@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        data = request.POST
        amount = data.get('amount')
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        item_ids_json = data.get('item_ids')
        item_ids = json.loads(item_ids_json) if item_ids_json else []

        try:
            # 🔐 Verify the payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # 📦 Fetch payment details to get email
            payment_info = client.payment.fetch(payment_id)
            payer_email = payment_info.get('email')
            amount = int(payment_info.get('amount')) / 100


            if not payer_email:
                return render(request, 'main/payment_failed.html', {"error": "Email not found in payment details."})

            # 🧾 Render invoice template to PDF
            html = render_to_string("main/invoice.html", {
                "payment_id": payment_id,
                "order_id" : order_id,
                "email": payer_email,
                "amount": amount,
                "date": datetime.now().date(),
            })
            result = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=result)

            if pisa_status.err:
                return render(request, "main/payment_failed.html", {"error": "PDF generation failed."})

            # 📧 Send invoice via email
            mail = EmailMessage(
                subject="Invoice for your Payment",
                body="Thank you for your purchase! Please find the invoice attached.",
                from_email=settings.EMAIL_HOST_USER,
                to=[payer_email],
            )
            mail.attach("invoice.pdf", result.getvalue(), "application/pdf")
            mail.send()
            CartModel.objects.filter(user=request.user, item__id__in=item_ids).delete()
            PurchaseHistory.objects.create(user=request.user,order_id = order_id, payment_id=payment_id, amount=amount, purchase_date=datetime.now().date(), email=payer_email)
            messages.success(request, 'Thank you for Shopping...')
            return render(request, 'main/payment_success.html', {"email": payer_email})

        except razorpay.errors.SignatureVerificationError:
            return render(request, 'main/payment_failed.html', {"error": "Payment verification failed."})

    return render(request, 'main/payment_failed.html', {"error": "Invalid request method."})

def send_Email(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST['message']
            Title = request.POST['name']
            Email_to = request.POST['email']
            send_mail(
                Title, message, 'settings.EMAIL_HOST_USER', [Email_to], fail_silently= False
            )
        username = request.user;
        return render(request, 'main/email.html',{'username':username})
    else:
        messages.error(request, 'First Login to sent Email.')
        return redirect('/#sale')

def order_history(request):
    orders = PurchaseHistory.objects.filter(user=request.user)
    return render(request, 'main/orders.html',{'orders':orders})

# Index View
def index(request):
    return render(request, 'main/index.html')

def testing(request):
    images = SideImage.objects.all()
    product = ProductModel.objects.get(id = 6)
    return render(request, 'main/payment_success.html', {'images': images, 'product':product})