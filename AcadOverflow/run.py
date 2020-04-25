import sys

sys.path.append("./app")
sys.path.append("./app/gql_client")
sys.path.append("./app/ml_module")

from app import app

app.secret_key = 'secret123'
app.run('127.0.0.1', 5005, debug=True)