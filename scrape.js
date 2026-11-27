
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const Q=JSON.parse(fs.readFileSync('q.json','utf8'));fs.mkdirSync('g',{recursive:true});
const b=await chromium.launch();const ctx=await b.newContext({userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',locale:'ko-KR',viewport:{width:1300,height:900}});const pg=await ctx.newPage();const log=[];
for(const [k,q] of Object.entries(Q)){try{
 await pg.goto('https://www.google.com/maps/search/?api=1&hl=ko&query='+encodeURIComponent(q),{waitUntil:'domcontentloaded',timeout:30000});
 if(/consent/.test(pg.url())){try{await pg.click('button:has-text("Accept all"),button:has-text("모두 수락")',{timeout:5000})}catch(e){}}
 let h=null;for(let i=0;i<20;i++){await pg.waitForTimeout(700);h=await pg.$('h1.DUwDvf');if(h)break;const a=await pg.$('a.hfpxzc');if(a&&i===5){await a.click()}}
 await pg.waitForTimeout(2000);
 const name=h?await h.innerText():'none';
 let ims0=[];try{const hb=await pg.$('button[jsaction*="heroHeaderImage"], .ZKCDEc button, button.aoRNLd');if(hb){await hb.click();await pg.waitForTimeout(3000);ims0=await pg.evaluate(()=>[...new Set([...document.querySelectorAll('img, [style*="googleusercontent"]')].map(i=>i.src||((i.style.backgroundImage||'').match(/url\("?([^")]+)/)||[])[1]).filter(s=>s&&/googleusercontent\.com\/(gps-cs-s|p\/|grass-cs)/.test(s)).map(s=>s.replace(/=[ws]\d+.*/,'=w800-h600-k-no')))]);await pg.goBack().catch(()=>{});}}catch(e){}
 const ims=await pg.evaluate(()=>{const m=document.querySelector('[role="main"]')||document;return [...new Set([...m.querySelectorAll('img')].map(i=>i.src).filter(s=>/googleusercontent\.com\/(gps-cs-s|p\/|grass-cs)/.test(s)).map(s=>s.replace(/=w\d+-h\d+.*/,'=w800-h600-k-no')))]});
 let n=0;for(const u of [...new Set([...ims0,...ims])]){if(n>=4)break;const r=await pg.request.get(u);if(r.ok()){const buf=await r.body();if(buf.length>8000){n++;fs.writeFileSync('g/'+k+'_'+n+'.jpg',buf)}}}
 log.push(k+'\t'+name+'\t'+ims.length+'\t'+n);console.log(k,name,ims.length,n);
}catch(e){log.push(k+'\tERR '+e.message.slice(0,80));console.log(k,'ERR',e.message.slice(0,80))}}
fs.writeFileSync('g/log.txt',log.join('\n'));await b.close()})();
