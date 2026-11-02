"""ずけいのアトリエ ver.01 — Streamlit / Supabase. Python 3.9+.
Run: streamlit run app_ver.01.py
HTML is embedded; generated component assets are version-hashed in a temp directory.
No private Supabase key is sent to the browser.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone
from uuid import UUID
import requests
import streamlit as st
import streamlit.components.v1 as components

VERSION = "01"
TABLE = "geometry_attempts_v1"
TOPICS = {"equal": "等積変形", "cut": "切って移す", "line": "補助線"}
FRONTEND = '<!doctype html>\n<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>\n:root{color-scheme:light;--ink:#243e48;--muted:#647a81;--line:#dce8e8;--paper:#fff;--accent:#197f73;--soft:#edf6f3;--blue:#3e7eae;--gold:#b58124}*{box-sizing:border-box}body{margin:0;background:#f7faf9;color:var(--ink);font:16px/1.65 system-ui,-apple-system,\'Noto Sans JP\',sans-serif}button,input,select{font:inherit}button{cursor:pointer;min-height:46px;border:1px solid var(--line);border-radius:12px;padding:10px 16px;background:#fff;color:var(--ink);font-weight:600}button:disabled{opacity:.45;cursor:default}button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #e3a63d;outline-offset:2px}.primary,button.selected{background:var(--accent);color:white;border-color:var(--accent)}button:hover:not(:disabled){filter:brightness(.97)}[hidden]{display:none!important}.wrap{max-width:760px;margin:auto;padding:18px 16px 28px}.top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:18px}.brand{font-size:24px;font-weight:700;letter-spacing:.05em}.version,.small{font-size:13px;color:var(--muted)}h1{font-size:26px;margin:10px 0}h2{font-size:21px;margin:8px 0 12px}h3{font-size:17px;margin:0 0 8px}p{margin:8px 0 14px}.hero{padding:18px 0}.rank{display:flex;gap:12px;align-items:center;background:#edf6f3;padding:16px;border-radius:16px}.rank-symbol{font-size:34px}.rank strong{font-size:20px}.modes{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}.mode{text-align:left;border-radius:17px;padding:18px;min-height:128px;display:flex;flex-direction:column;justify-content:center;gap:5px;box-shadow:0 3px 12px #1f4d4610}.mode strong{font-size:18px}.mode span{font-weight:400;font-size:13px;color:var(--muted)}.mode.main{background:var(--accent);color:#fff}.mode.main span{color:#e3f7ef}.bar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}.panel{background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px;margin-top:14px}.topics{display:grid;gap:10px;margin:14px 0}.topic{display:flex;justify-content:space-between;align-items:center;text-align:left;gap:10px;padding:16px}.topic small{display:block;color:var(--muted);font-weight:400}.topic b{white-space:nowrap;font-size:13px}.badge{font-size:12px;color:var(--accent);background:var(--soft);padding:4px 9px;border-radius:20px}.progress{height:6px;background:#dfebe8;border-radius:8px;margin:12px 0 18px;overflow:hidden}.progress i{display:block;background:var(--accent);height:100%}.prompt{font-size:19px;font-weight:600;margin-top:12px}.diagram{width:100%;height:290px;display:block;touch-action:pan-y}.diagram text{fill:var(--ink);font-size:15px}.shape{fill:#d4eee7;stroke:var(--accent);stroke-width:2.5;stroke-linejoin:round}.ghost{fill:none;stroke:#a8bcb9;stroke-width:1.5;stroke-dasharray:5 5}.aux{stroke:#bc7821;stroke-width:2;stroke-dasharray:6 4;fill:none}.cut{fill:#dfebf8;stroke:var(--blue);stroke-width:2}.edge{stroke:var(--ink);stroke-width:2;fill:none}.handle{fill:var(--accent);stroke:white;stroke-width:2}.drag-hit{fill:transparent;cursor:ew-resize;touch-action:none}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:8px 0}.controls label{min-height:44px;display:flex;align-items:center;gap:7px}.controls input[type=checkbox]{width:19px;height:19px;accent-color:var(--accent)}.controls button{font-size:14px}.range{width:100%;min-height:44px;accent-color:var(--accent);margin:0}.range-label{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;font-size:13px;color:var(--muted)}.choices{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}.feedback{background:var(--soft);padding:14px;border-radius:12px;margin-top:14px}.feedback.wrong{background:#fff4e8}.feedback strong{display:block;font-size:20px}.bottom{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.bottom button{flex:1}.sync{font-size:12px;color:var(--muted);margin-top:20px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}.sync button{font-size:12px;padding:5px 10px;min-height:36px}.stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:16px 0}.stat{background:var(--soft);border-radius:12px;padding:12px;text-align:center}.stat b{display:block;font-size:24px}.stat span{font-size:12px;color:var(--muted)}.history{width:100%;border-collapse:collapse;font-size:13px}.history th,.history td{text-align:left;padding:10px 5px;border-bottom:1px solid var(--line)}.setting{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:15px 0;border-bottom:1px solid var(--line)}.setting input{width:23px;height:23px;accent-color:var(--accent)}.quiet{color:var(--muted);font-size:13px}.empty{padding:28px 0;text-align:center;color:var(--muted)}@media(max-width:460px){.wrap{padding:12px 12px 22px}.modes{gap:10px}.mode{padding:14px;min-height:116px}.mode strong{font-size:16px}.panel{padding:14px}.brand{font-size:23px}.prompt{font-size:18px}.diagram{height:280px}.topic{padding:12px}.stat b{font-size:21px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}\n</style></head><body><main class="wrap"><div class="top"><span class="brand">ずけいのアトリエ</span><button id="homeBtn" hidden>← TOP</button></div><div id="app"></div><footer class="sync"><span id="syncText">記録を準備しています…</span><button id="syncBtn">再同期</button></footer><div class="version" style="margin-top:8px;text-align:right">ver.01</div></main>\n<script>\n\'use strict\';\nlet BANK=[],TOPICS={},server={},booted=false,device=\'\',records=[],outbox=[],storageOK=true,settings={voice:false},view=\'home\',mode=\'learn\',topic=\'\',queue=[],index=0,selection=null,checked=false,hint=false,t=0,usedHint=false,started=0,round=[],eventBusy=false,lastSend=null,anim=0;\nconst $=s=>document.querySelector(s),KEY=\'geometry_atelier_v1\',uuid=()=>crypto.randomUUID();\nfunction bridge(type,extra={}){parent.postMessage({isStreamlitMessage:true,type,...extra},\'*\')}\nfunction resize(){bridge(\'streamlit:setFrameHeight\',{height:Math.max(400,document.documentElement.scrollHeight)})}\nfunction store(){try{localStorage.setItem(KEY,JSON.stringify({device,records:records.slice(-1000),outbox,settings}))}catch(e){storageOK=false}status()}\nfunction status(){let text=server.message||\'この端末に保存\';if(!storageOK)text+=\' · 端末保存が使えません\';if(outbox.length)text+=` · 未同期 ${outbox.length}件`;$(\'#syncText\').textContent=text;resize()}\nfunction merge(rows){const all=new Map(records.map(r=>[r.id,r]));for(const r of rows||[])all.set(r.id,r);records=[...all.values()].sort((a,b)=>a.client_created.localeCompare(b.client_created)).slice(-1000);store()}\nfunction send(type,rows=[]){if(eventBusy)return;eventBusy=true;lastSend={request_id:uuid(),type,device_id:device,rows};bridge(\'streamlit:setComponentValue\',{value:lastSend,dataType:\'json\'})}\nfunction flush(){if(server.configured&&outbox.length&&!eventBusy)send(\'save\',outbox.slice(0,25))}\nwindow.addEventListener(\'message\',event=>{if(event.source!==parent||event.data.type!==\'streamlit:render\')return;const a=event.data.args||{};BANK=a.bank||BANK;TOPICS=a.topics||TOPICS;server=a.response||{};if(!booted){try{const v=JSON.parse(localStorage.getItem(KEY)||\'{}\');device=v.device||uuid();records=Array.isArray(v.records)?v.records:[];outbox=Array.isArray(v.outbox)?v.outbox:[];settings={voice:false,...v.settings}}catch(e){device=uuid();storageOK=false}booted=true;store();render();send(\'load\');return}if(lastSend&&server.request_id===lastSend.request_id){eventBusy=false;lastSend=null;if(server.ack){const ack=new Set(server.ack);outbox=outbox.filter(r=>!ack.has(r.id));store()}if(server.rows)merge(server.rows);if([\'home\',\'records\',\'menu\'].includes(view))render();if(server.ok)flush()}status()});\nbridge(\'streamlit:componentReady\',{apiVersion:1});\nnew ResizeObserver(()=>resize()).observe(document.body);\nfunction speak(text){if(!settings.voice||!(\'speechSynthesis\' in window))return;speechSynthesis.cancel();const parts=text.split(/[：:]/).filter(Boolean);let i=0;function next(){if(i>=parts.length)return;const u=new SpeechSynthesisUtterance(parts[i++]);u.lang=\'ja-JP\';u.rate=.8;const v=speechSynthesis.getVoices().find(v=>v.lang.startsWith(\'ja\'));if(v)u.voice=v;u.onend=()=>setTimeout(next,650);speechSynthesis.speak(u)}next()}\nfunction stopVoice(){if(\'speechSynthesis\' in window)speechSynthesis.cancel()}\nfunction esc(s){return String(s).replace(/[&<>"\']/g,c=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[c]))}\nfunction mastered(){const grouped={};for(const r of records.filter(r=>r.mode!==\'learn\')){(grouped[r.question_id]??=[]).push(r)}return new Set(Object.entries(grouped).filter(([,rows])=>{const last=rows.slice(-2);return last.length===2&&last.every(r=>r.correct&&!r.hint_used)}).map(([id])=>id))}\nfunction weaknesses(){const latest=new Map();for(const r of records.filter(r=>r.mode!==\'learn\'))latest.set(r.question_id,r);return new Set([...latest].filter(([,r])=>!r.correct||r.hint_used).map(([id])=>id))}\nfunction navigate(v){cancelAnimationFrame(anim);stopVoice();view=v;render()}\n$(\'#homeBtn\').onclick=()=>navigate(\'home\');$(\'#syncBtn\').onclick=()=>{eventBusy=false;send(\'load\')};\nfunction render(){const app=$(\'#app\');$(\'#homeBtn\').hidden=view===\'home\';if(view===\'home\'){const n=mastered().size,rank=n>=24?\'図形の名人\':n>=12?\'図形の探検家\':n>=3?\'図形の見習い\':\'はじめの一歩\';app.innerHTML=`<div class="hero"><h1>動かして、見つけよう。</h1><p class="quiet">形がかわっても、かわらないものがある。</p></div><div class="rank"><span class="rank-symbol" aria-hidden="true">◇</span><div><div class="small">あなたの階級</div><strong>${rank}</strong><div class="small">自力で2回続けて正解した問題 ${n} / ${BANK.length}</div></div></div><div class="modes"><button class="mode main" data-mode="learn"><strong>学習モード</strong><span>動かして、理由をたしかめる</span></button><button class="mode" data-mode="challenge"><strong>チャレンジ</strong><span>静止図で考える · 6問</span></button><button class="mode" data-mode="review"><strong>苦手克服</strong><span>間違えた問題をもう一度</span></button><button class="mode" data-nav="records"><strong>学習記録</strong><span>分野ごとの理解を確認</span></button><button class="mode" data-nav="settings"><strong>設定</strong><span>音声のON・OFF</span></button></div>`;app.querySelectorAll(\'[data-mode]\').forEach(b=>b.onclick=()=>{mode=b.dataset.mode;navigate(\'menu\')});app.querySelectorAll(\'[data-nav]\').forEach(b=>b.onclick=()=>navigate(b.dataset.nav))}\nelse if(view===\'menu\'){const weak=weaknesses();app.innerHTML=`<h2>${{learn:\'学習モード\',challenge:\'チャレンジ\',review:\'苦手克服\'}[mode]}</h2><p class="quiet">${mode===\'learn\'?\'分野をえらんで、図形を動かしてみよう。\':mode===\'challenge\'?\'ヒントなしの静止図で6問。時間制限はありません。\':\'最後に間違えた問題・ヒントを使った問題を復習します。\'}</p><div class="topics">${Object.entries(TOPICS).map(([k,v])=>{const count=BANK.filter(q=>q.topic===k&&(mode!==\'review\'||weak.has(q.id))).length;return `<button class="topic" data-topic="${k}" ${!count?\'disabled\':\'\'}><span><strong>${v}</strong><small>${{equal:\'底辺と高さに注目する\',cut:\'切って、移して、形を変える\',line:\'線を足して、隠れた形を見つける\'}[k]}</small></span><b>${count}問</b></button>`}).join(\'\')}</div>${mode===\'review\'&&!weak.size?\'<p class="empty">復習する問題はありません。</p>\':\'\'}`;app.querySelectorAll(\'[data-topic]\').forEach(b=>b.onclick=()=>start(b.dataset.topic))}\nelse if(view===\'question\'){renderQuestion()}\nelse if(view===\'result\'){const right=round.filter(r=>r.correct).length,first=round.length;app.innerHTML=`<div class="hero"><span class="badge">${TOPICS[topic]}</span><h2>今回の記録</h2></div><div class="stats"><div class="stat"><b>${right}/${first}</b><span>正解</span></div><div class="stat"><b>${round.filter(r=>r.correct&&!r.hint_used).length}</b><span>ヒントなし</span></div><div class="stat"><b>${mastered().size}</b><span>定着した問題</span></div></div><p>正解した理由を、言葉でも説明してみよう。</p><div class="bottom"><button class="primary" id="again">もう一度</button><button id="toMenu">分野をえらぶ</button></div>`;$(\'#again\').onclick=()=>start(topic);$(\'#toMenu\').onclick=()=>navigate(\'menu\')}\nelse if(view===\'records\'){const learned=mastered(),challenge=records.filter(r=>r.mode!==\'learn\');app.innerHTML=`<h2>学習記録</h2><p class="quiet">直近1,000件をもとに表示。定着＝静止図で、ヒントなしの正解が2回続いた問題。</p><div class="topics">${Object.entries(TOPICS).map(([k,v])=>{const total=BANK.filter(q=>q.topic===k),done=total.filter(q=>learned.has(q.id)).length;return `<div class="panel"><div class="bar"><strong>${v}</strong><b>${done} / ${total.length}</b></div><div class="progress"><i style="width:${done/total.length*100}%"></i></div></div>`}).join(\'\')}</div><p class="small">回答 ${records.length}件 · 静止図 ${challenge.length}件 · 復習対象 ${weaknesses().size}問</p><table class="history"><thead><tr><th>日時</th><th>分野</th><th>結果</th></tr></thead><tbody>${records.slice(-12).reverse().map(r=>`<tr><td>${esc(new Date(r.client_created).toLocaleString(\'ja-JP\',{month:\'numeric\',day:\'numeric\',hour:\'2-digit\',minute:\'2-digit\'}))}</td><td>${esc(TOPICS[BANK.find(q=>q.id===r.question_id)?.topic]||\'図形\')}</td><td>${r.correct?\'○\':\'×\'}${r.hint_used?\' ヒントあり\':\'\'}</td></tr>`).join(\'\')}</tbody></table>`}\nelse if(view===\'settings\'){app.innerHTML=`<h2>設定</h2><div class="panel"><label class="setting"><span>音声モード<small class="quiet" style="display:block">問題と判定を読み上げます</small></span><input id="voice" type="checkbox" ${settings.voice?\'checked\':\'\'}></label><p class="quiet">正解のときは「せいかい！」のみ。不正解のときは解説を読みます。次の問題へはボタンで進みます。</p><p class="quiet">記録はこのブラウザごとに分かれます。閲覧データを消すと、記録を復元するための端末IDも消えます。</p><button id="export">記録を保存</button></div>`;$(\'#voice\').onchange=e=>{settings.voice=e.target.checked;store();if(!settings.voice)stopVoice();else speak(\'音声をオンにしました。\')};$(\'#export\').onclick=()=>{const blob=new Blob([JSON.stringify({version:1,records},null,2)],{type:\'application/json\'});const a=document.createElement(\'a\');a.href=URL.createObjectURL(blob);a.download=\'geometry_records.json\';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}}status();resize()}\nfunction start(k){topic=k;const weak=weaknesses();let list=BANK.filter(q=>q.topic===k&&(mode!==\'review\'||weak.has(q.id)));if(mode!==\'learn\')list=list.map(q=>({q,r:Math.random()})).sort((a,b)=>a.r-b.r).map(x=>x.q);queue=mode===\'challenge\'?list.slice(0,6):list;index=0;round=[];newQuestion()}\nfunction newQuestion(){cancelAnimationFrame(anim);selection=null;checked=false;hint=false;usedHint=false;t=0;started=Date.now();view=\'question\';render();speak(current().prompt)}\nfunction current(){return queue[index]}\nfunction renderQuestion(){const q=current(),isLearn=mode===\'learn\';$(\'#app\').innerHTML=`<div class="bar"><span class="badge">${TOPICS[q.topic]} · ${isLearn?\'学習\':mode===\'review\'?\'復習\':\'チャレンジ\'}</span><span class="small">${index+1} / ${queue.length}</span></div><div class="progress"><i style="width:${index/queue.length*100}%"></i></div><div class="panel"><div class="prompt">${esc(q.prompt)}</div><svg id="diagram" class="diagram" role="img" aria-label="${esc(q.alt)}"></svg><div id="manipulation" ${!isLearn?\'hidden\':\'\'}><div class="range-label"><label for="movement">${esc(q.control)}</label><span id="positionLabel">はじめの形</span></div><input class="range" id="movement" type="range" min="0" max="100" value="0"><div class="controls"><button id="play">ゆっくり動かす</button><label><input id="hint" type="checkbox">${esc(q.hint_label)}</label></div></div><div class="choices">${q.choices.map((c,i)=>`<button type="button" data-choice="${i}" aria-pressed="false">${esc(c)}</button>`).join(\'\')}</div><button class="primary" id="check" style="width:100%">答えをたしかめる</button><button id="help" ${isLearn?\'hidden\':\'\'}>ヒントを見る</button><div id="feedback" class="feedback" aria-live="polite" hidden></div><div class="bottom" id="nextActions" hidden><button id="retry">同じ問題を再チャレンジ</button><button class="primary" id="next">${index+1===queue.length?\'結果を見る\':\'次の問題へ\'}</button></div></div>`;\n$(\'#movement\').oninput=e=>{cancelAnimationFrame(anim);$(\'#play\').textContent=\'ゆっくり動かす\';t=Number(e.target.value)/100;draw()};$(\'#hint\').onchange=e=>{hint=e.target.checked;if(hint)usedHint=true;draw()};$(\'#play\').onclick=()=>{cancelAnimationFrame(anim);if(t>=1)t=0;const from=t,begin=performance.now(),duration=matchMedia(\'(prefers-reduced-motion: reduce)\').matches?0:2200;function tick(now){t=duration?Math.min(1,from+(now-begin)/duration):1;$(\'#movement\').value=String(Math.round(t*100));draw();if(t<1)anim=requestAnimationFrame(tick)}anim=requestAnimationFrame(tick)};$(\'#help\').onclick=()=>{usedHint=true;hint=true;$(\'#manipulation\').hidden=false;$(\'#hint\').checked=true;$(\'#help\').hidden=true;draw();resize()};document.querySelectorAll(\'[data-choice]\').forEach(b=>b.onclick=()=>{if(checked)return;selection=Number(b.dataset.choice);document.querySelectorAll(\'[data-choice]\').forEach(x=>{x.classList.toggle(\'selected\',x===b);x.setAttribute(\'aria-pressed\',String(x===b))})});$(\'#check\').onclick=check;$(\'#next\').onclick=()=>{stopVoice();index++;if(index>=queue.length)navigate(\'result\');else newQuestion()};$(\'#retry\').onclick=()=>{stopVoice();newQuestion()};draw();bindDrag()}\nfunction check(){if(checked)return;const q=current();if(selection===null){$(\'#feedback\').hidden=false;$(\'#feedback\').textContent=\'答えをえらんでね。\';resize();return}checked=true;const correct=selection===q.answer;const row={id:uuid(),question_id:q.id,mode,answer:selection,correct,hint_used:usedHint,seconds:Math.min(86400,Math.max(0,Math.round((Date.now()-started)/1000))),client_created:new Date().toISOString()};records.push(row);records=records.slice(-1000);outbox.push(row);round.push(row);store();flush();const fb=$(\'#feedback\');fb.hidden=false;fb.classList.toggle(\'wrong\',!correct);fb.innerHTML=`<strong>${correct?\'せいかい！\':\'ざんねん！\'}</strong><span>${esc(q.explanation)}</span>`;document.querySelectorAll(\'[data-choice]\').forEach(b=>b.disabled=true);$(\'#check\').hidden=true;$(\'#help\').hidden=true;$(\'#manipulation\').hidden=false;$(\'#nextActions\').hidden=false;$(\'#retry\').hidden=correct;hint=true;$(\'#hint\').checked=true;draw();speak(correct?\'せいかい！\':\'ざんねん！\'+q.explanation);resize()}\nfunction draw(){const q=current(),svg=$(\'#diagram\');if(!svg)return;const w=svg.clientWidth,H=280;svg.setAttribute(\'viewBox\',`0 0 ${w} ${H}`);const text=(x,y,s,anchor=\'middle\')=>`<text x="${x}" y="${y}" text-anchor="${anchor}">${s}</text>`,poly=(pts,cls=\'shape\')=>`<polygon class="${cls}" points="${pts.map(p=>p.join(\',\')).join(\' \')}"/>`,line=(x1,y1,x2,y2,cls=\'edge\')=>`<line class="${cls}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"/>`;\nlet content=\'\';\nif(q.topic===\'equal\'){const b=w*.23,c=w*.77,yb=220,y0=140,x0=w*.43,x1=w*.82,x=x0+(x1-x0)*t,yy=q.motion===\'horizontal\'?y0:y0+(q.motion===\'up\'?-80:40)*t;content=line(20,y0,w-20,y0,\'ghost\')+poly([[b,yb],[x0,y0],[c,yb]],\'ghost\')+poly([[b,yb],[x,yy],[c,yb]])+line(b,yb,c,yb)+text((b+c)/2,252,`底辺 ${q.b}cm`)+text(x,yy-27,\'A\')+text(b-12,yb+5,\'B\')+text(c+12,yb+5,\'C\');if(hint){content+=line(x,yy,x,yb,\'aux\')+line(Math.min(x,b),yb,Math.max(x,c),yb,\'ghost\')+`<path class="edge" d="M${x},${yb-9}h-9v9"/>`+text(Math.max(8,x-14),yy+(yb-yy)*.55,`高さ ${Number((q.h+(q.h2-q.h)*t).toFixed(1))}cm`,\'end\')}content+=`<circle class="handle" cx="${x}" cy="${yy}" r="9"/><circle id="dragPoint" class="drag-hit" cx="${x}" cy="${yy}" r="23"/>`;svg.dataset.start=String(x0);svg.dataset.end=String(x1)}\nelse if(q.topic===\'cut\'){const x=w*.12,y=70,bw=w*.50,sh=w*.18,bottom=220;const p=[[x,y],[x+bw,y],[x+bw+sh,bottom],[x+sh,bottom]];content=poly(p,\'ghost\');const main=[[x+sh,y],[x+bw,y],[x+bw+sh,bottom],[x+sh,bottom]],piece=[[x,y],[x+sh,y],[x+sh,bottom]].map(([px,py])=>[px+bw*t,py]);content+=poly(main)+poly(piece,\'cut\');if(hint)content+=line(x+sh,y,x+sh,bottom,\'aux\');content+=text(x+sh+bw/2,252,`底辺 ${q.b}cm`)+text(x+sh+bw+10,152,`${q.h}cm`,\'start\');if(t>.99)content+=text(w/2,35,\'長方形になった！\');else content+=text(w/2,35,\'切った三角形を右へ移す\')}\nelse{const x=w*.19,y=68,bw=w*.62,bh=150;content=poly([[x,y],[x+bw,y],[x+bw,y+bh],[x,y+bh]])+text(x+bw/2,y+bh+32,`${q.b}cm`)+text(x-10,y+bh/2+4,`${q.h}cm`,\'end\');if(q.visual===\'diagonal\'){const ex=x+bw*t,ey=y+bh*t;if(t>0)content+=line(x,y,ex,ey,\'aux\');if(hint){content+=poly([[x,y],[x+bw,y],[x+bw,y+bh]],\'cut\')+line(x,y,x+bw,y+bh,\'aux\')}}else{const roofY=y+bh*(1-q.r/q.h),dx=x+bw*q.p/q.b;content=poly([[x,y+bh],[x+bw,y+bh],[x+bw,roofY],[dx,roofY],[dx,y],[x,y]])+text(x+bw/2,y+bh+32,`全体の横 ${q.b}cm`)+text(x-10,y+bh/2,`${q.h}cm`,\'end\')+text(x+bw*q.p/q.b/2,48,`上の横 ${q.p}cm`)+text(x+bw+8,roofY+(y+bh-roofY)/2,`${q.r}cm`,\'start\');if(t>0||hint){content+=line(dx,roofY,dx,roofY+(y+bh-roofY)*(hint?1:t),\'aux\')}if(hint)content+=text(dx+12,roofY+25,\'↓ 補助線\',\'start\')}}\nsvg.innerHTML=content;$(\'#positionLabel\').textContent=t===0?\'はじめの形\':t===1?\'動かした形\':`移動中 ${Math.round(t*100)}%`;\n}\nfunction bindDrag(){const svg=$(\'#diagram\');let dragging=false;svg.addEventListener(\'pointerdown\',e=>{if(e.target.id!==\'dragPoint\'||$(\'#manipulation\').hidden)return;dragging=true;svg.setPointerCapture(e.pointerId);e.preventDefault()});svg.addEventListener(\'pointermove\',e=>{if(!dragging)return;cancelAnimationFrame(anim);const rect=svg.getBoundingClientRect(),a=Number(svg.dataset.start),b=Number(svg.dataset.end);t=Math.max(0,Math.min(1,(e.clientX-rect.left-a)/(b-a)));$(\'#movement\').value=String(Math.round(t*100));draw()});[\'pointerup\',\'pointercancel\',\'lostpointercapture\'].forEach(k=>svg.addEventListener(k,()=>dragging=false))}\nwindow.addEventListener(\'resize\',()=>{if(view===\'question\')draw();resize()});\n</script></body></html>\n'


def question_bank():
    bank = []
    def add(topic, family, n, prompt, choices, answer, explanation, **kwargs):
        bank.append(dict(id=f"{topic}_{family}_{n}", topic=topic, family=family,
                         prompt=prompt, choices=[str(x) for x in choices], answer=answer,
                         explanation=explanation, **kwargs))
    for n, (b, h) in enumerate([(6, 4), (8, 6), (10, 8)]):
        base = dict(b=b,h=h,alt="底辺を固定した三角形。頂点の移動前と移動後を比較します。",hint_label="高さの補助線",control="点Aを左右に動かす")
        for family, motion, h2, ans, prompt in [
            ('same','horizontal',h,1,'点Aを横に動かすと、三角形の広さは？'),
            ('up','up',h*2,0,'底辺を変えず、高さを2倍にすると、広さは？'),
            ('down','down',h/2,2,'底辺を変えず、高さを半分にすると、広さは？')]:
            explanation = ('底辺も高さも同じなので、面積はかわりません。' if motion=='horizontal' else '底辺が同じなら、面積は高さに比例します。'+('高さが2倍なので、面積も2倍です。' if motion=='up' else '高さが半分なので、面積も半分です。'))
            add('equal',family,n,prompt,['大きくなる','かわらない','小さくなる'],ans,explanation,motion=motion,h2=h2,**base)
        area=b*h//2
        add('equal','area',n,f'底辺{b}cm、高さ{h}cm。この三角形の面積は？',[f'{area}cm²',f'{b*h}cm²',f'{area+b}cm²',f'{b+h}cm²'],0,f'三角形の面積は、底辺×高さ÷2。{b}×{h}÷2＝{area}cm²です。',motion='horizontal',h2=h,**base)
        cutbase=dict(b=b,h=h,alt="平行四辺形の左の三角形を切って右へ平行移動すると長方形になります。",hint_label="切る位置の補助線",control="切った三角形を右へ移す")
        add('cut','area',n,f'底辺{b}cm、高さ{h}cm。平行四辺形の面積は？',[f'{b*h//2}cm²',f'{b*h}cm²',f'{b*h+b}cm²',f'{b+h}cm²'],1,f'左の三角形を右に移すと、横{b}cm・縦{h}cmの長方形。面積は{b}×{h}＝{b*h}cm²です。',**cutbase)
        add('cut','same',n,'左の三角形を切って右へ移すと、全体の広さは？',['大きくなる','小さくなる','かわらない'],2,'切った部分を、重ならないようにすき間なく移しただけなので、全体の面積はかわりません。',**cutbase)
        add('cut','shape',n,'三角形を右へ移すと、どの形になる？',['長方形','三角形','台形'],0,'左の三角形を右へ移すと、すき間なく長方形になります。',**cutbase)
        add('cut','height',n,'長方形に変えたとき、縦の長さは？',[f'{b}cm',f'{h}cm',f'{b+h}cm'],1,f'切った部分を横へ移しても、高さはかわりません。縦は{h}cmです。',**cutbase)
        linebase=dict(b=b,h=h,alt="長方形。左上と右下を結ぶ補助線で2つの三角形に分けられます。",hint_label="対角線を全部出す",control="左上と右下を結ぶ")
        add('line','diagonal_area',n,f'長方形に左上から右下へ線を引きます。できる三角形1つの面積は？',[f'{b*h}cm²',f'{b*h//2}cm²',f'{b+h}cm²',f'{b*h//2+b}cm²'],1,f'対角線で同じ広さの三角形2つに分かれます。{b}×{h}÷2＝{b*h//2}cm²です。',visual='diagonal',**linebase)
        add('line','diagonal_same',n,'長方形の対角線で分けた2つの三角形。広さは？',['同じ','上側が広い','下側が広い'],0,'対角線でできる2つの三角形は、ぴったり重なる合同な形です。面積も同じです。',visual='diagonal',**linebase)
        p=b//2;r=h//2;area=p*h+(b-p)*r
        lbase=dict(b=b,h=h,p=p,r=r,visual='lshape',alt="L字の図形。くぼみから下へ補助線を引くと長方形2つに分かれます。",hint_label="くぼみから下へ線を出す",control="くぼみから下へ線を引く")
        add('line','lshape_area',n,'L字の図形の面積は？',[f'{b*h}cm²',f'{area}cm²',f'{area-p}cm²',f'{b*h//2}cm²'],1,f'くぼみから下へ線を引くと、長方形2つ。{p}×{h}＋{b-p}×{r}＝{area}cm²です。',**lbase)
        add('line','lshape_split',n,'くぼみから下へまっすぐ線を引くと、何ができる？',['三角形2つ','長方形2つ','台形2つ'],1,'くぼみから底辺へ垂直に補助線を引くと、長方形2つに分けられます。',**lbase)
    # Stable but varied answer positions; no always-first correct option.
    for i,q in enumerate(bank):
        shift=i%len(q['choices']);q['choices']=q['choices'][shift:]+q['choices'][:shift];q['answer']=(q['answer']-shift)%len(q['choices'])
        assert len(set(q['choices']))==len(q['choices']), q['id']
    return bank


BANK = question_bank()
BY_ID = {q['id']:q for q in BANK}


def setting(name):
    value=os.environ.get(name,'')
    if value:return value
    try:return str(st.secrets.get(name,''))
    except (FileNotFoundError,st.errors.StreamlitSecretNotFoundError):return ''


def cloud_config():
    url=setting('SUPABASE_URL').rstrip('/')
    key=setting('SUPABASE_SECRET_KEY') or setting('SUPABASE_SERVICE_ROLE_KEY')
    if not url or not key:return None
    if not url.startswith('https://'):raise ValueError('SUPABASE_URL は https:// で設定してください。')
    # Secret key is server-only; an anon/publishable key cannot use this schema.
    if key.startswith('sb_publishable_'):raise ValueError('サーバー用の SUPABASE_SECRET_KEY または SERVICE_ROLE_KEY が必要です。')
    headers={'apikey':key,'Content-Type':'application/json'}
    if not key.startswith('sb_secret_'):headers['Authorization']='Bearer '+key
    return url+'/rest/v1/'+TABLE,headers


def valid_uuid(value):
    return str(UUID(str(value)))


def validate_rows(rows,device):
    if not isinstance(rows,list) or len(rows)>25:raise ValueError('送信件数が不正です。')
    clean=[]
    for row in rows:
        q=BY_ID.get(row.get('question_id'))
        answer=row.get('answer');seconds=row.get('seconds',0)
        if not q or type(answer) is not int or not 0<=answer<len(q['choices']):raise ValueError('回答が不正です。')
        if row.get('mode') not in ['learn','challenge','review']:raise ValueError('モードが不正です。')
        if type(seconds) not in [int,float] or not math.isfinite(seconds) or not 0<=seconds<=86400:raise ValueError('時間が不正です。')
        if type(row.get('hint_used')) is not bool:raise ValueError('ヒント情報が不正です。')
        created=datetime.fromisoformat(str(row['client_created']).replace('Z','+00:00'))
        if created.tzinfo is None:raise ValueError('日時にはタイムゾーンが必要です。')
        clean.append(dict(id=valid_uuid(row['id']),device_id=device,question_id=q['id'],mode=row['mode'],answer=answer,correct=answer==q['answer'],hint_used=row['hint_used'],seconds=int(seconds),client_created=created.astimezone(timezone.utc).isoformat()))
    return clean


def process_event(event,session,config,request=requests.request):
    request_id=valid_uuid(event.get('request_id'))
    device=valid_uuid(event.get('device_id'))
    if session.get('device') and session['device']!=device:raise ValueError('端末IDが一致しません。ページを再読み込みしてください。')
    session['device']=device
    response={'request_id':request_id,'configured':bool(config),'ok':False,'message':'この端末に保存（Supabase未設定）'}
    if event.get('type') not in ['load','save']:raise ValueError('操作が不正です。')
    if not config:return response
    url,headers=config
    try:
        if event['type']=='load':
            # The full random device UUID is the possession capability. No device listing API.
            result=request('GET',url,headers=headers,params={'device_id':'eq.'+device,'select':'id,question_id,mode,answer,correct,hint_used,seconds,client_created','order':'client_created.desc,id.desc','limit':'1000'},timeout=(4,12))
            result.raise_for_status();response['rows']=list(reversed(result.json()))
        else:
            rows=validate_rows(event.get('rows'),device)
            if rows:
                result=request('POST',url,headers={**headers,'Prefer':'resolution=ignore-duplicates,return=minimal'},params={'on_conflict':'id'},json=rows,timeout=(4,12));result.raise_for_status()
            response['ack']=[r['id'] for r in rows]
        response.update(ok=True,message='Supabaseと同期済み')
    except requests.RequestException as exc:
        status=getattr(getattr(exc,'response',None),'status_code',None)
        response['message']='端末に保存済み · 同期できません'+(f'（HTTP {status}）' if status else '')
    return response


@st.cache_resource
def get_component():
    digest=hashlib.sha256(FRONTEND.encode()).hexdigest()[:16]
    path=Path(tempfile.gettempdir())/('geometry_atelier_'+digest)
    path.mkdir(parents=True,exist_ok=True)
    (path/'index.html').write_text(FRONTEND,encoding='utf-8')
    return components.declare_component('geometry_atelier_v1',path=str(path))


def main():
    st.set_page_config(page_title='chokomana_ずけいのアトリエ',page_icon='🔷',layout='centered')
    st.markdown('<style>.block-container{padding-top:1rem;padding-bottom:0;max-width:820px}header[data-testid="stHeader"]{background:transparent}[data-testid="stMainBlockContainer"]{padding-left:.4rem;padding-right:.4rem}</style>',unsafe_allow_html=True)
    try:config=cloud_config()
    except ValueError as exc:st.error(str(exc));config=None
    state=st.session_state.setdefault('geometry_state',{})
    state.setdefault('response',{'configured':bool(config),'message':'記録を準備しています…'})
    event=get_component()(bank=BANK,topics=TOPICS,response=state['response'],key='geometry_atelier',default=None)
    if isinstance(event,dict) and event.get('request_id')!=state.get('last_request'):
        state['last_request']=event.get('request_id')
        try:state['response']=process_event(event,state,config)
        except (ValueError,TypeError,KeyError,AttributeError) as exc:
            state['response']={'request_id':event.get('request_id'),'configured':bool(config),'ok':False,'message':'同期する記録を確認できません。再読み込みしてください。'}
        st.rerun()


if __name__=='__main__':main()
