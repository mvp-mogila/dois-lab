from flask import Blueprint, render_template, request
from database.sql_provider import SQLProvider
from database.connection import DBContextManager, db_config


catalog_app = Blueprint('catalog_app', __name__, template_folder = "templates")
sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)


@catalog_app.route('/')
def catalog_handler():
    return render_template('catalog.html')


@catalog_app.route('/name-filter', methods = ['GET'])
def name_search_handler():
    not_found = False
    with database as cursor:
        if cursor:
            name = request.args.get('product_name')
            params = {'name': name}
            sql_code = sql_provider.get_sql('get_product_by_name.sql', params)
            rows_count = cursor.execute(sql_code)
            result = cursor.fetchall()
            if (not rows_count):
                not_found = True
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('name-filter.html', rows_count = rows_count, searching_name = name, context = result, flag = not_found)


@catalog_app.route('/category-filter', methods = ['GET'])
def category_search_handler():
    not_found = False
    with database as cursor:
        if cursor:
            category = request.args.get('product_category')
            params = {'category': category}
            sql_code = sql_provider.get_sql('get_product_by_category.sql', params)
            rows_count = cursor.execute(sql_code)
            result = cursor.fetchall()
            if (not rows_count):
                not_found = True
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('category-filter.html', rows_count = rows_count, searching_category = category, context = result, flag = not_found)


@catalog_app.route('/price-filter', methods = ['GET'])
def price_search_handler():
    not_found = False
    with database as cursor:
        if cursor:
            price_lower = request.args.get('lower_bound')
            price_upper = request.args.get('upper_bound')
            if (price_lower and not price_upper):
                price_upper = 1000000
            elif (price_upper and not price_lower):
                price_lower = 1
            params = {'lower': price_lower, 'upper': price_upper}
            sql_code = sql_provider.get_sql('get_product_by_price.sql', params)
            rows_count = cursor.execute(sql_code)
            result = cursor.fetchall()
            if (not rows_count and price_lower and price_upper):
                    not_found = True
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('price-filter.html', rows_count = rows_count, context = result, flag = not_found)
