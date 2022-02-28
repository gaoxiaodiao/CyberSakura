from flask import *

app = Flask(__name__)

@app.route('/vault_is_intern', methods=['GET'])
def vault():
    return "Hello, World"

@app.route('/status/<int:id>', methods=['GET'])
def status(id):
    print(id)
    return "Hello, World"

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = '80',
        debug=True
    )
    
