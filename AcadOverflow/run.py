from app import app

app.secret_key = 'secret123'
app.run('127.0.0.1', 5001, debug=True)