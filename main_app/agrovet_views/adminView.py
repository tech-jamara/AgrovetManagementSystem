from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from main_app.forms import *
from main_app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Sum
from django.views.generic import (View)
from django.core.files.storage import FileSystemStorage 
import os
from django.conf import settings

# dashboard
def home(request):
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
    
    return render( request ,'Admin/dashboard.html',context)



# veterinarian
def add_veterinarian(request):
    form=VeterinarianForm()

    context={
        'form':form
    }
    if request.method == "POST":
        form = VeterinarianForm(request.POST, request.FILES)

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        if form.is_valid():
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
           
            try:
                user = CustomUser.objects.create_user(username=username, email=email,password=password, first_name=first_name, last_name=last_name,user_type=2 )
                user.veterinarian.address = address
                user.veterinarian.mobile = mobile
                user.veterinarian.profile_pic =profile_pic_url
            
                user.save()
                messages.success(request, "vet Added Successfully!")
                return redirect('add-vet1')
            except:
                messages.error(request, "vet Added Successfully!")
                return redirect('add-vet1')
        else:
            return redirect('add-vet1')

    context={
    "title":"Add Vet",
    'form':form
    }

    return render(request,'Admin/veterinarian/add_vet.html',context)


def manage_vet(request):
    staffs = Veterinarian.objects.all()
    context = {
        "staffs": staffs,
        "title":"Manage Vet",
             'role':'Veterinarian'

    }

    return render(request,'Admin/veterinarian/manage_vet.html',context)

def  view_vet(request,pk):
    staff = Veterinarian.objects.get(admin=pk)
    context = {
        "staffs": staff,
        "title":"Manage Vet",
             'role':'Veterinarian'
    }

    return render(request,'Admin/veterinarian/view_vet.html',context)

def edit_vet(request,staff_id):
    form=VeterinarianForm()

    context={
        'form':form
    }
    staff = Veterinarian.objects.get(admin=staff_id)

    if request.method == "POST":
        form = VeterinarianForm(request.POST, request.FILES)

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
       
        if form.is_valid():
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
        try:
        
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            staff = Veterinarian.objects.get(admin=staff_id)
            staff.address = address
            staff.mobile = mobile
            if profile_pic_url != None:
                staff.profile_pic = profile_pic_url
            staff.save()

            messages.success(request, "Vet Updated Successfully.")
            return redirect('manage-vet1')

        except:
            messages.error(request, "Vet Not Updated check form again and.")
            return redirect('/editVet/'+ staff_id)


    context = {
    "staff": staff,
    "id": staff_id,
    'title':"Edit Vet",
    'form':form

    }
    return render(request, "Admin/veterinarian/edit_vet.html", context)

def delete_vet(request,vet_id):
    vet=Veterinarian.objects.get(id=vet_id)
   
    if request.method == 'POST':
        vet.delete()
        messages.success(request, "Vet  deleted successfully")
        return redirect('manage-vet1')

    context={
  'clicked_vet':vet,
  'title':'delete vet'
    }
    return render(request,'Admin/supplier/delete_supplier.html',context)



def delete_supplier(request,pk):
    vet=Supplier.objects.get(id=pk)
    try:
        if request.method == 'POST':
            vet.delete()
            messages.success(request, "Vet  deleted successfully")
            return redirect('manage-supplier1')
    except:
        messages.error(request, "Error!! Vet bot  deleted ")
        return redirect('manage-supplier1')


    context={
  'clicked_vet':vet,
   'title': 'Delete Supplier',

    }
    return render(request,'Admin/veterinarian/delete_vet.html',context)

