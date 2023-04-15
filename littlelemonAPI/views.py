from django.contrib.auth.models import Group, User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView

from .models import MenuItem, Cart, Order, OrderItem, Category
from rest_framework.response import Response
from rest_framework import viewsets,generics,status
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, \
    OrderManagerSerializer, OrderDeliveryCrewSerializer, CategorySerializer
from rest_framework.decorators import permission_classes, api_view


# Create your views here.
#category endpoint

class CategoryItemView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def post(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().post(request,*args,**kwargs)

class CategorySingleItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def patch(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().patch(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().put(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().delete(request,*args,**kwargs)

#Menu items
class MenuItemView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    filterset_fields = ['price','category__title']
    search_fields = ['title', 'category__title']

    def post(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().post(request,*args,**kwargs)

class MenuSingleItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def patch(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().patch(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().put(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().delete(request,*args,**kwargs)


#usergroups


@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def managers(request):
    managers = Group.objects.get(name='manager')
    if request.method == 'GET':
        try:
            group = Group.objects.get(name='manager')
        except Group.DoesNotExist:
            return Response({"message": "Group doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        users = group.user_set.all()
        serializer_item = UserSerializer(users, many=True)

        return Response(serializer_item.data, status=200)

    elif request.method == 'POST':
        username = request.data.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                managers.user_set.add(user)
                return Response({"message": "User added to the group"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User Not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def manager_delete(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    managers = Group.objects.get(name='manager')
    if user in managers.user_set.all():
        managers.user_set.remove(user)
        return Response({"message": "User removed from group"}, status=status.HTTP_200_OK)
    else:
        return Response({"error":"User not found in the group"}, 404)

@api_view(['GET','POST'])
def delivery_crew(request):
    if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
        if request.method == 'GET':
            try:
                group = Group.objects.get(name='delivery_crew')
            except Group.DoesNotExist:
                return Response({"message": "Group doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            users = group.user_set.all()
            serializer_item = UserSerializer(users, many=True)

            return Response(serializer_item.data, status=200)

        elif request.method == 'POST':
            username = request.data.get('username')
            group = Group.objects.get(name='delivery_crew')
            if username:
                user = User.objects.filter(username=username).first()
                if user:
                    group.user_set.add(user)
                    return Response({"message": "User added to the group"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "User Not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "User forbidden"}, 403)

@api_view(['DELETE'])
def delivery_crew_delete(request, pk):
    if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"message": "user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        managers = Group.objects.get(name='delivery_crew')
        if user in managers.user_set.all():
            managers.user_set.remove(user)
            return Response({"message": "User removed from group"}, status=status.HTTP_200_OK)
        else:
            return Response({"error":"User not found in the group"}, 404)
    else:
        return Response({"error": "User forbidden"}, 403)


#Cart management endpoints views

class CartListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=204)
## order api endpoints


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    ordering_fields = ['status']
    filterset_fields = ['delivery_crew', 'date']
    search_fields = ['status']

    def get_queryset(self):
        if self.request.user.groups.filter(name='manager').exists() or self.request.user.is_superuser:
            user = self.request.user
            queryset = Order.objects.all()
            return queryset
        elif self.request.user.groups.filter(name='delivery_crew').exists():
            user = self.request.user
            queryset = Order.objects.filter(delivery_crew=user).prefetch_related('order_items')
            return queryset
        else:
            user = self.request.user
            queryset = Order.objects.filter(user=user).prefetch_related('order_items')
            return queryset

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        # Get the requested order object
        order = self.get_object()

        # Check if the order belongs to the current user
        if order.user != request.user:
            return Response({'error': 'This order does not belong to the current user.'}, status=status.HTTP_403_FORBIDDEN)

        # Serialize the order object and return it in the response
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() or request.user.is_superuser:
            return self.partial_update(request, *args, **kwargs)
        elif request.user.groups.filter(name='delivery_crew').exists():
            # Get the requested order object
            order = self.get_object()

            # Update the order status to 0 or 1
            data = {'status': request.data.get('status', None)}
            serializer = OrderDeliveryCrewSerializer(order, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Return a success message
            return Response({'message': 'Order status updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)


    def put(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='manager').exists() and not request.user.is_superuser:
            return Response({'error': 'You are not allowed to perform this action.'}, status=403)
        return super().delete(request, *args, **kwargs)

