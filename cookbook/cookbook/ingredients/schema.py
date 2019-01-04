# -*- coding: utf-8 -*-

# import json
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from cookbook.ingredients.models import Category, Ingredient
# from graphene_file_upload.scalars import Upload


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
            'id': ['exact'],
        }
    interfaces = (relay.Node, )


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
    interfaces = (relay.Node, )


#  定义动作 类似 POST PUT DELETE
class CategoryInput(graphene.InputObjectType):
    name = graphene.String(required=True)


class CreateCategory(graphene.Mutation):
    # api 的输入参数
    class Arguments:
        data = CategoryInput(required=True)
    
    # api 返回相应参数
    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    # api的相应操作  create
    def mutate(self, info, data):
        category = Category.objects.create(name=data['name'])
        ok = True
        return CreateCategory(category=category, ok=ok)

# class Category(graphene.ObjectType):
#     name = graphene.String()


# class CreateCategory(graphene.Mutation):
#     class Arguments:
#         name = graphene.String()

#     status = graphene.Boolean()
#     category = graphene.Field(CategoryType)
#     message = graphene.String()

#     def mutate(self, info, name):
#         if Category.objects.filter(name=name).exists():
#             return CreateCategory(status=False, message="{} already exists".format(name))
#         category = Category.objects.create(name=name)
#         return CreateCategory(category=category, status=True)


# class CreateCategory(graphene.Mutation):
#     class input:
#         data = graphene.String()

#     status = graphene.Boolean()
#     category = graphene.Field(CategoryType)
#     message = graphene.String()

#     @staticmethod
#     def mutate(self, info, args, **kwargs):
#         print args.get('message', '').strip()
#         name = "aa"
#         if Category.objects.filter(name=name).exists():
#             return CreateCategory(status=False, message="{} already exists".format(name))
#         category = Category.objects.create(name=name)
#         return CreateCategory(category=category, status=True)


class UpdateCategoryInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String()


class UpdateCategoryItem(graphene.ObjectType):
    category = graphene.Field(CategoryType)
    status = graphene.Boolean()


class UpdateCategory(graphene.Mutation):
    class Arguments:
        data = UpdateCategoryInput(required=True)

    detail = graphene.Field(UpdateCategoryItem)

    def mutate(self, info, data):
        id = data.pop('id')
        update_instance = Category.objects.filter(id=id).update(**data)
        if update_instance != 1:
            return UpdateCategory(detail=UpdateCategoryItem(status=False))
        else:
            instance = Category.objects.get(pk=id)
            return UpdateCategory(detail=UpdateCategoryItem(category=instance, status=True))


class DeleteCategoryInput(graphene.InputObjectType):
    id = graphene.Int(required=True)


class DeleteCategoryItem(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    info = graphene.String()
    status = graphene.Boolean()
    category = graphene.Field(CategoryType)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        where = DeleteCategoryInput(required=True)
     
    detail = graphene.Field(DeleteCategoryItem)

    def mutate(self, info, where):
        id = where.get('id')
        if not Category.objects.filter(id=id).exists():
            return DeleteCategory(detail=DeleteCategoryItem(info='id not exists', status=False))
        instance = Category.objects.get(id=id)
        name = instance.name
        instance.delete()
        return DeleteCategory(detail=DeleteCategoryItem(id=id, name=name, status=True, info='delete success'))


class CreateIngredient(graphene.Mutation):
    class Arguments:
        category_id = graphene.Int(required=True)
        name = graphene.String()
        notes = graphene.String()

    status = graphene.Boolean()
    message = graphene.String()
    ingredient = graphene.Field(IngredientType) 

    def mutate(self, info, **params):
        if not Category.objects.filter(id=params['category_id']).exists():
            return CreateIngredient(status=False, message='Category not exists')
        if Ingredient.objects.filter(name=params['name']).exists():
            return CreateCategory(status=False, message='Ingredient name already exists: \'{}\''.format(params['name']))
        
        ingredient = Ingredient.objects.create(name=params['name'],
                                               notes=params['notes'],
                                               category=Category.objects.get(id=params['category_id']))

        return CreateIngredient(status=True, message=True, ingredient=ingredient)


# 定义查询 类似GET
class Query(object):
    is_staff = graphene.Boolean()

    def resolve_is_staff(self, info):
        return True

    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())

    all_categories = graphene.List(CategoryType)

    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())

    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()
    
    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None

    hello = graphene.String(argument=graphene.String(default_value="World"))
    
    def resolve_hello(self, info, argument):
        return "Hello " + argument
