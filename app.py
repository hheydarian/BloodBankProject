from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

# 1. صفحه اصلی (فرم ثبت داوطلب)
@app.route('/')
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

# 6. نمایش لیست تمام داوطلبان
@app.route('/all_donors')
def all_donors():
    conn = get_db_connection()
    # دریافت همه داوطلبان از دیتابیس به ترتیب جدیدترین
    donors = conn.execute("SELECT * FROM donors ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('all_donors.html', donors=donors)


if __name__ == '__main__':
    app.run(debug=True)