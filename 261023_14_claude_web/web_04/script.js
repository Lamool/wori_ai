"use strict";

const OPERATORS = ["+", "−", "×", "÷"];
const MAX_DIGITS = 15;
const MAX_HISTORY = 50;
const STORAGE_KEY = "calc-tape";
const DIV_ZERO_MESSAGE = "0으로 나눌 수 없어요";
const OVERFLOW_MESSAGE = "숫자가 너무 커요";

const els = {
  expr: document.getElementById("expr"),
  value: document.getElementById("value"),
  keys: document.getElementById("keys"),
  tape: document.getElementById("tape"),
  tapeList: document.getElementById("tapeList"),
  tapeEmpty: document.getElementById("tapeEmpty"),
  tapeClear: document.getElementById("tapeClear"),
};

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

// 입력 상태: tokens는 완성된 숫자와 연산자, current는 입력 중인 숫자
let state = freshState();
let history = loadHistory();

function freshState() {
  return { tokens: [], current: "0", justEvaluated: false, lastExpr: "", error: "" };
}

/* ---------- 계산 ---------- */

class CalcError extends Error {}

// 곱셈·나눗셈을 먼저 묶고, 덧셈·뺄셈을 나중에 처리
function evaluate(tokens) {
  const terms = [Number(tokens[0])];
  const addOps = [];

  for (let i = 1; i < tokens.length; i += 2) {
    const op = tokens[i];
    const n = Number(tokens[i + 1]);
    const last = terms.length - 1;

    if (op === "×") {
      terms[last] *= n;
    } else if (op === "÷") {
      if (n === 0) throw new CalcError(DIV_ZERO_MESSAGE);
      terms[last] /= n;
    } else {
      addOps.push(op);
      terms.push(n);
    }
  }

  let result = terms[0];
  addOps.forEach((op, i) => {
    result = op === "+" ? result + terms[i + 1] : result - terms[i + 1];
  });

  if (!Number.isFinite(result)) throw new CalcError(OVERFLOW_MESSAGE);
  return result;
}

// 0.1 + 0.2 같은 부동소수점 오차를 12자리에서 정리
function formatNumber(x) {
  let r = parseFloat(x.toPrecision(12));
  if (Object.is(r, -0)) r = 0;
  const abs = Math.abs(r);
  if (abs >= 1e15 || (abs !== 0 && abs < 1e-6)) {
    return r.toExponential(6).replace(/\.?0+e/, "e");
  }
  return String(r);
}

function normalize(numStr) {
  return formatNumber(Number(numStr));
}

/* ---------- 입력 처리 ---------- */

function inputDigit(d) {
  if (state.error || state.justEvaluated) state = freshState();

  const { current } = state;
  if (current === "0") state.current = d;
  else if (current === "-0") state.current = "-" + d;
  else if (current.replace(/[-.]/g, "").length >= MAX_DIGITS) return;
  else state.current = current + d;
}

function inputDot() {
  if (state.error || state.justEvaluated) state = freshState();

  if (state.current === "") state.current = "0.";
  else if (!state.current.includes(".") && !state.current.includes("e")) state.current += ".";
}

function inputOperator(op) {
  if (state.error) return;
  state.justEvaluated = false;

  if (state.current === "") {
    // 연산자를 연달아 누르면 마지막 연산자를 바꿈
    if (state.tokens.length) state.tokens[state.tokens.length - 1] = op;
    return;
  }

  state.tokens.push(normalize(state.current), op);
  state.current = "";
}

function percent() {
  if (state.error || state.current === "") return;
  state.current = formatNumber(Number(state.current) / 100);
}

function negate() {
  if (state.error || state.current === "" || Number(state.current) === 0) return;
  state.current = state.current.startsWith("-") ? state.current.slice(1) : "-" + state.current;
}

function backspace() {
  if (state.error) {
    state = freshState();
    return;
  }
  if (state.justEvaluated) return;

  if (state.current === "") {
    if (!state.tokens.length) return;
    state.tokens.pop();
    state.current = state.tokens.pop();
    return;
  }

  state.current = state.current.slice(0, -1);
  if (state.current === "" || state.current === "-") {
    state.current = state.tokens.length ? "" : "0";
  }
}

function clearAll() {
  state = freshState();
}

function equals() {
  if (state.error || state.justEvaluated) return;

  const tokens = [...state.tokens];
  if (state.current !== "") tokens.push(normalize(state.current));
  else tokens.pop(); // 끝에 남은 연산자는 버림

  if (tokens.length < 3) return;

  const expr = formatExpr(tokens);
  try {
    const result = formatNumber(evaluate(tokens));
    addHistory({ expr, result });
    state = { tokens: [], current: result, justEvaluated: true, lastExpr: expr + " =", error: "" };
  } catch (err) {
    if (!(err instanceof CalcError)) throw err;
    state = { ...freshState(), lastExpr: expr + " =", error: err.message };
  }
}

