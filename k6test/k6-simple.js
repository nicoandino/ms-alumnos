import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 10,           // 10 usuarios virtuales
  duration: '30s',   // Durante 30 segundos
};

const BASE_URL = 'http://localhost:5000';

export default function () {
  // Health check
  let res = http.get(`${BASE_URL}/health`);
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}