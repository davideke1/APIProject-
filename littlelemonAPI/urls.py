from django.urls import path
from . import views
urlpatterns =[
    path('category',views.CategoryItemView.as_view()),
    path('category/<int:pk>',views.CategorySingleItemView.as_view()),
    path('menu-items',views.MenuItemView.as_view()),
    path('menu-items/<int:pk>',views.MenuSingleItemView.as_view()),
    path('groups/manager/users', views.managers),
    path('groups/manager/users/<int:pk>', views.manager_delete),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('groups/delivery-crew/users/<int:pk>', views.delivery_crew_delete),
    path('cart/menu-items', views.CartListCreateView.as_view()),
    path('orders', views.OrderListView.as_view()),
    path('orders/<int:pk>', views.OrderDetailView.as_view()),



]