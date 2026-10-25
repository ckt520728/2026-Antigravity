// 數學內容包：三角函數的特殊角值與象限符號
// 一條鏈固定 4 格：函數 → 角度 → 等號 → 精確函數值。
// 所有亂數只使用傳入的 rng；誘答對準正餘弦混淆、特殊角值、象限符號與 tan 不存在。
import { pick, weighted } from '../../engine.js';

export const FUNCTIONS = ['sin', 'cos', 'tan'];

// 0°～330° 的特殊角；值一律用精確根號與分數，不用小數近似。
export const ANGLE_VALUES = {
  0:   { sin: '0',       cos: '1',       tan: '0' },
  30:  { sin: '1/2',     cos: '√3/2',    tan: '√3/3' },
  45:  { sin: '√2/2',    cos: '√2/2',    tan: '1' },
  60:  { sin: '√3/2',    cos: '1/2',     tan: '√3' },
  90:  { sin: '1',       cos: '0',       tan: '不存在' },
  120: { sin: '√3/2',    cos: '-1/2',    tan: '-√3' },
  135: { sin: '√2/2',    cos: '-√2/2',   tan: '-1' },
  150: { sin: '1/2',     cos: '-√3/2',   tan: '-√3/3' },
  180: { sin: '0',       cos: '-1',      tan: '0' },
  210: { sin: '-1/2',    cos: '-√3/2',   tan: '√3/3' },
  225: { sin: '-√2/2',   cos: '-√2/2',   tan: '1' },
  240: { sin: '-√3/2',   cos: '-1/2',    tan: '√3' },
  270: { sin: '-1',      cos: '0',       tan: '不存在' },
  300: { sin: '-√3/2',   cos: '1/2',     tan: '-√3' },
  315: { sin: '-√2/2',   cos: '√2/2',    tan: '-1' },
  330: { sin: '-1/2',    cos: '√3/2',    tan: '-√3/3' },
};

export const ANGLES = Object.keys(ANGLE_VALUES).map((a) => `${a}°`);
export const EQUATIONS = Object.entries(ANGLE_VALUES).flatMap(([angle, funcs]) =>
  FUNCTIONS.map((fn) => ({ fn, angle: `${angle}°`, value: funcs[fn] })),
);
const EQUATION_MAP = new Map(EQUATIONS.map((e) => [`${e.fn}|${e.angle}`, e.value]));
const VALUE_POOL = [...new Set(EQUATIONS.map((e) => e.value))];
const VALID_PREFIXES = new Set();
for (const e of EQUATIONS) {
  const parts = [e.fn, e.angle, '=', e.value];
  for (let n = 1; n <= 4; n++) VALID_PREFIXES.add(parts.slice(0, n).join('|'));
}

// 每個誘答都能由 check() 獨立診斷；kind 只用於測試覆蓋確認。
export const TRAPS = [
  { kind: 'sin_cos_swap', parts: ['sin', '30°', '=', '√3/2'] },
  { kind: 'sin_cos_swap', parts: ['cos', '30°', '=', '1/2'] },
  { kind: 'special_value_mixup', parts: ['sin', '45°', '=', '√3/2'] },
  { kind: 'special_value_mixup', parts: ['tan', '60°', '=', '√3/3'] },
  { kind: 'quadrant_sign', parts: ['sin', '210°', '=', '1/2'] },
  { kind: 'quadrant_sign', parts: ['cos', '120°', '=', '1/2'] },
  { kind: 'tan_undefined', parts: ['tan', '90°', '=', '0'] },
  { kind: 'tan_undefined', parts: ['tan', '270°', '=', '0'] },
];

function tagOf(text) {
  if (FUNCTIONS.includes(text)) return 'function';
  if (text === '=') return 'equals';
  if (/^\d+°$/.test(text)) return 'angle';
  return 'value';
}
const toTiles = (parts) => parts.map((text) => ({ text, tag: tagOf(text) }));
const partsOf = (tiles) => tiles.map((t) => String(t.text).trim());
const keyOf = (parts) => parts.join('|');
const equationText = (fn, angle, value) => `${fn} ${angle} = ${value}`;
const oppositeValue = (value) => {
  if (value === '0' || value === '不存在') return null;
  return value.startsWith('-') ? value.slice(1) : `-${value}`;
};

function quadrantOf(angle) {
  const n = Number.parseInt(angle, 10);
  if ([0, 90, 180, 270].includes(n)) return '坐標軸上';
  if (n < 90) return '第一象限';
  if (n < 180) return '第二象限';
  if (n < 270) return '第三象限';
  return '第四象限';
}

