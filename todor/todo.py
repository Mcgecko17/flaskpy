from flask import Blueprint, render_template, request, redirect, url_for
from .models import Inventario
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/index')
def index():
    nombre = request.args.get('nombre')
    codigo = request.args.get('codigo')
    
    query = Inventario.query
    
    if nombre:
        query = query.filter(Inventario.nombre.ilike(f'%{nombre}%'))
    if codigo:
        query = query.filter(Inventario.codigo.ilike(f'%{codigo}%'))
    
    todos = query.all()
    return render_template('todo/index.html', todos=todos)


@bp.route('/add', methods=['GET', 'POST'], endpoint='add_todo')
def add_todo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo = request.form['codigo']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        
        new_todo = Inventario(nombre=nombre, codigo=codigo, cantidad=cantidad, precio=precio)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    
    return render_template('todo/add.html')
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = Inventario.query.get_or_404(id)
    if request.method == 'POST':
        todo.nombre = request.form['nombre']
        todo.codigo = request.form['codigo']
        todo.cantidad = request.form['cantidad']
        todo.precio = request.form['precio']
        
        db.session.commit()
        return redirect(url_for('todo.index'))
    
    return render_template('todo/update.html', todo=todo)

@bp.route('/delete/<int:id>')
def delete(id):
    todo = Inventario.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))