from db import add_product, increase_stock
def addInventoryItem(itemName, amount, price): #sets the stock and price
    add_product(itemName, amount, price)


def addInventoryStock(itemName, amount): #ADDS stock to existing
    increase_stock(itemName, amount)


#addInventoryItem('Apple', 50, 0.50)

#addInventoryItem('Banana', 100, 0.38)

#addInventoryItem('Chair', 30, 24.99)