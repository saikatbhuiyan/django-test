from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tag', views.TagViewset)
router.register('ingredients', views.IngredientViewset)
router.register('recipe', views.RecipeViewSet)
app_name = 'recipe'

urlpatterns = [
  path('', include(router.urls))
]