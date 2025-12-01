from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# In-memory storage for warehouses
warehouses = {}
warehouse_counter = 0


def get_next_id():
    global warehouse_counter
    warehouse_counter += 1
    return warehouse_counter


@app.route('/')
def index():
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
            alku_saldo = float(request.form.get('alku_saldo', 0))
        except ValueError:
            return render_template('create.html', error='Invalid numbers provided')
        
        if not name:
            return render_template('create.html', error='Name is required')
        
        warehouse_id = get_next_id()
        warehouses[warehouse_id] = {
            'name': name,
            'varasto': Varasto(tilavuus, alku_saldo)
        }
        return redirect(url_for('index'))
    
    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    if warehouse_id not in warehouses:
        return redirect(url_for('index'))
    
    warehouse = warehouses[warehouse_id]
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            tilavuus = float(request.form.get('tilavuus', 0))
        except ValueError:
            return render_template('edit.html', warehouse=warehouse, warehouse_id=warehouse_id, 
                                   error='Invalid capacity value')
        
        if not name:
            return render_template('edit.html', warehouse=warehouse, warehouse_id=warehouse_id,
                                   error='Name is required')
        
        # Update name and create new warehouse with same balance but new capacity
        current_saldo = warehouse['varasto'].saldo
        warehouse['name'] = name
        warehouse['varasto'] = Varasto(tilavuus, current_saldo)
        return redirect(url_for('index'))
    
    return render_template('edit.html', warehouse=warehouse, warehouse_id=warehouse_id)


@app.route('/add/<int:warehouse_id>', methods=['POST'])
def add_to_warehouse(warehouse_id):
    if warehouse_id not in warehouses:
        return redirect(url_for('index'))
    
    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        return redirect(url_for('index'))
    
    warehouses[warehouse_id]['varasto'].lisaa_varastoon(amount)
    return redirect(url_for('index'))


@app.route('/remove/<int:warehouse_id>', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    if warehouse_id not in warehouses:
        return redirect(url_for('index'))
    
    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        return redirect(url_for('index'))
    
    warehouses[warehouse_id]['varasto'].ota_varastosta(amount)
    return redirect(url_for('index'))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete_warehouse(warehouse_id):
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
