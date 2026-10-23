const expressionEl = document.getElementById("expression");
const resultEl = document.getElementById("result");
const historyEl = document.getElementById("history");
const historyListEl = document.getElementById("historyList");
const historyEmptyEl = document.getElementById("historyEmpty");

const OPERATORS = ["+", "−", "×", "÷"];
const HISTORY_KEY = "calc-history";
const THEME_KEY = "calc-theme";

let expr = "";          // 현재 입력 중인 수식
let justEvaluated = false;
let history = loadHistory();

// ---------- 수식 계산 (eval 없이 직접 파싱) ----------

function tokenize(input) {
  const tokens = [];
  let i = 0;
  while (i < input.length) {
    const ch = input[i];
    if (/[0-9.]/.test(ch)) {
      let num = "";
      while (i < input.length && /[0-9.]/.test(input[i])) num += input[i++];
      if ((num.match(/\./g) || []).length > 1) throw new Error("잘못된 숫자");
      tokens.push({ type: "num", value: parseFloat(num) });
      if (input[i] === "%") {
        tokens[tokens.length - 1].value /= 100;
        i++;
      }
      continue;
    }
    if (OPERATORS.includes(ch) || ch === "(" || ch === ")") {
      tokens.push({ type: "op", value: ch });
      i++;
      continue;
    }
    throw new Error("알 수 없는 문자");
  }
  return tokens;
}

// 재귀 하강 파서: expr := term (( + | − ) term)*
function parse(tokens) {
  let pos = 0;
  const peek = () => tokens[pos];
  const next = () => tokens[pos++];

  function parseExpr() {
    let value = parseTerm();
    while (peek() && (peek().value === "+" || peek().value === "−")) {
      const op = next().value;
      const rhs = parseTerm();
      value = op === "+" ? value + rhs : value - rhs;
    }
    return value;
  }

  function parseTerm() {
    let value = parseFactor();
    while (peek() && (peek().value === "×" || peek().value === "÷")) {
      const op = next().value;
      const rhs = parseFactor();
      if (op === "÷" && rhs === 0) throw new Error("0으로 나눌 수 없습니다");
      value = op === "×" ? value * rhs : value / rhs;
    }
    return value;
  }

  function parseFactor() {
    const tok = next();
    if (!tok) throw new Error("수식이 완전하지 않습니다");
    if (tok.type === "num") return tok.value;
    if (tok.value === "−") return -parseFactor();
    if (tok.value === "+") return parseFactor();
    if (tok.value === "(") {
      const value = parseExpr();
      if (!next() || tokens[pos - 1].value !== ")") throw new Error("괄호가 닫히지 않았습니다");
      // 괄호 뒤 % 처리: (50)% 형태는 지원하지 않음
      return value;
    }
    throw new Error("잘못된 수식");
  }

  const result = parseExpr();
  if (pos < tokens.length) throw new Error("잘못된 수식");
  return result;
}

function evaluate(input) {
  // 닫히지 않은 괄호는 자동으로 닫아줌
  const open = (input.match(/\(/g) || []).length - (input.match(/\)/g) || []).length;
  const closed = input + ")".repeat(Math.max(0, open));
  const value = parse(tokenize(closed));
  if (!Number.isFinite(value)) throw new Error("계산할 수 없습니다");
  return roundResult(value);
}

function roundResult(n) {
  // 부동소수점 오차 보정 (예: 0.1 + 0.2)
  return parseFloat(n.toPrecision(12));
}

// ---------- 표시 ----------

function formatNumber(n) {
  if (Math.abs(n) >= 1e15 || (Math.abs(n) < 1e-9 && n !== 0)) {
    return n.toExponential(6).replace(/\.?0+e/, "e");
  }
  const [int, dec] = String(n).split(".");
  const intFormatted = Number(int).toLocaleString("en-US");
  return dec !== undefined ? `${intFormatted}.${dec}` : intFormatted;
}

