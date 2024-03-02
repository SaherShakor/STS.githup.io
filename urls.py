from django.urls import path
from sts import views

app_name = "sts"


urlpatterns = [
    
    # Authentication operations
    path('signup/', views.Signup.as_view(), name = 'signup'),
    
    path('verify_account/', views.VerifyAccount.as_view(), name = 'verify_account'),
    
    path('login/', views.LogInAPI.as_view(), name = 'login'),

    path('orders/', views.CreateOrderView.as_view(), name='create_order'),

    path('list_orders/', views.ListOrders.as_view(), name='create_order'),

    path('add_captain/', views.AddCaptainView.as_view(), name='add-captain'),

    path('remove_captain/<int:captain_id>/', views.RemoveCaptainView.as_view(), name='add-captain'),

    path('list_order/<int:trip_id>/', views.UserTripDataView.as_view(), name='add-captain'),
    path('trip/<int:trip_id>/status/<str:action>/', views.TripStatusUpdateView.as_view(), name='add-captain'),
    
    path('userdata/', views.UserData.as_view(), name = 'userdata')
]
