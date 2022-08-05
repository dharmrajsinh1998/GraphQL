import graphene
from graphene_django import DjangoObjectType
from .models import Product, Order, Brand, Category


class ProductType(DjangoObjectType):
    class Meta:

        model = Product
        fields = ["id", "name", "category", "brand", "price", "qty", "image"]


class CategoryType(DjangoObjectType):

    class Meta:
        model = Category
        fields = ["id", "name"]


class CreateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()

        return CreateCategory(category=category)


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ["id", "name", "timestamp", "placed", "total_price", "total_qty", "products"]


class Query(graphene.ObjectType):

    all_orders = graphene.List(OrderType)
    order_by_id = graphene.Field(OrderType, id=graphene.Int())

    def resolve_all_orders(root, info):

        return Order.objects.all()

    def resolve_order_by_id(root, info, id):

        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
