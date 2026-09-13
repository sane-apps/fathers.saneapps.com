import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { JSDOM } from 'jsdom';
const script = readFileSync(new URL('../assets/site.js', import.meta.url), 'utf8');
const catalog = readFileSync(new URL('../dist/works/index.html', import.meta.url), 'utf8');
const reader = readFileSync(new URL('../dist/works/origen-numbers-homily-21/index.html', import.meta.url), 'utf8');
const index = JSON.parse(readFileSync(new URL('../dist/data/search-index.json', import.meta.url), 'utf8'));
const settle = () => new Promise(resolve => setImmediate(resolve));
function mount(html, path='/works/', fetcher=async()=>({ok:true,json:async()=>index})) {
  const dom=new JSDOM(html,{url:`https://fathers.saneapps.com${path}`,runScripts:'outside-only',pretendToBeVisual:true});
  dom.window.fetch=fetcher;
  dom.window.eval(script);
  return dom;
}
function query(dom, value) {
  const input=dom.window.document.querySelector('#works-q');
  input.value=value;input.dispatchEvent(new dom.window.Event('input'));
}
test('work passages are searchable, including words beyond 400 characters',async()=>{
  const dom=mount(catalog);await settle();
  query(dom,'second numbering');await settle();
  assert.ok([...dom.window.document.querySelectorAll('#passage-results a')].some(a=>a.href.includes('origen-numbers-homily-21')));
  const row=index.find(r=>r.kind==='work'&&r.text.length>600);
  query(dom,row.text.slice(450,510));
  assert.ok([...dom.window.document.querySelectorAll('#passage-results a')].some(a=>a.getAttribute('href')===row.href));
  dom.window.close();
});
test('failed passage index reports error and Retry recovers',async()=>{
  let calls=0;
  const dom=mount(catalog,'/works/?q=numbering',async()=> ++calls===1?{ok:false}:{ok:true,json:async()=>index});
  await settle();
  assert.match(dom.window.document.querySelector('#passage-results').textContent,/could not load/);
  dom.window.document.querySelector('.search-retry').click();await settle();
  assert.ok(dom.window.document.querySelector('#passage-results a'));
  dom.window.close();
});
test('invalid filters fall back to All and empty searches explain recovery',async()=>{
  const dom=mount(catalog,'/works/?filter=invalid');await settle();
  assert.equal(dom.window.document.querySelector('[data-filter="all"]').getAttribute('aria-pressed'),'true');
  query(dom,'zzzznonexistent');await settle();
  assert.equal(dom.window.document.querySelector('.search-empty').hidden,false);
  assert.match(dom.window.document.querySelector('#passage-results').textContent,/No matching passages/);
  dom.window.close();
});
test('mobile menu closes on Escape and returns focus',()=>{
  const dom=mount(reader);const doc=dom.window.document;const toggle=doc.querySelector('.nav-toggle');
  toggle.click();assert.equal(toggle.getAttribute('aria-expanded'),'true');
  doc.dispatchEvent(new dom.window.KeyboardEvent('keydown',{key:'Escape'}));
  assert.equal(toggle.getAttribute('aria-expanded'),'false');assert.equal(doc.activeElement,toggle);
  dom.window.close();
});
test('Contents links reopen a collapsed table of contents',()=>{
  const dom=mount(reader);const doc=dom.window.document;
  doc.querySelector('#contents').open=false;
  doc.querySelector('.reader-quick a').click();
  assert.equal(doc.querySelector('#contents').open,true);dom.window.close();
});

test('catalog browsing does not download the passage index until a search',async()=>{
  let calls=0;const dom=mount(catalog,'/works/',async()=>{calls++;return {ok:true,json:async()=>index};});
  await settle();assert.equal(calls,0);query(dom,'numbering');await settle();assert.equal(calls,1);dom.window.close();
});
