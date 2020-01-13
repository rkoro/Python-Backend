#!/usr/bin/python3
import psycopg2
import psycopg2.extras
import sys

conn = None
def connect(host, database, user, password):
    global conn
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        cursor_factory=psycopg2.extras.NamedTupleCursor
    )

def close():
    global conn
    conn.close()
    conn = None

def sql_in(column, values):
    if len(values) == 0:
        return "1 = 0"
    values = list(map(lambda v: "E'" + str(v) + "'", values))
    return "%s IN(%s)" % (column, ",".join(values))

def delete(table, filter="1 = 0", args = []):
    global conn
    sql_string = "DELETE FROM {} WHERE {}".format(table, filter)
    cur = conn.cursor()
    cur.execute(sql_string, args)
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()
    return rows_deleted

def update(table, key_columns, values):
    global conn
    if not isinstance(values, list):
        (sql_string, args) = _update_row_sql(table, key_columns, values)
    else:
        (sql_string, args) = _update_massive_sql(table, key_columns, values)
    cur = conn.cursor()
    cur.execute(sql_string, args)
    rows_updated = cur.rowcount
    conn.commit()
    cur.close()
    return rows_updated

def _update_row_sql(table, key_columns, value):
    key_columns_hash = {}
    where = []
    args = []
    for key_column in key_columns:
        key_columns_hash[key_column] = 1
        where.append("{}=%s".format(key_column))
        args.append(value[key_column])
    where_sql = " AND ".join(where)

    values = []
    for key in filter(lambda x: x not in key_columns_hash, value.keys()):
        values.append("{}='{}'".format(key, value[key]))
    values_sql = ",".join(values)

    sql_string = "UPDATE {} SET {} WHERE {}".format(table, values_sql, where_sql)
    return (sql_string, args)

def _update_massive_sql(table, key_columns, values):
    return ("", [])

def insert(table, values):
    global conn
    is_massive = True
    if not isinstance(values, list):
        values = [values]
        is_massive = False
    value_row_strings = []
    keys = values[0].keys()
    keys_string = '(' + ','.join(keys) + ')'

    for values_row in values:
        row_values = list(map(lambda k: "E\'" + str(values_row[k]) + "\'", keys))
        value_row_strings.append('(' + ",".join(row_values) + ')')
    values_string = ','.join(value_row_strings)

    sql_string = "INSERT INTO %s%s VALUES%s RETURNING id" % (table, keys_string, values_string)
    cur = conn.cursor()
    cur.execute(sql_string)
    conn.commit()
    ids = cur.fetchall()
    cur.close()
    if is_massive:
        return list(map(lambda x: x.id, ids))
    else:
        return ids[0].id

def fetch(table, fields = '*', filter = None, args=[], sort = None):
    global conn
    where = ""
    orderby = ""
    if filter is not None:
        where = "WHERE " + filter
    if sort is not None:
        orderby = "ORDER BY " + sort

    sql_string = "SELECT %s FROM %s %s %s" % (fields, table, where, orderby)
    cur = conn.cursor()
    cur.execute(sql_string, args)
    data = cur.fetchall()
    cur.close()
    return list(map(lambda x: dict(x._asdict()), data))

def fetch_one(table, fields = '*', filter = None, args=()):
    rows = fetch(table, fields, filter, args)
    if len(rows) == 0:
        return None
    elif len(rows) == 1:
        return rows[0]
    else:
        print("fetch_one returned more than 1 row. Arguments: ", table, fields, filter, args, "<br>")
        print("fetch_one returned more than 1 row. Arguments: ", table, fields, filter, args, file=sys.stderr)
        return None