from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from main_app.forms import *
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Sum
from django.views.generic import (View)
from django.core.files.storage import FileSystemStorage 
import os
from django.conf import settings

def vet_dashboard(request):
    today = datetime.today()

    total_sales = CustomerItemsales.objects.all().count()
    total_purcahses = PurchaseBill.objects.all().count()

    total_stock = New_stock.objects.all().count()
 
    total_sales_total2=Stock_puchases.objects.filter().values('time2').order_by('time2').annotate(sum=Sum('totalprice'))
    total_sales_total=CustomerOrderItem.objects.filter().values('time2').order_by('time2').annotate(sum=Sum('totalprice'))
    # exipred=New_stock.objects.annotate(
    # expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    # ).filter(expired=True).count()
    total_par_cost=Stock_puchases.objects.filter().values('time2').order_by('time2').annotate(sum=Sum('totalprice'))

    exipred=New_stock.objects.filter(is_deleted=False).annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True).count()

    context={
        'total_sales':total_sales,
        'total_stock':total_stock,
        'moy':total_sales_total,
        'total_pur':total_purcahses,
        "expired_total":exipred,
        'pur':total_par_cost

            # "expired_total":exipred,
    }
    
    return render( request ,'veterinarian/dashboard.html',context)



# Supplier
def create_supplier(request):
    form=SupplierForm()
    if request.method == 'POST':
        form=SupplierForm(request.POST ,request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Supplier added Successfully!")
                return redirect('manage-supplier')
        except:
                messages.error(request, "Supplier nod Created an error occured!!")
                return redirect('manage-supplier')
    context={
        "form":form,
        "title":"Add Supplier"
    }

    return render(request,'veterinarian/supplier/add_supplier.html',context)

def manage_suppier(request):
    supplier = Supplier.objects.all()
    context = {
        "staffs": supplier,
        "title":"Manage Supplier",
        'role':'Supplier'
    }

    return render(request,'veterinarian/supplier/manage_supplier.html',context)


#  stock
def add_stockCategory(request):
    form=CategoryForm()

   
    if request.method == 'POST':
        form=CategoryForm(request.POST ,request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")
                return redirect('add-stock-category')
        except:
            messages.error(request, "Category not created an error occured!")
            return redirect('add-stock-category')

   

    
    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    category = Stock_category.objects.filter(is_deleted=False)
    context={
        'category':category,
        'form':form
    }
    return render(request,'veterinarian/stock/add_stockCategory.html',context)

def edit_category(request,pk):
    category2 = Stock_category.objects.get(id=pk)

    form = CategoryForm()
    form.fields['name'].initial = category2.name
    if request.method =='POST':
        form=CategoryForm(request.POST ,request.FILES,instance=category2)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Category updated Successfully!")
                return redirect('add-stock-category')
        except:
            messages.error(request, "Category not updated !")
            return redirect('add-stock-category')
    context={
        'form':form
    }
    return render(request,'veterinarian/stock/edit_stockCategory.html',context)


def delete_category(request,pk):
    category2 = Stock_category.objects.get(id=pk)
    try:
        category2.delete()
        messages.success(request,'category deleted successsfully')
        return redirect('add-stock-category')
    except:
        messages.error(request,'Category not deleled')
        return redirect('add-stock-category')


    return render(request,'veterinarian/stock/add_stockCategory.html',context)

# class StockCategoryDeleteView(View):                                                            # view class tostock
#     template_name = "veterinarian/stock/deleteCateg.html"                                                 
#     success_message = "Stock has been deleted successfully"                             
    
#     def get(self, request, pk):
#         stock = get_object_or_404(Stock_category, id=pk)
#         return render(request, self.template_name, {'object' : stock})

#     def post(self, request, pk):  
#         stock = get_object_or_404(Stock_category, id=pk)
#         stock.is_deleted = True
#         stock.save()                                               
#         messages.success(request, self.success_message)
#         return redirect('add-stock-category')



def create_stock(request):
    form=New_stockForm()
    if request.method == 'POST':
        form=New_stockForm(request.POST)
        try:
            if form.is_valid():
                form=New_stockForm(request.POST,request.FILES)
                form.save()
                messages.success(request, "Stock created succefully Successfully!")
                return redirect('add-stock2')
        except:
            messages.error(request, "Stock not added an error occured !")
            return redirect('add-stock2')

    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    return render(request,'veterinarian/stock/add_stock.html',context)
    
def edit_stock(request,pk):
    stock = New_stock.objects.get(id=pk)
    form = New_stockForm(instance=stock)
    form.fields['stock_name'].initial = stock.stock_name
    form.fields['category'].initial = stock.category
    form.fields['quantity'].initial = stock.quantity
    form.fields['stock_description'].initial = stock.stock_description
    # form.fields['stock_name'].initial = stock.stock_name
    if request.method == "POST":

        form =New_stockForm(request.POST,request.FILES ,instance=stock )
        try:
            if form.is_valid():
                # stock.stock_pic = request.FILES['stock_pic']
                # stock.save()
                image_path = stock.stock_pic.path
                if os.path.exists(image_path):
                    os.remove(image_path)
                form.save()
                messages.success(request, "Stock Updated Successfully")
                return redirect('manage-stock')
        except:
            messages.error(request, "Stock not  Updated ")
            return redirect('manage-stock')

    
    context = {'singleimagedata': stock, 'form': form}
  
    return render(request,'veterinarian/stock/edit_stock.html',context)

    
def manage_stock(request):
    stocks = New_stock.objects.filter(is_deleted=False)
    ex=New_stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo=New_stock.objects.annotate(
    expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    context = {
        "stocks": stocks,
        "expired":ex,
        "expa":eo,
        "title":"Manage Stocked Drugs"
    }

    return render(request,'veterinarian/stock/manage_stock.html',context)

class StockDeleteView(View):                                                            
    template_name = "veterinarian/stock/del.html"                                                 
    success_message = "Stock has been deleted successfully"                             
    
    def get(self, request, pk):
        stock = get_object_or_404(New_stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(New_stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('manage-stock')



# Purchases

def select_supplier(request): 
    form = SelectSupplierForm()
    context={
            'form': form
    }
    form = SelectSupplierForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)

    context={
    'form': form
    }
    return render(request,'veterinarian/purchases/select_supplier.html',context)


def create_purchase(request,pk):                                                 

    formset = PurchaseItemForm(request.GET or '0')                      
    supplierobj = get_object_or_404(Supplier, pk=pk)                       
    context = {
        'form'   : formset,
        'supplier'  : supplierobj,
    }                                                                      

    form = PurchaseItemForm(request.POST)                              
    supplierobj = get_object_or_404(Supplier, pk=pk)
    try:                  
        if form.is_valid():
            billobj = PurchaseBill(supplier=supplierobj)                        
            billobj.save()                                                     
                                        
            billitem = form.save(commit=False)
            billitem.billno = billobj                                     

            stock = get_object_or_404(New_stock, stock_name=billitem.stock.stock_name)       
            billitem.totalprice = billitem.perprice * billitem.quantity
            stock.quantity += billitem.quantity                              
            stock.save()
            billitem.save()
            messages.success(request, "Purchased items have been created successfully")
    except:
            messages.error(request, "Purchased items have been updated")
    form = PurchaseItemForm(request.GET or None)
    context = {
        'form'   : form,
        'supplier'  : supplierobj
    }
    return render(request, "veterinarian/purchases/add_newPurchase.html", context)



def view_purchases(request):
    purchase = PurchaseBill.objects.all()

    context = {
        "purchase": purchase,
    }

    return render(request,'veterinarian/purchases/view_purchases.html',context)
def delete_purchase(request,billno):
    category2 = PurchaseBill.objects.get(billno=billno)
    try:
        if request.method == 'POST':
            category2.delete()
            messages.success(request,'category deleted successsfully')
            return redirect('view-purchase')
    except:
        messages.error(request,'Category not deleled')
        return redirect('view-purchase')

    return render(request,'veterinarian/purchases/delete_purchase.html',context)

# sales
def create_sale(request):
    form = SalesItemForm()
    form2 = SalesForm()
    stocks = New_stock.objects.filter(is_deleted=False)

    context={
        "form":form,
        "formset":form2,
        'stocks': stocks

    }

    if request.method == 'POST':
        form = SalesItemForm(request.POST or request.FILES)
        form2 = SalesForm(request.POST , request.FILES)
        try:
            if form2.is_valid() and form.is_valid():
                billobj = form2.save(commit=False)
                billobj.save() 
                order = form.save(commit=False)
                order.billno = billobj                                      
                stock = get_object_or_404(New_stock, stock_name=order.product.stock_name)      
                order.totalprice = order.perprice * order.quantity
                stock.quantity -= order.quantity   
                stock.save()
                order.save()
                messages.success(request, "Sales items have been Created successfully")
                return redirect('add-sale')
        except:
            messages.error(request, "Sales items have not been created")
            return redirect('add-sale')

    form = SalesItemForm()

    context={
        "form":form,
        "formset":form2,
        'stocks': stocks

    }
    return render(request,'veterinarian/sales/add_sales.html',context)


def manage_sales(request):
    sales = CustomerItemsales.objects.all()

    context={
        "sales":sales
    }
    return render(request,'veterinarian/sales/manage_sales.html',context)

# admin profile
def profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=Veterinarian.objects.get(admin=customuser.id)
    context={
        "admin":admin,
    }

    return render(request,'veterinarian/vetProfile/profile.html',context)


def edit_profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=Veterinarian.objects.get(admin=customuser.id)

    form=AdminForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.email = email
        customuser.save()

        admin=Veterinarian.objects.get(admin=customuser.id)
        form =AdminForm(request.POST,request.FILES,instance=admin)
        admin.address = address
        admin.mobile=mobile
        admin.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "admin":admin,
        "user":customuser
    }

    return render(request,'veterinarian/vetProfile/edit_profile.html',context)



# Email ,username validation

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


