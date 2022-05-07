from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime
from django.forms import formset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
today = datetime.today().date()
time = datetime.today().time()
print('TODAY ___=====',time)


class PatientForm(forms.ModelForm):
    # profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model=Customer
        fields=['address','mobile','profile_pic']

class AdminForm(forms.ModelForm):
    class Meta:
        model=SysAdmin
        fields='__all__'
        exclude=['admin','mobile','address']

class DateInput(forms.DateInput):
    input_type = "date"

class TimeInput(forms.TimeInput):
    input_type='time'


class VeterinarianForm(forms.Form):
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

class CustomerForm(forms.Form):
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
  
  

class CustomUserForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields='__all__'
        # exclude=['mobile','address']



class Stock_puchasesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = Stock_puchases
        fields = ['stock', 'quantity', 'perprice']


class CategoryForm(forms.ModelForm):
  
    name = forms.CharField(label="", max_length=40,required=False,widget=forms.TextInput(attrs={"class":"form-control"}))
    class Meta:
        model=Stock_category
        fields=['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if  not  name:
            raise ValidationError("This field is required")
       
        for instance in Stock_category.objects.all():
            if instance.name==name:
                raise ValidationError( "Category aready exist")
        return name
   

class New_stockForm(forms.ModelForm):
    
    valid_to= forms.DateField(label="",required=False, widget=DateInput(attrs={"class":"form-control"}))
    stock_name = forms.CharField(label="",max_length=50,required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    stock_description = forms.CharField(label="",max_length=150,required=False, widget=forms.Textarea(attrs={"class":"form-control"}))
    # stock_pic= forms.ImageField(label="", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    def __init__(self, *args, **kwargs):                                                        
        super().__init__(*args, **kwargs)
        # self.fields['category'].queryset = Stock_category.objects.filter(is_deleted=False)
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control',  'value':'0'})

    class Meta:
        model=New_stock
        fields='__all__'
        exclude=['valid_from']

         
    def clean_stock_name(self):
        stock_name = self.cleaned_data['stock_name']
        if  not  stock_name:
            raise ValidationError("This field is required")
        return stock_name
       
    def clean_valid_to(self):
        valid_to = self.cleaned_data['valid_to']
        if  not  valid_to:
            pass
      
        return valid_to
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if  quantity == None  or quantity < 0 :
            raise ValidationError("quantity can either be zero or greater but not empty")
        return quantity
  
class SupplierForm(forms.ModelForm):
    name = forms.CharField(label="",max_length=50,required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="", max_length=50,required=False, widget=forms.EmailInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="",max_length=150,required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone = forms.CharField( label="",max_length=50,required=False,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"2547xxxxxxxx"}), validators=[
        RegexValidator(
            regex='^(2547)([0-9|7])(\d){7}$',
            message='Invalid Phone Number format',
            code='invalid_number'
        )])
    phone_2 = forms.CharField( label="",max_length=50,required=False,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"2547xxxxxxxx"}), validators=[
        RegexValidator(
            regex='^(2547)([0-9|7])(\d){7}$',
            message='Invalid Phone Number format',
            code='invalid_number'
        )])
    class Meta:
        model=Supplier
        fields='__all__'
    def clean_name(self):
        name = self.cleaned_data['name']
        if  not  name:
            raise ValidationError("This field is required")
     
        return name
    def clean_email(self):
        email = self.cleaned_data['email']
        if  not  email:
            raise ValidationError("This field is required")
        for instance in Supplier.objects.all():
            if instance.email==email:
                raise ValidationError( "Supplier aready exist")
        return email
    def clean_phone(self):
            phone = self.cleaned_data['phone']
            if  not  phone:
                raise ValidationError("This field is required")
            for instance in Supplier.objects.all():
                if instance.phone==phone:
                    raise ValidationError( "Phone Number aready exist")
            return phone
    def clean_phone_2(self):
        phone_2 = self.cleaned_data['phone_2']
        if  not  phone_2:
            raise ValidationError("This field is required")
        for instance in Supplier.objects.all():
            if instance.phone_2==phone_2:
                raise ValidationError( "Phone Number aready exist")
        return phone_2
    def clean_address(self):
            address = self.cleaned_data['address']
            if  not  address:
                raise ValidationError("This field is required")
           
            return address
        
