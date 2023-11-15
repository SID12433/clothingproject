from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from yousta.views import SignUpView,SignInView,CategoryCreateView,remove_category\
,ClothCreateView,ClothListView,ClothUpdateView,remove_clothview,ClothDetailView\
    ,ClothVarientCreateView,ClothVarientUpdateView,remove_varientview,OfferCreateView,remove_offerview,signoutview,IndexView



urlpatterns=[


    path("register/",SignUpView.as_view(),name="signup"),
    path("",SignInView.as_view(),name="signin"),
    path("logout/",signoutview,name="signout"),
    path("categories/add",CategoryCreateView.as_view(),name="add-category"),
    path("categories/<int:pk>/remove",remove_category,name="remove-category"),
    path("cloth/add",ClothCreateView.as_view(),name="cloth-add"),
    path("cloth/list",ClothListView.as_view(),name="cloth-list"),
    path("cloth/<int:pk>/edit",ClothUpdateView.as_view(),name="cloth-edit"),
    path("cloth/<int:pk>/remove",remove_clothview,name="cloth-remove"),
    path("cloth/<int:pk>/detail",ClothDetailView.as_view(),name="cloth-detail"),
    path("cloth/<int:pk>/varients/add",ClothVarientCreateView.as_view(),name="add-varient"),
    path("varients/<int:pk>/edit",ClothVarientUpdateView.as_view(),name="edit-varient"),
    path("varients/<int:pk>/remove",remove_varientview,name="remove-varient"),
    path("varients/<int:pk>/offer/add",OfferCreateView.as_view(),name="offer-add"),
    path("varients/<int:pk>/offer/remove",remove_offerview,name="offer-remove"),
    path("index/",IndexView.as_view(),name="index")
   


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)