import sqlite3
import psycopg2

def remove_null_bytes(text):
    """NULL文字を削除する関数"""
    if isinstance(text, str):
        return text.replace('\x00', '')
    return text

# ローカルのSQLiteデータベースに接続
sqlite_conn = sqlite3.connect('onwut_data.db')
sqlite_cursor = sqlite_conn.cursor()

# HerokuのPostgreSQLデータベースに接続
heroku_conn = psycopg2.connect("postgres://udqo9u95b9ver2:p818daad9176bfa7f5c5cdd3e15d0993517d981a6cbbfa671f8399ccd3e80a2be@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7qbcmbmrj0c0b")
heroku_cursor = heroku_conn.cursor()

# Heroku上のデータベースにテーブルを作成（既に作成済みならスキップ）
heroku_cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        title TEXT,
        date TEXT,
        url TEXT,
        content TEXT,
        source TEXT
    );
''')

# SQLiteからデータを取得し、HerokuのPostgreSQLに挿入
sqlite_cursor.execute("SELECT title, date, url, content, source FROM reports")
rows = sqlite_cursor.fetchall()

for row in rows:
    cleaned_row = tuple(remove_null_bytes(value) for value in row)
    heroku_cursor.execute(
        "INSERT INTO reports (title, date, url, content, source) VALUES (%s, %s, %s, %s, %s)",
        cleaned_row
    )

# コミットして接続を閉じる
heroku_conn.commit()
heroku_conn.close()
sqlite_conn.close()
