const MAX_DIGITS = 15;
const MAX_HISTORY = 20;
const ERROR_MESSAGE = '0으로 나눌 수 없습니다';

const exprEl = document.getElementById('expr');
const resultEl = document.getElementById('result');
const keypadEl = document.querySelector('.keypad');
const historyListEl = document.getElementById('history-list');
const historyEmptyEl = document.getElementById('history-empty');
const historyClearEl = document.getElementById('history-clear');

// tokens: 확정된 숫자와 연산자가 번갈아 들어감. current: 지금 입력 중인 숫자('' 이면 연산자 직후)
const state = {
  tokens: [],
  current: '0',
  justEvaluated: false,
  lastExpression: '',
  error: false,
};

let history = [];

/* ---------- 계산 ---------- */

function isOperator(token) {
  return token === '+' || token === '−' || token === '×' || token === '÷';
}

// eval 없이 두 단계로 계산: × ÷ 먼저, 그다음 + −
function compute(tokens) {
  const values = [Number(tokens[0])];
  const ops = [];

  for (let i = 1; i < tokens.length; i += 2) {
    const op = tokens[i];
    const n = Number(tokens[i + 1]);

    if (op === '×' || op === '÷') {
      if (op === '÷' && n === 0) throw new Error('divide-by-zero');
      const left = values.pop();
      values.push(op === '×' ? left * n : left / n);
    } else {
      ops.push(op);
      values.push(n);
    }
  }

  let result = values[0];
  ops.forEach((op, i) => {
    result = op === '+' ? result + values[i + 1] : result - values[i + 1];
  });

  // 0.1 + 0.2 같은 부동소수 오차 정리
  return parseFloat(result.toPrecision(12));
}

/* ---------- 표시 ---------- */

function formatNumber(str) {
  if (str === '' || /e/i.test(str)) return str;

  const negative = str.startsWith('-');
  const body = negative ? str.slice(1) : str;
  const [intPart, fracPart] = body.split('.');
  const grouped = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  const formatted = fracPart === undefined ? grouped : `${grouped}.${fracPart}`;

  return negative ? `−${formatted}` : formatted;
}

function formatTokens(tokens) {
  return tokens.map((t) => (isOperator(t) ? t : formatNumber(t))).join(' ');
}

function render() {
  resultEl.classList.remove('is-long', 'is-longer', 'is-error');

  if (state.error) {
    exprEl.textContent = state.lastExpression;
    resultEl.textContent = ERROR_MESSAGE;
    resultEl.classList.add('is-error');
    return;
  }

  if (state.justEvaluated) {
    exprEl.textContent = state.lastExpression;
  } else {
    exprEl.textContent = formatTokens(state.tokens);
  }

  // 연산자 직후에는 바로 앞 숫자를 계속 보여 줌
  const shown = state.current !== '' ? state.current : state.tokens[state.tokens.length - 2];
  const text = formatNumber(shown);
  resultEl.textContent = text;

  if (text.length > 14) resultEl.classList.add('is-longer');
  else if (text.length > 10) resultEl.classList.add('is-long');
}

/* ---------- 입력 ---------- */

function reset() {
  state.tokens = [];
  state.current = '0';
  state.justEvaluated = false;
  state.lastExpression = '';
  state.error = false;
}

function digitCount(str) {
  return str.replace(/[^0-9]/g, '').length;
}

function trimNumber(str) {
  return str.endsWith('.') ? str.slice(0, -1) : str;
}

function inputDigit(d) {
  if (state.error || state.justEvaluated) reset();

  if (state.current === '0') {
    state.current = d;
  } else if (state.current === '-0') {
    state.current = `-${d}`;
  } else if (digitCount(state.current) < MAX_DIGITS) {
    state.current += d;
  }
}

function inputDot() {
  if (state.error || state.justEvaluated) reset();

  if (state.current === '') {
    state.current = '0.';
  } else if (!state.current.includes('.') && digitCount(state.current) < MAX_DIGITS) {
    state.current += '.';
  }
}

function inputOperator(op) {
  if (state.error) reset();
  state.justEvaluated = false;

  if (state.current === '') {
    // 연산자를 연달아 누르면 마지막 연산자만 교체
    state.tokens[state.tokens.length - 1] = op;
    return;
  }

  state.tokens.push(trimNumber(state.current), op);
  state.current = '';
}