function formatExpr(s) {
  // 수식 안의 숫자에 천 단위 쉼표 적용
  return s.replace(/\d+(\.\d*)?/g, (m) => {
    const [int, dec] = m.split(".");
    const intFormatted = Number(int).toLocaleString("en-US");
    return dec !== undefined ? `${intFormatted}.${dec}` : intFormatted;
  });
}

function setResult(text, { error = false } = {}) {
  resultEl.textContent = text;
  resultEl.classList.toggle("error", error);
  resultEl.classList.toggle("small", !error && text.length > 12);
}

function render() {
  if (justEvaluated) return;
  expressionEl.textContent = "";
  if (expr === "") {
    setResult("0");
    return;
  }
  setResult(formatExpr(expr));
  // 미리보기: 계산 가능한 상태면 결과를 위쪽에 표시
  try {
    const preview = evaluate(expr);
    if (/[+−×÷%(]/.test(expr.replace(/^−/, ""))) {
      expressionEl.textContent = "= " + formatNumber(preview);
    }
  } catch {
    /* 입력 중인 미완성 수식은 무시 */
  }
}

// ---------- 입력 처리 ----------

function lastChar() {
  return expr.slice(-1);
}

function currentNumber() {
  const m = expr.match(/[0-9.]+%?$/);
  return m ? m[0] : "";
}

function input(value) {
  if (justEvaluated) {
    // 결과 직후 숫자 입력 → 새 계산, 연산자 입력 → 결과에 이어서 계산
    if (OPERATORS.includes(value)) {
      expr = String(lastResult).replace("-", "−");
    } else {
      expr = "";
    }
    justEvaluated = false;
  }

  const last = lastChar();

  if (/[0-9]/.test(value)) {
    if (last === ")" || last === "%") expr += "×";
    if (currentNumber() === "0") expr = expr.slice(0, -1);
    if (currentNumber().replace(/\D/g, "").length >= 15) return;
    expr += value;
  } else if (value === ".") {
    if (currentNumber().includes(".")) return;
    if (last === ")" || last === "%") expr += "×";
    if (!/[0-9]/.test(lastChar())) expr += "0";
    expr += ".";
  } else if (OPERATORS.includes(value)) {
    if (expr === "" || last === "(") {
      if (value === "−") expr += "−"; // 음수 시작 허용
      return render();
    }
    if (OPERATORS.includes(last)) {
      expr = expr.slice(0, -1);
      if (expr === "" || lastChar() === "(") {
        if (value === "−") expr += "−";
        return render();
      }
    }
    if (last === ".") expr = expr.slice(0, -1);
    expr += value;
  } else if (value === "(") {
    if (/[0-9.)%]/.test(last)) expr += "×";
    expr += "(";
  } else if (value === ")") {
    const open = (expr.match(/\(/g) || []).length - (expr.match(/\)/g) || []).length;
    if (open <= 0 || OPERATORS.includes(last) || last === "(" || last === "") return;
    expr += ")";
  }
  render();
}

let lastResult = 0;

function equals() {
  if (expr === "" || justEvaluated) return;
  try {
    const value = evaluate(expr);
    const shownExpr = formatExpr(expr);
    addHistory(shownExpr, value);
    expressionEl.textContent = shownExpr + " =";
    setResult(formatNumber(value));
    lastResult = value;
    justEvaluated = true;
    expr = String(value).replace("-", "−");
  } catch (err) {
    expressionEl.textContent = formatExpr(expr);
    setResult(err.message, { error: true });
  }
}

function clearAll() {
  expr = "";
  justEvaluated = false;
  render();
}

function backspace() {
  if (justEvaluated) {
    justEvaluated = false;
    expr = "";
  } else {
    expr = expr.slice(0, -1);
  }
  render();
}

function percent() {
  justEvaluated = false;
  const num = currentNumber();
  if (!num || num.endsWith("%")) return;
  expr += "%";
  render();
}

