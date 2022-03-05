import pytest
from project.models.model_user import UsersModel


def test_user_password_hash_not_is_equal_to_true_password(simple_user):
    user = simple_user
    assert user.password_hash != "123456789"


def test_user_password_is_not_accessible(simple_user):
    user = simple_user
    with pytest.raises(AttributeError):
        user.password
        
        
def test_user_verify_password(simple_user):
    user = simple_user
    verify = user.verify_password("123456789")
    assert verify == True
    
def test_user_object_representation(simple_user):
    expected = f"<Name: {simple_user.username}>"
    representation = simple_user.__repr__()
    assert representation == expected
