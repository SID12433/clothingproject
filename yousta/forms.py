from django import forms


from yousta.models import User,Category,Cloths,ClothVarients,Offers
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2","phone","address"]


class LoginForm(forms.Form):

    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class CategoryCreateForm(forms.ModelForm):

    class Meta:
        model=Category
        fields=["name"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
        }

class ClothAddForm(forms.ModelForm):
    class Meta:
        model=Cloths
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "brand":forms.TextInput(attrs={"class":"form-control"})
        }
        
class ClothVarientForm(forms.ModelForm):
    class Meta:
        model=ClothVarients
        exclude=("cloth",) #in case if only one object to not include
        
class OfferAddForm(forms.ModelForm):
    class Meta:
        model=Offers
        exclude=("clothvarient",)
          
        widgets={
            "start_date":forms.DateInput(attrs={"type":"date"}),
            "due_date":forms.DateInput(attrs={"type":"date"})
        }