from fastapi.testclient import TestClient 
from main import app
from app.core.security import create_token_access


client = TestClient(app) 


class TestApp: 
    TEST_USER = {"username": "Itoshi", "password": "ghpH1845"}
    ACCESS_TOKEN = create_token_access({"sub": TEST_USER["username"]})

    def test_reg_user(self): 
        response = client.post("/auth/register", json={"username": "Raichi3", "password": "qwerty1234"})

        try:
            assert response.status_code == 200 
        except: 
            assert response.status_code == 409


    def test_log_user(self): 
        response = client.post("/auth/login", json={"username": self.TEST_USER["username"], "password": self.TEST_USER["password"]})

        assert response.status_code == 200


    def test_get_task(self): 
        response = client.get("/tasks/get_all_tasks", headers={"Authorization": f"Bearer {self.ACCESS_TOKEN}"}) 

        assert response.status_code == 200


    def test_add_task(self): 
        response = client.post("/tasks/add_task", json={"name": "Learn GO", "state": "in process..."}, headers={"Authorization": f"Bearer {self.ACCESS_TOKEN}"})
        
        try:
            assert response.status_code == 200
        except: 
            assert response.status_code == 409


    def test_update_task(self): 
        response = client.put("/tasks/update_task", json={"name": "Learn GO", "state": "complete"}, headers={"Authorization": f"Bearer {self.ACCESS_TOKEN}"})

        assert response.status_code == 200


    def test_delete_task(self): 
        response = client.delete("/tasks/delete_task", headers={"Authorization": f"Bearer {self.ACCESS_TOKEN}"})

        assert response.status_code == 200




