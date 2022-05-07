from django.urls import path
from .agrovet_views import adminView 
from .agrovet_views import vetViews
from .agrovet_views import customerViews

from  . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #  login
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'), 
    path('signup/', views.customer_signup_view,name='signup'),

    # ----------------ADMIN URLS -----------------
    
    # admin dashboard
    path('',adminView.home ,name ='dashboard' ),

    # admin profile
    path('profile/',adminView.profile,name ='profile'),
    path('profile/edit/',adminView.edit_profile,name ='edit-profile'),


    # Veterinarian
    path('addVet/',adminView.add_veterinarian ,name ='add-vet1' ),
    path('manageVet/',adminView.manage_vet ,name ='manage-vet1' ),
    path('editVet/<staff_id>/',adminView.edit_vet ,name ='edit-vet1' ),
    path('deleteVet/<vet_id>/',adminView.delete_vet ,name ='delete-vet1' ),
    path('viewVet/<pk>',adminView.view_vet ,name ='view-vet1' ),


   
    # Supplier
    path('addSupplier/',adminView.create_supplier,name ='add-supplier1' ),
    path('manageSupplier/',adminView.manage_suppier,name ='manage-supplier1' ),
    path('selectSupplier/',adminView.select_supplier,name ='select-supplier1' ),
    path('editSupplier/<pk>/',adminView.edit_supplier,name ='edit-supplier1' ),
    path('deleteSupplier/<pk>/',adminView.delete_supplier,name ='delete-supplier1' ),
 

#    Customer
    path('manageCustomer/',adminView.manage_customer,name ='manage-customer1' ),
    path('deleteCustomer/<pk>/',adminView.delete_customer,name ='delete-customer1' ),
    path('manageAppointment/',adminView.manageAppointment ,name ='manage-appoint' ),
    path('viewAppointment/<pk>/',adminView.view_appointment ,name ='view-appoint' ), 
        path('approveAppointment/<pk>/',adminView.approve_appointment ,name ='approve-appoint' ), 
    path('deleteAppointment/<pk>/',adminView.delete_appointment,name ='delete-appoint1' ),


    # Purchase
    path('purchases/new/<pk>', adminView.create_purchase, name='new-purchase1'),
    path('viewPurchases/',adminView.view_purchases,name ='view-purchase1' ),
    path('deletePurchases/<billno>/', adminView.delete_purchase, name='delete-purchase1'),
    path("purchases/<billno>", adminView.PurchaseBillView.as_view(), name="purchase-bill"),


    # sales
    path('addSale/',adminView.create_sale,name ='add-sale1' ),
    path('manageSale/',adminView.manage_sales,name ='manage-sale1' ),
    path('deleteSales/<billno>/', adminView.delete_sales, name='delete-sales1'),

   

     
    # stock
    path('addStockCategory/',adminView.add_stockCategory,name ='add-stock-category1'),
    path('editStockCategory/<pk>/',adminView.edit_category,name ='edit-stock-category1'),
        # path('deletestock/<pk>/', adminView.StockDeleteView.as_view(), name='delete-stock'),
    path('admin_user/reorder_level/<str:pk>/', adminView.reorder_level, name="reorder_level"),

    path('deleteStockCategory/<pk>/',adminView.delete_category,name ='delete-stock-category1'),
    path('addStock/',adminView.create_stock,name ='add-stock21'),
    path('editStock/<pk>/',adminView.edit_stock,name ='edit-stock1'),
    path('manageStock/',adminView.manage_stock,name ='manage-stock1'),
    # path('deleteStock/<pk>/',adminView.delete_stock,name ='delete-stock'),
    path('deletestock/<pk>/', adminView.StockDeleteView.as_view(), name='delete-stock1'),
    path('viewstock/<pk>/', adminView.view_stock, name='view-stock1'),

    

    # Validations
    path('check_username_exist/', adminView.check_username_exist, name="check_username_exist"),
    path('check_email_exist/', adminView.check_email_exist, name="check_email_exist"),


    path('check_username_exist/', views.check_username_exist, name="check_username_exist"),
    path('check_email_exist/', views.check_email_exist, name="check_email_exist"),

# -----------------------------------------
    # -------------------------- VET URLS --------------------------

    # admin dashboard
    path('dash/',vetViews.vet_dashboard ,name ='dash' ), 

    # attendant profile
    path('staff-profile/',vetViews.profile,name ='profile2'),
    path('staff-profile/edit/',vetViews.edit_profile,name ='edit-profile2'),

    # Supplier
    path('staff-addSupplier/',vetViews.create_supplier,name ='add-supplier' ),
    path('staff-manageSupplier/',vetViews.manage_suppier,name ='manage-supplier' ),
    path('staff-selectSupplier/',vetViews.select_supplier,name ='select-supplier' ),

    # Purchase
    path('staff-purchases/new/<pk>', vetViews.create_purchase, name='new-purchase'),
    path('staff-viewPurchases/',vetViews.view_purchases,name ='view-purchase' ),
    path('staff-deletePurchases/<billno>/', vetViews.delete_purchase, name='delete-purchase'),

    # sales
    path('staff-addSale/',vetViews.create_sale,name ='add-sale' ),
    path('staff-manageSale/',vetViews.manage_sales,name ='manage-sale' ),


     
    # stock
    path('staff-addStockCategory/',vetViews.add_stockCategory,name ='add-stock-category'),
    path('staff-editStockCategory/<pk>/',vetViews.edit_category,name ='edit-stock-category'),
        # path('deletestock/<pk>/', vetViews.StockDeleteView.as_view(), name='delete-stock'),

    path('staff-deleteStockCategory/<pk>/',vetViews.delete_category,name ='delete-stock-category'),
    path('staff-addStock/',vetViews.create_stock,name ='add-stock2'),
    path('staff-editStock/<pk>/',vetViews.edit_stock,name ='edit-stock'),
    path('staff-manageStock/',vetViews.manage_stock,name ='manage-stock'),
    # path('deleteStock/<pk>/',vetViews.delete_stock,name ='delete-stock'),
    path('staff-deletestock/<pk>/', vetViews.StockDeleteView.as_view(), name='delete-stock'),

    # Validations
    path('check_username_exist/', vetViews.check_username_exist, name="check_username_exist"),
    path('check_email_exist/', vetViews.check_email_exist, name="check_email_exist"),




     # -------------------------- Customer URLS --------------------------
    # admin dashboard
    path('customer/',customerViews.customer_dashboard ,name ='customer' ), 
    path('customer-profile/',customerViews.profile,name ='profile3'),
    path('customer-profile/edit/',customerViews.edit_profile,name ='edit-profile3'),

    #Appointment
    path('makeAppointment/',customerViews.make_appointment ,name ='appoint-make' ),
    path('cust-manageAppointment/',customerViews.manage_appointment ,name ='manage-appnt3' ), 
 

]
