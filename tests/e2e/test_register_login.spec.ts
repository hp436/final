import { test, expect } from "@playwright/test";

const BASE_URL = "http://127.0.0.1:8000";


test.describe("Minimal Login Tests", () => {

    test("Positive Test 1 — Register page loads", async ({ page }) => {
        await page.goto(`${BASE_URL}/register`);
        await expect(page.locator("h1")).toContainText("Create an Account");
    });

    test("Positive Test 2 — Login page loads", async ({ page }) => {
        await page.goto(`${BASE_URL}/login`);
        await expect(page.locator("h1")).toContainText("Login");
    });

    test("Negative Test 1 — Register empty submit shows error", async ({ page }) => {
        await page.goto(`${BASE_URL}/register`);

        await page.click("#registerBtn");

        const msg = page.locator("#message");
        await expect(msg).toBeVisible();
    });

    test("Negative Test 2 — Login empty submit shows error", async ({ page }) => {
        await page.goto(`${BASE_URL}/login`);

        await page.click("#loginBtn");

        const msg = page.locator("#message");
        await expect(msg).toBeVisible();
    });

});



test.describe("Calculations API E2E", () => {
  
    let token: string = "";
    let calcId: string = "";

    // LOGIN FIRST
    test("Login and receive JWT token", async ({ request }) => {
        const res = await request.post(`${BASE_URL}/auth/login`, {
            data: {
                username: "test@test.com",
                password: "password"
            }
        });

        expect(res.ok()).toBeTruthy();

        const body = await res.json();
        expect(body.access_token).toBeTruthy();

        token = body.access_token;
    });

    // CREATE CALC
    test("Create calculation successfully", async ({ request }) => {
        const res = await request.post(`${BASE_URL}/calculations/`, {
            data: { operation: "add", a: 5, b: 10 },
            headers: { Authorization: `Bearer ${token}` }
        });

        expect(res.ok()).toBeTruthy();

        const body = await res.json();
        expect(body.result).toBe(15);

        calcId = body.id;
    });

    // GET ALL
    test("Retrieve all calculations", async ({ request }) => {
        const res = await request.get(`${BASE_URL}/calculations/`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        expect(res.ok()).toBeTruthy();

        const list = await res.json();
        expect(Array.isArray(list)).toBe(true);
    });

    // UPDATE CALC
    test("Update calculation", async ({ request }) => {
        const res = await request.put(`${BASE_URL}/calculations/${calcId}`, {
            data: { operation: "multiply", a: 2, b: 6 },
            headers: { Authorization: `Bearer ${token}` }
        });

        expect(res.ok()).toBeTruthy();

        const body = await res.json();
        expect(body.result).toBe(12);
    });

    // DELETE CALC
    test("Delete calculation", async ({ request }) => {
        const res = await request.delete(`${BASE_URL}/calculations/${calcId}`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        expect(res.status()).toBe(204);
    });

    /* -------------------------
       NEGATIVE SCENARIOS
    -------------------------- */

    test("Unauthorized access → 401", async ({ request }) => {
        const res = await request.get(`${BASE_URL}/calculations/`);
        expect(res.status()).toBe(401);
    });

    test("Invalid operation → 400", async ({ request }) => {
        const res = await request.post(`${BASE_URL}/calculations/`, {
            data: {
                operation: "WRONG_OPERATION",
                a: 1,
                b: 2
            },
            headers: { Authorization: `Bearer ${token}` }
        });

        expect(res.status()).toBe(400);
    });

});
