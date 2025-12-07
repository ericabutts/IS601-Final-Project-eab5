const { test, expect } = require('@playwright/test');

test.describe('User Registration & Login', () => {

  test('Positive: Register with valid data', async ({ page }) => {
    await page.goto('http://127.0.0.1:5500/register.html');

    await page.fill('#email', 'testuser@example.com');
    await page.fill('#password', 'testpass123');
    await page.click('#registerBtn');

    // Wait for the message text to appear
    await expect(page.locator('#message')).toHaveText(/Registration successful!/i, { timeout: 10000 });
  });

  test('Negative: Register with short password', async ({ page }) => {
    await page.goto('http://127.0.0.1:5500/register.html');

    await page.fill('#email', 'shortpass@example.com');
    await page.fill('#password', '123');
    await page.click('#registerBtn');

    await expect(page.locator('#message')).toHaveText(/Password too short/i);
  });

  test('Positive: Login with correct credentials', async ({ page }) => {
    await page.goto('http://127.0.0.1:5500/login.html');

    await page.fill('#email', 'testuser@example.com');
    await page.fill('#password', 'testpass123');
    await page.click('#loginBtn');

    await expect(page.locator('#message')).toHaveText(/Login successful/i, { timeout: 10000 });
  });

  test('Negative: Login with wrong password', async ({ page }) => {
    await page.goto('http://127.0.0.1:5500/login.html');

    await page.fill('#email', 'testuser@example.com');
    await page.fill('#password', 'wrongpass');
    await page.click('#loginBtn');

    await expect(page.locator('#message')).toHaveText(/Invalid credentials/i, { timeout: 10000 });
  });

});
