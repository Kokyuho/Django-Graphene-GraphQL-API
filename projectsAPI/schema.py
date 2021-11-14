import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Keyword, Project


#******************* TYPES *************************#
class KeywordType(DjangoObjectType):
    class Meta:
        model = Keyword
        fields = ("id","word","date")

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ("id","name","date","duration","description","keywords")


#******************* QUERY *************************#
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


#******************* KEYWORD-CRUD-MUTATIONS *************************#
class CreateKeyword(graphene.Mutation):

    # Define the arguments we can pass to the create method
    class Arguments:
        word = graphene.String(required=True)
    
    # Define what it returns
    keyword = graphene.Field(KeywordType)

    # Define the mutation itself
    @classmethod
    def mutate(cls, root, info, word):
        keyword = Keyword(word=word)
        keyword.save()
        # return an instance of the Mutation class
        return CreateKeyword(keyword=keyword)

class UpdateKeyword(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        word = graphene.String(required=True)
    
    keyword = graphene.Field(KeywordType)

    @classmethod
    def mutate(cls, root, info, id, word):
        keyword = Keyword.objects.get(pk=id)
        keyword.word = word
        keyword.save()
        return UpdateKeyword(keyword=keyword)

class DeleteKeyword(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
    
    keyword = graphene.Field(KeywordType)

    @classmethod
    def mutate(cls, root, info, id):
        keyword = Keyword.objects.get(pk=id)
        keyword.delete()
        return DeleteKeyword(keyword=keyword)

#******************* PROJECT-CRUD-MUTATIONS *************************#
class CreateProject(graphene.Mutation):

    # Define the arguments we can pass to the create method
    class Arguments:
        name = graphene.String(required=True)
        date = graphene.Date(required=True)
        duration = graphene.Int(required=True)
    
    # Define what it returns
    project = graphene.Field(ProjectType)

    # Define the mutation itself
    @classmethod
    def mutate(cls, root, info, name, date, duration):
        project = Project(name=name, date=date, duration=duration)
        project.save()
        # return an instance of the Mutation class
        return CreateProject(project=project)

class UpdateProject(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
    
    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, name):
        project = Project.objects.get(pk=id)
        project.name = name
        project.save()
        return UpdateProject(project=project)

class DeleteProject(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
    
    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id):
        project = Project.objects.get(pk=id)
        project.delete()
        return DeleteProject(project=project)


#******************* MUTATION *************************#
class Mutation(graphene.ObjectType):
    create_keyword = CreateKeyword.Field()
    update_keyword = UpdateKeyword.Field()
    delete_keyword = DeleteKeyword.Field()

    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


