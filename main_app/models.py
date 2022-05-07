from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from django.db.models import Sum


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Veterinarian"),(3,"Customer"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=20)




class SysAdmin(models.Model):
 
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    mobile=models.CharField(max_length=12,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default='',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_employed=models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()
    def __str__(self):
        return str(self.admin)

    class Meta:
        verbose_name_plural = 'Admin'
    


class Veterinarian(models.Model):
 
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    mobile =models.CharField(max_length=12,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic = models.FileField(upload_to='profile_pic', default="down.png",null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    class Meta:
        verbose_name_plural = 'Veterinarian'

    def __str__(self):
        return str(self.admin)



class Customer(models.Model):
    admin = models.OneToOneField(CustomUser,null=True, on_delete = models.CASCADE)
    mobile =models.CharField(max_length=12,null=True,blank=True)
    address=models.CharField(max_length=300,null=True,blank=True)
    profile_pic=models.ImageField(default="",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    class Meta:
        verbose_name_plural = 'Customer'

    def __str__(self):
        return str(self.admin)

class CustomerFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vet_id=models.ForeignKey( Veterinarian,null=True, on_delete=models.CASCADE)
    feedback = models.TextField(null=True)
    feedback_reply = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Appointment(models.Model):
    service_category=(
        ('Vaccinations','Vaccinations'),
        ('Surgery','Surgery'),
          ('Dehorning','Dehorning'),
          ('Routine Exam','Routine Exam'),
          ('Pregnancy Diagnosis','Pregnancy Diagnosis'),
          ('Artificial Insemination','Artificial Insemination'),
    )
    customerId=models.PositiveIntegerField(null=True)
    customerName=models.CharField(max_length=40,null=True,blank=True)
    reason = models.CharField(max_length=100,null=True,blank=True, choices=service_category)
    pic=models.ImageField(default="down.png",null=True,blank=True)
    appointmentDate=models.DateField(auto_now=True,null=True,blank=True)
    description=models.TextField(max_length=500,null=True,blank=True)
    address =models.CharField(max_length=100,null=True,blank=True)
    date_to = models.DateTimeField(blank=True, null=True)
    appointmentTime =models.TimeField(blank=True,null=True)
    status=models.BooleanField(default=False,null=True,blank=True)
     
class Stock_category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

class ExpiredManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
        )       


class New_stock(models.Model):
    stock_name = models.CharField(max_length=100,null=True,unique=True, blank=True)
    category = models.ForeignKey(Stock_category,null=True,on_delete=models.SET_NULL,blank=False)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    stock_description=models.TextField(blank=True,max_length=1000,null=True)
    stock_pic=models.ImageField(default="",null=True,blank=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    objects = ExpiredManager()

    
    def get_purchase(self):
        return PurchaseBill.objects.filter(billno=self)


  

    def __str__(self):
        return str(self.stock_name)

class Supplier(models.Model):
    name = models.CharField(max_length=150,blank=True,null=True)
    phone = models.CharField(max_length=12,blank=True, null=True,unique=True)
    address = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=254,blank=True, null=True,unique=True)
    phone_2= models.CharField(max_length=12,blank=True, null=True)
    def __str__(self):
        return str(self.name)

class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True,blank=False, null=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE,blank=False, null=True)
    def get_items_list(self):
        return Stock_puchases.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return   'Ksh {:20,.2f}'.format(total)
    def get_subTax(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        total = 0
        total1 =0
 
        for item in purchaseitems:
            total1 +=item.totalprice
            total = 0.16 * total1
        return   'Ksh {:20,.2f}'.format(total)
    
    def get_shipping(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        total = 0
        total1 =0
        for item in purchaseitems:
            total1 += item.totalprice
            total = 0.05 * total1
        return   'Ksh {:20,.2f}'.format(total)
    def get_alltotal(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        total = 0
        total1=0
        for item in purchaseitems:
            total1 += item.totalprice
            total2 = 0.05 * total1
            total3 = 0.01 * total1
            total = total1 + total2 + total3
        return   'Ksh {:20,.2f}'.format(total)
    
    def get_perprice(self):
            purchaseitems = Stock_puchases.objects.filter(billno=self)
            item = 0
            for item in purchaseitems:
                item = item.perprice
            return   'Ksh {:20,.2f}'.format(item)
    def get_item_price(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        item=0
        for item in purchaseitems:
            item = item.quantity
            
        return   'Ksh {:20,.2f}'.format(item)

    def total_item_price(self):
        purchaseitems = Stock_puchases.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total = item.quantity * item.perprice
        return   'Ksh {:20,.2f}'.format(total)





class Stock_puchases(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE,blank=False, null=True)
    stock = models.ForeignKey(New_stock,null=True,blank=True, on_delete = models.CASCADE)
    time2 = models.ForeignKey(PurchaseBill,null=True,blank=True, on_delete = models.CASCADE,related_name='purchasebilltime' )
    quantity = models.IntegerField(default=1,blank=False, null=True)
    perprice = models.IntegerField(default=1,blank=False, null=True)
    totalprice = models.IntegerField(default=1,blank=False, null=True)

    @property
    def total(self):
        tot = self.perprice * self.quantity
        return  'Ksh {:20,.2f}'.format(tot)

    def __str__(self):
        return str(self.stock.stock_name)

   

class CustomerItemsales(models.Model):
    billno=models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=120,blank=True,null=True)
    email=models.CharField(max_length=220,blank=True,null=True)
    saf_phone = models.CharField(max_length=14,blank=True,null=True)
    address=models.CharField(max_length=120,blank=True,null=True)
    sale_date=models.DateField(auto_now_add=True,blank=True,null=True)
    time =models.DateTimeField(auto_now=True,blank=False, null=True)

    def get_items_list(self):
        return CustomerOrderItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = CustomerOrderItem.objects.filter(billno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
          
        return   'Ksh {:20,.2f}'.format(total)

  
    def get_item_price(self):
            purchaseitems = CustomerOrderItem.objects.filter(billno=self)
            item=0
            for item in purchaseitems:
                item = item.quantity
                
            return   'Ksh {:20,.2f}'.format(item)

      

class CustomerOrderItem(models.Model):
    billno =models.ForeignKey(CustomerItemsales, on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(New_stock, on_delete=models.CASCADE,blank=True,null=True)
    time2 = models.ForeignKey(CustomerItemsales, on_delete=models.CASCADE,blank=True,null=True,related_name='customeritemsalestime')
    quantity = models.IntegerField(default=0,blank=True,null=True)
    perprice =models.IntegerField(default=0,blank=True,null=True)
    totalprice=models.IntegerField(default=0,blank=True,null=True)




@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            SysAdmin.objects.create(admin=instance)
        if instance.user_type == 2:
            Veterinarian.objects.create(admin=instance)
        if instance.user_type == 3:
            Customer.objects.create(admin=instance)
  
       
       
       

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.sysadmin.save()
    if instance.user_type == 2:
        instance.veterinarian.save()
    if instance.user_type == 3:
        instance.customer.save()
  

