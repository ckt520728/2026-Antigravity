// 三角函數連線的內容包清單；學生端與老師端都從這裡讀取。
import trig from './math/trig.js';

export const PACKS = [trig];
export const DEFAULT_PACK = PACKS[0].id;

export const getPack = (id) => PACKS.find((p) => p.id === id) || null;

// 誤解代碼的中文說明（老師端用；找不到就顯示代碼本身）
export function kindLabel(kind, packId) {
  const p = getPack(packId);
  if (p?.misconceptions?.[kind]) return p.misconceptions[kind];
  for (const x of PACKS) if (x.misconceptions?.[kind]) return x.misconceptions[kind];
  return kind;
}
