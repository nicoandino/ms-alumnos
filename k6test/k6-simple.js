import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  insecureSkipTLSVerify: true,   // Necesario por Traefik + mkcert
  vus: 10,                       // 10 usuarios virtuales
  duration: '30s',               // Ejecutar durante 30 segundos
};

// Se entra por IP pero se fuerza el Host para que Traefik rote correctamente
const BASE_URL = 'https://127.0.0.1';
const PARAMS = {
  headers: {
    Host: 'alumnos.universidad.localhost',
  },
};

export default function () {
  // Health check sobre tu microservicio real
  let res = http.get(`${BASE_URL}/health`, PARAMS);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1); // Cada usuario espera 1s entre iteraciones
}
