

# Verificación del Balanceo de Carga con Traefik y Whoami
Para comprobar el balanceo entre múltiples réplicas, se usa el servicio whoami. Con varias réplicas levantadas, ejecutar repetidamente:
curl.exe -k https://whoami.universidad.localhost
El hostname debe alternarse entre distintos contenedores, confirmando el round-robin de Traefik.
# Verificación de Retry
El endpoint /debug/unstable simula fallos aleatorios. Las etiquetas Traefik definen el middleware retry. Para testearlo:
•	for ($i=0; $i -lt 20; $i++) { curl.exe -k -s -o NUL -w "%{http_code}`n" https://alumnos.universidad.localhost/debug/unstable }
La presencia constante de códigos 502 con reintentos internos confirma que Traefik ejecuta el middleware retry.
# Verificación del Circuit Breaker
El endpoint /debug/slow-cb simula un recurso externo inestable. Se implementaron umbrales de error para activar el circuito. Para probar:
•	curl.exe -k https://alumnos.universidad.localhost/debug/slow-cb
Observar en la respuesta JSON los campos circuit_state y fallas.
# Verificación del Caché Distribuido de Objetos con Redis
El endpoint /debug/cache/<clave> utiliza Redis para almacenar resultados. Primer acceso → MISS, segundo acceso → HIT.
•	curl.exe -k https://alumnos.universidad.localhost/debug/cache/test1
La primera respuesta debe indicar "cached": false. La segunda, "cached": true y devolver el mismo valor.
Para verificar directamente en Redis:
•	docker exec -it redis redis-cli -a redispass
•	keys *
Debe aparecer la clave cache:test1 con su valor correspondiente.
# Prueba Interna desde el Microservicio
Para confirmar que el microservicio se conecta correctamente a Redis desde adentro del contenedor:
•	docker exec -it docker-alumnos-service-1 python
•	import redis, os
r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), password=os.getenv("REDIS_PASSWORD"), decode_responses=True)
print(r.ping())
r.set("prueba", "ok")
Luego consultar en Redis para validar persistencia:
•	get prueba
# Conclusión
Los mecanismos de balanceo, retry, circuit breaker y caché distribuido funcionan correctamente. Redis almacena y comparte objetos entre réplicas, y Traefik ejecuta sus middlewares según lo esperado.
