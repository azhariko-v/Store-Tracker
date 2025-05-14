from storage import load_data, save_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Item:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.item_id}: {self.name} - ${self.price:.2f}"
    
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price
        }


class Store:
    def __init__(self):
        logger.info("Initializing Store and loading data...")
        # Load data from file
        data = load_data()
        logger.info(f"Loaded data: {data}")
        
        # Initialize inventory from loaded data
        self.inventory = {}
        for item_data in data.get("inventory", []):
            item_id = item_data["item_id"]
            self.inventory[item_id] = Item(
                item_id=item_id,
                name=item_data["name"],
                price=item_data["price"]
            )
        
        # Initialize sales from loaded data
        self.sales = data.get("sales", [])
        
        logger.info(f"Store initialized with {len(self.inventory)} items and {len(self.sales)} sales records")

    def add_item(self, name, price):
        # Generate a unique ID
        existing_ids = [int(item_id) for item_id in self.inventory.keys() if item_id.isdigit()]
        next_id = str(max(existing_ids, default=0) + 1)
        
        logger.info(f"Adding item: ID={next_id}, Name={name}, Price={price}")
        self.inventory[next_id] = Item(next_id, name, price)
        self._save_data()
        return next_id

    def get_inventory(self):
        return list(self.inventory.values())

    def purchase_item(self, item_id, quantity):
        item = self.inventory.get(item_id)
        if item:
            total_price = item.price * quantity
            logger.info(f"Purchasing {quantity} of {item.name} for ${total_price:.2f}")
            self.sales.append([item.name, quantity, total_price])
            self._save_data()
            return True
        logger.warning(f"Item with ID {item_id} not found in inventory")
        return False

    def get_sales(self):
        return self.sales
    
    def _save_data(self):
        # Convert data to serializable format
        data = {
            "inventory": [item.to_dict() for item in self.inventory.values()],
            "sales": self.sales
        }
        logger.info(f"Saving data: {data}")
        save_data(data)


# Test the Store class directly
if __name__ == "__main__":
    print("Testing Store class...")
    store = Store()
    item_id = store.add_item("Test Product", 19.99)
    print(f"Added item with ID: {item_id}")
    print(f"Current inventory: {[str(item) for item in store.get_inventory()]}")
    
    if store.purchase_item(item_id, 2):
        print("Purchase successful")
    else:
        print("Purchase failed")
    
    print(f"Sales history: {store.get_sales()}")