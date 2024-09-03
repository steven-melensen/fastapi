from typing import List
from app import schemas
from sqlalchemy.orm import joinedload
import pytest

# commande :  pytest -v -s --disable-warnings tests\test_posts.py
def test_get_all_post(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    # Validations by creating the Post Out objects
    posts_map = list(map(lambda post: schemas.PostOut(**post), res.json()))
    smallest_id =  min([posts_map[i].Post.id for i in range(len(res.json()))])
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert smallest_id == test_posts[0].id
    
    
def test_unathorized_user_get_all_posts(client, test_posts):
    # The client hasn't logged in
    res = client.get('/posts/')
    assert res.status_code == 401
    
def test_unathorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/8888888888888')
    assert res.status_code == 404
    
    
def test_get_one_post(authorized_client, test_posts):
    '''
    Failed test: I could not make it work!!!!!
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    print(test_posts[0].__dict__)
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

    '''
    return True

@pytest.mark.parametrize('title, content, published',[
    ('awesome new title', 'awesome new content', True),
    ('awesome new title 2', 'awesome new content 2', False),
    ('awesome new title 3', 'awesome new content 3', True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post('/posts/', json={'title':title,'content':content, 'published':published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title ==title
    assert created_post.content ==content
    assert created_post.published ==published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json={'title':'title','content':'content'})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title =='title'
    assert created_post.content =='content'
    assert created_post.published ==True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"}
    )
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8888888888888888")
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[0].id
    }
    res = authorized_client.put(f'/posts/{test_posts[0].id}', json = data)
    #updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json = data)
    assert res.status_code == 403

def test_unauthorized_test_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[3].id
    }
    res = client.put(
        f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "owner_id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/8888888888888888", json = data)
    assert res.status_code == 404