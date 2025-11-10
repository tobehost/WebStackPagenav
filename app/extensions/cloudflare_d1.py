# Cloudflare D1 数据库扩展
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_d1(app):
    """初始化 Cloudflare D1 数据库连接"""
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get('CLOUDFLARE_D1_DATABASE_URI')
    db.init_app(app)

    with app.app_context():
        db.create_all()

        return db
    return None

def get_d1_connection():
    return db.engine.raw_connection()

def get_d1_cursor():
    connection = get_d1_connection()
    cursor = connection.cursor()
    return cursor

def close_d1_connection():
    connection = get_d1_connection()
    connection.close()
    return True

def rollback_d1_transaction():
    connection = get_d1_connection()
    connection.rollback()
    return True

def commit_d1_transaction():
    connection = get_d1_connection()
    connection.commit()
    return True

def execute_d1_query(query, params=None):
    cursor = get_d1_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    return cursor.fetchall()

def execute_d1_non_query(query, params=None):
    cursor = get_d1_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    commit_d1_transaction()
    return cursor.rowcount

def close_d1_cursor():
    cursor = get_d1_cursor()
    cursor.close()
    return True

def d1_query_to_dicts(query, params=None):
    cursor = get_d1_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    close_d1_cursor()
    return results

def d1_query_single_row(query, params=None):
    cursor = get_d1_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    row = cursor.fetchone()
    if row:
        columns = [col[0] for col in cursor.description]
        result = dict(zip(columns, row))
    else:
        result = None
    close_d1_cursor()
    return result

def d1_query_scalar(query, params=None):
    cursor = get_d1_cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    row = cursor.fetchone()
    if row:
        result = row[0]
    else:
        result = None
    close_d1_cursor()
    return result

def d1_close():
    close_d1_connection()
    return True