export default {
  id: 'math/trig',
  subject: '數學',
  title: '三角函數連線',
  unit: '高中一年級　特殊角值與象限符號',
  grade: 10,
  board: { cols: 8, rows: 6 },
  minLen: 4,
  maxLen: 4,
  searchMaxLen: 4,
  plants: [3, 4],
  refillPlantProb: 0.55,
  instructions: '依序串出「函數 → 角度 → = → 函數值」，例如 sin → 30° → = → 1/2；也要判斷象限負號，以及 tan 90°、tan 270° 不存在。',
  hintStrategy: '先找 sin、cos 或 tan，再接角度與等號；最後先判斷象限正負，回想特殊角的精確值。',
  misconceptions: {
    sin_cos_swap: '正弦與餘弦混淆：把同一角度的 sin、cos 值互換',
    special_value_mixup: '特殊角函數值記錯，或把另一個特殊角的值搬過來',
    quadrant_sign: '象限正負錯誤：只記參考角大小，忽略函數在該象限的正負',
    tan_undefined: '誤把 tan 90° 或 tan 270° 當成有限值；此時 cos = 0，不能除以 0',
    invalid_relation: '關係順序錯誤：要依序是函數、角度、等號、函數值',
    short: '不足 4 格（可能手滑，不計入）',
  },
  makeTile(rng) {
    const role = weighted(rng, [['function', 3], ['angle', 3], ['equals', 1], ['value', 3]]);
    if (role === 'function') return toTiles([pick(rng, FUNCTIONS)])[0];
    if (role === 'angle') return toTiles([pick(rng, ANGLES)])[0];
    if (role === 'equals') return toTiles(['='])[0];
    return toTiles([pick(rng, VALUE_POOL)])[0];
  },
  plant(rng) {
    const e = pick(rng, EQUATIONS);
    return toTiles([e.fn, e.angle, '=', e.value]);
  },
  plantTrap(rng) {
    return toTiles(pick(rng, TRAPS).parts);
  },
  canExtend(tiles) {
    return VALID_PREFIXES.has(keyOf(partsOf(tiles)));
  },
  check(tiles) {
    const parts = partsOf(tiles);
    if (parts.length < 4) {
      return { ok: false, kind: 'short', counted: false, reason: `只選了 ${parts.length} 格，要串滿 4 格：函數 → 角度 → = → 函數值` };
    }
    if (parts.length > 4) {
      return { ok: false, kind: 'invalid_relation', counted: true, reason: '一條三角函數等式只能是 4 格：函數 → 角度 → = → 函數值' };
    }
    const [fn, angle, equals, actual] = parts;
    const correct = EQUATION_MAP.get(`${fn}|${angle}`);
    if (equals !== '=' || !FUNCTIONS.includes(fn) || correct === undefined) {
      return { ok: false, kind: 'invalid_relation', counted: true, reason: '順序要是「函數 → 角度 → = → 函數值」，例如 sin → 30° → = → 1/2' };
    }
    if (actual === correct) {
      return { ok: true, gain: 2, summary: equationText(fn, angle, correct) };
    }
    if (fn === 'tan' && correct === '不存在') {
      return {
        ok: false, kind: 'tan_undefined', counted: true,
        reason: `${equationText(fn, angle, correct)}，不是 ${actual}：因為 cos ${angle} = 0，tan 不能除以 0`,
      };
    }
    if (fn !== 'tan') {
      const other = fn === 'sin' ? 'cos' : 'sin';
      const otherValue = EQUATION_MAP.get(`${other}|${angle}`);
      if (actual === otherValue && actual !== correct) {
        return {
          ok: false, kind: 'sin_cos_swap', counted: true,
          reason: `${fn} ${angle} 應為 ${correct}；${actual} 是 ${other} ${angle} 的值，正弦與餘弦不要互換`,
        };
      }
    }
    if (actual === oppositeValue(correct)) {
      const sign = correct.startsWith('-') ? '負' : '正';
      return {
        ok: false, kind: 'quadrant_sign', counted: true,
        reason: `${angle} 在${quadrantOf(angle)}，${fn} 為${sign}，所以 ${fn} ${angle} 應為 ${correct}，不是 ${actual}`,
      };
    }
    const otherAngle = EQUATIONS.find((e) => e.fn === fn && e.angle !== angle && e.value === actual);
    if (otherAngle) {
      return {
        ok: false, kind: 'special_value_mixup', counted: true,
        reason: `${actual} 是 ${fn} ${otherAngle.angle} 的值；${fn} ${angle} 應為 ${correct}`,
      };
    }
    return {
      ok: false, kind: 'special_value_mixup', counted: true,
      reason: `${fn} ${angle} 的函數值不是 ${actual}，應為 ${correct}`,
    };
  },
  preview(tiles) {
    return partsOf(tiles).join(' ');
  },
};
