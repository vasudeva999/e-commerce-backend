import graphene
from auth.schema import Query as auth_query, Mutation as auth_mutation
from products.schema import Query as product_query, Mutation as product_mutation

class Query(auth_query, product_query, graphene.ObjectType):
    ...

class Mutation(auth_mutation, product_mutation, graphene.ObjectType):
    ...

schema = graphene.Schema(query=Query, mutation=Mutation)