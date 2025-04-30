from fastapi.testclient import TestClient
import faker
from app.main import app

client = TestClient(app)
fake = faker.Faker()

test_user_email = fake.email()
test_user_password = fake.password()
auth_token = ""

def test_register():
    response = client.post(
        "/v1/auth/register",
        json={
            "email": test_user_email,
            "password": test_user_password
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь создан"}

def test_login_wrong_password():
    response = client.post(
        "/v1/auth/login",
        json={
            "email": test_user_email,
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401
    assert "Неверный email или пароль" in response.json()["detail"]

def test_protected_endpoint():
    response = client.get(
        "/v1/hotels/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200