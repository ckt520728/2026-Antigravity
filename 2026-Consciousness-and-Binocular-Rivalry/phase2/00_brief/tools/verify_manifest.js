const fs = require("fs"), path = require("path"), crypto = require("crypto");
const file = path.resolve(__dirname, "..", "..", "..", "task_manifest.json");
const d = JSON.parse(fs.readFileSync(file, "utf8"));
function sortKeys(v) { if (Array.isArray(v)) return v.map(sortKeys); if (v && typeof v === "object") { const o = {}; for (const k of Object.keys(v).sort()) o[k] = sortKeys(v[k]); return o; } return v; }
const claimed = d.sha256; delete d.sha256;
const actual = crypto.createHash("sha256").update(JSON.stringify(sortKeys(d)), "utf8").digest("hex");
const CAPS = new Set(["read", "local_write", "destructive", "network_egress", "process_spawn", "credential_access", "spend", "other"]);
const errs = []; const chk = (c, m) => { if (!c) errs.push(m); };
chk(d.schema === "jev.task_manifest/1", "schema");
chk(actual === claimed, "hash mismatch " + actual + " vs " + claimed);
const L = d.limits, seen = new Set(), outs = new Set(); let total = 0;
chk(d.tasks.length <= L.max_tasks, "too many tasks");
const FIELDS = ["task_id", "objective", "inputs", "outputs", "acceptance", "capabilities", "depends_on", "max_output_tokens", "model", "tier", "data_class", "confidence"];
for (const t of d.tasks) {
  for (const f of FIELDS) chk(f in t, t.task_id + " missing " + f);
  chk(!seen.has(t.task_id), "dup id " + t.task_id);
  for (const p of t.depends_on) chk(seen.has(p), t.task_id + " depends on non-earlier " + p);
  seen.add(t.task_id);
  for (const o of t.outputs) { chk(!outs.has(o), "dup output " + o); outs.add(o); }
  for (const c of t.capabilities) chk(CAPS.has(c), t.task_id + " bad capability " + c);
  chk(t.max_output_tokens <= L.max_worker_output_tokens, t.task_id + " tokens > worker max");
  chk(JSON.stringify(t).length <= L.max_task_chars, t.task_id + " chars > max_task_chars");
  chk(!/(sk-|api[_-]?key|secret|password)/i.test(JSON.stringify(t)), t.task_id + " credential-like string");
  total += t.max_output_tokens;
}
chk(total <= L.max_total_output_tokens, "total tokens " + total + " > " + L.max_total_output_tokens);
console.log("tasks=" + d.tasks.length + " total_max_output_tokens=" + total + " sha256=" + actual);
console.log(errs.length ? "FAIL\n" + errs.join("\n") : "PASS: hash, unique ids, depends_on order, unique outputs, capabilities, token limits, no credential-like strings");
process.exit(errs.length ? 1 : 0);
