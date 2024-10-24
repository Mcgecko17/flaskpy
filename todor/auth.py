from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from todor.models import User  # Importación absoluta
from todor import db

bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
       
        
        user = User.query.filter_by(username=username).first()
        if user is None:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado con exito.')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('El usuario ya existe.')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'usuario incorrecto.'
        elif not check_password_hash(user.password, password):
            error = 'contraseña incorrecta.'
        elif not user.is_approved:
            error = 'tu cuenta todavia no esta activada.'
        
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Decorador para requerir inicio de sesión
def require_login(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)
    return wrapped_view