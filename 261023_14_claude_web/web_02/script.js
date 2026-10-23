const OPS = { '+': '+', '-': '−', '*': '×', '/': '÷' };
const MAX_DIGITS = 15;
const HISTORY_KEY = 'calc-history';
const HISTORY_LIMIT = 20;

const mainEl = document.getElementById('main');
const subEl = document.getElementById('sub');
const historyList = document.getElementById('historyList');
const historyEmpty = document.getElementById('historyEmpty');

// 수식은 숫자와 연산자가 번갈아 오는 토큰 배열로 관리한다. 예: ['2', '+', '3']
let tokens = [];
let justEvaluated = false; // '=' 직후 상태
let lastExpression = '';   // '=' 직후 위쪽에 보여줄 수식
let error = false;
let history = loadHistory();

const isOp = (t) => t in OPS;
const last = () => tokens[tokens.length - 1];
const isNumberToken = (t) => t !== undefined && !isOp(t);

// ---------- 입력 처리 ----------

function startFreshIfNeeded() {
  if (justEvaluated || error) {
    tokens = [];
    justEvaluated = false;
    error = false;
  }
}

function inputDigit(d) {
  startFreshIfNeeded();
  const t = last();
  if (!isNumberToken(t)) {
    tokens.push(d);
  } else if (t === '0' || t === '-0') {
    tokens[tokens.length - 1] = t.replace('0', d);
  } else if (t.replace(/[-.]/g, '').length < MAX_DIGITS) {
    tokens[tokens.length - 1] = t + d;
  }
}

function inputDot() {
  startFreshIfNeeded();
  const t = last();
  if (!isNumberToken(t)) {
    tokens.push('0.');
  } else if (!t.includes('.')) {
    tokens[tokens.length - 1] = t + '.';
  }
}

function inputOp(op) {
  if (error) startFreshIfNeeded();
  justEvaluated = false; // 결과에 이어서 계산
  if (tokens.length === 0) tokens.push('0');
  const t = last();
  if (isOp(t)) {
    tokens[tokens.length - 1] = op;
  } else {
    if (t.endsWith('.')) tokens[tokens.length - 1] = t.slice(0, -1);
    tokens.push(op);
  }
}

function percent() {
  if (error) return;
  const t = last();
  if (!isNumberToken(t)) return;
  tokens[tokens.length - 1] = toTokenString(round(parseFloat(t) / 100));
  justEvaluated = false;
}

function negate() {
  if (error) return;
  const t = last();
  if (!isNumberToken(t)) return;
  tokens[tokens.length - 1] = t.startsWith('-') ? t.slice(1) : '-' + t;
  justEvaluated = false;
}

function backspace() {
  if (error || justEvaluated) {
    clearAll();
    return;
  }
  const t = last();
  if (t === undefined) return;
  if (isOp(t)) {
    tokens.pop();
    return;
  }
  const next = t.slice(0, -1);
  if (next === '' || next === '-') tokens.pop();
  else tokens[tokens.length - 1] = next;
}

function clearAll() {
  tokens = [];
  justEvaluated = false;
  error = false;
  lastExpression = '';
}

function equals() {
  if (error || tokens.length === 0) return;
  if (isOp(last())) tokens.pop();
  if (tokens.length < 3) return; // 연산자가 없으면 계산할 것이 없음

  const expression = formatExpression(tokens);
  const result = evaluate(tokens);
  lastExpression = expression + ' =';

  if (result === null) {
    error = true;
    tokens = [];
    return;
  }

  const resultStr = toTokenString(result);
  addHistory(expression, resultStr);
  tokens = [resultStr];
  justEvaluated = true;
}

// ---------- 계산 ----------

// 부동소수점 오차 보정 (0.1 + 0.2 → 0.3)
function round(n) {
  return parseFloat(n.toPrecision(12));
}

function toTokenString(n) {
  return Object.is(n, -0) ? '0' : String(n);
}

// eval 없이 연산자 우선순위(× ÷ 먼저, + − 나중)에 따라 계산. 0으로 나누면 null.
function evaluate(list) {
  const nums = [parseFloat(list[0])];
  const ops = [];

  for (let i = 1; i < list.length; i += 2) {
    const op = list[i];
    const n = parseFloat(list[i + 1]);
    if (op === '*' || op === '/') {
      if (op === '/' && n === 0) return null;
      const prev = nums.pop();
      nums.push(op === '*' ? prev * n : prev / n);
    } else {
      ops.push(op);
      nums.push(n);
    }
  }

  let result = nums[0];
  ops.forEach((op, i) => {
    result = op === '+' ? result + nums[i + 1] : result - nums[i + 1];
  });

  return Number.isFinite(result) ? round(result) : null;
}

