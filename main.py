import json
from datetime import datetime
import pandas as pd
import os

# ============================================
# FILE INITIALIZATION FUNCTION
# ============================================

def initialize_json_files():
    """Create JSON files with default data if they don't exist"""
    
    # Default products data - ALL ARRAYS HAVE SAME LENGTH (12 items)
    default_products = {
        'products': ['Speakers', 'Mouse', 'Headfree', 'Headphones', 'Screen', 'LED Light',
                     'Tube light', 'Iron', 'Sensors', 'Airbuds', 'Ipads', 'Laptops'],
        'prices': [200, 230, 300, 1200, 3000, 500, 600, 1400, 5000, 3500, 1200, 34000],
        'Stock': [23, 50, 14, 300, 20, 70, 19, 10, 150, 40, 21, 15]  # Now 12 items (added 15)
    }
    
    # Create products.json if not exists
    if not os.path.exists('products.json'):
        with open('products.json', 'w') as file:
            json.dump(default_products, file, indent=4)
        print("✅ products.json created with default data!")
    
    # Create cart.json if not exists
    if not os.path.exists('cart.json'):
        with open('cart.json', 'w') as file:
            json.dump({}, file, indent=4)
        print("✅ cart.json created!")
    
    # Create orders.json if not exists
    if not os.path.exists('orders.json'):
        with open('orders.json', 'w') as file:
            json.dump([], file, indent=4)
        print("✅ orders.json created!")

# Call this function at program start
initialize_json_files()

# ============================================
# DICTIONARY CODE START
# ============================================

personal_detail = {
    'mozam_ali_365': {'password': 'murtaza333', 'email': 'webdeveloper252525@gmail.com'}
}

# ============================================
# FUNCTIONS CODE START
# ============================================

# VIEW PRODUCTS FUNCTION START
def view_products():
    try:
        with open('products.json', 'r') as file:
            customer_menu = json.load(file)
        
        # Check if all arrays have same length
        if len(customer_menu["products"]) != len(customer_menu["prices"]) or \
           len(customer_menu["products"]) != len(customer_menu["Stock"]):
            print("❌ Data error: Products, Prices, and Stock arrays have different lengths!")
            print(f"Products: {len(customer_menu['products'])} items")
            print(f"Prices: {len(customer_menu['prices'])} items")
            print(f"Stock: {len(customer_menu['Stock'])} items")
            return
        
        df = pd.DataFrame({
            "ID": range(1, len(customer_menu["products"]) + 1),
            "Product Name": customer_menu["products"],
            "Price": ["$" + str(p) for p in customer_menu["prices"]],
            "Stock": customer_menu["Stock"]
        })

        print("\n=== ALL PRODUCTS ===")
        print(df.to_string(index=False))
        print("-" * 50)

        low_stock_items = df[df["Stock"] < 5]
        for _, item in low_stock_items.iterrows():
            print(f"⚠️ LOW STOCK: {item['Product Name']} (only {item['Stock']} left)")
            
    except FileNotFoundError:
        print("❌ products.json not found!")
    except Exception as e:
        print(f"❌ Error viewing products: {e}")
# VIEW PRODUCTS FUNCTION STOP

# ADD PRODUCTS TO CART FUNCTION START
def add_cart_products():
    print(' ✅ Ok Sir You Want To Add Products To Cart')
    view_products()
    print('Select The Product That You Want To Add To The Cart')

    while True:
        cart_add_product_name = input('Enter The Product Name : ').capitalize()
        cart_add_product_stock = int(input('Enter The Product Quantity : '))

        try:
            with open('cart.json', 'r') as file:
                cart = json.load(file)

            with open('products.json', 'r') as file:
                customer_menu = json.load(file)

            if cart_add_product_name in customer_menu['products']:
                index = customer_menu["products"].index(cart_add_product_name)
                cart_add_product_price = customer_menu['prices'][index]

                if cart_add_product_stock <= customer_menu["Stock"][index]:
                    if cart_add_product_name in cart:
                        # Update existing cart item
                        cart[cart_add_product_name]['stock'] += cart_add_product_stock
                    else:
                        # Add new cart item
                        cart[cart_add_product_name] = {
                            'product': cart_add_product_name,
                            'prices': cart_add_product_price,
                            'stock': cart_add_product_stock
                        }

                    with open('cart.json', 'w') as file:
                        json.dump(cart, file)

                    print(' ✅ Your Product Added Successfully To The Cart')
                else:
                    print(f" ❌ Sorry Sir We Have Only {customer_menu['Stock'][index]} Available")
            else:
                print(' ❌ Invalid Product Name')

        except FileNotFoundError:
            print("❌ Required file not found!")
        except Exception as e:
            print(f"❌ Error: {e}")

        back_menu_option = input('Add More Products (Yes or No) : ').lower()
        if back_menu_option == 'yes':
            continue
        elif back_menu_option == 'no':
            break
