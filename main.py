import json
from datetime import datetime
import pandas as pd
import os

                                  # DICTIONARY CODE START

personal_detail = {
    'mozam_ali_365' : {'password' : 'murtaza333', 'email' : 'webdeveloper252525@gmail.com'}
}

customer_menu = {
 
    'products' : ['Speakers' , 'Mouse' , 'Headfree' , 'Headphones' , 'Screen' , 'LED Light',
                  'Tube light' , 'Iron' , 'Sensors' , 'Airbuds' , 'Ipads' , 'Laptops'],
     'prices'  : [200 , 230 , 300 , 1200 , 3000 , 500 , 600 , 1400 , 5000 , 3500 , 1200 , 34000],
     "Stock" : [23,50,14,300,20,70,19,10,150,40,21]
                }

                                  #  DICTIONARY CODE STOP



                                  # FUNCTIONS CODE START

# VIEW PRODUCTS FUNCTON START

def view_products ():
          
          with open('products.json' , 'r')as file:
            customer_menu = json.load(file)

          # Create DataFrame
          df = pd.DataFrame({
          "ID": range(1, len(customer_menu["products"]) + 1),
          "Product Name": customer_menu["products"],
          "Price": ["$" + str(p) for p in customer_menu["prices"]],
          "Stock": customer_menu["Stock"]
        })

          # Display the table
          print("=== ALL PRODUCTS ===")
          print(df.to_string(index=False))
          print("-" * 50)

          # Low stock warning
          low_stock_items = df[df["Stock"] < 5]
          for _, item in low_stock_items.iterrows():
           print(f"⚠️ LOW STOCK: {item['Product Name']} (only {item['Stock']} left)")
# VIEW PRODUCTS FUNCTON STOP



# ADD PRODUCTS TO CART FUNCTION START
def add_cart_products():
    print(' ✅ Ok Sir You Want To Add Products To Cart')
    view_products()
    print('Slect The Product That you Want To Add The Cart ')

    while True : 

      cart_add_product_name = input('Enter The Product Name : ').capitalize()
      cart_add_product_stock = int(input('Enter The Product Quantity : '))
      
          
      with open('cart.json' , 'r') as file:
        cart = json.load(file)

      with open('products.json' , 'r') as file:
        customer_menu = json.load(file)
          
      if(cart_add_product_name in customer_menu['products']):
         index = customer_menu["products"].index(cart_add_product_name)
         cart_add_product_price = customer_menu['prices'][index]

         if(cart_add_product_stock < customer_menu["Stock"][index]):

            cart[cart_add_product_name] = {'product' : cart_add_product_name,
                                           'prices' : cart_add_product_price,
                                           'stock' : cart_add_product_stock}
            
            with open('cart.json', 'w') as file:
              json.dump(cart, file)
             
            print(' ✅ Your Product Add Successfully In The Cart')

         else:
            print(" ❌ Sorry Sir We Have Not Enough Avaialable Quantity")



      back_menu_option = input('Add More Products (Yes or No) : ')
      

      if(back_menu_option == 'yes'):
        continue
      elif(back_menu_option == 'no'):
          break
              
      else:
          print(' ❌ Invalid Product Name')
# ADD PRODUCTS TO CART FUNCTION STOP



# REMOVE PRODUCTS FROM CART FUNCTION START
def remove_cart_products():
   
   print(' ✅ Ok Sir You Want To Remove Products From Cart')
   cart_remove_product_name = input('Enter The Product Name : ').capitalize()
        
   with open('cart.json' , 'r') as file:
     cart = json.load(file)
          
   if(cart_remove_product_name in cart):

    del cart[cart_remove_product_name]
    
   with open('cart.json', 'w') as file:
      json.dump(cart, file)

   print(' ✅ Your Product Successfully Remove From Cart')
# REMOVE PRODUCTS FROM CART FUNCTION STOP



