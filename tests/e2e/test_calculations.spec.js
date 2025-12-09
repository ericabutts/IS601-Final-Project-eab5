const { test, expect, request } = require('@playwright/test');

test.describe('Calculation API', () => {

  test('Positive: Create calculation with valid data', async ({ request }) => {
    // Step 1: Register a test user
    const email = `calcuser${Date.now()}@example.com`;
    const password = 'testpass123';

    const registerResponse = await request.post('http://127.0.0.1:8000/register', {
      data: {
        email,
        username: email,
        password
      }
    });
    expect(registerResponse.status()).toBe(200);
    const registerData = await registerResponse.json();
    const token = registerData.access_token;
    expect(token).not.toBeNull();

    // Step 2: Use token to create a calculation
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      data: {
        a: 10,
        b: 5,
        type: 'add'
      },
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('id');
    expect(data.result).toBe(15);
    expect(data.type).toBe('ADD');
  });


});

test.describe('Calculation API', () => {

  test('Negative: Create calculation without token', async ({ request }) => {
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      data: {
        a: 10,
        b: 5,
        type: 'add'
      }
    });

    // Expect unauthorized status
    expect(response.status()).toBe(401);

    const data = await response.json();
    expect(data.detail).toBe('Not authenticated');
  });

});


test.describe('Calculation API', () => {

  test('Negative: Create calculation with invalid type', async ({ page, request }) => {
    const email = `calcuser@example.com`;
    const password = 'testpass123';

    // Ensure the test user exists
    try {
      await request.post('http://127.0.0.1:8000/register', {
        data: { email, username: email, password }
      });
    } catch (e) {
      // Ignore if user already exists
    }

    // Log in to get a valid token
    const loginResponse = await request.post('http://127.0.0.1:8000/login', {
      data: { username: email, password }
    });

    expect(loginResponse.status()).toBe(200);
    const loginData = await loginResponse.json();
    const token = loginData.access_token;
    expect(token).not.toBeNull();

    // Attempt to create a calculation with invalid type
    const response = await request.post('http://127.0.0.1:8000/calculations', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      data: {
        a: 5,
        b: 3,
        type: 'invalid_op'  // invalid type
      }
    });

    // Expect backend to reject invalid type
    expect(response.status()).toBe(422); // Pydantic validation error
    const responseData = await response.json();
    expect(responseData.detail).toBeDefined();
    expect(responseData.detail[0].msg).toMatch(/Unsupported operation/i);
  });

});

