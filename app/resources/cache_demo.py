import time
import random
import json
import redis
from flask import Blueprint, jsonify

cache_bp = Blueprint("cache", __name__)

# Configuracion de conexion a Redis
r = redis.Redis(
    host="redis", 
    port=6379, 
    password="redispass",
    decode_responses=True
)

def recurso_lento():
    """Simula un recurso externo con latencia de 1 segundo"""
    time.sleep(1.0)
    return {
        "msg": "dato generado",
        "valor": random.randint(1, 9999)
    }

@cache_bp.route("/debug/cache/<clave>")
def cache_test(clave):

    # 1. Verificar si el dato existe en la cache
    data = r.get(f"cache:{clave}")
    if data is not None:
        return jsonify({
            "cached": True,
            "data": json.loads(data)
        }), 200

    # 2. Si no esta en la cache, calcular el resultado
    result = recurso_lento()

    # 3. Almacenar el resultado en la cache por 30 segundos
    r.setex(f"cache:{clave}", 30, json.dumps(result))

    return jsonify({
        "cached": False,
        "data": result
    }), 200
