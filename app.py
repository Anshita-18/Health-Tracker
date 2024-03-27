from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/button_clicked', methods=['POST'])
def handle_button_click():
    button_clicked = request.form['button']
    if button_clicked == 'button1':
        # Redirect to the attendance form
        return redirect('/attendance_form')
    elif button_clicked == 'button2':
        # Execute capture.py
        subprocess.Popen(['python', 'get_faces_from_camera_tkinter.py'])
        return "capture.py executed"
    elif button_clicked == 'button3':
        # Execute newstudent.py
        subprocess.Popen(['python', 'attendance_taker.py'])
        return "newstudent.py executed"
    else:
        return "Invalid button clicked"

@app.route('/attendance_form')
def attendance_form():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)
