from db import add_product, increase_stock, add_item, remove_product
def addInventoryItem(itemName, amount, price): #sets the stock and price
    add_product(itemName, amount, price)

def removeInventoryItem(itemName):
    remove_product(itemName)


def addInventoryStock(itemName, amount): #ADDS stock to existing
    increase_stock(itemName, amount)


#addInventoryItem('Apple', 50, 0.50)

#addInventoryItem('Banana', 100, 0.38)

#addInventoryItem('Chair', 30, 24.99)
#add_item("1A", "Apple", "../static/img/apples.png", "Food", 80, 0.50)

