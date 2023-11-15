from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet,ModelViewSet
from api.serializer import UserSerializer,ClothSerializer,CartSerializer,OrderSerializer,ReviewSerializer
from rest_framework.response import Response
from yousta.models import Cloths,ClothVarients,Carts,User,Orders
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions

class UserCreationView(APIView):  
    
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class ClothsView(ModelViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ClothSerializer
    model=Cloths
    queryset=Cloths.objects.all()
    
    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args,**Kwargs):
        vid=Kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    @action(methods=["post"],detail=True)
    def place_order(self,request,*args, **kwargs):
        oid=kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=oid)
        user=request.user
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args, **kwargs):
        c_id=kwargs.get("pk")
        user=request.user
        cloth_object=Cloths.objects.get(id=c_id)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cloth=cloth_object,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    

class CartsView(ViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CartSerializer
    
    def list(self,request,*args,**kwargs):
        qs=Carts.objects.filter(user=request.user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        instance=Carts.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"message":"cart removed successfully"})
        else:
            return Response(data={"message":"permission denied for current user"})
    
class OrderView(ViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer
    
    def list(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        instance=Orders.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"message":"order removed successfully"})
        else:
            return Response(data={"message":"permission denied for current user"})
            


 