# ADD PRODUCTS TO CART FUNCTION STOP

# REMOVE PRODUCTS FROM CART FUNCTION START
def remove_cart_products():
    print(' ✅ Ok Sir You Want To Remove Products From Cart')
    cart_remove_product_name = input('Enter The Product Name : ').capitalize()

    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)

        if cart_remove_product_name in cart:
            del cart[cart_remove_product_name]
            with open('cart.json', 'w') as file:
                json.dump(cart, file)
            print(' ✅ Your Product Successfully Removed From Cart')
        else:
            print(' ❌ Product Not Found In Cart')
    except FileNotFoundError:
        print("❌ Cart file not found!")
    except Exception as e:
        print(f"❌ Error: {e}")
# REMOVE PRODUCTS FROM CART FUNCTION STOP

# CHECKOUT FUNCTION START
def checkout():
    print("\n=== CHECKOUT ===")

    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
    except FileNotFoundError:
        cart = {}

    if not cart:
        print("🛒 Your cart is empty! Cannot checkout.")
        return

    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
    except FileNotFoundError:
        print("❌ Products file not found!")
        return

    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
    except FileNotFoundError:
        orders = []

    order_items = []
    subtotal = 0

    for product_name, item in cart.items():
        item_subtotal = item['prices'] * item['stock']
        subtotal += item_subtotal
        order_items.append({
            "product_name": product_name,
            "price": item['prices'],
            "quantity": item['stock'],
            "subtotal": item_subtotal
        })

    tax = subtotal * 0.10
    discount = subtotal * 0.05 if subtotal > 500 else 0
    total = subtotal + tax - discount

    # Update product stock
    for product_name, item in cart.items():
        if product_name in products['products']:
            index = products['products'].index(product_name)
            current_stock = products['Stock'][index]
            bought_quantity = item['stock']
            products['Stock'][index] = current_stock - bought_quantity

    with open('products.json', 'w') as file:
        json.dump(products, file, indent=4)

    # Create new order
    if isinstance(orders, dict):
        orders = list(orders.values())
    
    new_order = {
        "order_id": len(orders) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": order_items,
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total
    }

    orders.append(new_order)
    with open('orders.json', 'w') as file:
        json.dump(orders, file, indent=4)

    # Clear cart
    with open('cart.json', 'w') as file:
        json.dump({}, file)

    # Print receipt
    print("\n" + "=" * 50)
    print("           RECEIPT")
    print("=" * 50)
    print(f"Order ID: {new_order['order_id']}")
    print(f"Date: {new_order['date']}")
    print("-" * 50)
    print(f"{'Item':<20} {'Qty':<5} {'Price':<10} {'Total':<10}")
    print("-" * 50)

    for item in order_items:
        print(f"{item['product_name']:<20} {item['quantity']:<5} ${item['price']:<9} ${item['subtotal']:<10}")

    print("-" * 50)
    print(f"{'Subtotal':<36} ${subtotal:<10}")
    print(f"{'Tax (10%)':<36} ${tax:<10}")
    print(f"{'Discount':<36} -${discount:<9}")
    print("-" * 50)
    print(f"{'TOTAL':<36} ${total:<10}")
    print("=" * 50)
    print("   Thank you for shopping!")
    print("=" * 50)
# CHECKOUT FUNCTION STOP

