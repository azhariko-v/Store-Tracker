from flask import Flask, render_template, request, redirect, url_for, flash
from store import Store
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'store_app_secret_key'  # Required for flash messages

# Create a global store instance
store = Store()
logger.info("Flask application initialized with Store")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            
            if not name or price <= 0:
                flash("Please provide a valid name and price", "error")
                return render_template('add_item.html')
                
            item_id = store.add_item(name, price)
            logger.info(f"Added item via web interface: ID={item_id}, Name={name}, Price={price}")
            flash(f"Item '{name}' added successfully!", "success")
            return redirect(url_for('inventory'))
        except Exception as e:
            logger.error(f"Error adding item: {str(e)}")
            flash(f"Error adding item: {str(e)}", "error")
            
    return render_template('add_item.html')

@app.route('/inventory')
def inventory():
    items = store.get_inventory()
    logger.info(f"Displaying inventory with {len(items)} items")
    return render_template('inventory.html', items=items)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        try:
            item_id = request.form['item_id']
            quantity = int(request.form['quantity'])
            
            if quantity <= 0:
                flash("Please enter a valid quantity", "error")
                return render_template('purchase.html', items=store.get_inventory())
                
            success = store.purchase_item(item_id, quantity)
            
            if success:
                item = next((item for item in store.get_inventory() if item.item_id == item_id), None)
                if item:
                    flash(f"Successfully purchased {quantity} of {item.name}", "success")
                else:
                    flash("Purchase recorded successfully", "success")
                logger.info(f"Purchase recorded via web interface: Item ID={item_id}, Quantity={quantity}")
                return redirect(url_for('sales'))
            else:
                flash("Item not found in inventory", "error")
        except Exception as e:
            logger.error(f"Error processing purchase: {str(e)}")
            flash(f"Error processing purchase: {str(e)}", "error")
            
    return render_template('purchase.html', items=store.get_inventory())

@app.route('/sales')
def sales():
    sales_data = store.get_sales()
    logger.info(f"Displaying sales history with {len(sales_data)} records")
    return render_template('sales.html', sales=sales_data)

if __name__ == '__main__':
    # Create a test item if inventory is empty
    if not store.get_inventory():
        logger.info("Adding sample item to empty inventory")
        store.add_item("Sample Product", 9.99)
    
    logger.info("Starting Flask application")
    app.run(debug=True)