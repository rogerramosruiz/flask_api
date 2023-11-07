from flask import Flask, abort, jsonify
from connection import connection


app = Flask(__name__)

@app.route('/api/info/<ci>', methods=['GET'])
def get_users(ci):
     with connection() as (cur, _):
        query = """
        SELECT tp.nombres, 
        CASE
            WHEN tp.ap_paterno::text = '--'::text THEN ''::character varying
            ELSE tp.ap_paterno
            END AS ap_paterno,
        CASE
            WHEN tp.ap_materno::text = '--'::text THEN ''::character varying
            ELSE tp.ap_materno
            END AS ap_materno, 
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
            'nombres': data[0],
            'ap_paterno': data[1],
            'ap_materno': data[2],
            'matricula': data[3],
            'titulo': data[4],
            'formacion': data[5],
        }
        return jsonify(person_data), 200


if __name__ == '__main__':
    app.run('0.0.0.0', 8081, True)