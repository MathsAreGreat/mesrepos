import os
import json
from flask import Flask, request, render_template_string, redirect, url_for, flash, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME']
    )


UPLOAD_FORM = """
<!doctype html>
<title>Upload JSON</title>
<h1>Upload a JSON files !</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file accept=".json">
  <input type=submit value=Upload>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
"""


@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/fall', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Return rows as dicts

        cursor.execute(
            "SELECT * FROM shows")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.json'):
            flash("Please upload a valid JSON file.")
            return redirect(request.url)

        try:
            datas = json.load(file)

            if not isinstance(datas, list):
                datas = [datas]

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                id INT PRIMARY KEY,
                name VARCHAR(100),
                lang VARCHAR(100),
                status VARCHAR(100),
                rating VARCHAR(100),
                poster VARCHAR(255),
                summary TEXT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS episode (
                id INT PRIMARY KEY,
                show_id INT,
                ep_number INT,
                ss_number INT,
                name VARCHAR(100),
                aired VARCHAR(100),
                runtime INT,
                rating VARCHAR(100),
                poster VARCHAR(255),
                summary TEXT
            )
            """)

            show_query = """
            INSERT IGNORE INTO shows (
                id,
                name,
                lang,
                status,
                rating,
                poster,
                summary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            ep_query = """
            INSERT IGNORE INTO episode (
                id,
                show_id, 
                ep_number,
                ss_number,
                name,
                aired,
                runtime,
                rating,
                poster,
                summary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            show_dts = []
            ep_dts = []
            for data in datas:
                rated = None
                poster = None
                if data.get('rating'):
                    rated = data.get('rating').get('average')
                if data.get('image'):
                    poster = data.get('image').get('original')
                dd = (
                    data['id'],
                    data['name'],
                    data.get('language'),
                    data.get('status'),
                    rated,
                    poster,
                    data.get('summary')
                )
                show_dts.append(dd)
                for episode in data["_embedded"]["episodes"]:
                    rated = None
                    poster = None
                    if episode.get('rating'):
                        rated = episode.get('rating').get('average')
                    if episode.get('image'):
                        poster = episode.get('image').get('original')
                    dd = (
                        episode['id'],
                        data['id'],
                        episode['number'],

                        episode['season'],
                        episode['name'],
                        episode['airdate']+"_"+episode['airtime'],

                        episode['runtime'],
                        rated,
                        poster,
                        episode['summary']
                    )
                    ep_dts.append(dd)

            cursor.executemany(
                ep_query,
                ep_dts
            )

            cursor.executemany(
                show_query,
                show_dts
            )

            conn.commit()

            cursor.close()

            conn.close()

            flash("Data imported successfully.")
        except Exception as e:
            flash(f"Error: {str(e)}")

        return redirect(request.url)

    return render_template_string(UPLOAD_FORM)
