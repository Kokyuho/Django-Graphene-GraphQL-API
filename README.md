# Django-Graphene-GraphQL-API

In this project, I build a simple GraphQL API in Django with Django-Graphene able 
to perform CRUD operations on a 'Projects' database.

### Install steps:
0. Running with python 3.8
1. "pip install -r requirements.txt" in your venv
2. "python manage.py runserver"

### API endpoint:
- http://127.0.0.1:8000/graphql --> graphiQL

### Queries:
- apiDescription
- allKeywords
- allProjects
- keywordById(id:id)
- projectById(id:id)

### Mutations:
- createKeyword
- updateKeyword
- deleteKeyword 
- createProject
- updateProject
- deleteProject

### To Do:
- Implement unit testing of all
- Implement continuous integration with github actions
