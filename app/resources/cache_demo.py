import time
import random
import json
import redis
from flask import Blueprint, jsonify

cache_bp = Blueprint("cache", __name__)

# Config Redis
r = redis.Redis(
    host="redis", 
    port=6379, 
    password="redispass",
    decode_responses=True
)

def recurso_lento():
    """Simula un recurso externo lento (1 segundo)"""
    time.sleep(1.0)
    return {
        "msg": "dato generado",
        "valor": random.randint(1, 9999)
    }

@cache_bp.route("/debug/cache/<clave>")
def cache_test(clave):

    # 1. ¿Existe en cache?
    data = r.get(f"cache:{clave}")
    if data is not None:
        return jsonify({
            "cached": True,
            "data": json.loads(data)
        }), 200

    # 2. No está en cache → calcular
    result = recurso_lento()

    # 3. Guardarlo en cache (expira en 30 segundos)
    r.setex(f"cache:{clave}", 30, json.dumps(result))

    return jsonify({
        "cached": False,
        "data": result
    }), 200
