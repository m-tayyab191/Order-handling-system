from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

orders = []
logs = []

def log_action(action_type, performed_by):
    logs.append({
        'action_type': action_type,
        'performed_by': performed_by,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/')
def index():
    return render_template('index.html', orders=orders, logs=logs)

@app.route('/add', methods=['POST'])
def add_order():
    order = {
        'order_id': request.form['order_id'],
        'num_items': request.form['num_items'],
        'delivery_date': request.form['delivery_date'],
        'sender_name': request.form['sender_name'],
        'recipient_name': request.form['recipient_name'],
        'recipient_address': request.form['recipient_address'],
        'status': 'Ongoing'
    }
    orders.append(order)
    log_action(f"Created Order {order['order_id']}", request.form['sender_name'])
    return redirect(url_for('index'))

@app.route('/edit/<order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    if request.method == 'POST':
        order['num_items'] = request.form['num_items']
        order['delivery_date'] = request.form['delivery_date']
        order['sender_name'] = request.form['sender_name']
        order['recipient_name'] = request.form['recipient_name']
        order['recipient_address'] = request.form['recipient_address']
        log_action(f"Edited Order {order_id}", request.form['sender_name'])
        return redirect(url_for('index'))

    return render_template('edit_order.html', order=order)

@app.route('/delete/<order_id>')
def delete_order(order_id):
    global orders
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order:
        log_action(f"Deleted Order {order_id}", order['sender_name'])
        orders = [o for o in orders if o['order_id'] != order_id]
    return redirect(url_for('index'))

@app.route('/deliver/<order_id>')
def mark_delivered(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order:
        order['status'] = 'Delivered'
        log_action(f"Marked Delivered Order {order_id}", order['sender_name'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
