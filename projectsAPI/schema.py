import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Keyword, Project


class KeywordType(DjangoObjectType):
    class Meta:
        model = Keyword
        fields = ("id","word","date")

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id","name","date","duration","description","keywords")


class Query(graphene.ObjectType):
    api_description = graphene.String()

    all_keywords = graphene.List(KeywordType)
    all_projects = graphene.List(ProjectType)

    keyword_by_id = graphene.Field(KeywordType, id=graphene.Int())
    project_by_id = graphene.Field(ProjectType, id=graphene.Int())

    def resolve_api_description(info, root):
        return "GraphQL API with CRUD operations of keywords and projects."

    def resolve_all_keywords(root, info):
        return Keyword.objects.all()

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_keyword_by_id(root, info, id):
        return Keyword.objects.get(pk=id)

    def resolve_project_by_id(root, info, id):
        return Project.objects.get(pk=id)


schema = graphene.Schema(query=Query)


