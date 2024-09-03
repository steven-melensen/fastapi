from app import schemas
# Import of the below line is replaced with the conftest.py file that is accessible through pytest
#from .database import client, session # we need to import session, even though not directly referenced here!
import pytest
from jose import jwt
from app.config import settings


'''
Philosphy: we want every test to be independent of one another!
'''

#def test_root(client):
#    res = client.get('/')
#    print(res.json().get('message'))
#    assert res.json().get('message') == 'Welcome to my api!'
#    assert res.status_code == 200
    

    
def test_creater_user(client):
    #The json arguments actually takes the keys/vals of the UserCreate schema
    res = client.post('/users/', json = {'email': 'test4@test.com', 'password':'test'}) #Make sure a trailling '/' appears at the end of the path: /Users/ and not /Users, as otherwise FastAPI will create a307 redicrect, which will fail the 201 expected response
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'test4@test.com' # The Pydantic model does the validation for us!
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    # We sent the data through form-data using Postman, hence the data= instead of json=
    res = client.post('/login', data = {'username': test_user['email'], 'password':test_user['password']}) # No trailing required here 
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = str(payload.get('user_id'))  # Ensure id is treated as a string
    id = int(id)
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("sanjeev@gmail.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("sanjeev@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data = {'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials' # won't received the error message for missing info, hence the line commenting
    

