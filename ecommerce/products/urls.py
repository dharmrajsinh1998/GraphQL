from django.urls import path
from graphene_django.views import GraphQLView

app_name = "app"

urlpatterns = [
    path("graphql/", GraphQLView.as_view(graphiql=True), name="graphql"),
]
