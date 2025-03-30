from flask import Flask, request, jsonify
import pandas as pd
app = Flask(__name__)

# Carrega o CSV ao iniciar o servidor
df = pd.read_csv("Relatorio_cadop.csv", delimiter=";", encoding="utf-8")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])

    # Busca em todas as colunas: converte cada linha para string e procura pela query
    mask = df.apply(lambda row: query in row.to_string().lower(), axis=1)
    filtered_df = df[mask]
    
    # Limita a resposta aos 10 primeiros resultados (ajuste conforme necessário)
    result = filtered_df.head(10).to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