// ---------- 표시 ----------

function formatNumber(t) {
  if (/e/i.test(t)) return t;
  const neg = t.startsWith('-');
  const [int, frac] = t.replace('-', '').split('.');
  const grouped = int.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  return (neg ? '-' : '') + grouped + (frac !== undefined ? '.' + frac : '');
}

function formatExpression(list) {
  return list.map((t) => (isOp(t) ? OPS[t] : formatNumber(t))).join(' ');
}

function fitText(el) {
  const len = el.textContent.length;
  el.style.fontSize = len > 18 ? '1.5rem' : len > 12 ? '2rem' : '';
}

function render() {
  mainEl.classList.toggle('is-error', error);

  if (error) {
    mainEl.textContent = '오류';
    subEl.textContent = lastExpression;
  } else {
    mainEl.textContent = tokens.length ? formatExpression(tokens) : '0';
    if (justEvaluated) {
      subEl.textContent = lastExpression;
    } else {
      // 입력 중에는 미리보기 결과를 보여준다
      const list = isOp(last()) ? tokens.slice(0, -1) : tokens;
      const preview = list.length >= 3 ? evaluate(list) : null;
      subEl.textContent = preview !== null ? '= ' + formatNumber(toTokenString(preview)) : '';
    }
  }
  fitText(mainEl);

  // 마지막 입력이 연산자면 해당 버튼 강조
  document.querySelectorAll('[data-op]').forEach((btn) => {
    btn.classList.toggle('is-active', !error && last() === btn.dataset.op);
  });
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
    // 저장소를 쓸 수 없으면 이번 세션에만 유지
  }
}

function addHistory(expression, result) {
  history.unshift({ expression, result });
  history = history.slice(0, HISTORY_LIMIT);
  saveHistory();
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = '';
  history.forEach(({ expression, result }) => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.className = 'history__item';
    btn.innerHTML = '<span class="history__expr"></span><span class="history__result"></span>';
    btn.querySelector('.history__expr').textContent = expression + ' =';
    btn.querySelector('.history__result').textContent = formatNumber(result);
    btn.addEventListener('click', () => {
      tokens = [result];
      justEvaluated = true;
      error = false;
      lastExpression = expression + ' =';
      render();
    });
    li.appendChild(btn);
    historyList.appendChild(li);
  });
  historyEmpty.hidden = history.length > 0;
}

document.getElementById('clearHistory').addEventListener('click', () => {
  history = [];
  saveHistory();
  renderHistory();
});

// ---------- 이벤트 ----------

const actions = { clear: clearAll, backspace, percent, negate, dot: inputDot, equals };

document.querySelector('.keys').addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;
  if (btn.dataset.digit) inputDigit(btn.dataset.digit);
  else if (btn.dataset.op) inputOp(btn.dataset.op);
  else if (btn.dataset.action) actions[btn.dataset.action]();
  render();
});

function flash(selector) {
  const btn = document.querySelector(selector);
  if (!btn) return;
  btn.classList.add('is-pressed');
  setTimeout(() => btn.classList.remove('is-pressed'), 100);
}

document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const k = e.key;
  let selector = null;

  if (/^\d$/.test(k)) {
    inputDigit(k);
    selector = `[data-digit="${k}"]`;
  } else if (k in OPS) {
    inputOp(k);
    selector = `[data-op="${k}"]`;
  } else if (k === 'Enter' || k === '=') {
    equals();
    selector = '[data-action="equals"]';
  } else if (k === 'Backspace') {
    backspace();
    selector = '[data-action="backspace"]';
  } else if (k === 'Escape' || k === 'Delete') {
    clearAll();
    selector = '[data-action="clear"]';
  } else if (k === '.' || k === ',') {
    inputDot();
    selector = '[data-action="dot"]';
  } else if (k === '%') {
    percent();
    selector = '[data-action="percent"]';
  } else {
    return;
  }

  e.preventDefault();
  flash(selector);
  render();
});

render();
renderHistory();
