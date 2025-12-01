const express = require('express');
const path = require('path');
const Varasto = require('./varasto');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// In-memory storage for warehouses
const warehouses = new Map();
let warehouseCounter = 0;

function getNextId() {
    warehouseCounter++;
    return warehouseCounter;
}

// API Routes
app.get('/api/warehouses', (req, res) => {
    const result = [];
    warehouses.forEach((wh, id) => {
        result.push({
            id,
            name: wh.name,
            tilavuus: wh.varasto.tilavuus,
            saldo: wh.varasto.saldo,
            paljonkoMahtuu: wh.varasto.paljonkoMahtuu()
        });
    });
    res.json(result);
});

app.post('/api/warehouses', (req, res) => {
    const { name, tilavuus, alkuSaldo } = req.body;
    
    if (!name || !name.trim()) {
        return res.status(400).json({ error: 'Name is required' });
    }
    
    const capacity = parseFloat(tilavuus);
    const initialStock = parseFloat(alkuSaldo) || 0;
    
    if (isNaN(capacity)) {
        return res.status(400).json({ error: 'Invalid capacity value' });
    }
    
    const id = getNextId();
    warehouses.set(id, {
        name: name.trim(),
        varasto: new Varasto(capacity, initialStock)
    });
    
    res.status(201).json({ id, message: 'Warehouse created' });
});

app.put('/api/warehouses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    const { name, tilavuus } = req.body;
    
    if (!warehouses.has(id)) {
        return res.status(404).json({ error: 'Warehouse not found' });
    }
    
    if (!name || !name.trim()) {
        return res.status(400).json({ error: 'Name is required' });
    }
    
    const capacity = parseFloat(tilavuus);
    if (isNaN(capacity)) {
        return res.status(400).json({ error: 'Invalid capacity value' });
    }
    
    const warehouse = warehouses.get(id);
    const currentSaldo = warehouse.varasto.saldo;
    warehouse.name = name.trim();
    warehouse.varasto = new Varasto(capacity, currentSaldo);
    
    res.json({ message: 'Warehouse updated' });
});

app.delete('/api/warehouses/:id', (req, res) => {
    const id = parseInt(req.params.id);
    
    if (!warehouses.has(id)) {
        return res.status(404).json({ error: 'Warehouse not found' });
    }
    
    warehouses.delete(id);
    res.json({ message: 'Warehouse deleted' });
});

app.post('/api/warehouses/:id/add', (req, res) => {
    const id = parseInt(req.params.id);
    const { amount } = req.body;
    
    if (!warehouses.has(id)) {
        return res.status(404).json({ error: 'Warehouse not found' });
    }
    
    const amountValue = parseFloat(amount);
    if (isNaN(amountValue)) {
        return res.status(400).json({ error: 'Invalid amount' });
    }
    
    warehouses.get(id).varasto.lisaaVarastoon(amountValue);
    res.json({ message: 'Added to warehouse' });
});

app.post('/api/warehouses/:id/remove', (req, res) => {
    const id = parseInt(req.params.id);
    const { amount } = req.body;
    
    if (!warehouses.has(id)) {
        return res.status(404).json({ error: 'Warehouse not found' });
    }
    
    const amountValue = parseFloat(amount);
    if (isNaN(amountValue)) {
        return res.status(400).json({ error: 'Invalid amount' });
    }
    
    const removed = warehouses.get(id).varasto.otaVarastosta(amountValue);
    res.json({ message: 'Removed from warehouse', removed });
});

// Serve the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

if (require.main === module) {
    app.listen(PORT, () => {
        console.log(`Warehouse app running at http://localhost:${PORT}`);
    });
}

module.exports = app;