# Supplier
def create_supplier(request):
    form=SupplierForm()
    if request.method == 'POST':
        form=SupplierForm(request.POST ,request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Supplier Created  successfully")
                return redirect('manage-supplier1')
        except:
            messages.error(request, "An Error Occured Supplier not created  ")
            return redirect('add-supplier1')

    context={
        "form":form,
        "title":"Add Supplier"
    }
    return render(request,'Admin/supplier/add_supplier.html',context)

def edit_supplier(request,pk):
    stock = Supplier.objects.get(id=pk)
    form = EditSupplierForm(instance=stock)
    form.fields['name'].initial = stock.name
    form.fields['phone'].initial = stock.phone
    form.fields['email'].initial = stock.email
    form.fields['address'].initial = stock.address
    form.fields['phone_2'].initial = stock.phone_2

    if request.method == "POST":
        form =EditSupplierForm(request.POST,instance=stock )
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Supplier Details Updated Successfully")
                return redirect('manage-supplier1')
        except:
            messages.success(request, "Supplier Details not Updated an Error Occured")
            return redirect('edit-supplier1')

    context = {'form': form ,'title':'Edit Supplier'}
  
    return render(request,'Admin/supplier/edit_supplier.html',context)


def manage_suppier(request):
    supplier = Supplier.objects.all()
    context = {
        "staffs": supplier,
        "title":"Manage Supplier",
        'role':'Supplier'
    }

    return render(request,'Admin/supplier/manage_supplier.html',context)



#  stock
def add_stockCategory(request):
    form=CategoryForm()


    if request.method == 'POST':
        form=CategoryForm(request.POST ,request.FILES)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Category added Successfully!")
                return redirect('add-stock-category1')
        except:
            messages.error(request, "Category not added an Error!")
            return redirect('add-stock-category1')

    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    category = Stock_category.objects.filter(is_deleted=False)
    context={
        'category':category,
        'form':form,
        'title':'Add Stock Category'
    }
    return render(request,'Admin/stock/add_stockCategory.html',context)

def edit_category(request,pk):
    category2 = Stock_category.objects.get(id=pk)

    form = CategoryForm()
    form.fields['name'].initial = category2.name

    if request.method =='POST':
        form=CategoryForm(request.POST ,request.FILES,instance=category2)
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Category Updated Successfully!")
                return redirect('add-stock-category1')
        except:
            messages.error(request, "Category not updated an Error occured!")
            return redirect('add-stock-category1')

    context={
        'form':form
    }
    return render(request,'Admin/stock/edit_stockCategory.html',context)


def delete_category(request,pk):
    category2 = Stock_category.objects.get(id=pk)
    try:
        category2.delete()
        messages.success(request,'category deleted successsfully')
        return redirect('add-stock-category1')
    except:
        messages.error(request,'Category not deleled')
        return redirect('add-stock-category1')
    
    context={
        'title':'Delete Category'
    }


    return render(request,'Admin/stock/add_stockCategory.html',context)

# class StockCategoryDeleteView(View):                                                            # view class tostock
#     template_name = "Admin/stock/deleteCateg.html"                                                 
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
                messages.success(request, "Stock added Successfully!")
                return redirect('add-stock21')
        except:
            messages.error(request, "Stock not created an error occured !")
            return redirect('add-stock21')

    context={
        "form":form,
        "title":"Add a New Drug Category"
    }
    return render(request,'Admin/stock/add_stock.html',context)
    
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
                if stock.stock_pic:
                    image_path = stock.stock_pic.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                form.save()
                messages.success(request, "Stock Updated Successfully")
                return redirect('manage-stock1')
        except:
            messages.error(request, "Stock not Updated an error occured")
            return redirect('manage-stock1')

    context = {'form': form ,'title':'Edit Stock'}
  
    return render(request,'Admin/stock/edit_stock.html',context)

    
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

    return render(request,'Admin/stock/manage_stock.html',context)
def view_stock(request,pk):
    stock = get_object_or_404(New_stock,pk=pk)
    context={
        'stock':stock
    }
    return render(request,'Admin/stock/view_stock.html',context)

    


class StockDeleteView(View):                                                         
    template_name = "Admin/stock/del.html"                                                 
    success_message = "Stock has been deleted successfully"                             
    
    def get(self, request, pk):
        stock = get_object_or_404(New_stock, pk=pk)
        return render(request, self.template_name, {'object' : stock ,'title':'Delete Stock'})

    def post(self, request, pk):  
        stock = get_object_or_404(New_stock, pk=pk)
        stock.is_deleted = True
        stock.save()                                               
        messages.success(request, self.success_message)
        return redirect('manage-stock1')



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
            return redirect('new-purchase1', supplier.pk)

    context={
    'form': form,
    'title':'Select Supplier'
    }
    return render(request,'Admin/purchases/select_supplier.html',context)


def create_purchase(request,pk):                                                 

    formset = PurchaseItemForm()                      
    supplierobj = get_object_or_404(Supplier, pk=pk)                       
    context = {
        'formset'   : formset,
        'supplier'  : supplierobj,
    }                                                                      

    # form = PurchaseItemForm(request.POST) 
    formset = PurchaseItemFormset(request.POST)                            
                             
    supplierobj = get_object_or_404(Supplier, pk=pk)
                    
    if formset.is_valid():
        billobj = PurchaseBill(supplier=supplierobj)                        
        billobj.save()                                                     
        for form in formset:                                                
            billitem = form.save(commit=False)
            billitem.billno = billobj                                     
            stock = get_object_or_404(New_stock, stock_name=billitem.stock.stock_name)       
            billitem.totalprice = billitem.perprice * billitem.quantity
            stock.quantity += billitem.quantity                              
            stock.save()
            billitem.save()
        messages.success(request, "Purchased items have been added successfully")
    

    formset = PurchaseItemFormset(request.GET or None)

    # form = PurchaseItemForm(request.GET or None)
    context = {
        'formset'   : formset,
        'supplier'  : supplierobj,
        'title':'Create A purchase'
    }
    return render(request, "Admin/purchases/add_newPurchase.html", context)



def view_purchases(request):
    purchase = PurchaseBill.objects.all()

    context = {
        "purchase": purchase,
        'title':'View Purchase'
    }

    return render(request,'Admin/purchases/view_purchases.html',context)

def delete_purchase(request,billno):
    category2 = PurchaseBill.objects.get(billno=billno)
    try:
        if request.method == 'POST':
            category2.delete()
            messages.success(request,'category deleted successsfully')
            return redirect('view-purchase1')
    except:
        messages.error(request,'Category not deleled')
        return redirect('view-purchase1')
    context={
        'title':'Delete Purchase'
    }

    return render(request,'Admin/purchases/delete_purchase.html',context)

# sales
def create_sale(request):
    form = SalesItemForm()
    form2 = SalesForm()
    stocks = New_stock.objects.filter(is_deleted=False)

    context={
        "form":form,
        "formset":form2,
        'stocks': stocks,
                'title':'Make Sale'


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
                messages.success(request, "Purchased items have been registered successfully")

                return redirect('add-sale1')
        except:
            messages.error(request, "An error occured and purchase not added ")
            return redirect('add-sale1')

    form = SalesItemForm()

    context={
        "form":form,
        "formset":form2,
        'stocks': stocks,
        'title':'Make Sale'

    }
    return render(request,'Admin/sales/add_sales.html',context)


def manage_sales(request):
    sales = CustomerItemsales.objects.all()

    context={
        "sales":sales,
        'title':'Manage Sale'
    }
    return render(request,'Admin/sales/manage_sales.html',context)

def delete_sales(request,billno):
    category2 = CustomerItemsales.objects.get(billno=billno)
    try:
        if request.method == 'POST':
            category2.delete()
            messages.success(request,'category deleted successsfully')
            return redirect('manage-sale1')
    except:
        messages.error(request,'Category not deleled')
        return redirect('manage-sale1')
    
    context={
        'title':'Delete Sales'
    }

    return render(request,'Admin/sales/delete_sales.html',context)


# admin profile
def profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=SysAdmin.objects.get(admin=customuser.id)
    context={
        "admin":admin,
        'title':' Profile'
    }

    return render(request,'Admin/adminProfile/profile.html',context)


def edit_profile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    admin=SysAdmin.objects.get(admin=customuser.id)

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

        admin=SysAdmin.objects.get(admin=customuser.id)
        form =AdminForm(request.POST,request.FILES,instance=admin)
        admin.address = address
        admin.mobile=mobile
        admin.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "admin":admin,
        "user":customuser,
        'title':'Edit Profile'
    }

    return render(request,'Admin/adminProfile/edit_profile.html',context)
def manage_customer(request):
    customer = Customer.objects.all()
    context={
        'staffs':customer,
        'title':'Manage Customer'
    }
    return render(request,'Admin/customer/manage_customer.html',context)

def delete_customer(request,pk):
    vet=Customer.objects.get(id=pk)
    try:
        if request.method == 'POST':
            vet.delete()
            messages.success(request, "Customer  deleted successfully")
            return redirect('manage-customer1')
    except:
        messages.error(request, "Customer not deleted")
        return redirect('manage-customer1')
    context={
  'title':'delete Customer'
    }
    return render(request,'Admin/customer/delete_customer.html',context)

def manageAppointment(request):
    customer = Appointment.objects.all()
    context={
        'staffs':customer,
        'title':'Manage Customer'
    }
    return render(request,'Admin/customer/manage_appoint.html',context)


def view_appointment(request,pk):
    customer = Appointment.objects.get(id=pk)
    context={
        'staffs':customer,
        'title':'Manage Customer'
    }
    return render(request,'Admin/customer/view_appointment.html',context)

def approve_appointment(request,pk):
    appoint=Appointment.objects.get(id=pk)
    appoint.status=True
    appoint.save()
    return redirect('manage-appoint')

def delete_appointment(request,pk):
    customer = Appointment.objects.get(id=pk)
    try:
        if request.method == 'POST':
            customer.delete()
            messages.success(request, "Appointment  deleted successfully")
            return redirect('manage-appoint')
    except:
        messages.error(request, "Appointment not deleted")
        return redirect('manage-appoint')
    context={
  'title':'delete Customer'
    }
    return render(request,'Admin/customer/delete_appoint.html',context)


class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "Admin/purchases/purchase_invoice.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : Stock_puchases.objects.filter(billno=billno),
            'admin'         : SysAdmin.objects.get(admin=request.user ),
            'title'         : 'Purchase Order'

        }
        return render(request, self.template_name, context)

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






def reorder_level(request, pk):
    queryset = New_stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.stock_name) + " is updated to " + str(instance.reorder_level))

        return redirect("manage-stock1")
    context ={
        "instance": queryset,
        "form": form,
        "title":"Reorder Level"
    }

    return render(request,'Admin/stock/reoder_level.html',context)