import assert from 'node:assert/strict';
import { performance } from 'node:perf_hooks';

function deferred() {
  let resolve;
  const promise = new Promise(r => { resolve = r; });
  return { promise, resolve };
}
// State queue model, not a React renderer.
// Real React race regression/fix: react-race/README.md. Other fixtures below
// remain host models; the renderer evidence does not verify this whole file.
const snapshot = 0;
let replacement = snapshot;
for (const next of [snapshot + 1, snapshot + 1, snapshot + 1]) replacement = next;
assert.equal(replacement, 1);
let functional = snapshot;
for (const update of [v => v + 1, v => v + 1, v => v + 1]) functional = update(functional);
assert.equal(functional, 3);
console.log('PASS snapshot/functional queue model');

async function race(guarded, completionOrder) {
  const a = deferred(), b = deferred();
  let current = 0, displayed = '';
  function launch(request) {
    const owner = ++current;
    return request.promise.then(result => {
      if (!guarded || owner === current) displayed = result;
    });
  }
  const pa = launch(a), pb = launch(b);
  for (const name of completionOrder) {
    (name === 'A' ? a : b).resolve(name);
    await (name === 'A' ? pa : pb);
  }
  return displayed;
}
assert.equal(await race(false, ['B', 'A']), 'A');
assert.equal(await race(true, ['B', 'A']), 'B');
assert.equal(await race(true, ['A', 'B']), 'B');
console.log('PASS forced response race / both completion orders');

const beforeA = { title: 'initial', version: 0 };
const afterB = { title: 'B', version: 2 };
const unsafeRollback = () => beforeA;
const rollback = current => current.version === 1 ? beforeA : current;
assert.equal(unsafeRollback(afterB).title, 'initial');
assert.equal(rollback(afterB).title, 'B');
assert.equal(rollback({ title:'A', version:1 }).title, 'initial');
console.log('PASS rollback ownership');

function parseTask(raw) {
  if (!raw || typeof raw !== 'object' || typeof raw.title !== 'string' ||
      typeof raw.done !== 'boolean') throw new TypeError('Invalid task');
  return { title: raw.title, done: raw.done };
}
assert.deepEqual(parseTask({title:'a',done:false}), {title:'a',done:false});
for (const raw of [null, {}, {title:null,done:false}, {title:'a',done:'false'}]) {
  assert.throws(() => parseTask(raw), TypeError);
}
console.log('PASS runtime shape including null/wrong types');
assert.notEqual(0.1 + 0.2, 0.3);
assert.equal(10 + 20, 30); // Fixture uses integer cents; not every currency uses cents.
console.log('PASS money fixture in integer minor units');

const start = performance.now();
const timer = new Promise(resolve => setTimeout(() => resolve(performance.now()-start), 5));
while (performance.now()-start < 40) { /* Deliberately bounded CPU work. */ }
const delay = await timer;
assert.ok(delay >= 35, `Expected blocked timer, observed ${delay}`);
console.log(`PASS event-loop blocking; timer observed after ${delay.toFixed(1)}ms`);
