import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:5000';

export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    checks: ['rate>0.99'],
    'http_req_duration{name:GET /posts}': ['p(95)<500'],
    'http_req_duration{name:POST /posts}': ['p(95)<2000'],
  },
};

export default function () {
  if (Math.random() < 0.9) {
    const res = http.get(`${BASE_URL}/posts`, { tags: { name: 'GET /posts' } });
    check(res, { 'GET /posts status 200': (r) => r.status === 200 });
  } else {
    const res = http.post(
      `${BASE_URL}/posts`,
      JSON.stringify({ author: `k6_vu_${__VU}`, title: 'k6 post', content: 'stress' }),
      { headers: { 'Content-Type': 'application/json' }, tags: { name: 'POST /posts' } },
    );
    check(res, { 'POST /posts status 201': (r) => r.status === 201 });
  }
  sleep(1);
}
