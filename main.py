from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    # Gerçek istemci IP adresini al
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Başlıktaki ilk IP adresini alın (gerçek istemci IP adresi)
        user_ip = forwarded_for.split(',')[0]
    else:
        # X-Forwarded-For başlığı yoksa, request.remote_addr kullanın
        user_ip = request.remote_addr
    return f'Sizin IP adresiniz: {user_ip}a'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
