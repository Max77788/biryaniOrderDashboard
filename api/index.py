from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/orders/', methods=['GET','POST'])
def add_order_record():
    data = request.json
    order_number = data.get('orderNumber')
    items = data.get('items')
    
    # Process the data (e.g., store in a database)
    
    # For illustration, we'll just return the received order number and a message
    if items != None:
        return jsonify({
        'orderId': order_number,
        'message': 'Order record added successfully'
    })
    else:
        return "No orders to display"

if __name__ == '__main__':
    app.run(debug=True)
