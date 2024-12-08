from flask import Blueprint, render_template, request
from database.sql_provider import SQLProvider
from database.connection import DBContextManager, db_config
from access.control import group_required
from datetime import datetime


report_app = Blueprint('report_app', __name__, template_folder = "templates")
sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)


@report_app.route('/')
@group_required
def report():
    return render_template('report-menu.html')


@report_app.route('/create', methods=['GET', 'POST'])
@group_required
def report_create():
    if request.method == 'GET':
        return render_template('report-create.html', title="Введите параметры")
    else:
        with database as cursor:
            if (cursor):
                product_name = request.form.get('product_name')
                sql_code = sql_provider.get_sql('get_product_id.sql', {'product': product_name})
                rows_count = cursor.execute(sql_code)
                if (rows_count):
                    product = cursor.fetchone()
                    product_id = product['product_id']

                    year = request.form.get('year')
                    try:
                        year = int(year)
                    except:
                        ValueError
                        return render_template('report-create.html', title="Ошибка в дате")
                    if (year < 2000 or year > 2023):
                        return render_template('report-create.html', title="Ошибка в дате")
                    
                    month = request.form.get('month')
                    try:
                        month = int(month)
                    except:
                        ValueError
                        return render_template('report-create.html', title="Ошибка в дате")
                    if (month < 1 or month > 12):
                        return render_template('report-create.html', title="Ошибка в дате")
                    
                    sql_code = sql_provider.get_sql('check_report.sql', {'product': product_id, 'year': year, 'month': month})
                    rows_count = cursor.execute(sql_code)
                    if (rows_count):
                        return render_template('report-create.html', title="Данный отчет уже существует")
                    else:
                        sql_code = sql_provider.get_sql('check_sell.sql', {'product': product_id, 'year': year, 'month': month})
                        rows_count = cursor.execute(sql_code)
                        if (rows_count):
                            cursor.callproc('create_report', [product_id, year, month])
                            return render_template('report-create.html', title="Отчет успешно создан")
                        else:
                            return render_template('report-create.html', title="Продукт не продавался в указанный период")
                else:
                    return render_template('report-create.html', title="Нет такого продукта")
            else:
                raise ValueError("ERROR. CURSOR NOT CREATED!")


@report_app.route('/check', methods=['GET', 'POST'])
@group_required
def check_reports():
    if (request.method == 'POST'):
        with database as cursor:
            if (cursor):
                product_name = request.form.get('product_name')
                sql_code = sql_provider.get_sql('get_product_id.sql', {'product': product_name})
                rows_count = cursor.execute(sql_code)
                if (rows_count):
                    product = cursor.fetchone()
                    product_id = product['product_id']

                    year = request.form.get('year')
                    try:
                        year = int(year)
                    except:
                        ValueError
                        return render_template('report-create.html', title="Ошибка в дате")
                    if (year < 2000 or year > datetime.now().year):
                        return render_template('report-create.html', title="Ошибка в дате")
                    
                    month = request.form.get('month')
                    try:
                        month = int(month)
                    except:
                        ValueError
                        return render_template('report-create.html', title="Ошибка в дате")
                    if (month < 1 or month > 12):
                        return render_template('report-create.html', title="Ошибка в дате")
                    
                    sql_code = sql_provider.get_sql('get_report.sql', {'product': product_id, 'year': year, 'month': month})
                    rows_count = cursor.execute(sql_code)
                    report_info = cursor.fetchone()
                    if (rows_count):
                        return render_template('report-create.html', title="Введите параметры", report=report_info, product_name=product_name)
                    else:
                        return render_template('report-create.html', title="Отчета не найдено")
                else:
                    return render_template('report-create.html', title="Нет такого продукта")
            else:
                raise ValueError("ERROR. CURSOR NOT CREATED!")
    return render_template('report-create.html',  title="Введите параметры")