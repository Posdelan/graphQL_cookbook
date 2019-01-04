# -*- coding: utf-8 -*-

import graphene
import graphql_jwt
import cookbook.ingredients.schema
import cookbook.users.schema
# import cookbook.users.schema


class Query(cookbook.ingredients.schema.Query, cookbook.users.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutations(graphene.ObjectType):

    create_category = cookbook.ingredients.schema.CreateCategory.Field()
    update_category = cookbook.ingredients.schema.UpdateCategory.Field()
    delete_category = cookbook.ingredients.schema.DeleteCategory.Field()
    create_ingredient = cookbook.ingredients.schema.CreateIngredient.Field()
    create_user = cookbook.users.schema.CreateUser.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# class UploadMu(graphene.ObjectType):
#     upload_file = cookbook.ingredients.schema.MyUpload.Field()

# upload_schema = graphene.Schema(mutation=UploadMu, types=[])


schema = graphene.Schema(query=Query,
                         mutation=Mutations
                         )