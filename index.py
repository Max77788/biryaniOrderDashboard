from flask import Flask, request, jsonify, render_template
import os
#from mongoengine import connect
from flask_mongoengine import MongoEngine
from models.models_mongo import Order, Item

app = Flask(__name__)

#connect(host = os.getenv("MONGODB_URI"))

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Set a secret key for security purposes
app.config['MONGODB_HOST'] = os.getenv("MONGODB_URI")
  
# use a database named "myDatabase"
db = MongoEngine(app)

order_number_counter = 2

@app.route('/', methods=['GET'])
def hi():
    return "Hello World"

@app.route('/orders', methods=['GET','POST'])
def add_order_record():
    
    global order_number_counter

    if request.method == 'POST':
        data = request.json
        items_data = data.get('items', [])  # Default to an empty list if not provided

        # Create Item instances for each item in the request
        items = [Item(name=item['name'], quantity=item['quantity']) for item in items_data]

        # Create a new Order instance and save it to the database
        order = Order(items=items, orderNumber=order_number_counter).save()  # Save the order and keep the reference
        
        order_number_counter += 1

        # Return the order ID and a success message
        return jsonify({
            'orderId': str(order.id),  # Convert ObjectId to string
            'message': 'Order record added successfully'
        })

    elif request.method == 'GET':
        # For a GET request, return a simple message
        return 'Send a POST request to submit an order.'


@app.route('/orders/view', methods=['GET'])
def view_orders():
    # Query all orders from the database
    orders = Order.objects.all()

    # Format orders for display
    orders_list = []
    for order in orders:
        # Assuming 'orderNumber' is already a string that represents the order ID
        # If 'orderNumber' is not defined in your Order model, you might want to use str(order.id)
        order_info = {
            'orderId': order.orderNumber,
            'foods': [{'name': item.name, 'quantity': item.quantity} for item in order.items]
        }
        orders_list.append(order_info)
        print(orders_list)

    # Render the HTML page with orders
    return render_template('orders.html', orders=orders_list)

    # For simplicity, return JSON representation of the orders
    #return jsonify(orders=orders_list)

@app.route('/privacy-policy', methods=['GET'])
def view_policy():
    return render_template('policy.html')

if __name__ == '__main__':
    app.run(debug=True)
