import sqlite3
from flask import Flask, session, render_template, request, g
from datetime import datetime

from cart import Cart

cart = Cart()

#from SQLDriver import *

app = Flask(__name__)



@app.route("/")
def testing():
    return render_template("home.html")

@app.route('/add_item', methods=['GET', 'POST'], endpoint='add_item')
def add_item():
    if request.method == 'POST':
        itemType = request.form['itemtype']
        if 'Remove' in itemType:
            itemType = itemType.lstrip('Remove')
            print (itemType)
            message = cart.removeItem(itemType)
            return render_template("home.html", SHOPPINGCART_ITEMS=message) 
        else:
            cart.addItem(itemType)
            return render_template("home.html", SHOPPINGCART_ITEMS=f"Added 1 {itemType}") 
           
    else:
        print("an error occured.")
        return render_template("home.html")
    
@app.route('/check_cart', methods=['GET', 'POST'], endpoint='check_cart')
def check_cart():
    if request.method == 'POST':
        return render_template("cart.html", SHOPPINGCART_ITEMS=Cart.decorateCart(cart.shoppingCart))

@app.route('/back', methods=['GET', 'POST'], endpoint='back')
def go_back():
    if request.method == 'POST':
        return render_template("home.html")
    
@app.route('/confirm', methods=['GET', 'POST'], endpoint='confirm')
def confirm_purchase():
    if request.method == 'POST':
    #check the stock of the items in the receipt in the database.
    #if not enough stock, error message and return to home.

    #if stock is enough, proceed to next page with delivery info.
        return render_template("checkout.html")
    
@app.route('/checkoutInfo', methods=['GET', 'POST'], endpoint='checkoutInfo')
def confirm_purchase():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            #add functionality here.
            return render_template("checkout.html")
        else:
            return render_template("cart.html")


# @app.route('/add_member', methods=['GET', 'POST'], endpoint='add_member')
# def add_member():
#     if request.method == 'POST':
#         player_ucid = request.form['player_id']
#         success, msg = add_team_member(player_ucid, CurrentUser[0][0])
#         if success:
#             print("PLAYER UCID: ", player_ucid)
#             return render_template("editTeams.html", ADD_MEMBER_MSG=msg)
#         else:
#             return render_template("editTeams.html", ADD_MEMBER_MSG=msg)
#     else:
#         return render_template("home.html")






# @app.route('/add_member', methods=['GET', 'POST'], endpoint='add_member')
# def add_member():
#     if request.method == 'POST':
#         player_ucid = request.form['player_id']
#         success, msg = add_team_member(player_ucid, CurrentUser[0][0])
#         if success:
#             print("PLAYER UCID: ", player_ucid)
#             return render_template("editTeams.html", ADD_MEMBER_MSG=msg)
#         else:
#             return render_template("editTeams.html", ADD_MEMBER_MSG=msg)
#     else:
#         return render_template("home.html")