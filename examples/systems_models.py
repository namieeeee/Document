"""Ownership/time/resource models; no claim to emulate MCU memory ordering."""
from collections import deque
from pathlib import Path
import tempfile

buffer = bytearray(b'first')
queue = deque([buffer])
buffer[:] = b'later'
assert queue.popleft() == b'later'  # Pointer/reference handoff is not a copy.
buffer[:] = b'first'
queue.append(bytes(buffer))
buffer[:] = b'later'
assert queue.popleft() == b'first'
print('PASS queued buffer reference vs immutable snapshot')

queue = deque()
capacity = 2
dropped = 0
for sequence in range(3):
    if len(queue) == capacity:
        dropped += 1
    else:
        queue.append(sequence)
assert list(queue) == [0, 1] and dropped == 1
print('PASS bounded queue with visible drop policy')

def elapsed8(now, start):
    return (now-start) % 256

start, timeout = 250, 10
wrong_deadline = (start + timeout) % 256
assert start >= wrong_deadline  # Incorrect comparison expires immediately.
for elapsed in range(15):
    now = (start + elapsed) % 256
    assert (elapsed8(now,start) >= timeout) == (elapsed >= timeout)
# Works only for intervals/observations that do not lose a full counter cycle.
print('PASS tick rollover model with explicit bounded interval')

with tempfile.TemporaryDirectory(prefix='curriculum-fixture-') as folder:
    path = Path(folder)/'sample.txt'
    handles = []
    for index in range(20):
        with path.open('w', encoding='utf-8') as handle:
            handles.append(handle)
            handle.write(str(index))
    assert all(handle.closed for handle in handles)
    try:
        with path.open('r',encoding='utf-8') as handle:
            raise ValueError('fixture failure')
    except ValueError:
        assert handle.closed
print('PASS file lifecycle success and exception path (host, not Linux FD count)')

unbounded=[]
bounded=deque(maxlen=10)
for index in range(100):
    payload=bytes([index])*1024
    unbounded.append(payload)
    bounded.append(payload)
assert sum(map(len,unbounded)) == 102400
assert sum(map(len,bounded)) == 10240
print('PASS retained payload bound; not a total-RSS leak benchmark')
