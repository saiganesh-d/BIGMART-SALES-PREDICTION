from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
import joblib

import numpy as np

def sales(request):
    voting=joblib.load('voting.sav')
   
    if request.method == "GET":
        return render(request,"sales.html")
    Item_Identifier=request.POST['Item_Identifier']
    Item_Weight=float(request.POST['Item_Weight'])
    Item_Fat_Content=int(request.POST['Item_Fat_Content'])
    Item_Visibility=float(request.POST['Item_Visibility'])
    Item_Type=int(request.POST['Item_Type'])
    Item_MRP=float(request.POST['Item_MRP'])
    new_out=int(request.POST['Outlet_Identifier'])
    Outlet_Establishment_Year=int(request.POST['Outlet_Establishment_Year'])
    Outlet_Size=int(request.POST['Outlet_Size'])
    Outlet_Location_Type=int(request.POST['Outlet_Location_Type'])
    Outlet_Type=int(request.POST['Outlet_Type'])
   
    
    iden=Item_Identifier[:2]
    if(iden=='DR'):
        Item_Cateogory = 0
    if(iden=='FD'):
        Item_Cateogory = 1
    if(iden=='NC'):
        Item_Cateogory = 2
    new_Item = int(Item_Identifier[-2:])
    if Item_MRP<=67.5:
        MRP_bins=0
    elif (Item_MRP>67.5) & (Item_MRP<=134.5):
        MRP_bins=1
    elif (Item_MRP>134.5) & (Item_MRP<=201.1):
        MRP_bins=2
    else:
        MRP_bins=3
    total=2021-Outlet_Establishment_Year
    
    list=[Item_Weight,Item_Fat_Content,Item_Visibility,Item_Type, Item_MRP,Outlet_Size,
                        Outlet_Location_Type,Outlet_Type	,Item_Cateogory,new_Item,
                        MRP_bins,new_out,total	]
    print(list)
    
    b = np.array(list, dtype=float) #  convert using numpy
    c = [float(i) for i in list] #  convert with for loop
    prediction=voting.predict([c])
    prediction = abs(prediction)
    return  render(request,"sales.html",{'prediction':prediction})

def home(request):
    return render(request,"portfolio.html")