from django.shortcuts import render
from .models import ProductType,Product,Purchase,Vendor,Sell,Department
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .seriallizers import ProductTypeSerializer, ProductSerializer, PurchaseSerializer, DepartmentSerializer, VendorSerializer, SellSerializer,UserSerializer,GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group,User
from rest_framework.permissions import AllowAny,DjangoModelPermissions,IsAuthenticated
from django.contrib.auth.models import Group
# Create your views here.
class productTypeView(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    


class ProductView(GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['type']
    search_fields = ['name','description']
    
    def list(self,request):
        permission_classes = DjangoModelPermissions
        product_objs = self.get_queryset()
        filtered_queryset = self.filter_queryset(product_objs)    #filter need exact value
        paginate_queryset = self.paginate_queryset(filtered_queryset)
        serializer = self.get_serializer(paginate_queryset,many=True)
        response = self.get_paginated_response(serializer.data)
        return response
    
    def create(self,request):
        permission_classes = [IsAuthenticated,DjangoModelPermissions]
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:                                            #if request is sent from user you must send response
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)  
    
    def retrieve(self,request,pk):

        product_obj = self.get_object()   #id call automatically by lookup field
        serializer = self.get_serializer(product_obj)  
        return Response(serializer.data) 
    
    def update(self,request,pk):
        product_obj = self.get_object()
        serializer = self.get_serializer(product_obj,data=request.data)  #existing dat replace by request.data
        if serializer.is_valid():
            serializer.save()
            return Response("user created")
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk):
        product_obj = self.get_object()
        product_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseView(GenericViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
   
    
    def list(self,request):
        purchase_obj = self.get_queryset()
        serializer = self.get_serializer(purchase_obj,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class VendorView(GenericViewSet):    
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def list(self,reqeust):
        vendor_obj = self.get_queryset()
        serializer = self.get_serializer(vendor_obj,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class SellView(GenericViewSet):
    queryset = Sell.objects.all()
    serializer_class = SellSerializer
    
    def list(self,request):
        purchase_obj = self.get_queryset()
        serializer = self.get_serializer(purchase_obj,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class DepartmentView(GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    def list(self,request):
        purchase_obj = self.get_queryset()
        serializer = self.get_serializer(purchase_obj,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
        
    
@api_view(['GET'])
@permission_classes([AllowAny])
def group_listing(request):
    permission_classes = DjangoModelPermissions
    objs = Group.objects.all()
    serializer = GroupSerializer(objs,many =True)
    return Response(serializer.data)
    


class register_view(GenericViewSet):       
    queryset = User.objects.all()   
    serializer = UserSerializer()
    permission_classes = [] 
    
    def create(self,request):    
        password = request.data.get('password')
        hash_password = make_password(password)
        data = request.data.copy()
        data['password'] = hash_password
        serializer = UserSerializer(data = data)
        if serializer.is_valid():        
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class login_view(GenericViewSet):       
    queryset = User.objects.all() 
    permission_classes = []  
       
    def create(self,request):    
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username = username, password=password)
        
        if user == None:
            return Response({'detail'"Invalid Creditinaila"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key},status=status.HTTP_200_OK)



class group_view(GenericViewSet):
    queryset = Group.objects.all()
    permission_classes = []  
    
    def list(self,request):
        group_objs = Group.objects.all()
        serializer = GroupSerializer(group_objs,many=True)
        return Response(serializer.data)
            
        

