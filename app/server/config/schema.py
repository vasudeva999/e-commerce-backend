import graphene
from auth.schema import Query as auth_query, Mutation as auth_mutation
from products.schema import Query as product_query, Mutation as product_mutation
from category.schema import Query as category_query, Mutation as category_mutation

class Query(auth_query, product_query, category_query, graphene.ObjectType):
    ...

class Mutation(auth_mutation, product_mutation, category_mutation, graphene.ObjectType):
    ...

schema = graphene.Schema(query=Query, mutation=Mutation)