# CHECKOUT FUNCTION START
def checkout():
          print("\n=== CHECKOUT ===")
          
          # Step 1: Load cart
          try:
              with open('cart.json', 'r') as file:
                  cart = json.load(file)
          except FileNotFoundError:
              cart = {}
          
          # Step 2: Check if cart is empty
          if not cart:
              print("🛒 Your cart is empty! Cannot checkout.")
              return
          
          # Step 3: Load products to update stock
          try:
              with open('products.json', 'r') as file:
                  products = json.load(file)
          except FileNotFoundError:
              print("❌ Products file not found!")
              return
          
          # Step 4: Load existing orders
          try:
              with open('orders.json', 'r') as file:
                  orders = json.load(file)
          except FileNotFoundError:
              orders = []
          
          # Step 5: Calculate totals and prepare order items
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
          
          # Step 6: Calculate tax and discount
          tax = subtotal * 0.10  # 10% tax
          
          if subtotal > 500:
              discount = subtotal * 0.05  # 5% discount
          else:
              discount = 0
          
          total = subtotal + tax - discount
          
          # Step 7: Update product stock
          for product_name, item in cart.items():
              if product_name in products['products']:
                  index = products['products'].index(product_name)
                  current_stock = products['Stock'][index]
                  bought_quantity = item['stock']
                  
                  # Subtract bought quantity from stock
                  products['Stock'][index] = current_stock - bought_quantity
          
          # Step 8: Save updated products
          with open('products.json', 'w') as file:
              json.dump(products, file, indent=4)
          
          # Step 9: Create new order
          new_order = {
              "order_id": len(orders) + 1,
              "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "items": order_items,
              "subtotal": subtotal,
              "tax": tax,
              "discount": discount,
              "total": total
          }
          
          # Step 10: Save order to history
          order_id = len(orders) + 1
          orders[order_id] = new_order

          # orders.append(new_order)
          with open('orders.json', 'w') as file:
              json.dump(orders, file, indent=4)
          
          # Step 11: Clear the cart
          with open('cart.json', 'w') as file:
              json.dump({}, file)
          
          # Step 12: Print receipt
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
    with open('products.json' , 'r') as file:
      products = json.load(file)
          # Step 13: Show low stock warning
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
            
            # Fix: Convert dictionary to list if needed
            if isinstance(orders, dict):
                # Convert {"1": {...}, "2": {...}} to [{...}, {...}]
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

                            # FUNCTIONS CODE STOP

