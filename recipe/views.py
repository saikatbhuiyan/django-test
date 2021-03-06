from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, authentication, permissions, status
from django.http import HttpResponse

from core.models import Tag, Ingredient, Recipe

from . import serializers


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin
                        ):
  """Base viewset for user owned recipe attributes"""
  authentication_class = (authentication.TokenAuthentication,)
  permission_class = (permissions.IsAuthenticated,)

  def get_queryset(self):
    """Return objects for the current authenticated user only"""
    return self.queryset.filter(user=self.request.user).order_by('-name')

  def perform_create(self, serializer):
    """Create a new object"""
    serializer.save(user=self.request.user)
  
class TagViewset(BaseRecipeViewSet):
  """Manage tags in the database"""
  queryset = Tag.objects.all()
  serializer_class = serializers.TagSerializer


class IngredientViewset(BaseRecipeViewSet):
  """Manage ingredients in the database"""
  queryset = Ingredient.objects.all()
  serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
  """Manage recipes in the database"""
  authentication_class = (authentication.TokenAuthentication,)
  permission_class = (permissions.IsAuthenticated,)
  serializer_class = serializers.RecipeSerializer
  queryset = Recipe.objects.all()

  def get_queryset(self):
    """Retrive the recipe for the authenticated user"""
    return self.queryset.filter(user=self.request.user)

  def get_serializer_class(self):
    """Return approprite serializer class"""
    if self.action == 'retrieve':
      return serializers.RecipeDetailSerializer
    elif self.action == 'upload_image':
      return serializers.RecipeImageSerializer
    return self.serializer_class

  def perform_create(self, serializer):
    """Create a new recipe"""
    serializer.save(user=self.request.user)

  @action(methods=['POST'], detail=True, url_path='upload-image')
  def upload_image(self, request, pk=None):
    """Upload an image to a recipe"""
    recipe = self.get_object()
    serializer = self.get_serializer(
      recipe,
      data=request.data
    )

    if serializer.is_valid():
      serializer.save()
      return Response(
        serializer.data,
        status=status.HTTP_200_OK
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class TagViewset(viewsets.GenericViewSet,
#                   mixins.ListModelMixin,
#                   mixins.CreateModelMixin
#                   ):
#   """Manage tags in the database"""
#   authentication_class = (authentication.TokenAuthentication)
#   permissions_class = (permissions.IsAuthenticated)
#   queryset = Tag.objects.all()
#   serializer_class = serializers.TagSerializer

#   def get_queryset(self):
#     """Return objects for the current authenticationed user only"""
#     return self.queryset.filter(user=self.request.user).order_by('-name')

#   def perform_create(self, serializer):
#     """Create a new object"""
#     serializer.save(user=self.request.user)


# class IngredientViewset(viewsets.GenericViewSet,
#                   mixins.ListModelMixin,
#                   mixins.CreateModelMixin
#                   ):
      
#   """Manage ingredients in the database"""
#   authentication_class = (authentication.TokenAuthentication)
#   permissions_class = (permissions.IsAuthenticated)
#   queryset = Ingredient.objects.all()
#   serializer_class = serializers.IngredientSerializer

#   def get_queryset(self):
#     """Return objects for the current authenticationed user only"""
#     return self.queryset.filter(user=self.request.user).order_by('-name')

#   def perform_create(self, serializer):
#     """Create a new object"""
#     serializer.save(user=self.request.user)