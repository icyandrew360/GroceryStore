import sqlite3
import re
from flask import Flask, session, render_template, request, g
from datetime import datetime

from cart import Cart
from db import login_user
from db import add_registereduser
from admin_config import isUserAdmin

cart = Cart()
userLoggedIn = [] #upon succesful login, userdata is temporarily saved in this list.
#upon logout, this list is cleared.
admin = False #if logged in user is an admin, set to true

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'], endpoint='login')
def login():
    username = request.form['Username']
    password = request.form['Password']
    print(username, password)
    userlogin = login_user(username, password)
    print(userlogin)
    if userlogin[0] == True:
        #save the userdata into userlogin list.
        userLoggedIn = userlogin[1]
        global admin
        admin = isUserAdmin(username)
        if admin == True:
            return render_template("admin_home.html", ADMIN_MSG = "Logged in as admin.")
        else:
            return render_template("home.html")
    else:
        return render_template("login.html", LOGIN_ERROR_MSG = "There was an error logging in.")


@app.route("/register", methods=['GET', 'POST'], endpoint='register')
def register():
    username = request.form['Username']
    password = request.form['Password']
    fname = request.form["Fname"]
    lname = request.form["Lname"]
    address = request.form["Address"]

    status = add_registereduser(username, password, fname, lname, address)

    if status == True:
        return render_template("login.html", REGISTER_MSG = 'Succesful account creation. Please log in with account details.')

    else:
        return render_template("login.html", REGISTER_MSG = 'Error creating account.')
   # if re.fullmatch(regex, email):
       
    
#adds or removes desired item while on home screen
@app.route('/add_item', methods=['GET', 'POST'], endpoint='add_item')
def add_item():
    if request.method == 'POST':
        itemType = request.form['itemtype']
        if 'Remove' in itemType:
            itemType = itemType.lstrip('Remove')
            print (itemType)
            message = cart.removeItem(itemType)
            if admin == True:
                return render_template("admin_home.html", SHOPPINGCART_ITEMS=message)
            return render_template("home.html", SHOPPINGCART_ITEMS=message) 
        else:
            cart.addItem(itemType)
            if admin == True:
                return render_template("admin_home.html", SHOPPINGCART_ITEMS=f"Added 1 {itemType}") 
            return render_template("home.html", SHOPPINGCART_ITEMS=f"Added 1 {itemType}") 
           
    else:
        print("an error occured.")
        return render_template("home.html")
    
#pulls out the current recipt
@app.route('/check_cart', methods=['GET', 'POST'], endpoint='check_cart')
def check_cart():
    if request.method == 'POST':
        return render_template("cart.html", SHOPPINGCART_ITEMS=Cart.decorateCart(cart.shoppingCart))

#a back button that returns to the home page.
@app.route('/back', methods=['GET', 'POST'], endpoint='back')
def go_back():
    if request.method == 'POST':
        if admin == True:
            return render_template("admin_home.html")
        return render_template("home.html")
    
@app.route('/confirm', methods=['GET', 'POST'], endpoint='confirm')
def confirm_purchase():
    if request.method == 'POST':
        cart.shoppingCart
    #check the stock of the items in the receipt in the database.
    #if not enough stock, error message and return to home.

    #if stock is enough, proceed to next page with delivery info.
        return render_template("checkout.html")
    
#
@app.route('/checkoutInfo', methods=['GET', 'POST'], endpoint='checkoutInfo')
def confirm_purchase():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            #add functionality here. communicate with database.
            return render_template("checkout.html")
        else: #if cancel pressed.
            return render_template("cart.html", SHOPPINGCART_ITEMS=Cart.decorateCart(cart.shoppingCart)[0]
                                   , TOTAL_PRICE=Cart.decorateCart(cart.shoppingCart)[1])


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