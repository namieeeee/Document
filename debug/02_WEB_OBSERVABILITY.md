# Debug Web: evidence từ browser tới database

Phạm vi: DevTools browser/React19 và ASP.NET8/Mongo8. Tool UI/fields version-sensitive; không claim framework fixture đã chạy.

## 1. Mục tiêu học

Chọn Network/Console/Performance/React tools/server traces/debugger/DB explain cho câu hỏi cụ thể, nối request/intent/version từ browser tới commit và UI.

## 2. Kiến thức tiên quyết

[Scientific debug](01_EVIDENCE_METHOD.md), một Web path trong [index](../00_INDEX.md); HTTP/JS/React/ASP/DB model cho target layer.

## 3. Vấn đề mà cơ chế này giải quyết

Browser error có thể tới từ transport, policy, server, storage hoặc apply state. Một tool chỉ thấy vài boundaries; phối evidence mới phân biệt cause.

## 4. Khái niệm

Observability là external/internal evidence cho state/flow. Logs events, metrics aggregate trends, traces spans/timing causally linked theo IDs, debugger state snapshots, profiler samples execution/allocations. Telemetry không full perfect execution record.

## 5. Thành phần bên trong

Network request URL/method/headers/status/timing/initiator/cache/cookie reason; Console stack/rejections/client warnings. Performance long tasks/style/layout/paint; React DevTools props/state/identity và Profiler commits. Server structured logs/trace spans routing/auth/service/dependency; debugger locals/exception; DB explain access path/cost counters, profiler workload.

## 6. Data representation

Trace ID/requestID/intent key/entity version/client generation/build identifiers không interchange. Distributed clocks offset means timestamps alone unreliable order; causal parent/span/sequence better. Profile sample proportions not exact every call counts. Redact tokens/password/body PII trước sink.

## 7. Control flow

```text
browser request/owner → proxy trace → server endpoint span
→ DB operation/commit/affected count → HTTP status/body
→ client parse/apply/version → React commit → layout/paint
```

Locate first divergent boundary. Status200 correct body followed wrong state directs mapper/owner; server queue high DBfast directs pool/middleware; index used high examined directs plan/filter.

## 8. Lifetime / ownership / state

Recording sessions bounded and fixture-specific; heap snapshots may keep inspected objects/browser console refs, account observer retention. Debug breakpoints change scheduling/network deadlines; tracing overhead/log sampling may drop events. Credentials forbidden evidence, synthetic actors needed.

## 9. Invariants

Same fixture/build/config comparison, telemetry supports claimed layer only; no inference of DBcommit from clienttimeout/status alone. Logs retain stable correlation and outcome with redaction. Unobserved spans not prove no handler if sampling/logging disabled.

## 10. Ví dụ tối thiểu

**Predicted experiment** API10ms but UI500ms: Network low response latency, Performance longJS400ms after response, React commit20ms. Hypothesis DB slow predicts dependency slow contradicted fixture; focus JS computation/long task. Measurement numbers illustrative, no benchmark.

HTTP403 vs CORS: server principal/policy deny trace+status403 differs HTTP success inaccessible cross-origin response; inspect raw browser reason/headers not refresh all errors.

## 11. Failure modes

Console-only server guesses, network cache hit mistaken controller, missing correlation mixes users, profiler dev/production mismatch, broad logs exposure, plan tiny data mislabeled production perf, double counting spans, client token logged. Fix measurement scope before application change.

## 12. Debug / observability

Procedure: freeze raw response/status/build→record owner apply timeline→check server last completed stage→DB conditions/plan→profile layer proven slow. Use source maps/debug symbols matching build. Force delay/response drop/barrier in synthetic environment, compare orders/error paths. React Profiler vs browser Performance quantify different work.

## 13. Liên hệ với bug/lab hiện có

[BE-23](../labs/backend/BE-23.md) correlation, [BE-24](../labs/backend/BE-24.md) redaction, [FE-05](../labs/frontend/FE-05.md) apply race, [BE-18](../labs/backend/BE-18.md) explain, [INT-20](../labs/integration/INT-20.md) unknown outcome.

## 14. Sai lầm thường gặp

Console sees server logs only if server output explicitly available, not browser default. React render count≠paint count/business requests. DevTools disable cache affects browser cache not every server layer. No error recorded≠operation succeeded.

## 15. Câu hỏi tự kiểm tra

1. Cache hit proof controller? Đáp án:no trace origin needed.
2. CPU low+latency high always DB? Đáp án:queue/wait/contention alternatives.
3. Correct raw/wrong state need tool? Đáp án:debugger/apply trace/React state.
4. Explain index used enough? Đáp án:examined/sort/returned/workload.
5. Token needed correlate? Đáp án:no stable safe IDs.

## 16. Nguồn

[Chrome Network](https://developer.chrome.com/docs/devtools/network), [Console](https://developer.chrome.com/docs/devtools/console), [Performance](https://developer.chrome.com/docs/devtools/performance), [React DevTools](https://react.dev/learn/react-developer-tools), [dotnet diagnostics](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/), [Mongo8 explain](https://www.mongodb.com/docs/v8.0/reference/explain-results/). Specific commands/counters pin tool/runtime actual.

[Index](../00_INDEX.md) · [Coverage](../THEORY_COVERAGE_MATRIX.md).
