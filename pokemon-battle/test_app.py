import unittest
import json
from app import app  # Import the Flask app from your project

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

   
    def test_list_pokemon(self):
        response = self.app.get('/api/pokemon?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)

    def test_initiate_battle(self):
        battle_data = {
            'pokemon1': 'Pikachu',
            'pokemon2': 'Charmander'
        }
        response = self.app.post('/api/battle', json=battle_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('battle_id', data)
    
    def test_get_battle_status(self):
        battle_data = {
            'pokemon1': 'Pikachu',
            'pokemon2': 'Charmander'
        }
        response = self.app.post('/api/battle', json=battle_data)
        data = json.loads(response.data)
        battle_id = data['battle_id']
        response = self.app.get(f'/api/battle/{battle_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)

if __name__ == '__main__':
    unittest.main()
