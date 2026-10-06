// @vitest-environment jsdom
import { createElement } from 'react';
import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import { BrokenSearchResult, FixedSearchResult } from './SearchResult.js';

afterEach(cleanup);
const Component = process.env.RACE_VARIANT === 'broken'
  ? BrokenSearchResult : FixedSearchResult;

function requests() {
  const pending = new Map();
  const load = query => new Promise(resolve => pending.set(query, resolve));
  const settle = async query => {
    expect(pending.has(query)).toBe(true);
    await act(async () => { pending.get(query)(query); });
  };
  return { load, settle };
}

test('keeps latest result when B completes before stale A', async () => {
  const { load, settle } = requests();
  const view = render(createElement(Component, { query: 'A', load }));
  view.rerender(createElement(Component, { query: 'B', load }));
  await settle('B');
  expect(screen.getByLabelText('search result').textContent).toBe('B');
  await settle('A');
  // This invariant is identical for both implementations. Broken observes A.
  expect(screen.getByLabelText('search result').textContent).toBe('B');
});

test('publishes B when responses complete in request order', async () => {
  const { load, settle } = requests();
  const view = render(createElement(Component, { query: 'A', load }));
  await settle('A');
  expect(screen.getByLabelText('search result').textContent).toBe('A');
  view.rerender(createElement(Component, { query: 'B', load }));
  await settle('B');
  expect(screen.getByLabelText('search result').textContent).toBe('B');
});
