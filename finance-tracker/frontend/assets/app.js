const API_BASE = "http://127.0.0.1:8000";

function getToken() { return localStorage.getItem("token"); }
function getUsername() { return localStorage.getItem("username") || "User"; }

async function apiRequest(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (getToken()) headers.Authorization = `Bearer ${getToken()}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();
  if (!response.ok) throw new Error(payload.detail || payload || "Request failed");
  return payload;
}

async function registerUser(data) { return apiRequest("/auth/register", { method: "POST", body: JSON.stringify(data) }); }
async function loginUser(data) { return apiRequest("/auth/login", { method: "POST", body: JSON.stringify(data) }); }
async function getTransactions() { return apiRequest("/transactions"); }
async function createTransaction(data) { return apiRequest("/transactions", { method: "POST", body: JSON.stringify(data) }); }
async function updateTransaction(id, data) { return apiRequest(`/transactions/${id}`, { method: "PUT", body: JSON.stringify(data) }); }
async function deleteTransaction(id) { return apiRequest(`/transactions/${id}`, { method: "DELETE" }); }
async function searchTransactions(q) { return apiRequest(`/transactions/search?q=${encodeURIComponent(q)}`); }
async function getBudgets() { return apiRequest("/budgets"); }
async function setBudget(data) { return apiRequest("/budgets", { method: "POST", body: JSON.stringify(data) }); }
async function getBudgetStatus() { return apiRequest("/budgets/status"); }
async function getAnalyticsSummary() { return apiRequest("/analytics/summary"); }
async function getAnalyticsByCategory() { return apiRequest("/analytics/by-category"); }
async function getAnalyticsMonthlyTrend() { return apiRequest("/analytics/monthly-trend"); }
async function getAnalyticsTopExpenses() { return apiRequest("/analytics/top-expenses"); }
async function getAiAdvice() { return apiRequest("/ai/advice", { method: "POST", body: JSON.stringify({}) }); }
async function askAiQuestion(question) { return apiRequest("/ai/question", { method: "POST", body: JSON.stringify({ question }) }); }
async function getWeeklyReport() { return apiRequest("/reports/weekly"); }
async function getMonthlyReport() { return apiRequest("/reports/monthly"); }
function getCsvReportUrl() { return `${API_BASE}/reports/export-csv`; }

function showMessage(msg, isError = false) {
  const messageNode = document.getElementById("message");
  if (!messageNode) return;
  messageNode.textContent = msg;
  messageNode.style.color = isError ? "#ff7575" : "#71ff8f";
}

function initAuthPage() {
  const tabs = document.querySelectorAll(".tab");
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  if (!tabs.length || !loginForm || !registerForm) return;

  tabs.forEach((tab) => tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    loginForm.classList.toggle("active", tab.dataset.tab === "login");
    registerForm.classList.toggle("active", tab.dataset.tab === "register");
  }));

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      await registerUser({
        username: document.getElementById("register-username").value,
        email: document.getElementById("register-email").value,
        password: document.getElementById("register-password").value,
      });
      showMessage("Registration successful. Please login.");
    } catch (err) {
      showMessage(err.message, true);
    }
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser({
        username: document.getElementById("login-username").value,
        password: document.getElementById("login-password").value,
      });
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("username", document.getElementById("login-username").value);
      window.location.href = "dashboard.html";
    } catch (err) {
      showMessage(err.message, true);
    }
  });
}

function renderContent(title, payload) {
  const content = document.getElementById("content");
  if (!content) return;
  content.innerHTML = `<h2>${title}</h2><pre>${JSON.stringify(payload, null, 2)}</pre>`;
}

function initDashboardPage() {
  const content = document.getElementById("content");
  if (!content) return;
  if (!getToken()) window.location.href = "index.html";

  document.getElementById("username-label").textContent = `Welcome, ${getUsername()}`;
  document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "index.html";
  });

  document.querySelectorAll(".sidebar button").forEach((btn) => btn.addEventListener("click", async () => {
    try {
      if (btn.dataset.view === "transactions") renderContent("Transactions", await getTransactions());
      if (btn.dataset.view === "budget") renderContent("Budget Status", await getBudgetStatus());
      if (btn.dataset.view === "analytics") {
        renderContent("Analytics", {
          summary: await getAnalyticsSummary(),
          byCategory: await getAnalyticsByCategory(),
          monthlyTrend: await getAnalyticsMonthlyTrend(),
          topExpenses: await getAnalyticsTopExpenses(),
        });
      }
      if (btn.dataset.view === "ai") renderContent("AI Advice", await getAiAdvice());
      if (btn.dataset.view === "reports") {
        renderContent("Reports", {
          weekly: await getWeeklyReport(),
          monthly: await getMonthlyReport(),
          csvExport: getCsvReportUrl(),
        });
      }
    } catch (err) {
      renderContent("Error", err.message);
    }
  }));
}

initAuthPage();
initDashboardPage();
