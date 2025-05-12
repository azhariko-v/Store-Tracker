class Item:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.item_id}: {self.name} - ${self.price:.2f}"


class Store:
    def __init__(self):
        self.inventory = {}
        self.sales = []

    def add_item(self, name, price):
        item_id = str(len(self.inventory) + 1)
        self.inventory[item_id] = Item(item_id, name, price)

    def get_inventory(self):
        return list(self.inventory.values())

    def purchase_item(self, item_id, quantity):
        item = self.inventory.get(item_id)
        if item:
            total_price = item.price * quantity
            self.sales.append((item.name, quantity, total_price))
            return True
        return False

    def get_sales(self):
        return self.sales
