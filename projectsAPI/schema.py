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
    all_keywords = graphene.List(KeywordType)
    all_projects = graphene.List(ProjectType)

    def resolve_all_keywords(root, info):
        return Keyword.objects.all()

    def resolve_all_projects(root, info):
        return Project.objects.all()


schema = graphene.Schema(query=Query)


