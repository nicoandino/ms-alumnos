import http from 'k6/http';
import { Trend, Counter } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');
const successCounter = new Counter('successful_requests');
const errorCounter = new Counter('error_requests');

export const options = {
    // Usamos https con certificados locales (mkcert + Traefik)
    insecureSkipTLSVerify: true,

    // Spike: sube a 100 VUs, mantiene, y baja a 0
    stages: [
        { duration: "10s", target: 100 },
        { duration: "20s", target: 100 },
        { duration: "10s", target: 0 },
    ],
};

export default function () {
    // URL de TU microservicio
    const BASE_URL = 'https://alumnos.universidad.localhost';

    // Para tu proyecto es GET, no POST
    const res = http.get(`${BASE_URL}/api/v1/alumno/`);

    statusTrend.add(res.status);

    const isSuccess = check(res, {
        'status es 200 o 404': (r) => [200, 404].includes(r.status),
        'sin errores 5xx': (r) => r.status < 500,
    });

    if (isSuccess) {
        successCounter.add(1);
    } else {
        errorCounter.add(1);
        console.log(`Error: status=${res.status}, body=${res.body}`);
    }
}