function evaluate() {
  if (state.error || state.justEvaluated) return;

  const tokens = [...state.tokens];
  if (state.current === '') tokens.pop();
  else tokens.push(trimNumber(state.current));

  // 연산자가 없는 식은 계산할 것이 없음
  if (tokens.length < 3) return;

  const expression = `${formatTokens(tokens)} =`;

  try {
    const result = String(compute(tokens));
    addHistory(expression, result);

    state.tokens = [];
    state.current = result;
    state.justEvaluated = true;
    state.lastExpression = expression;
  } catch {
    state.error = true;
    state.lastExpression = expression;
  }
}

function backspace() {
  if (state.error || state.justEvaluated) {
    reset();
    return;
  }

  if (state.current !== '') {
    state.current = state.current.slice(0, -1);
    if (state.current === '' || state.current === '-') {
      state.current = state.tokens.length ? '' : '0';
    }
  } else if (state.tokens.length) {
    state.tokens.pop();
    state.current = state.tokens.pop();
  }
}

function handleAction(action, value) {
  switch (action) {
    case 'digit': inputDigit(value); break;
    case 'dot': inputDot(); break;
    case 'op': inputOperator(value); break;
    case 'equals': evaluate(); break;
    case 'clear': reset(); break;
    case 'backspace': backspace(); break;
  }
  render();
}

/* ---------- 기록 ---------- */

function addHistory(expression, result) {
  history.unshift({ expression, result });
  history = history.slice(0, MAX_HISTORY);
  renderHistory();
}

function renderHistory() {
  historyListEl.replaceChildren(
    ...history.map((entry, index) => {
      const li = document.createElement('li');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'history-item';
      button.dataset.index = index;
      button.setAttribute('aria-label', `${entry.expression} ${formatNumber(entry.result)}, 결과 불러오기`);

      const expr = document.createElement('span');
      expr.className = 'history-expr';
      expr.textContent = entry.expression;

      const result = document.createElement('span');
      result.className = 'history-result';
      result.textContent = formatNumber(entry.result);

      button.append(expr, result);
      li.append(button);
      return li;
    }),
  );

  historyEmptyEl.hidden = history.length > 0;
  historyClearEl.disabled = history.length === 0;
}

historyListEl.addEventListener('click', (e) => {
  const item = e.target.closest('.history-item');
  if (!item) return;

  const entry = history[Number(item.dataset.index)];
  reset();
  state.current = entry.result;
  state.justEvaluated = true;
  state.lastExpression = entry.expression;
  render();
});

historyClearEl.addEventListener('click', () => {
  history = [];
  renderHistory();
});

/* ---------- 버튼 · 키보드 ---------- */

keypadEl.addEventListener('click', (e) => {
  const key = e.target.closest('.key');
  if (!key) return;

  handleAction(key.dataset.action, key.dataset.value);

  // 마우스로 누른 버튼에 포커스가 남으면 키보드 Enter가 그 버튼을 다시 누르게 됨
  if (e.detail > 0) key.blur();
});

const KEY_MAP = {
  '+': ['op', '+'],
  '-': ['op', '−'],
  '*': ['op', '×'],
  '/': ['op', '÷'],
  '.': ['dot'],
  '=': ['equals'],
  Enter: ['equals'],
  Escape: ['clear'],
  Delete: ['clear'],
  Backspace: ['backspace'],
};

function flashKey(action, value) {
  const selector = value === undefined
    ? `.key[data-action="${action}"]`
    : `.key[data-action="${action}"][data-value="${value}"]`;
  const key = keypadEl.querySelector(selector);
  if (!key) return;

  key.classList.add('is-pressed');
  setTimeout(() => key.classList.remove('is-pressed'), 120);
}

document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey || e.altKey) return;

  // 포커스된 버튼의 Enter·Space는 브라우저 기본 동작(버튼 누르기)에 맡김
  const onButton = e.target instanceof Element && e.target.closest('button');
  if ((e.key === 'Enter' || e.key === ' ') && onButton) return;

  let mapped;
  if (/^[0-9]$/.test(e.key)) mapped = ['digit', e.key];
  else mapped = KEY_MAP[e.key];
  if (!mapped) return;

  e.preventDefault();
  const [action, value] = mapped;
  flashKey(action, value);
  handleAction(action, value);
});

render();
renderHistory();
