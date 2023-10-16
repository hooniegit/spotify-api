
# create mysql connector
def open_connector():
    import MySQLdb
    from configparser import ConfigParser
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(current_dir, f'../config/config.ini')

    config = ConfigParser()
    config.read(config_dir)

    host = config.get("MySQL", "host")
    user = config.get("MySQL", "user")
    passwd = config.get("MySQL", "passwd")
    database = config.get("MySQL", "database")

    conn = MySQLdb.connect(
    host=host,
    user=user,
    passwd=passwd,
    database=database
    )

    return conn


# execute query
def execute_query(conn, query, values:None):
    cursor = conn.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()


# fetchall query
# query = " ..(%s).. "
# values = ("data", )
def fetchall_query(conn, query, values=None):
    cursor = conn.cursor()
    if values != None:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    return result


# test
if __name__ == "__main__":
    # confirmed - 23.10.06
    conn = open_connector()
    query = "SELECT COUNT(*) FROM albums where insert_date = (%s)"
    values = ("2023-10-11",)
    result = fetchall_query(conn, query, values)
    print(result)