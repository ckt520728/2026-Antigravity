// 數學內容包：三角函數連線（特殊角值與象限符號）
import test from 'node:test';
import assert from 'node:assert/strict';
import pack, { FUNCTIONS, ANGLES, EQUATIONS, TRAPS } from '../../site/games/trig-chain/content/math/trig.js';
import { commonPackChecks } from './_packs.mjs';

const T = (...texts) => texts.map((text) => ({ text }));

test('共通檢查：plant 必成立、誘答鏈必不成立且計入誤解', () => {
  const kinds = commonPackChecks(pack);
  assert.ok(kinds.has('sin_cos_swap'), '誘答應包含 sin_cos_swap');
  assert.ok(kinds.has('special_value_mixup'), '誘答應包含 special_value_mixup');
  assert.ok(kinds.has('quadrant_sign'), '誘答應包含 quadrant_sign');
  assert.ok(kinds.has('tan_undefined'), '誘答應包含 tan_undefined');
});

test('正確等式驗證：基礎特殊角、坐標軸角與各象限符號', () => {
  assert.equal(pack.check(T('sin', '30°', '=', '1/2')).ok, true);
  assert.equal(pack.check(T('cos', '60°', '=', '1/2')).ok, true);
  assert.equal(pack.check(T('tan', '45°', '=', '1')).ok, true);
  assert.equal(pack.check(T('sin', '90°', '=', '1')).ok, true);
  assert.equal(pack.check(T('cos', '90°', '=', '0')).ok, true);
  assert.equal(pack.check(T('tan', '90°', '=', '不存在')).ok, true);
  assert.equal(pack.check(T('sin', '210°', '=', '-1/2')).ok, true);
  assert.equal(pack.check(T('cos', '120°', '=', '-1/2')).ok, true);
  assert.equal(pack.check(T('tan', '135°', '=', '-1')).ok, true);
});

test('誤解診斷與回饋文字覆蓋', () => {
  // short
  const short = pack.check(T('sin', '30°', '='));
  assert.equal(short.ok, false);
  assert.equal(short.kind, 'short');
  assert.equal(short.counted, false);

  // invalid_relation
  const inv = pack.check(T('30°', 'sin', '=', '1/2'));
  assert.equal(inv.ok, false);
  assert.equal(inv.kind, 'invalid_relation');

  // sin_cos_swap
  const swap = pack.check(T('sin', '30°', '=', '√3/2'));
  assert.equal(swap.ok, false);
  assert.equal(swap.kind, 'sin_cos_swap');
  assert.match(swap.reason, /cos 30°/);

  // quadrant_sign
  const sign = pack.check(T('sin', '210°', '=', '1/2'));
  assert.equal(sign.ok, false);
  assert.equal(sign.kind, 'quadrant_sign');
  assert.match(sign.reason, /第三象限/);

  // tan_undefined
  const undef = pack.check(T('tan', '90°', '=', '0'));
  assert.equal(undef.ok, false);
  assert.equal(undef.kind, 'tan_undefined');
  assert.match(undef.reason, /不存在/);

  // special_value_mixup
  const mix = pack.check(T('sin', '45°', '=', '√3/2'));
  assert.equal(mix.ok, false);
  assert.equal(mix.kind, 'special_value_mixup');
});

test('canExtend 剪枝正確性', () => {
  assert.equal(pack.canExtend(T('sin')), true);
  assert.equal(pack.canExtend(T('sin', '30°')), true);
  assert.equal(pack.canExtend(T('sin', '30°', '=')), true);
  assert.equal(pack.canExtend(T('sin', '30°', '=', '1/2')), true);
  assert.equal(pack.canExtend(T('sin', '30°', '=', '√3/2')), false);
  assert.equal(pack.canExtend(T('tan', '90°', '=')), true);
});
