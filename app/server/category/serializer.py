import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Category

class CategoryType(SQLAlchemyObjectType):
    pk = graphene.Int(source="id")

    class Meta:
        model = Category
        interfaces = graphene.relay.Node,