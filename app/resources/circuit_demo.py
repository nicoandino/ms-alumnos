import time
import random
from flask import Blueprint, jsonify

circuit_bp = Blueprint("circuit", __name__)

# --- Estado del circuito (implementacion simple en memoria del proceso) ---
estado = "closed"          # "closed" o "open"
fallas = 0                 # contador de fallas consecutivas
umbral_fallas = 5          # Número máximo de fallas consecutivas antes de abrir el circuito
tiempo_apertura = 0.0      # Marca de tiempo en la que se abrio el circuito
tiempo_espera = 15.0       # Duracion en segundos que el circuito permanece abierto


def recurso_lento_e_inestable():
    time.sleep(1.0)
    if random.random() < 0.9:  # Probabilidad del 90% de fallo simulado
        raise RuntimeError("Fallo simulado del recurso externo (90%)")
    return {"msg": "respuesta OK del recurso externo"}



@circuit_bp.route("/slow-cb")
def slow_con_circuit_breaker():
    global estado, fallas, tiempo_apertura

    ahora = time.time()

    # 1) Si el circuito está abierto, verificar si ya paso el tiempo de espera
    if estado == "open":
        if (ahora - tiempo_apertura) < tiempo_espera:
            # Sigue abierto: devolver respuesta 503 inmediatamente (cortocircuito)
            return jsonify({
                "ok": False,
                "circuit_state": estado,
                "reason": "circuit open, skipping call"
            }), 503
        else:
            # Terminó el tiempo de espera finalizo: cerrar el circuito y reiniciar el contador de fallas
            estado = "closed"
            fallas = 0

    # 2) Con el circuito cerrado: intentar acceder al recurso externo
    try:
        data = recurso_lento_e_inestable()
    except Exception as exc:
        # La llamada falló: incrementar el contador de fallas
        fallas += 1
        # Si se supera el umbral de fallas consecutivas, abrir el circuito
        if fallas >= umbral_fallas:
            estado = "open"
            tiempo_apertura = ahora
        return jsonify({
            "ok": False,
            "circuit_state": estado,
            "error": str(exc),
            "fallas": fallas
        }), 500

    # 3) Si la llamada fue exitosa, reiniciar el contador de fallas
    fallas = 0
    return jsonify({
        "ok": True,
        "circuit_state": estado,
        "data": data
    }), 200
