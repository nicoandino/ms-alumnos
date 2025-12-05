import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Subir a 20 usuarios en 30s
    { duration: '1m', target: 20 },   // Mantener 20 usuarios por 1 minuto
    { duration: '30s', target: 50 },  // Subir a 50 usuarios
    { duration: '1m', target: 50 },   // Mantener 50 usuarios
    { duration: '30s', target: 0 },   // Bajar a 0 usuarios
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% de requests deben ser < 1s
    http_req_failed: ['rate<0.05'],    // Menos del 5% de errores
  },
};

const BASE_URL = 'http://localhost:5000';

export default function () {
  group('Health Check', function () {
    let res = http.get(`${BASE_URL}/health`);
    check(res, { 
      'health status 200': (r) => r.status === 200,
      'health returns ok': (r) => r.json('status') === 'ok'
    });
  });

  sleep(1);

  group('Listar Alumnos', function () {
    let res = http.get(`${BASE_URL}/api/v1/alumno/`);
    check(res, { 
      'listado status 200': (r) => r.status === 200,
      'response is array': (r) => Array.isArray(r.json())
    });
  });

  sleep(1);

  // Solo si tenés datos de prueba, descomentá esto:
  /*
  group('Crear Alumno', function () {
    const payload = JSON.stringify({
      nombre: 'K6Test',
      apellido: 'User',
      nrodocumento: `${Date.now()}`,
      tipo_documento_id: 1, // Ajustá según tu BD
      fecha_nacimiento: '1995-05-15',
      sexo: 'M',
      nro_legajo: Math.floor(Math.random() * 999999),
      fecha_ingreso: '2024-01-01',
    });

    const params = {
      headers: { 'Content-Type': 'application/json' },
    };

    let res = http.post(`${BASE_URL}/api/v1/alumno/`, payload, params);
    check(res, { 'crear status 200': (r) => r.status === 200 });
  });
  */

  sleep(2);
}