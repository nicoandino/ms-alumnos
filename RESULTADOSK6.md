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
