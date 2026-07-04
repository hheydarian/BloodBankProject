from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# تابع کمکی برای وصل شدن به دیتابیس
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # این خط باعث می‌شود دیتابیس مثل یک دیکشنری پایتون رفتار کند (بسیار راحت‌تر است)
    conn.row_factory = sqlite3.Row 
    return conn

# مسیر صفحه اصلی (نمایش فرم)
@app.route('/')
def donor_form():
    return render_template('donor_form.html')

# مسیری که فرم اطلاعات را به آن می‌فرستد
@app.route('/submit_donor', methods=['POST'])
def submit_donor():
    # گرفتن اطلاعات از فرم HTML
    name = request.form['name']
    blood_type = request.form['blood_type']
    city = request.form['city']
    phone = request.form['phone']

    # ذخیره در دیتابیس
    conn = get_db_connection()
    conn.execute("INSERT INTO donors (name, blood_type, city, phone) VALUES (?, ?, ?, ?)",
                 (name, blood_type, city, phone))
    conn.commit()
    conn.close()

    # هدایت کاربر به صفحه موفقیت
    return redirect('/success')

# مسیر صفحه موفقیت
@app.route('/success')
def success_page():
    return render_template('success.html')

# مسیر نمایش فرم درخواست بیمارستان
@app.route('/request')
def request_form():
    return render_template('request_form.html')

# مسیر جستجوی هوشمند در دیتابیس
@app.route('/search_donors', methods=['POST'])
def search_donors():
    hospital_name = request.form['hospital_name']
    needed_blood = request.form['needed_blood_type']
    city = request.form['city']

    # ثبت درخواست در دیتابیس
    conn = get_db_connection()
    conn.execute("INSERT INTO requests (hospital_name, needed_blood_type, city) VALUES (?, ?, ?)",
                 (hospital_name, needed_blood, city))
    conn.commit()

    # جستجوی هوشمند: پیدا کردن داوطلبانی که گروه خونی و شهرشان با درخواست یکی است
    cursor = conn.execute("SELECT * FROM donors WHERE blood_type=? AND city=?", (needed_blood, city))
    matched_donors = cursor.fetchall()
    conn.close()

    # فرستادن نتایج به صفحه نمایش
    return render_template('results.html', donors=matched_donors, hospital=hospital_name, blood=needed_blood, city=city)

if __name__ == '__main__':
    app.run(debug=True)