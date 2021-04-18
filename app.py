from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, current_user, logout_user, login_user, UserMixin 
from forms import LoginForm, SignupForm, VoluntierRegistrationForm, MessgeForm
from app_config import app
from modals import db, User, Role, UserRole, Voluntier, Message
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime, timedelta
import stripe
from stripe_pay import init_strip, get_publishable_key

# Login
login_manager = LoginManager()
login_manager.init_app(app)

# Stripe Init
stripe_keys = init_strip()

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/', methods=['GET', 'POST'])
def index():
    stripe_config = get_publishable_key(stripe_keys)
    return render_template("index.html", current_user = current_user, stripe_config=stripe_config)

@app.route('/contributors', methods=['GET'])
def contributors():
    voluntiers = Voluntier.query.all()
    return render_template("contributors.html", voluntiers=voluntiers)

@app.route("/voluntiers-map", methods=["GET", "POST"])
def voluntiers_map():
    key = os.environ['MAP_KEY']
    voluntiers = Voluntier.query.all()
    
    # Message Voluntier:
    form = MessgeForm()

    if form.validate_on_submit():

        # Just Testing stuffs
        if not current_user.is_authenticated:
            vol_id = request.form.get("voluntier")
            msg = request.form.get("message")

            voluntier = Voluntier.query.filter_by(id=vol_id).first()

            if voluntier:
                new_msg = Message(msg, voluntier)
                db.session.add(new_msg)
                db.session.commit()
    
    return render_template("map.html", key=key, voluntiers=voluntiers, form=form)

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='inr',
        description='Flask Charge'
    )
    return render_template('charge.html', amount=amount)


@app.route('/voluntier-register', methods=["GET", "POST"])
def voluntier_register():
    form = VoluntierRegistrationForm()
    
    if current_user.is_authenticated:
        # Already Logged In
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # Get all data from html
        name = request.form.get("name").title()
        mob = request.form.get("mob")
        email = request.form.get("email")
        quallifaications = request.form.get("quallifaications").title()
        state = request.form.get("state").title()
        district = request.form.get("district").title()
        bio = request.form.get("bio").title()
        gov_doc = request.files["gov_doc"]
        
        filename = secure_filename(gov_doc.filename)
        gov_doc.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        password = request.form.get("password")

        voluntier = Voluntier.query.filter_by(email=email).first()
        if voluntier:
            flash("User Already Exist")
        else:
            new_voluntier = Voluntier(name, email, mob, state, district, bio, filename, quallifaications, password)
            # Assign role
            role = Role.query.filter_by(name="Voluntier").first()
            if not role:
                role = Role(name='Voluntier')
            new_voluntier.role = [role,]
            db.session.add(new_voluntier)
            db.session.commit()            
            return redirect(url_for('login'))
    return render_template("voluntier_registration.html", form=form)


# User Management
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        flash("Already Login")
        return redirect(url_for("index"))

    # Get Data from the html
    if form.validate_on_submit():
        user = User.query.filter_by(email=request.form.get("username")).first()
        
        if not user:
            flash("Invalid Username")
        elif user.verify_password(request.form.get("password")):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Incorrect Username or Password")

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        # Already Logged In
        return redirect(url_for('index'))

    form = SignupForm()
    if form.validate_on_submit():
        # Get all data from html
        username = request.form.get("username")
        address = request.form.get("address")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User Already Exist")
        else:
            new_user = User(username, address, password, email)
            # Assign role
            role = Role.query.filter_by(name="User").first()
            if not role:
                role = Role(name='User')
            new_user.role = [role,]

            db.session.add(new_user)
            db.session.commit()            
            return redirect(url_for('login'))
    return render_template("signup.html", form=form)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out!")
        return redirect(url_for("index"))
    flash("Not Logged In")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)