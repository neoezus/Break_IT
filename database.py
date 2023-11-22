import mysql.connector
from datetime import datetime


def connect_to_database():
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='breaker'
    )
    return connection


def send_score_to_website(pseudo, score):

    connection = connect_to_database()
    cursor = connection.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = "INSERT INTO result (pseudo, score, created) VALUES (%s, %s, %s)"
    data = (pseudo, score, current_time)
    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()


def get_top_scores(limit=10):

    connection = connect_to_database()
    cursor = connection.cursor()
    query = "SELECT pseudo, score, created FROM result ORDER BY score DESC LIMIT %s"
    data = (limit,)
    cursor.execute(query, data)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
