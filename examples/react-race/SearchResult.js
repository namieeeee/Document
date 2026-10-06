import { createElement, useEffect, useState } from 'react';

// Both versions render through React. The loader is injected so the test can
// control response order without wall-clock sleeps or a live HTTP service.
export function BrokenSearchResult({ query, load }) {
  const [result, setResult] = useState('loading');
  useEffect(() => {
    load(query).then(setResult);
  }, [query, load]);
  return createElement('output', { 'aria-label': 'search result' }, result);
}

export function FixedSearchResult({ query, load }) {
  const [result, setResult] = useState('loading');
  useEffect(() => {
    let stale = false;
    load(query).then(value => {
      if (!stale) setResult(value);
    });
    return () => { stale = true; };
  }, [query, load]);
  return createElement('output', { 'aria-label': 'search result' }, result);
}
