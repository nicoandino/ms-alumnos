# Antes de los test
En Windows, abre el siguiente directorio:
C:\Windows\System32\drivers\etc\hosts

En la última línea del archivo agrega:
127.0.0.1 alumnos.universidad.localhost

# Tests de rendimiento con k6
Este proyecto incluye pruebas de rendimiento y validación mediante k6.

Requisitos
Para ejecutar k6, primero debemos instalarlo:

1. Opcion 1
En power shell ejecutar (si se tiene winget)

winget install grafana.k6

Cuando se termine, verificar con:
k6 version

2. Opción B – con Chocolatey (si no tenés winget)
abrir powershell como administrador
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

cerrar powershell y ejecutar:

choco install k6 -y

Verificar con:
k6 version

# Ejecutar tests de carga

Los scripts se encuentran en la carpeta /k6tests (o donde el equipo los ubicó).

Ejecutar pruebas k6
Dentro del proyecto existe una carpeta de tests donde encontraremos scripts como:
-k6-load-test (test de carga)
-k6-simple.js (test liviano)
-spike_test.js (test de estres)

Para ejecutar el test:
1. En powershell nos ubicamos en la raiz del proyecto
2. Ejecutamos
k6 run --out web-dashboard .\k6test\<nombre_del_test>.js
ejemplo:
k6 run --out web-dashboard .\k6test\spike_tests.js


Ver el dashboard en tiempo real
http://127.0.0.1:5665/

modificar la URL objetivo dentro del script:
const BASE_URL = 'https://alumnos.universidad.localhost';

# explicacion del spike_test

Spike Test(incluido)
El archivo spike_test.js simula:

.Subida a 10.000 usuarios virtuales
.Mantener carga por 20s
.Descenso a 0 usuarios

Sirve para probar:
.Resiliencia
.Errores 500 / 429 / 400
.Saturación del endpoint

Además del Spike Test, el proyecto contiene archivos demo utilizados como pruebas rápidas:

.Validan si el microservicio está respondiendo
.Permiten probar Traefik
.Útiles antes de cargar k6


# Resultados obtenidos
En spike_test.js


  █ TOTAL RESULTS

    checks_total.......: 114036  2850.666295/s
    checks_succeeded...: 100.00% 114036 out of 114036
    checks_failed......: 0.00%   0 out of 114036

    ✓ status es 200 o 404
    ✓ sin errores 5xx

    CUSTOM
    status_codes...................: avg=200     min=200    med=200     max=200      p(90)=200      p(95)=200
    successful_requests............: 57018  1425.333148/s

    HTTP
    http_req_duration..............: avg=52.55ms min=1.01ms med=45.01ms max=532.89ms p(90)=100.72ms p(95)=122.61ms
      { expected_response:true }...: avg=52.55ms min=1.01ms med=45.01ms max=532.89ms p(90)=100.72ms p(95)=122.61ms
    http_req_failed................: 0.00%  0 out of 57018
    http_reqs......................: 57018  1425.333148/s

    EXECUTION
    iteration_duration.............: avg=52.72ms min=1.01ms med=45.19ms max=533.35ms p(90)=100.94ms p(95)=122.84ms
    iterations.....................: 57018  1425.333148/s
    vus............................: 1      min=1          max=100
    vus_max........................: 100    min=100        max=100

    NETWORK
    data_received..................: 61 MB  1.5 MB/s
    data_sent......................: 2.6 MB 66 kB/s




running (0m40.0s), 000/100 VUs, 57018 complete and 0 interrupted iterations
default ✓ [======================================] 000/100 VUs  40s

Interpretacion de los resultados (IA)


 Resultados del Test de Carga (100 VUs – 40s)

Checks totales: 114.036
Checks exitosos: 100% (sin fallos)
Checks fallidos: 0%

 Validaciones

 `status es 200 o 404` → OK
 `sin errores 5xx` → OK

 Códigos de estado

Promedio: 200
Mínimo: 200
Máximo: 200
p90: 200
p95: 200
requests exitosos: 57.018 (≈ 1.425 req/s)

Rendimiento HTTP

Duración promedio:52,55 ms
Mediana: 45,01 ms
Mínimo: 1,01 ms
Máximo: 532,89 ms
p90: 100,72 ms
p95: 122,61 ms
Errores HTTP: 0%

Iteraciones

Total: 57.018
Velocidad: 1.425 iter/s
Duración de iteración:

  * Promedio: 52,72 ms
  * p90: 100,94 ms
  * p95: 122,84 ms

Usuarios virtuales

* **VUs utilizados:** min 1 – max 100
* **VUs máximo permitido:** 100

 Red

Datos recibidos: 61 MB (1,5 MB/s)
Datos enviados: 2,6 MB (66 kB/s)



* La API manejó 100 usuarios concurrentes durante 40s sin errores.
* Tiempo de respuesta estable, con p95 ≈ 122 ms, excelente para alta concurrencia.
* Sin fallos 5xx ni timeouts.
