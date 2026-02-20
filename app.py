from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import os

app = Flask(__name__)

# Конфигурация БД (Postgres)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Конфигурация Redis Кеша
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL')

db = SQLAlchemy(app)
cache = Cache(app)

# Модель данных
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

# CRUD Эндпоинты
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    cache.clear() # Очищаем кеш при изменении данных
    return jsonify({"id": new_item.id, "name": new_item.name}), 201

@app.route('/items', methods=['GET'])
@cache.cached(timeout=60) # Кешируем результат на 60 секунд
def get_items():
    items = Item.query.all()
    return jsonify([{"id": i.id, "name": i.name} for i in items])

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    db.session.get(Item, id)
    db.session.delete(item)
    db.session.commit()
    cache.clear()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0')
