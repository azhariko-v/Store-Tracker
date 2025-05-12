from flask import Flask, render_template, request, redirect, url_for
from store import Store

app = Flask(__name__)
store = Store()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        store.add_item(name, price)
        return redirect(url_for('inventory'))
    return render_template('add_item.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', items=store.get_inventory())

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        store.purchase_item(item_id, quantity)
        return redirect(url_for('sales'))
    return render_template('purchase.html', items=store.get_inventory())

@app.route('/sales')
def sales():
    return render_template('sales.html', sales=store.get_sales())

if __name__ == '__main__':
    app.run(debug=True)
