from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from todor.models import User, Admin, Inventario  # Importación absoluta
from todor import db


bp = Blueprint('adm_bp', __name__, url_prefix='/adm')

# Configurar la cola RQ


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        admin = Admin.query.filter_by(username=username).first()
        if admin is None:
            error = 'Incorrect username.'
        elif not check_password_hash(admin.password, password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['admin_id'] = admin.id
            return redirect(url_for('adm_bp.approve_users'))
        flash(error)
    
    return render_template('adm/login.html')

@bp.route('/approve_users', methods=['GET', 'POST'])
def approve_users():
    if 'admin_id' not in session:
        return redirect(url_for('adm_bp.login'))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = User.query.get(user_id)
        user.is_approved = True
        db.session.commit()
        flash(f'User {user.username} approved.')
        return redirect(url_for('adm_bp.approve_users'))
    
    users = User.query.filter_by(is_approved=False).all()
    return render_template('adm/approve_users.html', users=users)



@bp.before_app_request
def load_logged_in_admin():
    admin_id = session.get('admin_id')

    if admin_id is None:
        g.admin = None
    else:
        g.admin = Admin.query.get(admin_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Decorador para requerir inicio de sesión de administrador
def require_admin(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('adm_bp.login'))
        return view(**kwargs)
    return wrapped_view