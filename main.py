from flask import Flask, jsonify
from connection import connection
from flask_cors import CORS, cross_origin


app = Flask(__name__)

origin = 'locahost'
CORS(app)

@app.route('/api/info/<ci>', methods=['GET'])
@cross_origin()
def get_users(ci):
     with connection() as (cur, _):
        query = """
        SELECT  
            (btrim(f.letmat::text) || ' - '::text) || btrim(f.nromat::text) AS matricula,
            tt.des_titulo,
            tf.des_tipoformacion
        FROM t_formacion as f
        JOIN t_persona as tp on tp.cedula = f.cedula
        JOIN t_titulo as tt on tt.cod_titulo = f.cod_titulo
        JOIN t_tipoformacion as tf on f.cod_tipoformacion = tf.cod_tipoformacion
        WHERE tp.cedula = %s
        """
        cur.execute(query, (str(ci), ))
        data = cur.fetchone()
        if data is None:
           return jsonify({'error': 'Cedula invalida'}), 404
        person_data = {
            'matricula': data[0],
            'titulo': data[1],
        }
        return jsonify(person_data), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 8081, True)