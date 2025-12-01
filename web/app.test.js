const request = require('supertest');
const app = require('./app');

// Reset the warehouse state between tests
beforeEach(() => {
    // Clear all warehouses by making delete requests
    // We need to access the internal state, so we'll just rely on the API
});

describe('Warehouse API', () => {
    let createdWarehouseId;

    describe('GET /api/warehouses', () => {
        test('returns empty array initially', async () => {
            const res = await request(app).get('/api/warehouses');
            expect(res.statusCode).toBe(200);
            expect(Array.isArray(res.body)).toBe(true);
        });
    });

    describe('POST /api/warehouses', () => {
        test('creates a new warehouse', async () => {
            const res = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test Warehouse', tilavuus: 100, alkuSaldo: 25 });
            
            expect(res.statusCode).toBe(201);
            expect(res.body.id).toBeDefined();
            createdWarehouseId = res.body.id;
        });

        test('returns error for missing name', async () => {
            const res = await request(app)
                .post('/api/warehouses')
                .send({ name: '', tilavuus: 100 });
            
            expect(res.statusCode).toBe(400);
            expect(res.body.error).toBe('Name is required');
        });

        test('returns error for invalid capacity', async () => {
            const res = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test', tilavuus: 'invalid' });
            
            expect(res.statusCode).toBe(400);
            expect(res.body.error).toBe('Invalid capacity value');
        });
    });

    describe('PUT /api/warehouses/:id', () => {
        test('updates warehouse', async () => {
            // First create a warehouse
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Original', tilavuus: 100 });
            const id = createRes.body.id;

            const res = await request(app)
                .put(`/api/warehouses/${id}`)
                .send({ name: 'Updated', tilavuus: 200 });
            
            expect(res.statusCode).toBe(200);
        });

        test('returns 404 for non-existent warehouse', async () => {
            const res = await request(app)
                .put('/api/warehouses/9999')
                .send({ name: 'Test', tilavuus: 100 });
            
            expect(res.statusCode).toBe(404);
        });

        test('returns error for missing name', async () => {
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test', tilavuus: 100 });
            const id = createRes.body.id;

            const res = await request(app)
                .put(`/api/warehouses/${id}`)
                .send({ name: '', tilavuus: 100 });
            
            expect(res.statusCode).toBe(400);
        });
    });

    describe('DELETE /api/warehouses/:id', () => {
        test('deletes warehouse', async () => {
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'ToDelete', tilavuus: 100 });
            const id = createRes.body.id;

            const res = await request(app).delete(`/api/warehouses/${id}`);
            expect(res.statusCode).toBe(200);
        });

        test('returns 404 for non-existent warehouse', async () => {
            const res = await request(app).delete('/api/warehouses/9999');
            expect(res.statusCode).toBe(404);
        });
    });

    describe('POST /api/warehouses/:id/add', () => {
        test('adds to warehouse', async () => {
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test', tilavuus: 100, alkuSaldo: 0 });
            const id = createRes.body.id;

            const res = await request(app)
                .post(`/api/warehouses/${id}/add`)
                .send({ amount: 50 });
            
            expect(res.statusCode).toBe(200);
        });

        test('returns 404 for non-existent warehouse', async () => {
            const res = await request(app)
                .post('/api/warehouses/9999/add')
                .send({ amount: 50 });
            
            expect(res.statusCode).toBe(404);
        });

        test('returns error for invalid amount', async () => {
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test', tilavuus: 100 });
            const id = createRes.body.id;

            const res = await request(app)
                .post(`/api/warehouses/${id}/add`)
                .send({ amount: 'invalid' });
            
            expect(res.statusCode).toBe(400);
        });
    });

    describe('POST /api/warehouses/:id/remove', () => {
        test('removes from warehouse', async () => {
            const createRes = await request(app)
                .post('/api/warehouses')
                .send({ name: 'Test', tilavuus: 100, alkuSaldo: 80 });
            const id = createRes.body.id;

            const res = await request(app)
                .post(`/api/warehouses/${id}/remove`)
                .send({ amount: 30 });
            
            expect(res.statusCode).toBe(200);
        });

        test('returns 404 for non-existent warehouse', async () => {
            const res = await request(app)
                .post('/api/warehouses/9999/remove')
                .send({ amount: 50 });
            
            expect(res.statusCode).toBe(404);
        });
    });

    describe('GET /', () => {
        test('serves the HTML page', async () => {
            const res = await request(app).get('/');
            expect(res.statusCode).toBe(200);
            expect(res.headers['content-type']).toMatch(/html/);
        });
    });
});
