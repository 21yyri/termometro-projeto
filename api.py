from flask import Flask, jsonify, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

def conexao():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    return conn, cursor


def tabela():
    conn, cursor = conexao()
    cursor.execute('''CREATE table IF NOT EXISTS termometros (
        macaddress TEXT,
        temperatura REAL NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()


tabela()

@app.route('/post', methods=['POST'])
def pegar_temp():
    macadd: str = request.json.get('macaddress')
    temperatura: float = request.json.get('temperatura')
    data: datetime = datetime.today().strftime('%d/%m %H:%M:%S')
    
    conn, cursor = conexao()
    cursor.execute("INSERT INTO termometros (macaddress, temperatura, data) VALUES (?, ?, ?)", (macadd, temperatura, data,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'OK'}), 201 
    

@app.route('/', methods=['GET'])
def postar_temp():
    conn, cursor = conexao()
    
    cursor.execute('SELECT * FROM termometros ORDER BY rowid DESC LIMIT 1')
    leitura: tuple = cursor.fetchone()
    if leitura:
        dados: dict = {
            'macadd': leitura[0],
            'temperatura': leitura[1],
            'data': leitura[2]
        }
        return jsonify(dados)
    return jsonify({'ERRO': 'Sem dados'}), 404
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