# STOCK WARNING FUNCTION START
def stock_warning():
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)

        print("\n" + "-" * 50)
        print("⚠️ STOCK ALERT:")
        low_stock_found = False
        for i, product_name in enumerate(products['products']):
            if products['Stock'][i] < 5:
                print(f"   Low stock: {product_name} (only {products['Stock'][i]} left)")
                low_stock_found = True

        if not low_stock_found:
            print("   ✅ All products have sufficient stock")
        print("-" * 50)
    except FileNotFoundError:
        print("❌ products.json not found!")
    except Exception as e:
        print(f"❌ Error: {e}")
# STOCK WARNING FUNCTION STOP

# ORDER HISTORY CODE START
def view_order_history():
    print("\n=== ORDER HISTORY ===")

    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
    except FileNotFoundError:
        print("No order history found!")
        return

    if isinstance(orders, dict):
        orders = list(orders.values())

    if not orders:
        print("No orders placed yet!")
        return

    for order in orders:
        print("\n" + "=" * 50)
        print(f"📦 ORDER #{order['order_id']}")
        print(f"📅 Date: {order['date']}")
        print("-" * 50)
        print(f"{'Item':<20} {'Qty':<5} {'Price':<10} {'Total':<10}")
        print("-" * 50)

        for item in order['items']:
            print(f"{item['product_name']:<20} {item['quantity']:<5} ${item['price']:<9} ${item['subtotal']:<10}")

        print("-" * 50)
        print(f"{'Subtotal':<36} ${order['subtotal']:<10}")
        print(f"{'Tax (10%)':<36} ${order['tax']:<10}")

        if order['discount'] > 0:
            print(f"{'Discount':<36} -${order['discount']:<9}")

        print("-" * 50)
        print(f"{'TOTAL PAID':<36} ${order['total']:<10}")
        print("=" * 50)
# ORDER HISTORY CODE STOP

# SAVE DATA FUNCTION START
def save_data():
    print("\n=== SAVE DATA ===")

    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
        with open('products.json', 'w') as file:
            json.dump(products, file, indent=4)
        print("✅ Products saved successfully!")
    except FileNotFoundError:
        print("❌ No products file to save!")

    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
        with open('cart.json', 'w') as file:
            json.dump(cart, file, indent=4)
        print("✅ Cart saved successfully!")
    except FileNotFoundError:
        print("❌ No cart file to save!")

    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
        with open('orders.json', 'w') as file:
            json.dump(orders, file, indent=4)
        print("✅ Orders saved successfully!")
    except FileNotFoundError:
        print("❌ No orders file to save!")

    print("\n📁 All data saved to JSON files!")

# LOAD DATA FUNCTION START
def load_data():
    print("\n=== LOAD DATA ===")

    try:
        with open('products.json', 'r') as file:
            products = json.load(file)
        print("✅ Products loaded successfully!")
    except FileNotFoundError:
        print("❌ No products.json file found!")
        products = {"products": [], "prices": [], "Stock": []}
    except json.JSONDecodeError:
        print("❌ products.json is corrupted!")
        products = {"products": [], "prices": [], "Stock": []}

    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
        print("✅ Cart loaded successfully!")
    except FileNotFoundError:
        print("❌ No cart.json file found!")
        cart = {}
    except json.JSONDecodeError:
        print("❌ cart.json is corrupted!")
        cart = {}

    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
        print("✅ Orders loaded successfully!")
    except FileNotFoundError:
        print("❌ No orders.json file found!")
        orders = []
    except json.JSONDecodeError:
        print("❌ orders.json is corrupted!")
        orders = []

    print("\n📂 All data loaded from JSON files!")
    return products, cart, orders

# ============================================
# MAIN PROGRAM LOOP
# ============================================

