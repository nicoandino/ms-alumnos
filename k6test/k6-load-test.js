import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  insecureSkipTLSVerify: true,

  stages: [
    { duration: '10s', target: 20 },  // Subida rápida a 20 VUs
    { duration: '10s', target: 20 },  // Mantener 20 VUs
    { duration: '10s', target: 50 },  // Aumentar a 50 VUs (pico)
    { duration: '10s', target: 0 },   // Bajar a 0 VUs
  ],

  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% < 1s
    http_req_failed: ['rate<0.05'],    // < 5% fallos
  },
};


// Entramos por IP pero simulamos el Host para Traefik
const BASE_URL = 'https://127.0.0.1';
const COMMON_PARAMS = {
  headers: {
    Host: 'alumnos.universidad.localhost',
  },
};

export default function () {
  group('Health Check', function () {
    let res = http.get(`${BASE_URL}/health`, COMMON_PARAMS);
    check(res, {
      'health status 200': (r) => r.status === 200,
      // ajustá esto si tu /health devuelve otra cosa
      'health returns ok': (r) => r.json('status') === 'ok',
    });
  });

  sleep(1);

  group('Listar Alumnos', function () {
    let res = http.get(`${BASE_URL}/api/v1/alumno/`, COMMON_PARAMS);
    check(res, {
      'listado status 200': (r) => r.status === 200,
      'response is array': (r) => Array.isArray(r.json()),
    });
  });

  sleep(1);


  sleep(2);
}
