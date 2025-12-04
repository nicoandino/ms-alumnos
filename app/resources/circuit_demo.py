import time
import random
from flask import Blueprint, jsonify

circuit_bp = Blueprint("circuit", __name__)

# --- Estado del circuito (muy simple, en memoria del proceso) ---
estado = "closed"          # "closed" o "open"
fallas = 0                 # fallas consecutivas
umbral_fallas = 5          # a partir de acá abrimos el circuito
tiempo_apertura = 0.0      # timestamp cuando se abrió
tiempo_espera = 15.0       # segundos que se mantiene abierto


def recurso_lento_e_inestable():
    time.sleep(1.0)
    if random.random() < 0.9:  # 90% de fallos
        raise RuntimeError("Fallo simulado del recurso externo (90%)")
    return {"msg": "respuesta OK del recurso externo"}



@circuit_bp.route("/slow-cb")
def slow_con_circuit_breaker():
    global estado, fallas, tiempo_apertura

    ahora = time.time()

    # 1) Si el circuito está abierto, ver si ya pasó el tiempo de espera
    if estado == "open":
        if (ahora - tiempo_apertura) < tiempo_espera:
            # Sigue abierto: devolvemos 503 al toque (cortocircuito)
            return jsonify({
                "ok": False,
                "circuit_state": estado,
                "reason": "circuit open, skipping call"
            }), 503
        else:
            # Terminó el tiempo de espera: volvemos a cerrado y reseteamos fallas
            estado = "closed"
            fallas = 0

    # 2) Circuito cerrado: intentamos llamar al recurso externo
    try:
        data = recurso_lento_e_inestable()
    except Exception as exc:
        # Falló la llamada al recurso: contamos la falla
        fallas += 1
        # Si superamos el umbral, abrimos el circuito
        if fallas >= umbral_fallas:
            estado = "open"
            tiempo_apertura = ahora
        return jsonify({
            "ok": False,
            "circuit_state": estado,
            "error": str(exc),
            "fallas": fallas
        }), 500

    # 3) Si salió bien, reseteamos las fallas
    fallas = 0
    return jsonify({
        "ok": True,
        "circuit_state": estado,
        "data": data
    }), 200
