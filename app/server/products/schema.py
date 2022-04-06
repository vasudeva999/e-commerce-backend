from sqlalchemy.exc import IntegrityError
import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required
from .serializer import ProductType
from .models import Product
from config.database import db_session


class Query(graphene.ObjectType):
    products = SQLAlchemyConnectionField(ProductType.connection)
    product = graphene.Field(ProductType, pk=graphene.Int())

    @classmethod
    # @query_header_jwt_required
    def resolve_products(cls, _, info):
        return Product.query.all()

    @classmethod
    # @query_header_jwt_required
    def resolve_product(cls, _, info, pk):
        return Product.query.filter_by(id=pk)

class ProductAttribute:
    name = graphene.String()
    description = graphene.String()
    category_id = graphene.Int()
    quantity = graphene.Int()
    price = graphene.Float()

class CreateProductInput(graphene.InputObjectType, ProductAttribute):
    ...

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)
    success = graphene.Boolean()
    error = graphene.String()

    class Arguments:
        input = CreateProductInput(required=True)

    @classmethod
    @mutation_header_jwt_required
    def mutate(cls, _, info, input):
        input['owner_id'] = get_jwt_identity()
        try:
            product = Product(**input)
            db_session.add(product)
            db_session.commit()
            return CreateProduct(success=True)
        except IntegrityError as e:
            return CreateProduct(error=f"{e.orig}", success=False)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