while True :
 

  print('✅ === MAIN MENU === ✅')
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

  user_option = int(input("Enter The Your Choice : "))
  


    # Admin Features Code Start
  if(user_option == 1):
      #  Login Code Start  
   print(' ✅ Ok Sir You Want To Login The Account ')
   login_username = input('Enter The Username : ')
   login_email = input('Enter The Email ')
   login_password = input('Enter The Password : ')

  #  with open('login_details.json', 'w') as file:
  #   json.dump(personal_detail, file)

   if(login_username in personal_detail and
      login_email == personal_detail[login_username]['email'] and
      login_password == personal_detail[login_username]['password']):
    print(' ✅ Login Successful ')
        #  Login Code End 


    while True :


      #  Admin Menu Code Start
      print('✅ === ADMIN MENU === ✅')
      print('1 : Add Products') 
      print('2 : Remove Products')
      print('3 : Update Products Price')
      print('4 : Update Stock')
      print('5 : Exit As Admin')
      admin_input = int(input('Enter The Choice Number : '))
        #  Admin Menu Code Stop



     # Admin Add Products Code Start 
      if(admin_input == 1):
     
       print(' ✅ Ok Sir You Want To Add The Products ')
       admin_product_name = input('Enter The Product Name : ').capitalize()
       admin_product_price = int(input('Enter The Product Price : '))
       admin_product_stock = int(input('Enter The Product Stock : '))
  
       with open('products.json' , 'r')as file:
        customer_menu = json.load(file)

       customer_menu["products"].append(admin_product_name)
       customer_menu["prices"].append(admin_product_price)
       customer_menu["Stock"].append(admin_product_stock)
    
       with open('products.json', 'w') as file:
        json.dump(customer_menu, file)

       print(' ✅ Your Product Add Successfully')

        # Admin Add Products Code Stop
 

        # Admin Remove Products Code Start 
      if(admin_input == 2):
       print(' ✅ Ok Sir You Want To Remove The Products ')
       admin_remove_product_name = input('Enter The Product Name : ').lower() 

       with open('products.json' , 'r')as file:
        customer_menu = json.load(file)

       if(admin_remove_product_name in customer_menu['products']):

        index = customer_menu["products"].index(admin_remove_product_name)
     
        customer_menu["products"].pop(index)
        customer_menu["prices"].pop(index)
        customer_menu["Stock"].pop(index)
     
        with open('products.json', 'w') as file:
         json.dump(customer_menu, file)

         print(' ✅ Your Product Remove Successfully')
       else:
         print(' ❌ Sorry Sir Your Product Is Already Not Present In Our Database')
        # Admin Remove Products Code Stop 
      
        
        # Admin Update Products Price Code Start
      if(admin_input == 3):
         print(' ✅ Ok Sir You Want To Update The Products Price')
         admin_update_product_name = input('Enter The Product Name : ').capitalize()
         admin_update_product_price = int(input('Enter The Product Price : '))
           
         with open('products.json' , 'r')as file:
           customer_menu = json.load(file)

         if(admin_update_product_name in customer_menu['products']):
        
          index = customer_menu["products"].index(admin_update_product_name)
          customer_menu["prices"][index] = admin_update_product_price

          with open('products.json', 'w') as file:
           json.dump(customer_menu, file)

           print(' ✅ Your Product Price Update Successfully')
         else:
          print('❌ Invalid Product Name')
        # Admin Update Products Price Code Stop
         

        # Admin Update Products Stock Code Start
      if(admin_input == 4):
         print(' ✅ Ok Sir You Want To Update The Products Stock')
         admin_update_product_stock_name = input('Enter The Product Name : ').capitalize()
         admin_update_product_stock_price = int(input('Enter The Product Stock : '))
         
         with open('products.json' , 'r')as file:
           customer_menu = json.load(file)

         if(admin_update_product_stock_name in customer_menu['products']):
        
          index = customer_menu["products"].index(admin_update_product_stock_name)
          customer_menu["Stock"][index] = admin_update_product_stock_price

          with open('products.json', 'w') as file:
           json.dump(customer_menu, file)

           print(' ✅ Your Product Stock Update Successfully')
         else:
          print('❌ Invalid Product Name')
        # Admin Update Products Stock Code Stop
           

        # Admin Exit Code Start
      if(admin_input == 5):
        print(' ✅ We Exit You From As Admin')
        break
        # Admin Exit Code Stop


      #  Main If Condition is this under else
   else:
    print(' ❌ Invalid Email , Username or password')
            # Admin Features Code Stop




              # Customer Features Code Start 
  elif(user_option == 2):
   print(' ✅ WellCome Sir To Our Customer Menu ')
   
   while True :

      print('✅ === CUSTOMER MENU === ✅')
      print('1 : View All Products')
      print('2 : Search Products By Name')
      print('3 : Sort Products  (Low To High Price)')
      print('4 : Sort Products  (High To Low Price)')
      print('5 : Add Products To Cart')
      print('6 : Remove Products From Cart')
      print('7 : View My Cart')
      print('8 : Checkout')
      print('9 : View My order History')
      print('10 : Back To Main Menu')
   
      customer_option = int(input('Enter The Your Choice : '))



        #  Customer View Products Code Start
      if(customer_option == 1):
        print(' ✅ Ok Sir You Want To See The All Products ')
        view_products()
        #  Customer View Products Code Stop
         


        #  Customer Search Products By Name Code Start
      elif(customer_option == 2):
        print(' ✅ Ok Sir You Want To Search Products ')
        search_product_name = input('Search The Product Name : ').capitalize()
        
        with open('products.json' , 'r')as file:
         customer_menu = json.load(file)
   
        if(search_product_name in customer_menu['products']):
          print(' ✅ Yes Your Product Is Available On Our Store ')
          
          index = customer_menu["products"].index(search_product_name)

          print(f'The Product Name is {search_product_name}')
          print(f"The Product Price is Rs{customer_menu['prices'][index]}")
          print(f'The Product Stock is {customer_menu['Stock'][index]}')
        else:
         print(' ❌ Sorry Sir Your Product Is Not Available On Our Store')
        #  Customer Search Products By Name Code start



      #  Sort Products Code (Low To High) Code Start
      elif(customer_option == 3):
        print(' ✅ Ok Sir You Want To Sort Products (Low To High Price) ')
       
        with open('products.json' , 'r')as file:
         customer_menu = json.load(file)

        df = pd.DataFrame({
                 "Product": customer_menu["products"],
                 "Price": customer_menu["prices"],
                 "Stock": customer_menu["Stock"]
                         })

           # Sort by Price (Low to High)
        df_sorted = df.sort_values(by="Price", ascending=True)

            # Display
        print("=== Products Sorted by Price (Low to High) ===")
        print(df_sorted.to_string(index=False))
      #  Sort Products Code (Low To High) Code Stop



      #  Sort Products Code (High To Low) Code Start
      elif(customer_option == 4):
          print(' ✅ Ok Sir You Want To Sort Products (High To Low Price) ')
       
          with open('products.json' , 'r')as file:
           customer_menu = json.load(file)

          df = pd.DataFrame({
                 "Product": customer_menu["products"],
                 "Price": customer_menu["prices"],
                 "Stock": customer_menu["Stock"]
                         })

           # Sort by Price (Low to High)
          df_sorted = df.sort_values(by="Price", ascending=False)

            # Display
          print("=== Products Sorted by Price (High To Low) ===")
          print(df_sorted.to_string(index=False))
      #  Sort Products Code (High To Low) Code Stop




      #  Add Products To The Cart Code  Start
      elif(customer_option == 5):
          add_cart_products()
      #  Add Products To The Cart Code Stop
          


      #  Remove Products From The Cart Code  Start
      elif(customer_option == 6):
          remove_cart_products()
      #  Remove Products From The Cart Code  Stop


      # Customer Features View Cart Code Start 
      elif(customer_option == 7):
          print(' ✅ Ok Sir You Want To View Your Cart')
          print('✅ === YOUR CART === ✅')
          
          with open('cart.json' , 'r') as file:
           cart = json.load(file)

          cart_df = pd.DataFrame([
        {
            "ID ": i + 1,
            "Product Name": product_name,
            "Price ": "Rs" + str(item["prices"]),
            "Quantity ": item["stock"],
            "Total ": "Rs" + str(item["prices"] * item["stock"])
        }
        for i, (product_name, item) in enumerate(cart.items())
    ])
          print(cart_df.to_string())
      # Customer Features View Cart Code Stop



        # Checkouts Code Start
      elif(customer_option == 8):
        checkout()
        stock_warning()
        #  Checkouts Cod Stop
  



          #  Customer Order History Code Start
      elif(customer_option == 9):
          print(' ✅ Ok Sir You Want To View Orders History')
          view_order_history()  
          # Step 4: Show grand total of all orders
          grand_total = sum(order['total'] for order in orders)
          print(f"\n💰 GRAND TOTAL OF ALL ORDERS: ${grand_total}")
          print(f"📊 TOTAL ORDERS PLACED: {len(orders)}")
          #  Customer Order History Code Start


      # exit Customer Menu Code Start
      elif(customer_option == 10):
       print('Back To Main Menu')
       break
      # exit Customer Menu Code Stop
       # Customer Features Code Stop






  elif(user_option == 3):
       print(' ✅ Ok Sir You Want To See The All Products ')
       view_products()



  elif(user_option == 4):
          add_cart_products()
     

  
  elif(user_option == 5):
          remove_cart_products()
  


  elif(user_option == 6):
         checkout()
         stock_warning()
         
  
  elif(user_option == 7):
        print(' ✅ Ok Sir You Want To See Order History ')
        view_order_history()  
        # Step 4: Show grand total of all orders
        grand_total = sum(order['total'] for order in orders)
        print(f"\n💰 GRAND TOTAL OF ALL ORDERS: ${grand_total}")
        print(f"📊 TOTAL ORDERS PLACED: {len(orders)}")
        


  
  elif(user_option == 8):
   print(' ✅ Ok Sir You Want To Save All The Data ')
   
   def save_data():
    print("\n=== SAVE DATA ===")
    
    try:
        # Save products
        with open('products.json', 'r') as file:
            products = json.load(file)
        with open('products.json', 'w') as file:
            json.dump(products, file, indent=4)
        print("✅ Products saved successfully!")
        
    except FileNotFoundError:
        print("❌ No products file to save!")
    
    try:
        # Save cart
        with open('cart.json', 'r') as file:
            cart = json.load(file)
        with open('cart.json', 'w') as file:
            json.dump(cart, file, indent=4)
        print("✅ Cart saved successfully!")
        
    except FileNotFoundError:
        print("❌ No cart file to save!")
    
    try:
        # Save orders
        with open('orders.json', 'r') as file:
            orders = json.load(file)
        with open('orders.json', 'w') as file:
            json.dump(orders, file, indent=4)
        print("✅ Orders saved successfully!")
        
    except FileNotFoundError:
        print("❌ No orders file to save!")
    
    print("\n📁 All data saved to JSON files!")
  
   save_data()




  elif(user_option == 9):
   print(' ✅ Ok Sir You Want To Load The Data ')
   def load_data():
    print("\n=== LOAD DATA ===")
    
    global products,orders,cart

    # Load products
    try:
        with open('products.json', 'r') as file:
          products = json.load(file)
        print("✅ Products loaded successfully!")
    except FileNotFoundError:
         print("❌ No products.json file found! Starting with empty products.")
         products = {"products": [], "prices": [], "Stock": []}
    except json.JSONDecodeError:
        print("❌ products.json is corrupted! Starting with empty products.")
        products = {"products": [], "prices": [], "Stock": []}
    
    # Load cart
    try:
        with open('cart.json', 'r') as file:
            cart = json.load(file)
        print("✅ Cart loaded successfully!")
    except FileNotFoundError:
        print("❌ No cart.json file found! Starting with empty cart.")
        cart = {}
    except json.JSONDecodeError:
        print("❌ cart.json is corrupted! Starting with empty cart.")
        cart = {}
    
    # Load orders
    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
        print("✅ Orders loaded successfully!")
    except FileNotFoundError:
        print("❌ No orders.json file found! Starting with empty orders.")
        orders = []
    except json.JSONDecodeError:
        print("❌ orders.json is corrupted! Starting with empty orders.")
        orders = []
    
    print("\n📂 All data loaded from JSON files!")
   load_data()
  
  elif(user_option == 10):
   print(' ✅ Ok Sir You Want To Exit From Our Store ')
   break