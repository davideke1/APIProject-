from django.contrib.auth.models import Group, User
from django.forms import model_to_dict
from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','title','price','category','featured']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class CartSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.ReadOnlyField(source='menuitem.title')
    price = serializers.SerializerMethodField(method_name='get_price')

    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_name', 'quantity', 'unit_price', 'price']

    def get_price(self,obj):
        return int(obj.quantity) * obj.unit_price

    def create(self, validated_data):
        user = self.context['request'].user
        cart_item = Cart.objects.create(user=user, **validated_data)
        return cart_item

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.BooleanField()

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Invalid status value. Must be either 0 or 1.")
        return value

    class Meta:
        model = Order
        fields = ['id', 'delivery_crew','status','date', 'total', 'order_items']


class OrderDeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Invalid status value. Must be either 0 or 1.")
        return value


class OrderManagerSerializer(serializers.ModelSerializer):
    delivery_crew = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(groups__name='delivery_crew'))

    class Meta:
        model = Order
        fields = ['delivery_crew', 'status']

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Invalid status value. Must be either 0 or 1.")
        return value
