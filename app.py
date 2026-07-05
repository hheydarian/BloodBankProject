from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

# صفحه اصلی دیگر فرم نیست، لندینگ پیج است
@app.route('/')
def landing_page():
    return render_template('landing.html')

# فرم داوطلب الان اینجا مستقر شده است
@app.route('/donor/register')
def donor_form():
    return render_template('donor_form.html')
# 2. پردازش فرم داوطلب (بدون نیاز به redirect)
@app.route('/submit_donor', methods=['POST'])
def submit_donor():
    name = request.form['name']
    blood_type = request.form['blood_type']
    city = request.form['city']
    phone = request.form['phone']

    conn = get_db_connection()
    conn.execute("INSERT INTO donors (name, blood_type, city, phone) VALUES (?, ?, ?, ?)",
                 (name, blood_type, city, phone))
    conn.commit()
    conn.close()

    # مستقیماً کد HTML صفحه موفقیت را برمی‌گردانیم
    return '''
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>ثبت موفق</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
        <style>
            @font-face { font-family: 'MyFont'; src: url('/static/fonts/SFArabic-Medium.ttf') format('truetype'); }
            * { font-family: 'MyFont', sans-serif; }
            body { background-color: #f4f6f9; display: flex; align-items: center; justify-content: center; height: 100vh; }
            .success-box { text-align: center; background: white; padding: 50px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
            .tick { font-size: 100px; color: #28a745; animation: pop 0.5s ease; }
            @keyframes pop { 0% { transform: scale(0); } 80% { transform: scale(1.2); } 100% { transform: scale(1); } }
            a { text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="success-box">
            <div class="tick">&#10004;</div>
            <h2 class="text-success mt-3">ثبت‌نام شما با موفقیت انجام شد!</h2>
            <p class="text-muted mt-3">اطلاعات شما در سامانه هوشمند اهدای خون ثبت گردید.</p>
            <a href="/" class="btn btn-outline-primary mt-4 px-5 py-3 rounded-pill">بازگشت به صفحه اصلی</a>
        </div>
    </body>
    </html>
    '''

# 3. صفحه درخواست بیمارستان
@app.route('/request')
def request_form():
    return render_template('request_form.html')

# 4. جستجوی هوشمند داوطلبان
@app.route('/search_donors', methods=['POST'])
def search_donors():
    hospital_name = request.form['hospital_name']
    needed_blood = request.form['needed_blood_type']
    city = request.form['city']

    conn = get_db_connection()
    conn.execute("INSERT INTO requests (hospital_name, needed_blood_type, city) VALUES (?, ?, ?)",
                 (hospital_name, needed_blood, city))
    conn.commit()

    cursor = conn.execute("SELECT * FROM donors WHERE blood_type=? AND city=?", (needed_blood, city))
    matched_donors = cursor.fetchall()
    conn.close()

    return render_template('results.html', donors=matched_donors, hospital=hospital_name, blood=needed_blood, city=city)



# 5. پردازش دکمه ارسال پیامک
@app.route('/send_sms', methods=['POST'])
def send_sms():
    donor_name = request.form['donor_name']
    # در پروژه واقعی اینجا کد API پیامک قرار می‌گرفت
    # ما اینجا فقط یک پیام برمی‌گردانیم تا در صفحه نمایش داده شود
    return f'''
    <div class="text-success mt-2" style="font-size: 0.9rem;">✅ پیامک اضطراری برای <b>{donor_name}</b> با موفقیت ارسال شد.</div>
    '''

# 6. نمایش لیست داوطلبان (فقط برای پنل بیمارستان)
@app.route('/hospital/manage_donors')
def manage_donors():
    conn = get_db_connection()
    donors = conn.execute("SELECT * FROM donors ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('manage_donors.html', donors=donors)

# 7. نمایش فرم لاگین بیمارستان
@app.route('/hospital/login')
def hospital_login():
    return render_template('hospital_login.html')

# 8. بررسی رمز عبور و ورود به داشبورد
@app.route('/hospital/dashboard', methods=['POST'])
def hospital_dashboard():
    password = request.form['password']
    # رمز عبور پیش‌فرض بیمارستان‌ها
    if password == 'admin123':
        return render_template('hospital_dashboard.html')
    else:
        # اگر رمز اشتباه بود، دوباره صفحه لاگین را با یک ارور نشان بده
        return render_template('hospital_login.html', error=True)


# 9. حذف داوطلب از دیتابیس
@app.route('/delete_donor/<int:id>', methods=['POST'])
def delete_donor(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM donors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    # بعد از حذف، دوباره برگرد به همون صفحه مدیریت
    return redirect('/hospital/manage_donors')

# 10. نمایش فرم ویرایش داوطلب
@app.route('/edit_donor/<int:id>')
def edit_donor(id):
    conn = get_db_connection()
    donor = conn.execute("SELECT * FROM donors WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit_donor.html', donor=donor)

# 11. ذخیره تغییرات ویرایش شده
@app.route('/update_donor/<int:id>', methods=['POST'])
def update_donor(id):
    name = request.form['name']
    blood_type = request.form['blood_type']
    city = request.form['city']
    phone = request.form['phone']
    
    conn = get_db_connection()
    conn.execute("UPDATE donors SET name=?, blood_type=?, city=?, phone=? WHERE id=?",
                (name, blood_type, city, phone, id))
    conn.commit()
    conn.close()
    return redirect('/hospital/manage_donors')


# 13. حذف گروهی (چند داوطلب با هم)
@app.route('/bulk_delete', methods=['POST'])
def bulk_delete():
    # گرفتن لیست آیدی‌های تیک خورده
    selected_ids = request.form.getlist('donor_ids')
    
    if selected_ids:
        conn = get_db_connection()
        # حلقه روی آیدی‌ها و حذف تک تک از دیتابیس
        for donor_id in selected_ids:
            conn.execute("DELETE FROM donors WHERE id=?", (donor_id,))
        conn.commit()
        conn.close()
    
    # بازگشت به صفحه مدیریت
    return redirect('/hospital/manage_donors')








if __name__ == '__main__':
    app.run(debug=True)