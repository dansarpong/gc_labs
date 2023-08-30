from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("birthdays.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
            id INTEGER PRIMARY KEY,
            name TEXT,
            month INTEGER,
            day INTEGER
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    create_table()  # Ensure the table exists
    
    if request.method == "POST":
        # Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        try:
            month = int(month)
            day = int(day)
        except:
            return redirect("/")

        if month > 0 and day > 0:
            conn = sqlite3.connect("birthdays.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO birthdays(name, month, day) VALUES (?, ?, ?)", (name, month, day))
            conn.commit()
            conn.close()

        return redirect("/")

    else:
        conn = sqlite3.connect("birthdays.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM birthdays")
        database = cursor.fetchall()
        print(database)
        conn.close()

        return render_template("index.html", database=database)

if __name__ == "__main__":
    app.run(debug=True)
