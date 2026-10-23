const statusEl = document.getElementById("status");
const logEl = document.getElementById("log");
const lineInput = document.getElementById("lineInput");
const multiInput = document.getElementById("multiInput");
const modeLineBtn = document.getElementById("modeLine");
const modeMultiBtn = document.getElementById("modeMulti");
const keypadEl = document.getElementById("keypad");
const keys = keypadEl.querySelectorAll(".key");

let pyodide = null;
let mode = "line";       // "line" | "multi"
let inputHistory = [];   // 한 줄 모드에서 실행한 입력들
let historyIndex = 0;

// ---------- 파이썬 준비 ----------
const SETUP_CODE = `
from pyodide.code import eval_code
def _calc_run(src):
    r = eval_code(src, globals())
    return None if r is None else repr(r)
`;

function setReady(ready) {
  lineInput.disabled = !ready;
  multiInput.disabled = !ready;
  keys.forEach((k) => (k.disabled = !ready));
}

async function initPython() {
  setReady(false);
  try {
    pyodide = await loadPyodide();
    pyodide.setStdout({ batched: (text) => appendLog(text, "out") });
    pyodide.setStderr({ batched: (text) => appendLog(text, "err") });
    pyodide.runPython(SETUP_CODE);
    statusEl.textContent = "준비됨";
    statusEl.className = "status ready";
    setReady(true);
    activeInput().focus();
  } catch (e) {
    statusEl.textContent = "불러오기 실패";
    statusEl.className = "status error";
    appendLog("파이썬을 불러오지 못했습니다. 인터넷 연결을 확인하고 새로고침하세요.\n" + e, "err");
  }
}

// ---------- 실행 ----------
function runCode() {
  if (!pyodide) return;
  const input = activeInput();
  const src = input.value;
  if (!src.trim()) return;

  appendLog(formatInput(src), "in");

  if (mode === "line") {
    inputHistory.push(src);
    historyIndex = inputHistory.length;
  }

  const runner = pyodide.globals.get("_calc_run");
  try {
    const result = runner(src);
    if (result !== undefined && result !== null) appendLog(result, "result");
  } catch (e) {
    appendLog(lastErrorLine(e), "err");
  } finally {
    runner.destroy();
  }

  input.value = "";
  input.focus();
}

// traceback 전체 대신 마지막 줄만 (예: ZeroDivisionError: division by zero)
function lastErrorLine(e) {
  const lines = String(e.message || e).trim().split("\n");
  return lines[lines.length - 1];
}

function formatInput(src) {
  return src
    .split("\n")
    .map((line, i) => (i === 0 ? ">>> " : "... ") + line)
    .join("\n");
}

function appendLog(text, kind) {
  const div = document.createElement("div");
  div.className = "entry " + kind;
  div.textContent = text;
  logEl.appendChild(div);
  logEl.scrollTop = logEl.scrollHeight;
}

// ---------- 입력 모드 ----------
function activeInput() {
  return mode === "line" ? lineInput : multiInput;
}

function setMode(next) {
  if (next === mode) return;
  const carried = activeInput().value;
  mode = next;
  lineInput.classList.toggle("hidden", mode !== "line");
  multiInput.classList.toggle("hidden", mode !== "multi");
  modeLineBtn.classList.toggle("active", mode === "line");
  modeMultiBtn.classList.toggle("active", mode === "multi");
  // 한 줄 입력에는 줄바꿈이 들어갈 수 없으므로 첫 줄만 옮김
  activeInput().value = mode === "line" ? carried.split("\n")[0] : carried;
  activeInput().focus();
}

modeLineBtn.addEventListener("click", () => setMode("line"));
modeMultiBtn.addEventListener("click", () => setMode("multi"));

// ---------- 키보드 ----------
lineInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    runCode();
  } else if (e.key === "ArrowUp") {
    if (historyIndex > 0) {
      e.preventDefault();
      historyIndex--;
      lineInput.value = inputHistory[historyIndex];
    }
  } else if (e.key === "ArrowDown") {
    if (historyIndex < inputHistory.length) {
      e.preventDefault();
      historyIndex++;
      lineInput.value = inputHistory[historyIndex] ?? "";
    }
  }
});

multiInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    runCode();
  } else if (e.key === "Tab") {
    e.preventDefault();
    insertText("    ");
  }
});

// ---------- 키패드 ----------
function insertText(text) {
  const input = activeInput();
  const start = input.selectionStart ?? input.value.length;
  const end = input.selectionEnd ?? input.value.length;
  input.value = input.value.slice(0, start) + text + input.value.slice(end);
  const pos = start + text.length;
  input.focus();
  input.setSelectionRange(pos, pos);
}

function backspace() {
  const input = activeInput();
  const start = input.selectionStart ?? input.value.length;
  const end = input.selectionEnd ?? input.value.length;
  if (start === end && start === 0) return input.focus();
  const from = start === end ? start - 1 : start;
  input.value = input.value.slice(0, from) + input.value.slice(end);
  input.focus();
  input.setSelectionRange(from, from);
}

// 버튼을 눌러도 입력창의 커서(포커스)를 잃지 않도록
keypadEl.addEventListener("mousedown", (e) => {
  if (e.target.closest(".key")) e.preventDefault();
});

keypadEl.addEventListener("click", (e) => {
  const key = e.target.closest(".key");
  if (!key || key.disabled) return;

  if (key.dataset.insert !== undefined) {
    insertText(key.dataset.insert);
  } else if (key.dataset.action === "run") {
    runCode();
  } else if (key.dataset.action === "clear") {
    activeInput().value = "";
    activeInput().focus();
  } else if (key.dataset.action === "backspace") {
    backspace();
  }
});

document.getElementById("clearLog").addEventListener("click", () => {
  logEl.innerHTML = "";
  activeInput().focus();
});

initPython();
