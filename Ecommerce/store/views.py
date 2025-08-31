from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import ProductCategory, Product, Cart, CartItem, Order, OrderItem
from .forms import ProfileUpdateForm
from .forms import RegisterForm

# ----------------- CART VIEWS -----------------
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})


@login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("cart")


# ----------------- AUTH VIEWS -----------------
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # auto login after register
            messages.success(request, f"Account created for {user.username}")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below ❌")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


# ----------------- PRODUCT VIEWS -----------------
def home(request):
    from django.db.models import Q
    import random

    categories = ProductCategory.objects.all()
    products = list(Product.objects.all())
    random.shuffle(products)
    
    clothes_category = ProductCategory.objects.filter(name="clothes").first()
    men_category = None
    women_category = None

    if clothes_category:
        men_category = ProductCategory.objects.filter(parents=clothes_category, name="men").first()
        women_category = ProductCategory.objects.filter(parents=clothes_category, name="women").first()

    return render(request, "home.html", {
        "categories": categories,
        "products": products[:9],
        "clothes_category": clothes_category,
        "men_category": men_category,
        "women_category": women_category,
    })

def category(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    products = category.products.all()
    return render(request, "category.html", {"category": category, "products": products})

def category_products(request, id):
    category = ProductCategory.objects.get(id=id)
    subcategories = category.get_all_subcategories()
    categories = [category] + subcategories
    products = Product.objects.filter(category__in=categories)
    return render(request, "category.html", {"category": category, "products": products})

def subcategory(request, category_id):
    subcategory = get_object_or_404(ProductCategory, id=category_id)
    products = Product.objects.filter(category=subcategory)
    return render(request, "category.html", {
        "category": subcategory,
        "products": products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})


# ----------------- PROFILE VIEWS -----------------
@login_required
def profile(request):
  orders = Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request, "profile.html")


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle password change
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")

            if password1 or password2:
                if password1 and password1 == password2:
                    user.set_password(password1)
                    messages.success(request, "Password changed successfully ✅")
                else:
                    messages.error(request, "Passwords do not match ❌")
                    return redirect("profile_edit")

            user.save()
            # Keep user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(request, "Your profile has been updated successfully ✅")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "profile_edit.html", {"form": form})


# ----------------- ORDER VIEWS -----------------
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if cart.items.exists():
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price()
        )
        # Move cart items into order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear cart
        cart.items.all().delete()

        messages.success(request, "✅ Your order has been placed successfully!")
        return redirect("order_history")

    messages.warning(request, "⚠️ Your cart is empty.")
    return redirect("cart")


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order_history.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})
    
    
def about(request):
  return render(request, "about.html")