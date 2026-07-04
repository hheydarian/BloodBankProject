from flask import Flask

# ساخت یک سایت (اپلیکیشن) ساده
app = Flask(__name__)

# تعریف صفحه اصلی سایت
@app.route('/')
def home_page():
    return "<h1>سلام! به سامانه اهدای خون خوش آمدید.</h1> <p>این اولین صفحه سایت ماست.</p>"

# روشن کردن سرور سایت
if __name__ == '__main__':
    app.run(debug=True)