import os

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .serializers import *
import json
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
users = []
invoices_temp = []
absolute_path = os.path.dirname(os.path.abspath(__file__))
filename = absolute_path + '/data.json'



# class UserSignUp(View):
#     def post(self, request):
#         user_data = json.loads(request.body)
#         user_data[0]["user_id"] = len(users) + 1
#         user_serialized = UserSerializer(data=user_data[0])
#         if user_serialized.is_valid():
#             users.append(user_serialized.data)
#             return JsonResponse(user_serialized.data, status=201)
#         else:
#             return HttpResponseBadRequest()
class UserSignUp(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserSignIn(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class GetAllInvoices(View):
#     def get(self, request):
#         item=open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json').read()
#         jsonData=json.loads(item)
#         return JsonResponse(jsonData, safe=False)

class GetAllInvoices(APIView):
    #permission_classes=[IsAuthenticated]
    def get(self, request):
        invoices=Invoice.objects.all().values()
        return JsonResponse(list(invoices), safe=False)

# class GetInvoiceByID(View):
#     def get(self, request,id):
#         item=open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json').read()
#         jsonData=json.loads(item)
#         for index,item in jsonData.items():
#             for value in item:
#                 if value['invoice_no']==id:
#                     return JsonResponse(value, safe=False)
                
class GetInvoiceByID(APIView):
    def get(self,request,invoice_no):
        #permission_classes=[IsAuthenticated]
        invoice=Invoice.objects.filter(invoice_no=invoice_no).first()
        items=invoice.item.all()
        items_list=[]
        for each in items:
            item_data={
                "item_id": each.item_id,
                "desc":each.desc,                
            }
            items_list.append(item_data)
        response={
            "client_name":invoice.client_name,
            "date":invoice.date,
            "total_amount":invoice.total_amount,
            "item":items_list
        }
        return JsonResponse(response,safe=False)



# class NewInvoice(View):
#     def post(self, request):
#         invoice_data = json.loads(request.body)
#         item=open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json').read()
#         jsonData=json.loads(item)
#         invoice_data["invoice_no"] = len(jsonData['data']) + 1
#         invoice_data["total_amount"] = 0
#         invoice_serialized = InvoiceSerializer(data=invoice_data)
#         if invoice_serialized.is_valid():
#             entry = invoice_serialized.data
#             with open(filename, "r+") as file:
#                 file_data = json.load(file)
#                 file_data['data'].append(entry)
#                 file.seek(0)
#                 json.dump(file_data, file, indent=6)
#             return JsonResponse(invoice_serialized.data, status=201)
#         else:
#             return HttpResponseBadRequest()
class NewInvoice(APIView):
    def post(self,request):
        #permission_classes=[IsAuthenticated]
        invoice=json.loads(request.body)
        try:
            Invoice.objects.create(**invoice)
            return JsonResponse("Invoice is added successfully",safe=False,status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

class AddItem(APIView):
    def post(self, request,invoice_no):
        #permission_classes=[IsAuthenticated]
        item_input=json.loads(request.body)
        try:
            items=Item.objects.create(**item_input)
            invoice=Invoice.objects.get(invoice_no=invoice_no)
            # itemId=Item.item_id
            # items=Item.objects.get(item_id=itemId)
            invoice.item.add(items)
            return JsonResponse("Added",safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))

        
# class AddItem(View):
#     def post(self,request,id):
#         item_array = []
#         item_data = json.loads(request.body)
#         # if item_data_serialized.is_valid():
#         with open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json', "r+") as file:
#             jsonData=json.load(file)
#         for index,item in jsonData.items():
#             for idx, value in enumerate(item):
#                 if value['invoice_no']==id:
#                     if('item'in value):
#                         value['item'].append(item_data)
#                         #item_array.append(value['item'])
#                         #item_array.append(item_data)
#                         #value['item']=item_array
#                         jsonData['data'][idx].update(value)
#                         with open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json','w') as jsonfile:
#                             json.dump(jsonData,jsonfile)
#                             jsonfile.close()
#                         return JsonResponse(value,status=200)
                        
#                     else:
#                         item_array.append(item_data)
#                         value['item']=item_array
#                         jsonData['data'][idx].update(value)
#                         with open('C:\\Users\\desai\\OneDrive\\Desktop\\invoice-back\\invoice_back_project\\invoice_app\\data.json','w') as jsonfile:
#                             json.dump(jsonData,jsonfile)
#                             jsonfile.close()
#                         return JsonResponse(value,status=200)                        
#         return HttpResponseBadRequest()


