from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
router.register("cloths",views.ClothsView,basename="cloths")
router.register("carts",views.CartsView,basename="cartlist")
router.register("orders",views.OrderView,basename="orderlist")


urlpatterns = [
    path("register/",views.UserCreationView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    
]+router.urls
