import unittest
from web_app import app, warehouses, warehouse_counter


class TestWebApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Reset state between tests
        warehouses.clear()
        global warehouse_counter
        import web_app
        web_app.warehouse_counter = 0

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_index_shows_no_warehouses_message(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_page_loads(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse(self):
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '25'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertEqual(len(warehouses), 1)

    def test_create_warehouse_empty_name(self):
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)
        self.assertEqual(len(warehouses), 0)

    def test_create_warehouse_invalid_numbers(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': 'invalid',
            'alku_saldo': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid numbers provided', response.data)

    def test_edit_page_loads(self):
        # First create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        response = self.client.get('/edit/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)
        self.assertIn(b'Test Warehouse', response.data)

    def test_edit_warehouse(self):
        # First create a warehouse
        self.client.post('/create', data={
            'name': 'Original Name',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        # Edit it
        response = self.client.post('/edit/1', data={
            'name': 'Updated Name',
            'tilavuus': '200'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Name', response.data)
        self.assertEqual(warehouses[1]['name'], 'Updated Name')
        self.assertEqual(warehouses[1]['varasto'].tilavuus, 200.0)

    def test_edit_nonexistent_warehouse(self):
        response = self.client.get('/edit/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to index
        self.assertIn(b'Warehouse Management', response.data)

    def test_edit_warehouse_empty_name(self):
        # First create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        response = self.client.post('/edit/1', data={
            'name': '',
            'tilavuus': '100'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)

    def test_edit_warehouse_invalid_capacity(self):
        # First create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        response = self.client.post('/edit/1', data={
            'name': 'Test',
            'tilavuus': 'invalid'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid capacity value', response.data)

    def test_add_to_warehouse(self):
        # Create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        # Add contents
        response = self.client.post('/add/1', data={
            'amount': '50'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(warehouses[1]['varasto'].saldo, 50.0)

    def test_add_to_nonexistent_warehouse(self):
        response = self.client.post('/add/999', data={
            'amount': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_invalid_amount(self):
        # Create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        response = self.client.post('/add/1', data={
            'amount': 'invalid'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should not crash, just redirect

    def test_remove_from_warehouse(self):
        # Create a warehouse with initial stock
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '80'
        })
        
        # Remove contents
        response = self.client.post('/remove/1', data={
            'amount': '30'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(warehouses[1]['varasto'].saldo, 50.0)

    def test_remove_from_nonexistent_warehouse(self):
        response = self.client.post('/remove/999', data={
            'amount': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_remove_invalid_amount(self):
        # Create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        
        response = self.client.post('/remove/1', data={
            'amount': 'invalid'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_warehouse(self):
        # Create a warehouse
        self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        
        self.assertEqual(len(warehouses), 1)
        
        # Delete it
        response = self.client.post('/delete/1', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(warehouses), 0)

    def test_delete_nonexistent_warehouse(self):
        response = self.client.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_multiple_warehouses(self):
        # Create multiple warehouses
        self.client.post('/create', data={
            'name': 'Warehouse 1',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        self.client.post('/create', data={
            'name': 'Warehouse 2',
            'tilavuus': '200',
            'alku_saldo': '100'
        })
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse 1', response.data)
        self.assertIn(b'Warehouse 2', response.data)
        self.assertEqual(len(warehouses), 2)
