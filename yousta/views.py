from django.db import models
from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView,ListView,UpdateView,DetailView,TemplateView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

from yousta.forms import RegistrationForm,LoginForm,CategoryCreateForm,ClothAddForm,ClothVarientForm,OfferAddForm
from yousta.models import User,Category,Cloths,ClothVarients,Offers

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session!..please login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def is_admin(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            messages.error(request,"Permission denied for current user !")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,is_admin]


class SignUpView(CreateView):

    template_name="yousta/register.html"
    form_class=RegistrationForm
    model=User
    success_url=reverse_lazy("signin")

    def form_valid(self,form):
        messages.success(self.request,"account created")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"failed to create account")
        return super().form_invalid(form)

class SignInView(FormView):
    template_name="yousta/login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
            else:
                messages.error(request,"invalid credential")
                return render(request,self.template_name,{"form":form})

@method_decorator(decs,name="dispatch")
class CategoryCreateView(CreateView,ListView):
    template_name="yousta/category_add.html"
    form_class=CategoryCreateForm
    model=Category
    context_object_name="categories"
    success_url=reverse_lazy("add-category")

    def form_valid(self, form):
        messages.success(self.request,"category added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"category adding failed")
        return super().form_invalid(form)
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)

@signin_required
@is_admin      
def remove_category(request,*args,**kwargs):
    id=kwargs.get("pk")
    Category.objects.filter(id=id).update(is_active=False)
    messages.success(request,"category removed")
    return redirect("add-category") 

@method_decorator(decs,name="dispatch")
class ClothCreateView(CreateView):
    template_name="yousta/cloth_add.html"
    model=Cloths
    form_class=ClothAddForm
    success_url=reverse_lazy("cloth-list")
    
    def form_valid(self, form):
        messages.success(self.request,"cloth added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Failed to add cloth")
        return super().form_invalid(form)

@method_decorator(decs,name="dispatch")    
class ClothListView(ListView):
    template_name="yousta/cloth_list.html"
    model=Cloths
    context_object_name="cloths"

@method_decorator(decs,name="dispatch")  
class ClothUpdateView(UpdateView):
    template_name="yousta/cloth_edit.html"
    form_class=ClothAddForm
    model=Cloths
    success_url=reverse_lazy("cloth-list")
    
    def form_valid(self, form):
        messages.success(self.request,"cloth updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Failed to update cloth")
        return super().form_invalid(form)

@signin_required
@is_admin      
def remove_clothview(request,*args,**kwargs):
    id=kwargs.get("pk")
    Cloths.objects.filter(id=id).delete()
    return redirect("cloth-list")   

@method_decorator(decs,name="dispatch")
class ClothVarientCreateView(CreateView):
    template_name="yousta/clothvarient_add.html"
    form_class=ClothVarientForm
    model=ClothVarients
    success_url=reverse_lazy("cloth-list")
    
    def form_valid(self,form):
        id=self.kwargs.get("pk")
        obj=Cloths.objects.get(id=id)
        messages.success(self.request,"varient added successfully!")
        form.instance.cloth=obj
        return super().form_valid(form)

@method_decorator(decs,name="dispatch")   
class ClothDetailView(DetailView):
    template_name="yousta/cloth_detail.html"
    model=Cloths
    context_object_name="cloth"

@method_decorator(decs,name="dispatch")   
class ClothVarientUpdateView(UpdateView):
    template_name="yousta/varient_edit.html"
    form_class=ClothVarientForm
    model=ClothVarients
    success_url=reverse_lazy("cloth-list")
    
    def form_valid(self, form):
        messages.success(self.request,"varient updated successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Failed to update cloth varient")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cloth_varient_object=ClothVarients.objects.get(id=id)
        cloth_id=cloth_varient_object.cloth.id
        return reverse("cloth-detail",kwargs={"pk":cloth_id})
    

@signin_required
@is_admin  
def remove_varientview(request,*args,**kwargs):
    id=kwargs.get("pk")
    cloth_varient_object=ClothVarients.objects.get(id=id)
    cloth_id=cloth_varient_object.cloth.id
    cloth_varient_object.delete()
    return redirect("cloth-detail",pk=cloth_id)    
    
@method_decorator(decs,name="dispatch")
class OfferCreateView(CreateView):
    template_name="yousta/offer_add.html"
    form_class=OfferAddForm
    model=Offers
    success_url=reverse_lazy("cloth-list")

    def form_valid(self, form):
        id=self.kwargs.get("pk")
        obj=ClothVarients.objects.get(id=id)
        form.instance.clothvarient=obj
        messages.success(self.request,"offer added successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"Failed to add offer")
        return super().form_invalid(form)
    
    def get_success_url(self):
        id=self.kwargs.get("pk")
        cloth_varient_object=ClothVarients.objects.get(id=id)
        cloth_id=cloth_varient_object.cloth.id
        
        return reverse("cloth-detail",kwargs={"pk":cloth_id})
        

@signin_required
@is_admin         
def remove_offerview(request,*args,**kwargs):
    id=kwargs.get("pk")
    offer_object=Offers.objects.get(id=id)
    cloth_id=offer_object.clothvarient.cloth.id
    offer_object.delete()
    return redirect("cloth-detail",pk=cloth_id)   

def signoutview(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


class IndexView(TemplateView):
    template_name="yousta/index.html"
