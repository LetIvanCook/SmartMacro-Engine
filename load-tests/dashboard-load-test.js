import http from 'k6/http';
import { check, sleep, fail } from 'k6';

// ── Environment Configuration ──────────────────────────────────────────
const BASE_URL = (__ENV.BASE_URL || 'http://localhost:8080').replace(/\/+$/, '');
const TEST_USER_EMAIL = __ENV.TEST_USER_EMAIL || '';
const TEST_USER_PASSWORD = __ENV.TEST_USER_PASSWORD || '';
const TARGET_ENDPOINT = __ENV.TARGET_ENDPOINT || '/api/optimizations/generate-plan';

// Dynamic Threshold Configuration (overrideable via environment variables)
const P95_THRESHOLD = __ENV.P95_THRESHOLD || '800';
const P99_THRESHOLD = __ENV.P99_THRESHOLD || '1500';
const MAX_ERROR_RATE = __ENV.MAX_ERROR_RATE || '0.01';
const PROFILE = (__ENV.PROFILE || 'standard').toLowerCase();

// Define execution profiles
function getStages(profile) {
  switch (profile) {
    case 'smoke':
      return [
        { duration: '5s', target: 1 },
        { duration: '10s', target: 2 },
        { duration: '5s', target: 0 },
      ];
    case 'stress':
      return [
        { duration: '30s', target: 20 },
        { duration: '1m', target: 50 },
        { duration: '1m', target: 100 },
        { duration: '30s', target: 0 },
      ];
    case 'standard':
    default:
      return [
        { duration: '30s', target: 20 },
        { duration: '1m', target: 50 },
        { duration: '30s', target: 0 },
      ];
  }
}

export const options = {
  scenarios: {
    smartmacro_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: getStages(PROFILE),
    },
  },
  thresholds: {
    http_req_duration: [`p(95)<${P95_THRESHOLD}`, `p(99)<${P99_THRESHOLD}`],
    http_req_failed: [`rate<${MAX_ERROR_RATE}`],
  },
};

/**
 * Setup Phase: Executed once before virtual users start.
 * Authenticates against /api/auth/login to obtain JWT token.
 * This ensures the 5 req/min Rate Limit on AuthPolicy is not exceeded by concurrent VUs.
 */
export function setup() {
  if (!TEST_USER_EMAIL || !TEST_USER_PASSWORD) {
    fail('TEST_USER_EMAIL and TEST_USER_PASSWORD environment variables are required.');
  }

  const loginUrl = `${BASE_URL}/api/auth/login`;
  const loginPayload = JSON.stringify({
    email: TEST_USER_EMAIL,
    password: TEST_USER_PASSWORD,
  });

  const loginHeaders = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const loginRes = http.post(loginUrl, loginPayload, loginHeaders);

  const loginOk = check(loginRes, {
    'setup: login succeeded (status 200)': (r) => r.status === 200,
    'setup: access token returned': (r) => {
      try {
        const body = r.json();
        return body && typeof body.accessToken === 'string' && body.accessToken.length > 0;
      } catch (e) {
        return false;
      }
    },
  });

  if (!loginOk) {
    fail(`Setup failed: Unable to authenticate with ${loginUrl}. Status: ${loginRes.status}, Body: ${loginRes.body}`);
  }

  const responseBody = loginRes.json();
  return {
    token: responseBody.accessToken,
    userId: responseBody.userId,
  };
}

/**
 * Default VU Function: Executed in parallel across simulated users.
 */
export default function (data) {
  let url;
  let res;

  const authHeaders = {
    headers: {
      'Authorization': `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  };

  if (TARGET_ENDPOINT.startsWith('/api/optimizations') || TARGET_ENDPOINT.includes('generate-plan')) {
    // LP Solver Optimization Endpoint (POST /api/optimizations/generate-plan)
    url = `${BASE_URL}${TARGET_ENDPOINT}`;
    const optimizationPayload = JSON.stringify({
      dailyTargetId: null,
      includeFoodIds: null,
    });

    res = http.post(url, optimizationPayload, authHeaders);

    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time within p95 threshold': (r) => r.timings.duration < Number(P95_THRESHOLD),
      'solver result valid': (r) => {
        try {
          const body = r.json();
          return body && body.solverStatus !== undefined;
        } catch (e) {
          return false;
        }
      },
    });
  } else if (TARGET_ENDPOINT.includes('dashboard')) {
    // Dashboard Endpoint (GET /api/dashboard/{userId}/dashboard)
    const resolvedPath = TARGET_ENDPOINT.includes('{userId}')
      ? TARGET_ENDPOINT.replace('{userId}', data.userId)
      : TARGET_ENDPOINT.startsWith('/api/dashboard')
        ? TARGET_ENDPOINT
        : `/api/dashboard/${data.userId}/dashboard`;

    url = `${BASE_URL}${resolvedPath}`;
    res = http.get(url, authHeaders);

    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time within p95 threshold': (r) => r.timings.duration < Number(P95_THRESHOLD),
    });
  } else {
    // Generic GET target
    url = `${BASE_URL}${TARGET_ENDPOINT}`;
    res = http.get(url, authHeaders);

    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time within p95 threshold': (r) => r.timings.duration < Number(P95_THRESHOLD),
    });
  }

  // Pacing: simulate realistic user pause between requests
  sleep(1);
}
