import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 200 }, // Ramp warmup
    { duration: '60s', target: 2000 }, // Peak 2000 VU
    { duration: '20s', target: 500 },  // Ramp down
    { duration: '10s', target: 0 },
  ],
};

const BASE_URL = __ENV.HOST || 'http://localhost:5000'; // Local: http://localhost:5000 | K8s Minikube: http://localhost:30000 (NodePort)

export default function () {
  const regNo = `2021${Math.floor(Math.random() * 4100 + 1000)}`; // Random from 5100 seeded students
  
  const payload = `reg_no=${regNo}&dob=2003-05-15`; // Uses demo DOB pattern (every 7th student)

  const params = {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  };

  const res = http.post(`${BASE_URL}/view-result`, payload, params);

  check(res, {
    'status 200': (r) => r.status === 200,
    'result loaded': (r) => r.body.includes('Marksheet'),
    'response <2500ms': (r) => r.timings.duration < 2500,
  });

  sleep(Math.random() * 0.5 + 0.3); // Realistic think time
}
