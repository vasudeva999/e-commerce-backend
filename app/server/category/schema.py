from email import message
from sqlalchemy.exc import IntegrityError
import graphene
from flask_graphql_auth import get_jwt_identity, query_header_jwt_required, mutation_header_jwt_required
from .serializer import CategoryType
from .models import Category
from config.database import db_session

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    category = graphene.List(CategoryType, pk=graphene.Int())

    @classmethod
    # @mutation_header_jwt_required
    def resolve_categories(cls, _, info):
        return Category.query.all()

    @classmethod
    # @mutation_header_jwt_required
    def resolve_category(cls, _, info, pk):
        return Category.query.filter_by(id=pk)

class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)
    success = graphene.Boolean()
    error = graphene.String(default_value="Not Authorised")

    class Arguments:
        name = graphene.String()

    @classmethod
    # @mutation_header_jwt_required
    def mutate(cls, _, info, name):
        try:
            new_category = Category(name=name)
            db_session.add(new_category)
            db_session.commit()
            return CreateCategory(success=True, category=new_category)
        except IntegrityError as e:
            return CreateCategory(error=f"{e.orig}")

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()