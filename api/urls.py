from django.urls import path
from core.views import OrderViewSet, InvoiceViewSet, CourierViewSet, DeliveryViewSet, AssetViewSet
from users.views import CustomerSignupView, AdminCreateView, UserListView, UserDetailView, PromoteToSystemAdminView, LoginView, LogoutView


urlpatterns = [
    # Order URLs
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list-create'),
    path('orders/<int:pk>/', OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='order-retrieve-update-destroy'),
    
    # Invoice URLs
    path('invoices/', InvoiceViewSet.as_view({'get': 'list', 'post': 'create'}), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='invoice-retrieve-update-destroy'),
    
    # Courier URLs
    path('couriers/', CourierViewSet.as_view({'get': 'list', 'post': 'create'}), name='courier-list-create'),
    path('couriers/<int:pk>/', CourierViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='courier-retrieve-update-destroy'),
    
    # Delivery URLs
    path('deliveries/', DeliveryViewSet.as_view({'get': 'list', 'post': 'create'}), name='delivery-list-create'),
    path('deliveries/<int:pk>/', DeliveryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='delivery-retrieve-update-destroy'),
    
    # Asset URLs
    path('assets/', AssetViewSet.as_view({'get': 'list', 'post': 'create'}), name='asset-list-create'),
    path('assets/<int:pk>/', AssetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='asset-retrieve-update-destroy'),
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/customer/', CustomerSignupView.as_view(), name='customer-signup'),
    path('admin/create/', AdminCreateView.as_view(), name='admin-create'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/promote/', PromoteToSystemAdminView.as_view(), name='promote-to-system-admin'),
]