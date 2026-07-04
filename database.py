import sqlite3

def init_db():
    # اتصال به فایل دیتابیس (اگر نباشد، خودش فایل database.db را می‌سازد)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # ساختن جدول داوطلبان
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            city TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')

    # ساختن جدول درخواست‌ها
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hospital_name TEXT NOT NULL,
            needed_blood_type TEXT NOT NULL,
            city TEXT NOT NULL,
            is_resolved INTEGER DEFAULT 0
        )
    ''')

    # ذخیره تغییرات و بستن دیتابیس
    conn.commit()
    conn.close()
    print("دیتابیس با موفقیت ساخته شد!")

# اجرای تابع بالا وقتی این فایل را اجرا می‌کنیم
if __name__ == '__main__':
    init_db()