while True:
    print('\n✅ === MAIN MENU === ✅')
    print('1 : Admin Login')
    print('2 : Customer Menu')
    print('3 : View Products')
    print('4 : Add to Cart')
    print('5 : Remove from Cart')
    print('6 : Checkout')
    print('7 : Order History')
    print('8 : Save Data')
    print('9 : Load Data')
    print('10 : Exit')

    try:
        user_option = int(input("Enter Your Choice : "))
    except ValueError:
        print("❌ Please enter a valid number!")
        continue

    # Admin Features Code Start
    if user_option == 1:
        print(' ✅ Ok Sir You Want To Login The Account ')
        login_username = input('Enter The Username : ')
        login_email = input('Enter The Email : ')
        login_password = input('Enter The Password : ')

        if (login_username in personal_detail and
            login_email == personal_detail[login_username]['email'] and
            login_password == personal_detail[login_username]['password']):
            print(' ✅ Login Successful ')

            while True:
                print('✅ === ADMIN MENU === ✅')
                print('1 : Add Products')
                print('2 : Remove Products')
                print('3 : Update Products Price')
                print('4 : Update Stock')
                print('5 : Exit As Admin')
                
                try:
                    admin_input = int(input('Enter The Choice Number : '))
                except ValueError:
                    print("❌ Please enter a valid number!")
                    continue

                if admin_input == 1:
                    print(' ✅ Ok Sir You Want To Add The Products ')
                    admin_product_name = input('Enter The Product Name : ').capitalize()
                    admin_product_price = int(input('Enter The Product Price : '))
                    admin_product_stock = int(input('Enter The Product Stock : '))

                    with open('products.json', 'r') as file:
                        customer_menu = json.load(file)

                    customer_menu["products"].append(admin_product_name)
                    customer_menu["prices"].append(admin_product_price)
                    customer_menu["Stock"].append(admin_product_stock)

                    with open('products.json', 'w') as file:
                        json.dump(customer_menu, file)

                    print(' ✅ Your Product Added Successfully')

                elif admin_input == 2:
                    print(' ✅ Ok Sir You Want To Remove The Products ')
                    admin_remove_product_name = input('Enter The Product Name : ').capitalize()

                    with open('products.json', 'r') as file:
                        customer_menu = json.load(file)

                    if admin_remove_product_name in customer_menu['products']:
                        index = customer_menu["products"].index(admin_remove_product_name)
                        customer_menu["products"].pop(index)
                        customer_menu["prices"].pop(index)
                        customer_menu["Stock"].pop(index)

                        with open('products.json', 'w') as file:
                            json.dump(customer_menu, file)

                        print(' ✅ Your Product Removed Successfully')
                    else:
                        print(' ❌ Product Not Found In Database')

                elif admin_input == 3:
                    print(' ✅ Ok Sir You Want To Update The Products Price')
                    admin_update_product_name = input('Enter The Product Name : ').capitalize()
                    admin_update_product_price = int(input('Enter The Product Price : '))

                    with open('products.json', 'r') as file:
                        customer_menu = json.load(file)

                    if admin_update_product_name in customer_menu['products']:
                        index = customer_menu["products"].index(admin_update_product_name)
                        customer_menu["prices"][index] = admin_update_product_price

                        with open('products.json', 'w') as file:
                            json.dump(customer_menu, file)

                        print(' ✅ Your Product Price Updated Successfully')
                    else:
                        print('❌ Invalid Product Name')

                elif admin_input == 4:
                    print(' ✅ Ok Sir You Want To Update The Products Stock')
                    admin_update_product_stock_name = input('Enter The Product Name : ').capitalize()
                    admin_update_product_stock_qty = int(input('Enter The Product Stock : '))

                    with open('products.json', 'r') as file:
                        customer_menu = json.load(file)

                    if admin_update_product_stock_name in customer_menu['products']:
                        index = customer_menu["products"].index(admin_update_product_stock_name)
                        customer_menu["Stock"][index] = admin_update_product_stock_qty

                        with open('products.json', 'w') as file:
                            json.dump(customer_menu, file)

                        print(' ✅ Your Product Stock Updated Successfully')
                    else:
                        print('❌ Invalid Product Name')

                elif admin_input == 5:
                    print(' ✅ Exiting Admin Menu')
                    break
        else:
            print(' ❌ Invalid Email, Username or Password')

    # Customer Features Code Start
    elif user_option == 2:
        print(' ✅ Welcome Sir To Our Customer Menu ')

        while True:
            print('✅ === CUSTOMER MENU === ✅')
            print('1 : View All Products')
            print('2 : Search Products By Name')
            print('3 : Sort Products (Low To High Price)')
            print('4 : Sort Products (High To Low Price)')
            print('5 : Add Products To Cart')
            print('6 : Remove Products From Cart')
            print('7 : View My Cart')
            print('8 : Checkout')
            print('9 : View My Order History')
            print('10 : Back To Main Menu')

            try:
                customer_option = int(input('Enter Your Choice : '))
            except ValueError:
                print("❌ Please enter a valid number!")
                continue

            if customer_option == 1:
                view_products()

            elif customer_option == 2:
                print(' ✅ Ok Sir You Want To Search Products ')
                search_product_name = input('Search The Product Name : ').capitalize()

                with open('products.json', 'r') as file:
                    customer_menu = json.load(file)

                if search_product_name in customer_menu['products']:
                    print(' ✅ Product Available On Our Store ')
                    index = customer_menu["products"].index(search_product_name)
                    print(f'Product Name: {search_product_name}')
                    print(f"Price: Rs{customer_menu['prices'][index]}")
                    print(f'Stock: {customer_menu["Stock"][index]}')
                else:
                    print(' ❌ Product Not Available')

            elif customer_option == 3:
                print(' ✅ Sorting Products (Low To High Price)')
                with open('products.json', 'r') as file:
                    customer_menu = json.load(file)

                df = pd.DataFrame({
                    "Product": customer_menu["products"],
                    "Price": customer_menu["prices"],
                    "Stock": customer_menu["Stock"]
                })
                df_sorted = df.sort_values(by="Price", ascending=True)
                print("=== Products Sorted by Price (Low to High) ===")
                print(df_sorted.to_string(index=False))

            elif customer_option == 4:
                print(' ✅ Sorting Products (High To Low Price)')
                with open('products.json', 'r') as file:
                    customer_menu = json.load(file)

                df = pd.DataFrame({
                    "Product": customer_menu["products"],
                    "Price": customer_menu["prices"],
                    "Stock": customer_menu["Stock"]
                })
                df_sorted = df.sort_values(by="Price", ascending=False)
                print("=== Products Sorted by Price (High to Low) ===")
                print(df_sorted.to_string(index=False))

            elif customer_option == 5:
                add_cart_products()

            elif customer_option == 6:
                remove_cart_products()

            elif customer_option == 7:
                print(' ✅ Viewing Your Cart')
                with open('cart.json', 'r') as file:
                    cart = json.load(file)

                if not cart:
                    print("🛒 Your cart is empty!")
                else:
                    cart_df = pd.DataFrame([
                        {
                            "ID": i + 1,
                            "Product Name": product_name,
                            "Price": "Rs" + str(item["prices"]),
                            "Quantity": item["stock"],
                            "Total": "Rs" + str(item["prices"] * item["stock"])
                        }
                        for i, (product_name, item) in enumerate(cart.items())
                    ])
                    print(cart_df.to_string(index=False))

            elif customer_option == 8:
                checkout()
                stock_warning()

            elif customer_option == 9:
                view_order_history()
                try:
                    with open('orders.json', 'r') as file:
                        orders = json.load(file)
                    if isinstance(orders, dict):
                        orders = list(orders.values())
                    if orders:
                        grand_total = sum(order['total'] for order in orders)
                        print(f"\n💰 GRAND TOTAL OF ALL ORDERS: ${grand_total}")
                        print(f"📊 TOTAL ORDERS PLACED: {len(orders)}")
                except:
                    pass

            elif customer_option == 10:
                print('Back To Main Menu')
                break

    elif user_option == 3:
        view_products()

    elif user_option == 4:
        add_cart_products()

    elif user_option == 5:
        remove_cart_products()

    elif user_option == 6:
        checkout()
        stock_warning()

    elif user_option == 7:
        view_order_history()
        try:
            with open('orders.json', 'r') as file:
                orders = json.load(file)
            if isinstance(orders, dict):
                orders = list(orders.values())
            if orders:
                grand_total = sum(order['total'] for order in orders)
                print(f"\n💰 GRAND TOTAL OF ALL ORDERS: ${grand_total}")
                print(f"📊 TOTAL ORDERS PLACED: {len(orders)}")
        except:
            pass

    elif user_option == 8:
        save_data()

    elif user_option == 9:
        load_data()

    elif user_option == 10:
        print(' ✅ Thanks For Our Store ')
        break
