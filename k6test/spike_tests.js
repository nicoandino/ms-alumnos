import http from 'k6/http';
import { Trend } from 'k6/metrics';
import { check } from 'k6';

const statusTrend = new Trend('status_codes');

export const options = {
    //Para los alumnos que siguen prefiriendo Windows 11 es posible que tengan que descomentar insecureSkipTLSVerify (https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/)
    //insecureSkipTLSVerify: true,
    stages: [
        { duration: "10s", target: 10000 },
        { duration: "20s", target: 10000 },
        { duration: "10s", target: 0 },
    ],
};

export default function () {
    //Tienen que modificar la url que quieren probar
    const BASE_URL = 'https://ecommerce.universidad.localhost';

    //Para probar con post enviando un json, no es el caso para ninguno de los proyectos
    const payload = JSON.stringify({ "producto": 1, "cantidad": 1, "entrada_salida":1 });
    
    const params = {
        headers: {
            'Content-Type': 'application/json',
            },
    };
    
    //Creo que para todos los proyectos es get
    const res = http.post(`${BASE_URL}/`, payload, params);
    
    statusTrend.add(res.status);

    check(res, {
        'status is 200': (r) => r.status === 200,
        'status is 409': (r) => r.status === 409,
        'status is 404': (r) => r.status === 404,
        'status is 400': (r) => r.status === 400,
        'status is 429': (r) => r.status === 429,
        'status is 500': (r) => r.status === 500,
    });

}
