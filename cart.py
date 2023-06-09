from db import getItemPrice
class Cart:
    def __init__(self) -> None:
        self.shoppingCart = {}

    def addItem(self, item):
        if item not in self.shoppingCart:
            self.shoppingCart[item]=0
        self.shoppingCart[item]+=1

    def removeItem(self, item):
        if item in self.shoppingCart:
            if self.shoppingCart[item] <= 0:
                return("Error: Item count is 0.")
            self.shoppingCart[item]-=1
            return(f"Removed 1 {item}")

        else:
            return("Error: Item count is 0.")

#takes in cart from retrieve cart, then adds html to make the cart look nice
    def decorateCart(cart):
        return_html = ""
        finalTotalPrice = 0
        for keys, value in cart.items():
            if value > 0:
                itemPrice = getItemPrice(keys)
                totalPrice = round(itemPrice * value, 2)
                return_html += f"{keys}: {value} = ${totalPrice}\n"
                finalTotalPrice += totalPrice
            
        return_html += "$" + str(round(finalTotalPrice, 2))
        return(return_html.split('\n'))
    
    def getTotal(cart):
        finalTotalPrice = 0
        for keys, value in cart.items():
            if value > 0:
                itemPrice = getItemPrice(keys)
                totalPrice = round(itemPrice * value, 2)
                finalTotalPrice += totalPrice
            
        return(finalTotalPrice)

