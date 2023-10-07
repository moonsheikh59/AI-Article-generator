from flask import Blueprint, render_template, request,flash,redirect, url_for,current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os 
auth = Blueprint('auth',__name__)

@auth.route("/login", methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.passward, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')

        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up" ,methods= ['GET','POST'])
def sign_up():

    if request.method == 'POST':
        email = request.form.get("email")
        fname = request.form.get("fname")
        user_image = request.files["user_img"]
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email)< 4:
            flash('Email Must be greater then 4 Characters', category = 'error')
        elif len(fname) < 2:
            flash('Name Must be greater then 2 Characters', category = 'error')
        elif password1 != password2:
            flash('Your password does not matched', category = 'error')
        elif len(password1) < 7:
            flash('Your password is too short', category = 'error')
        else:
            #add user to database
            new_user = User(email=email, fname=fname, passward= generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            # db.session.flush
            file_name = user_image.filename
            user_image.save(os.path.join(current_app.config["UPLOAD_FOLDER"],file_name))
            new_user.user_img = file_name
            
            db.session.commit()
            login_user(new_user, remember=True)
            flash('account created successfully', category = 'success')

            return redirect(url_for('views.home'))
            
    return render_template("signup.html",user=current_user) 