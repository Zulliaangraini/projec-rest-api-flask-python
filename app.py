from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Buat tabel jika belum ada
with app.app_context():
    db.create_all()

# API untuk mendapatkan semua produk
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price} for item in items])

# API untuk menambah produk
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data['name']
    description = data['description']
    price = data['price']
    
    new_item = Item(name=name, description=description, price=price)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Produk berhasil ditambahkan'}), 201

# API untuk memperbarui produk
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data['name']
    item.description = data['description']
    item.price = data['price']
    
    db.session.commit()
    return jsonify({'message': 'Produk berhasil diperbarui'})

# API untuk menghapus produk
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Produk berhasil dihapus'})

if __name__ == '__main__':
    app.run(debug=True)
