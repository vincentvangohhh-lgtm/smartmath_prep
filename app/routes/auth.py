from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User
import random
import re

# 1. KHỞI TẠO BLUEPRINT
auth_bp = Blueprint('auth', __name__)

# --- DECORATOR PHÂN QUYỀN GIÁO VIÊN & ADMIN ---
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = getattr(current_user, 'role', 'student')
        if not current_user.is_authenticated or user_role not in ['teacher', 'admin']:
            flash("Bạn không có quyền truy cập vào trang này!", "danger")
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTE ĐĂNG KÝ ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        # 🛡️ 1. KIỂM TRA MÃ XÁC MINH PHÉP TÍNH TOÁN HỌC
        user_input = request.form.get('captcha_input', '').strip()
        real_captcha = str(session.get('math_captcha_result', ''))

        if not user_input or user_input != real_captcha:
            flash('Mã xác minh phép tính không chính xác! Vui lòng tính lại.', 'danger')
            return redirect(url_for('auth.register'))

        username = request.form.get('username') or request.form.get('fullname') or request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        grade = request.form.get('grade')
        school = request.form.get('school')
        role = request.form.get('role', 'student')

        # 🛡️ 2. KIỂM TRA ĐIỀU KIỆN MẬT KHẨU BẢO MẬT
        if len(password) < 9:
            flash('Mật khẩu bảo mật phải có ít nhất 9 ký tự!', 'danger')
            return redirect(url_for('auth.register'))
            
        if not any(char.isdigit() for char in password):
            flash('Mật khẩu phải chứa ít nhất 1 chữ số!', 'danger')
            return redirect(url_for('auth.register'))
            
        # Kiểm tra ký tự đặc biệt (các ký tự không phải chữ cái và không phải số)
        if not any(not char.isalnum() for char in password):
            flash('Mật khẩu phải chứa ít nhất 1 ký tự đặc biệt (ví dụ: @, #, !, $, ...)!', 'danger')
            return redirect(url_for('auth.register'))

        if not username and email:
            username = email.split('@')[0]

        # 🛡️ 3. KIỂM TRA TRÙNG EMAIL
        user_exists_email = User.query.filter_by(email=email).first()
        if user_exists_email:
            flash('Email này đã được đăng ký sử dụng!', 'danger')
            return redirect(url_for('auth.register'))

        # 🛡️ 4. KIỂM TRA TRÙNG USERNAME
        user_exists_name = User.query.filter_by(username=username).first()
        if user_exists_name:
            flash('Tên người dùng (Username) này đã tồn tại, vui lòng chọn tên khác!', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(
            username=username, 
            email=email, 
            password=hashed_password,
            role=role,
            grade=grade,
            school=school
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Xóa session captcha sau khi đăng ký thành công
        session.pop('math_captcha_result', None)
        
        flash('Đăng ký tài khoản thành công! Hãy đăng nhập.', 'success')
        return redirect(url_for('auth.login'))

    # Sinh phép tính ngẫu nhiên cho form đăng ký (Cộng hoặc Trừ)
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 10)
    op = random.choice(['+', '-'])
    
    if op == '+':
        result = num1 + num2
        question = f"{num1} + {num2} = ?"
    else:
        if num1 < num2:
            num1, num2 = num2, num1
        result = num1 - num2
        question = f"{num1} - {num2} = ?"
        
    session['math_captcha_result'] = str(result)
    return render_template('auth/register.html', captcha_question=question)


# --- ROUTE ĐĂNG NHẬP ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user_role = getattr(current_user, 'role', 'student')
        if user_role in ['teacher', 'admin']:
            return redirect(url_for('main.teacher_dashboard'))
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Chào mừng {user.username} đã quay trở lại!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            user_role = getattr(user, 'role', 'student')
            if user_role in ['teacher', 'admin']:
                return redirect(url_for('main.teacher_dashboard'))
            
            return redirect(url_for('main.index'))
        else:
            flash('Tài khoản hoặc mật khẩu không chính xác.', 'danger')

    return render_template('auth/login.html')

# --- ROUTE ĐĂNG XUẤT ---
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất tài khoản.', 'info')
    return redirect(url_for('main.index'))