class EditSupplierForm(forms.ModelForm):
    name = forms.CharField(label="",max_length=50,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="", max_length=50,required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="",max_length=150,required=True, widget=forms.TextInput(attrs={"class":"form-control"}))
    phone = forms.CharField( label="",max_length=50,required=True,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"2547xxxxxxxx"}), validators=[
        RegexValidator(
            regex='^(2547)([0-9|7])(\d){7}$',
            message='Invalid Phone Number format',
            code='invalid_number'
        )])
    phone_2 = forms.CharField( label="",max_length=50,required=False,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"2547xxxxxxxx"}), validators=[
        RegexValidator(
            regex='^(2547)([0-9|7])(\d){7}$',
            message='Invalid Phone Number format',
            code='invalid_number'
        )])
    class Meta:
        model=Supplier
        fields='__all__'

class SelectSupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control'})
    class Meta:
        model = PurchaseBill
        fields = ['supplier']




class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = New_stock.objects.filter(is_deleted=False)

        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0', 'required': 'true'})
    class Meta:
        model = Stock_puchases
        fields = ['stock', 'quantity', 'perprice']
# formset used to render multiple 'PurchaseItemForm'
PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)

class SalesForm(forms.ModelForm):
    customer_name = forms.CharField(label='' , required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    email = forms.EmailField(label='' , required=False, widget=forms.EmailInput(attrs={"class":'form-control',"placeholder":"janedoe@gmail.com"}))
    address= forms.CharField(label='' , required=False, widget=forms.TextInput(attrs={"class":'form-control'}))
    saf_phone= forms.CharField(label='' , required=False, widget=forms.TextInput(attrs={"class":'form-control',"placeholder":"2547xxxxxxxx"}), validators=[
        RegexValidator(
            regex='^(2547)([0-9|7])(\d){7}$',
            message='Invalid Phone Number format',
            code='invalid_number'
        )])

    class Meta:
        model= CustomerItemsales
        fields ='__all__'

    def clean_customer_name(self):
        customer_name = self.cleaned_data['customer_name']
        if  not  customer_name:
            raise ValidationError("This field is required")
        
        return customer_name
    def clean_email(self):
        email = self.cleaned_data['email']
        if  not  email:
            raise ValidationError("This field is required")
      
        return email
    def clean_saf_phone(self):
        saf_phone = self.cleaned_data['saf_phone']
        if  not  saf_phone:
            raise ValidationError("This field is required")
    
        return saf_phone
    def clean_address(self):
        address = self.cleaned_data['address']
        if  not  address:
            raise ValidationError("This field is required")
     
        return address



class SalesItemForm(forms.ModelForm):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = New_stock.objects.filter(is_deleted=False)
        self.fields['product'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0'})
        self.fields['perprice'].widget.attrs.update({'class': 'textinput form-control setprice price', 'min': '0'})

    class Meta:
        model= CustomerOrderItem
        fields ='__all__'
        fields = ['product', 'quantity', 'perprice']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if  not  quantity:
            raise ValidationError("This field is required")
        return quantity
    def clean_perprice(self):
        perprice = self.cleaned_data['perprice']
        if  not  perprice:
            raise ValidationError("This field is required")

            
        return perprice

class AppointmentForm(forms.ModelForm):
    date_to= forms.DateField(label="Appointment Date",required=False, widget=DateInput(attrs={"class":"form-control"}))
    appointmentTime= forms.TimeField(label="Appointment Time",required=False, widget=TimeInput(attrs={"class":"form-control"}))
    pic = forms.ImageField(label="Upload an Image", required=False,  widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model= Appointment
        fields=['description','status' ,'date_to','pic','appointmentTime' ,'address','reason']

    def clean_date_to(self):
        date_to = self.cleaned_data['date_to']
        if  not  date_to:
            raise ValidationError("This field is required")
        elif date_to < today:
            raise ValidationError('Invalid Date')
        return date_to 

    def clean_description(self):
        description = self.cleaned_data['description']
        if  not  description:
            raise ValidationError("This field is required")
        return description
    def clean_reason(self):
        reason = self.cleaned_data['reason']
        if  not  reason:
            raise ValidationError("This field is required")
        return reason
    def clean_appointmentTime(self):
        appointmentTime = self.cleaned_data['appointmentTime']
        if  not  appointmentTime:
            raise ValidationError("This field is required")
     
        return appointmentTime


class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = New_stock
		fields = ['reorder_level']
