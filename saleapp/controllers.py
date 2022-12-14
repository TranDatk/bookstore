from flask import render_template, request, redirect, session, jsonify
from saleapp import app, dao, utils
from flask_login import login_user, logout_user
from saleapp.decorator import annonynous_user
import cloudinary.uploader


def index():
    books = dao.load_books(category_id=request.args.get('category_id'),
                                 kw=request.args.get('keyword'))
    return render_template('index.html', books=books)


def details(book_id):
    b = dao.get_book_by_id(book_id)
    return render_template('details.html', book=b)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@annonynous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             password=password,
                             username=request.form['username'], avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


def cart():
    return render_template('cart.html')

def seller():
    return render_template('bookseller\index.html')

def add_to_cart():
    data = request.json

    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    id = str(data['id'])
    name = data['name']
    price = data['price']

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return \
        jsonify(utils.cart_stats(cart))


def update_cart(product_id):
    key = app.config['CART_KEY']

    cart = session.get(key)
    if cart and product_id in cart:
        cart[product_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(product_id):
    key = app.config['CART_KEY']

    cart = session.get(key)
    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    try:
        dao.add_receipt(cart=cart)
    except:
        return jsonify({'status': 500},cart)
    else:
        del session[key]
        return jsonify({'status': 200})



