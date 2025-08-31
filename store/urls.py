from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #path("category/<int:category_id>/", views.category, name="category_products"),
    path('category/<int:id>/', views.category_products, name='category'),
    path("category-product/<int:id>/", views.category_products, name="category_products"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path('login/', views.login, name="login"),
    path('register/',views.register, name="register"),
    path('cart/', views.cart, name="cart"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit', views.profile_edit, name="profile_edit"),
    path('logout/', views.logout, name="logout"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("about", views.about, name="about"),
    path("subcategory/<int:category_id>/", views.subcategory, name="subcategory"),
]
