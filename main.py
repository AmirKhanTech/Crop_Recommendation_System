from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'smartfarm_super_secret_key'

# Foydalanuvchilar (Vaqtincha xotirada, keyinchalik DB ga ulash mumkin)
users = {}

@app.route('/')
def index():
    if 'user_email' in session:
        name = session.get('user_name', 'Foydalanuvchi')
        return redirect(f"http://localhost:8501?name={name}")
    return render_template('smartfarm_pro_register.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    
    # Ma'lumotlarni saqlash (Oddiy misol)
    users[email] = {
        "password": password,
        "name": first_name
    }
    
    # Sessiyaga yozish
    session['user_email'] = email
    session['user_name'] = first_name
    
    return jsonify({"status": "success", "message": "Ro'yxatdan o'tdingiz!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)