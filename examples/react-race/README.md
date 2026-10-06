# React: late response overwrites current result

Invariant: after query B is committed and response B is displayed, completing the previous request A must not replace B.

`BrokenSearchResult` publishes every response. `FixedSearchResult` marks the previous effect stale during cleanup and checks that flag before publishing. Both are actual React components rendered by React DOM through Testing Library. The same assertions and response schedule run against both implementations.

## Run

Prerequisites: Node 24 and Python 3.11, with npm available on PATH. From this directory:

```text
npm ci
python verify.py
```

The verifier writes raw logs, Vitest JSON reports, dependency versions, commands, exit codes and timestamp to [evidence/react-race](../../evidence/react-race/summary.json). It returns zero only if the broken version fails the reverse-response invariant (one specific assertion failure) and the fixed version passes both tests. An import error or missing test is a verification failure.

Expected: broken reverse-order test FAIL; broken normal-order test PASS; fixed tests PASS. The final invariant remains `result === B` for both versions; it is not adjusted to match the broken result A.

## Scope

This verifies React effect cleanup and DOM result under two controlled Promise schedules in jsdom. The request adapter is a fixture: this is not a live HTTP integration test, real browser rendering or a claim about every possible schedule. StrictMode, network cancellation, errors and unmount behavior are outside these two tests. Separate [MongoDB HTTP verification](../MongoApi/README.md) uses a real standalone database; it does not broaden this renderer fixture's scope.

Sources: [React useEffect, fetching data](https://react.dev/reference/react/useEffect#fetching-data-with-effects), [Vitest guide](https://vitest.dev/guide/), [Testing Library React API](https://testing-library.com/docs/react-testing-library/api/).

[React theory](../../web/04_REACT_MENTAL_MODEL.md) · [Examples](../README.md) · [Validation](../../VALIDATION.md).
