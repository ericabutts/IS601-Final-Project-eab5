const { test, expect } = require('@playwright/test');

test.describe('User Registration & Login', () => {

  test('Positive: Register with valid data', async ({ page }) => {
    const email = `user${Date.now()}@example.com`;
    const password = "testpass123";

    await page.goto('http://127.0.0.1:5500/register.html');

    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#registerBtn');

    await expect(page.locator('#message')).toHaveText(/Registration successful!/i, { timeout: 10000 });
  });

  // -------------------------------
  // Negative Test: Short Password
  // -------------------------------
  test('Negative: Register with short password', async ({ page }) => {
    const email = `user${Date.now()}@example.com`;
    const password = "123"; // too short

    await page.goto('http://127.0.0.1:5500/register.html');

    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.click('#registerBtn');

    await expect(page.locator('#message')).toHaveText(/Password too short/i, { timeout: 5000 });
  });

  test('Positive: Login with correct credentials', async ({ page }) => {
  // Step 1: Register a new user
  const email = `user${Date.now()}@example.com`;
  const password = "testpass123";

  await page.goto('http://127.0.0.1:5500/register.html');
  await page.fill('#email', email);
  await page.fill('#password', password);
  await page.click('#registerBtn');

  // Wait for registration to succeed
  await expect(page.locator('#message')).toHaveText(/Registration successful!/i, { timeout: 10000 });

  // Step 2: Log out or go to login page
  await page.goto('http://127.0.0.1:5500/login.html');

  // Step 3: Log in with the same credentials
  await page.fill('#email', email);
  await page.fill('#password', password);
  await page.click('#loginBtn');

  // Verify login success
  await expect(page.locator('#message')).toHaveText(/Login successful/i, { timeout: 10000 });
});

  test('Negative: Login with wrong password', async ({ page }) => {
    // Step 1: Register a new user first
    const email = `user${Date.now()}@example.com`;
    const correctPassword = "testpass123";
    const wrongPassword = "wrongpass456";

    await page.goto('http://127.0.0.1:5500/register.html');
    await page.fill('#email', email);
    await page.fill('#password', correctPassword);
    await page.click('#registerBtn');

    // Wait for registration success
    await expect(page.locator('#message')).toHaveText(/Registration successful!/i, { timeout: 10000 });

    // Step 2: Go to login page
    await page.goto('http://127.0.0.1:5500/login.html');

    // Step 3: Try to log in with wrong password
    await page.fill('#email', email);
    await page.fill('#password', wrongPassword);
    await page.click('#loginBtn');

    // Step 4: Verify login failed
    await expect(page.locator('#message')).toHaveText(/Invalid credentials/i, { timeout: 10000 });
  });



});
