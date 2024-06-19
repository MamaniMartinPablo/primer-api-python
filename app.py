from flask import Flask ,jsonify ,request
from flask_cors import CORS       
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from decouple import config

app=Flask(__name__) 
CORS(app) 


# configuracion
driver = config('DRIVER')
usuario = config('USUARIO')
contrasenia = config('CONTRASENIA')
dominio = config('DOMINIO')
nombreBD = config('NOMBRE_DE_BD')

app.config['SQLALCHEMY_DATABASE_URI']=f'{driver}://{usuario}:{contrasenia}@{dominio}/{nombreBD}'                       
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db= SQLAlchemy(app) 
ma=Marshmallow(app)



# defino una tabla
class Producto(db.Model):    
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    
    def __init__(self,nombre,precio,stock,imagen):
        self.nombre=nombre
        self.precio=precio
        self.stock=stock
        self.imagen=imagen



with app.app_context():
    db.create_all()


class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')


producto_schema=ProductoSchema() 
productos_schema=ProductoSchema(many=True)




# rutas


@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all() 
    result=productos_schema.dump(all_productos)              
    return jsonify(result)    



@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    
    producto=Producto.query.get(id)
    
    return producto_schema.jsonify(producto) 


@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    
    producto=Producto.query.get(id)
    
    db.session.delete(producto)
    db.session.commit()                   
    return producto_schema.jsonify(producto)


@app.route('/productos', methods=['POST']) 
def create_producto():
   
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    
    new_producto=Producto(nombre,precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit() 
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    
    producto=Producto.query.get(id)
 
    producto.nombre=request.json['nombre']
    producto.precio=request.json['precio']
    producto.stock=request.json['stock']
    producto.imagen=request.json['imagen']

    db.session.commit()  
    return producto_schema.jsonify(producto)




# Servidor
if __name__=='__main__':  
    app.run(debug=True, port=5000)