function negate() {
  justEvaluated = false;
  const num = currentNumber();
  if (!num) {
    if (expr === "" || lastChar() === "(" || OPERATORS.includes(lastChar())) {
      input("−");
    }
    return;
  }
  const start = expr.length - num.length;
  const before = expr.slice(0, start);
  // 숫자 앞의 단항 마이너스 여부 판단
  const prev = before.slice(-1);
  const prevPrev = before.slice(-2, -1);
  const isUnaryMinus = prev === "−" && (prevPrev === "" || prevPrev === "(" || OPERATORS.includes(prevPrev));
  if (isUnaryMinus) {
    expr = before.slice(0, -1) + num;
  } else if (prev === "" || prev === "(" || OPERATORS.includes(prev)) {
    expr = before + "−" + num;
  } else {
    return;
  }
  render();
}

// ---------- 기록 ----------

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
  } catch {
    return [];
  }
}

function saveHistory() {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
  } catch {
    /* 저장 불가 환경은 무시 */
  }
}

function addHistory(expression, result) {
  history.unshift({ expression, result });
  history = history.slice(0, 50);
  saveHistory();
  renderHistory();
}

function renderHistory() {
  historyListEl.innerHTML = "";
  historyEmptyEl.style.display = history.length ? "none" : "block";
  history.forEach((item) => {
    const li = document.createElement("li");
    const e = document.createElement("div");
    e.className = "h-expr";
    e.textContent = item.expression + " =";
    const r = document.createElement("div");
    r.className = "h-result";
    r.textContent = formatNumber(item.result);
    li.append(e, r);
    li.addEventListener("click", () => {
      expr = String(item.result).replace("-", "−");
      justEvaluated = false;
      render();
    });
    historyListEl.appendChild(li);
  });
}

// ---------- 테마 ----------

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(THEME_KEY, theme);
  } catch {
    /* 무시 */
  }
}

function initTheme() {
  let saved = null;
  try {
    saved = localStorage.getItem(THEME_KEY);
  } catch {
    /* 무시 */
  }
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(saved || (prefersDark ? "dark" : "light"));
}

// ---------- 이벤트 ----------

document.querySelector(".keys").addEventListener("click", (e) => {
  const btn = e.target.closest(".key");
  if (!btn) return;
  const { value, action } = btn.dataset;
  if (value !== undefined) input(value);
  else if (action === "equals") equals();
  else if (action === "clear") clearAll();
  else if (action === "backspace") backspace();
  else if (action === "percent") percent();
  else if (action === "negate") negate();
});

const KEY_MAP = {
  "+": "+",
  "-": "−",
  "*": "×",
  x: "×",
  "/": "÷",
  "(": "(",
  ")": ")",
  ".": ".",
  ",": ".",
};

function flashKey(selector) {
  const btn = document.querySelector(selector);
  if (!btn) return;
  btn.classList.add("pressed");
  setTimeout(() => btn.classList.remove("pressed"), 100);
}

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key;
  if (/^[0-9]$/.test(k)) {
    input(k);
    flashKey(`[data-value="${k}"]`);
  } else if (KEY_MAP[k]) {
    e.preventDefault();
    input(KEY_MAP[k]);
    flashKey(`[data-value="${KEY_MAP[k]}"]`);
  } else if (k === "Enter" || k === "=") {
    e.preventDefault();
    equals();
    flashKey('[data-action="equals"]');
  } else if (k === "Backspace") {
    backspace();
    flashKey('[data-action="backspace"]');
  } else if (k === "Escape" || k === "Delete") {
    clearAll();
    flashKey('[data-action="clear"]');
  } else if (k === "%") {
    percent();
    flashKey('[data-action="percent"]');
  }
});

document.getElementById("themeToggle").addEventListener("click", () => {
  const current = document.documentElement.dataset.theme;
  applyTheme(current === "dark" ? "light" : "dark");
});

document.getElementById("historyToggle").addEventListener("click", () => {
  historyEl.classList.toggle("open");
});

document.getElementById("clearHistory").addEventListener("click", () => {
  history = [];
  saveHistory();
  renderHistory();
});

initTheme();
renderHistory();
render();