function press(key) {
  if (/^[0-9]$/.test(key)) inputDigit(key);
  else if (key === ".") inputDot();
  else if (OPERATORS.includes(key)) inputOperator(key);
  else if (key === "%") percent();
  else if (key === "±") negate();
  else if (key === "Backspace") backspace();
  else if (key === "C") clearAll();
  else if (key === "=") equals();
  else return;
  render();
}

/* ---------- 표시 ---------- */

// 정수 부분에 천 단위 쉼표
function displayNumber(numStr) {
  if (numStr.includes("e")) return numStr;
  const [int, frac] = numStr.split(".");
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return frac === undefined ? grouped : grouped + "." + frac;
}

function formatExpr(tokens) {
  return tokens.map((t) => (OPERATORS.includes(t) ? t : displayNumber(t))).join(" ");
}

function render() {
  const { tokens, current, justEvaluated, lastExpr, error } = state;

  els.expr.textContent = justEvaluated || error ? lastExpr : formatExpr(tokens);

  els.value.classList.toggle("is-error", Boolean(error));
  if (error) {
    els.value.textContent = error;
    els.value.style.fontSize = "";
    return;
  }

  const shown = current !== "" ? current : tokens[tokens.length - 2] ?? "0";
  const text = displayNumber(shown);
  els.value.textContent = text;
  // 긴 숫자는 표시창 폭에 맞게 글자를 줄임
  els.value.style.fontSize = text.length > 11 ? `${Math.max(1.1, (2.5 * 11) / text.length)}rem` : "";
}

/* ---------- 테이프 기록 ---------- */

function loadHistory() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(saved) ? saved : [];
  } catch {
    return [];
  }
}

function saveHistory() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  } catch {
    // 저장이 막힌 환경에서도 계산기는 그대로 동작
  }
}

function addHistory(entry) {
  history.push(entry);
  if (history.length > MAX_HISTORY) history = history.slice(-MAX_HISTORY);
  saveHistory();
  renderTape(true);
}

function createTapeLine({ expr, result }, index) {
  const li = document.createElement("li");
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "tape-line";
  btn.dataset.index = String(index);
  btn.setAttribute("aria-label", `${expr} = ${displayNumber(result)}, 이 결과 다시 쓰기`);

  const exprEl = document.createElement("span");
  exprEl.className = "tape-line__expr";
  exprEl.textContent = expr;

  const resultEl = document.createElement("span");
  resultEl.className = "tape-line__result";
  resultEl.textContent = "= " + displayNumber(result);

  btn.append(exprEl, resultEl);
  li.append(btn);
  return li;
}

function renderTape(feed = false) {
  els.tapeEmpty.hidden = history.length > 0;
  els.tapeClear.hidden = history.length === 0;
  els.tapeList.replaceChildren(...history.map(createTapeLine));
  els.tape.scrollTop = els.tape.scrollHeight;

  if (feed && !reduceMotion.matches && els.tapeList.lastElementChild) {
    // 새 줄 높이만큼 내려두었다가 슬롯에서 밀려 올라오게 함
    const list = els.tapeList;
    list.classList.remove("is-feeding");
    list.style.transform = `translateY(${list.lastElementChild.offsetHeight}px)`;
    list.getBoundingClientRect();
    list.classList.add("is-feeding");
    list.style.transform = "";
  }
}

function reuseResult(index) {
  const entry = history[index];
  if (!entry) return;

  if (state.error || state.justEvaluated || !state.tokens.length) {
    state = { ...freshState(), current: entry.result, justEvaluated: true, lastExpr: entry.expr + " =" };
  } else {
    state.current = entry.result;
  }
  render();
}

/* ---------- 이벤트 ---------- */

els.keys.addEventListener("click", (e) => {
  const btn = e.target.closest(".key");
  if (btn) press(btn.dataset.key);
});

els.tapeList.addEventListener("click", (e) => {
  const line = e.target.closest(".tape-line");
  if (line) reuseResult(Number(line.dataset.index));
});

els.tapeClear.addEventListener("click", () => {
  history = [];
  saveHistory();
  renderTape();
});

const KEYBOARD_MAP = {
  "+": "+",
  "-": "−",
  "*": "×",
  x: "×",
  "/": "÷",
  "%": "%",
  ".": ".",
  ",": ".",
  "=": "=",
  Enter: "=",
  Backspace: "Backspace",
  Escape: "C",
  Delete: "C",
};

document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;

  const key = /^[0-9]$/.test(e.key) ? e.key : KEYBOARD_MAP[e.key];
  if (!key) return;

  // 포커스된 버튼에서 Enter가 두 번 눌리는 것을 막음
  e.preventDefault();
  press(key);
  flashKey(key);
});

function flashKey(key) {
  const btn = els.keys.querySelector(`[data-key="${CSS.escape(key)}"]`);
  if (!btn) return;
  btn.classList.add("is-pressed");
  setTimeout(() => btn.classList.remove("is-pressed"), 110);
}

render();
renderTape();
