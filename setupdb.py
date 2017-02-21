import urlparse

import mysql.connector

def create_db_conn():
    try:
        db_conn = mysql.connector.connect(user='root', password='root',
                                                host='localhost',
                                                database='ScrapeProject')
        return db_conn

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        db_conn.close()

    else:
        db_conn.close()

    return None


if __name__ == '__main__':
    db_conn = create_db_conn()
    cursor = db_conn.cursor()
    query = ("CREATE TABLE IF NOT EXISTS tbl_Proxies ("
                "  `id` INT AUTO_INCREMENT PRIMARY KEY,"
                "  `IP` CHAR(16) NOT NULL,"
                "  `Port` INT NOT NULL)")
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        print(err.msg)

    with open('proxies.txt', 'r') as f:
        for line in f:
            print("Line: {}".format(line))
            parsed_url = urlparse.urlparse(line)
            print("Parsed: {}:{}".format(parsed_url.hostname, parsed_url.port))
            insert_query = ("INSERT INTO tbl_Proxies (IP, Port)"
                            "  VALUES (%s, %s)")
            cursor.execute(insert_query, (parsed_url.hostname, parsed_url.port))

    db_conn.commit()
    cursor.close()
    db_conn.close()
