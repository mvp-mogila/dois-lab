from flask import Blueprint, render_template, request, session, redirect, url_for
from database.connection import DBContextManager, db_config
from database.sql_provider import SQLProvider
from access.control import login_required

basket_app = Blueprint('basket_app', __name__)
sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)


@basket_app.route('/', methods=['GET', 'POST'])
@login_required
def order_index():
    with database as cursor:
        if cursor:
            if request.method == 'GET':
                sql_code = sql_provider.get_sql('get_all_products.sql', dict())
                cursor.execute(sql_code)
                products = cursor.fetchall()
                basket_items = session.get('basket', {})
                return render_template('basket_order_list.html', items=products, basket=basket_items)
            else:
                prod_id = request.form.get('product_id')
                sql_code = sql_provider.get_sql('get_added_item.sql', {'product_id': prod_id})
                cursor.execute(sql_code)
                item = cursor.fetchone()
                add_to_basket(prod_id, item)
                return redirect(url_for('basket_app.order_index'))
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")



@basket_app.route('/')
@login_required
def add_to_basket(prod_id, item):
    session.permanent = True
    if prod_id in session.get('basket'):
        session['basket'][prod_id]['prod_amount'] += 1
    else:
        session['basket'][prod_id] = item
        session['basket'][prod_id]['prod_amount'] = 1


@basket_app.route('/clear')
@login_required
def clear_basket():
    session['basket'] = {}
    session.modified = True
    return redirect(url_for('basket_app.order_index'))


@basket_app.route('/submit_order')
@login_required
def register_order():
    database.conn.begin
    with database as cursor:
        user_login = session.get('user_login')
        sql_code = sql_provider.get_sql('get_user_id.sql', {'login': user_login})
        cursor.execute(sql_code)
        user_id = cursor.fetchone()['user_id']
        sql_code = sql_provider.get_sql('create_order.sql', {'user_id': user_id})
        cursor.execute(sql_code)
        sql_code = sql_provider.get_sql('last_inserted_order.sql', {'user_id': user_id})
        cursor.execute(sql_code)
        order_id = cursor.fetchone()['id']
        items = session.get('basket')
        for item in items.keys():
            params = {'order_id': order_id,
                      'product_id': items[item]['product_id'],
                      'quantity': items[item]['prod_amount'],
                      'cost': int(items[item]['product_price']) * int(items[item]['prod_amount'])}
            sql_code = sql_provider.get_sql('create_order_list.sql', params)
            cursor.execute(sql_code)
    database.conn.commit
    return redirect(url_for('basket_app.clear_basket'))
