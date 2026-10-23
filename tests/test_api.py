import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from app import database
from app.main import app


class TestItemsAPI(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.old_db_path = database.DB_PATH
        database.DB_PATH = self.temp_db.name
        database.init_db()
        self.client = TestClient(app)
        self.headers = {"X-API-Key": "dev-secret-change-me"}

    def tearDown(self):
        self.client.close()
        database.DB_PATH = self.old_db_path
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_authentication_required(self):
        self.assertEqual(self.client.get("/items").status_code, 401)
        bad = self.client.get("/items", headers={"X-API-Key": "wrong"})
        self.assertEqual(bad.status_code, 401)

    def test_create_and_read_item(self):
        response = self.client.post(
            "/items",
            json={"name": "Laptop", "description": "Student laptop", "price": 45000},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)
        item_id = response.json()["id"]
        response = self.client.get(f"/items/{item_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Laptop")

    def test_list_items(self):
        self.client.post("/items", json={"name": "A", "price": 1}, headers=self.headers)
        self.client.post("/items", json={"name": "B", "price": 2}, headers=self.headers)
        response = self.client.get("/items", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_update_and_delete_item(self):
        response = self.client.post(
            "/items",
            json={"name": "Mouse", "description": "Wireless mouse", "price": 500},
            headers=self.headers,
        )
        item_id = response.json()["id"]
        response = self.client.put(
            f"/items/{item_id}",
            json={"name": "Gaming Mouse", "description": "Updated", "price": 1000},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Gaming Mouse")
        response = self.client.delete(f"/items/{item_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f"/items/{item_id}", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_not_found(self):
        self.assertEqual(self.client.get("/items/999", headers=self.headers).status_code, 404)

    def test_invalid_price(self):
        response = self.client.post(
            "/items",
            json={"name": "Book", "description": "Python book", "price": -10},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
