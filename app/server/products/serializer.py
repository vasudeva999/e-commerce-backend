import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Product

class ProductType(SQLAlchemyObjectType):
    pk = graphene.Int(source="id")

    class Meta:
        model = Product
        interfaces = graphene.relay.Node,