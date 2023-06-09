import sqlite3
import re
from flask import Flask, session, render_template, request, g
from datetime import datetime

from cart import Cart
from db import login_user
from db import add_registereduser

import db
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
    global userLoggedIn
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
       
@app.route('/logout', methods=['GET', 'POST'], endpoint='logout')
def logout():
    global cart
    global userLoggedIn
    if request.method == 'POST':
        cart.shoppingCart = {}#clears cart
        userLoggedIn = []#clears userdata on logout.
        return render_template("login.html", LOGIN_ERROR_MSG = "User logged out.")


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
    
@app.route('/clear_cart', methods=['GET','POST'], endpoint="clear_cart")
def clear_cart():
    global cart
    global admin
    cart.shoppingCart = {}
    if admin == True:
        return render_template('admin_home.html', SHOPPINGCART_ITEMS=f"Cleared shopping cart.")
    else:
        return render_template('home.html', SHOPPINGCART_ITEMS="Cleared shopping cart.")

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
        for item, amount in cart.shoppingCart.items():
            if amount > db.get_product(item)[0][1]:#if amount requested of item is greater than current stock
                return render_template("cart.html", ERROR_MSG = f'Error: not enough {item} stock for this request.')
    #check the stock of the items in the receipt in the database.
    #if not enough stock, error message and return to home.

    #if stock is enough, proceed to next page with delivery info.
        
        return render_template("checkout.html")
    
#
@app.route('/checkoutInfo', methods=['GET', 'POST'], endpoint='checkoutInfo')
def confirm_purchase():
    global userLoggedIn
    global admin
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            shipping_address = request.form['address']
            credit_card = request.form['creditCard']
            total = round(Cart.getTotal(cart.shoppingCart), 2)
            username = userLoggedIn[0][0]
            print(userLoggedIn[0][0])
            db.checkout(username, shipping_address, total)
            for item, amount in cart.shoppingCart.items():
                db.increase_stock(item, -amount)#decrease stock by requested amount
            cart.shoppingCart = {}
            if admin == True:        
                return render_template("admin_home.html", SHOPPINGCART_MSG = "Successfully placed order.")
            else:
                return render_template("home.html", SHOPPINGCART_MSG = "Successfully placed order.")
        else: #if cancel pressed.
            return render_template("cart.html", SHOPPINGCART_ITEMS=Cart.decorateCart(cart.shoppingCart))

@app.route('/add_remove_farm', methods=['GET', 'POST'], endpoint='add_remove_farm')
def confirm_purchase():
    if request.method == 'POST':
        return render_template("add_remove_farm.html", FARMS=db.get_all_farms(), SUPPLIERS=db.get_all_suppliers())

@app.route('/add_farm_action', methods=['GET', 'POST'], endpoint='add_farm_action')
def confirm_purchase():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            farm_name = request.form['farm_name']
            location = request.form['location']
            supplier = request.form['supplier']
            db.add_farm(farm_name, location)
            db.add_sellsto(farm_name, supplier)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Added farm {farm_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")

@app.route('/remove_farm_action', methods=['GET', 'POST'], endpoint='remove_farm_action')
def confirm_purchase():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            farm_name = request.form['farm_name']
            db.remove_farm(farm_name)
            db.remove_sellsto(farm_name)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Removed farm {farm_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")
        
@app.route('/orders', methods=['GET', 'POST'], endpoint='orders')
def orders():
    user = userLoggedIn[0][0]
    order_history = db.get_orders(user)
    print(order_history)

    return render_template("orders.html", ORDER_HISTORY = order_history)

@app.route('/edit_inventory',  methods=['GET', 'POST'], endpoint='edit_inventory')
def edit_inventory():
    if request.method == 'POST':
        return render_template("edit_inventory.html", INVENTORY_ITEMS = db.get_inventory_stock())
    
@app.route('/edit_inventory_action',  methods=['GET', 'POST'], endpoint='edit_inventory_action')
def edit_inventory():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        msg = ''
        if buttonRequest == "Submit":
            item_name = request.form['item_name']
            amount_added = int(request.form['amount_added'])
            if db.get_product(item_name) == []:
                msg = 'Error: item does not exist.'
            else:
                db.increase_stock(item_name,amount_added)
                msg = f'Edited {item_name} stock by {amount_added}.'

        return render_template("admin_home.html", SHOPPINGCART_ITEMS = msg)

@app.route('/add_remove_supplier', methods=['GET', 'POST'], endpoint='add_remove_supplier')
def add_remove_supplier():
    if request.method == 'POST':
        return render_template("add_remove_supplier.html", SUPPLIERS=db.get_all_suppliers(), ITEMS=db.get_all_items())
    
@app.route('/add_supplier_action', methods=['GET', 'POST'], endpoint='add_supplier_action')
def add_supplier():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            supplier_name = request.form['supplier_name']
            product = request.form['product']
            product_id = request.form['product_id']
            db.add_supplier(supplier_name, product)
            db.add_supplies(supplier_name, product_id)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Added supplier {supplier_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")

@app.route('/remove_supplier_action', methods=['GET', 'POST'], endpoint='remove_supplier_action')
def confirm_purchase():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            supplier_name = request.form['supplier_name']
            db.remove_supplier(supplier_name)
            db.remove_supplies(supplier_name)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Removed supplier {supplier_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")
        
@app.route('/edit_admins', methods=['GET', 'POST'], endpoint='edit_admins')
def add_remove_admin():
    if request.method == 'POST':
        return render_template("edit_admins.html", ADMINS=db.get_all_admins(), USERS=db.get_all_registered_users())
    
@app.route('/add_admin', methods=['GET', 'POST'], endpoint='add_admin')
def add_admin():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            admin_name = request.form['admin_name']
            db.add_admin(admin_name)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Added admin {admin_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")


@app.route('/remove_admin', methods=['GET', 'POST'], endpoint='remove_admin')
def add_admin():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            admin_name = request.form['admin_name']
            db.remove_admin(admin_name)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Removed admin {admin_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")

@app.route('/manage_employees', methods=['GET', 'POST'], endpoint='manage_employees')
def manage_employees():
    if request.method == 'POST':
        return render_template("manage_employees.html", EMPLOYEES = db.get_all_employees())
    
@app.route('/add_employee', methods=['GET', 'POST'], endpoint='add_employee')
def add_admin():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            employee_id = request.form['employee_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            employer = request.form['employer']
            db.add_employee(employee_id, first_name, last_name, employer)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Added employee {first_name} {last_name}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")
        
@app.route('/remove_employee', methods=['GET', 'POST'], endpoint='remove_employee')
def add_admin():
    if request.method == 'POST':
        buttonRequest = request.form['submitType']
        if buttonRequest == "Submit":
            employee_id = request.form['employee_id']

            db.remove_employee(employee_id)
            return render_template("admin_home.html", SHOPPINGCART_ITEMS = f"Removed employee {employee_id}.")
        else: #if cancel pressed.
            return render_template("admin_home.html")