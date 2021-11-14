import json
import pytest
from graphene_django.utils.testing import graphql_query

from projectsAPI.models import Keyword, Project


# Fixtures

@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func

@pytest.fixture
def testKeywords():
    keywords = []
    keywords.append(Keyword.objects.create(word="AI"))
    keywords.append(Keyword.objects.create(word="Data Science"))
    keywords.append(Keyword.objects.create(word="Web Dev"))
        
    return keywords

@pytest.fixture
def testProjects(testKeywords):
    projects = []

    project = Project.objects.create(name="Project 1",
                                     date="2021-06-11",
                                     duration=12,
                                     description="This is project 1...")
    project.keywords.add(testKeywords[0])
    project.keywords.add(testKeywords[1])
    project.save()
    projects.append(project)

    project = Project.objects.create(name="Project 2",
                                     date="2020-08-16",
                                     duration=6,
                                     description="This is project 2...")
    project.keywords.add(testKeywords[1])
    project.keywords.add(testKeywords[2])
    project.save()
    projects.append(project)
        
    return projects


# GraphQL API Tests

def test_api_endpoint(client):
    res = client.get('/graphql')
    res = res.json()
    assert res['errors']

def test_apiDescription(client_query):
    response = client_query(
        '''
        query {
            apiDescription
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content

@pytest.mark.django_db
def test_allKeywords(client_query, testKeywords):
    response = client_query(
        '''
        query {
            allKeywords {
                id
                word
                date
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['allKeywords'][0]['word'] == testKeywords[0].word

@pytest.mark.django_db
def test_allProjects(client_query, testProjects):
    response = client_query(
        '''
        query {
            allProjects {
                id
                name
                date
                duration
                description
                keywords {
                    id
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['allProjects'][0]['name'] == testProjects[0].name

@pytest.mark.django_db
def test_keywordById(client_query, testKeywords):
    response = client_query(
        '''
        query {
            keywordById(id:1) {
                id
                word
                date
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['keywordById']['word'] == testKeywords[0].word

@pytest.mark.django_db
def test_projectById(client_query, testProjects):
    response = client_query(
        '''
        query {
            projectById(id:1) {
                id
                name
                date
                duration
                description
                keywords {
                    id
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['projectById']['name'] == testProjects[0].name

@pytest.mark.django_db
def test_createKeyword(client_query):
    response = client_query(
        '''
        mutation {
            createKeyword(word: "testing") {
                keyword {
                    id
                    word
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['createKeyword']['keyword']['word'] == 'testing'

@pytest.mark.django_db
def test_updateKeyword(client_query, testKeywords):
    response = client_query(
        '''
        mutation {
            updateKeyword(id:1, word: "testing") {
                keyword {
                    id
                    word
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['updateKeyword']['keyword']['word'] == 'testing'

@pytest.mark.django_db
def test_deleteKeyword(client_query, testKeywords):
    response = client_query(
        '''
        mutation {
            deleteKeyword(id:1) {
                keyword {
                    word
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content

    # Check that is gone
    response2 = client_query(
        '''
        query {
            allKeywords {
                id
                word
                date
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content2 = json.loads(response2.content)
    assert 'AI' not in content2['data']['allKeywords']

@pytest.mark.django_db
def test_createProject(client_query):
    response = client_query(
        '''
        mutation {
            createProject(name: "Test Project", 
                          date:"2021-06-11", 
                          duration:12) {
                project {
                    id
                    name
                    date
                    duration
                    description
                    keywords {
                        id
                    }
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['createProject']['project']['name'] == 'Test Project'

@pytest.mark.django_db
def test_updateProject(client_query, testProjects):
    response = client_query(
        '''
        mutation {
            updateProject(id:1, name: "Test Project") {
                project {
                    id
                    name
                    date
                    duration
                    description
                    keywords {
                        id
                    }
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content
    assert content['data']['updateProject']['project']['name'] == 'Test Project'

@pytest.mark.django_db
def test_deleteProject(client_query, testProjects):
    response = client_query(
        '''
        mutation {
            deleteProject(id:1) {
                project {
                    name
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content = json.loads(response.content)
    assert 'errors' not in content

    # Check that is gone
    response2 = client_query(
        '''
        query {
            allProjects {
                id
                name
                date
                duration
                description
                keywords {
                    id
                }
            }
        }
        ''',
        graphql_url='/graphql'
    )
    content2 = json.loads(response2.content)
    assert 'Project 1' not in content2['data']['allProjects']
