# frontend/crawler.py
# The neuron companion. It walks across the person's own words.
# Everything runs inside the browser: the words never leave this computer,
# and nothing is sent to any animation service.

import json

TEMPLATE = r'''<!doctype html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500&display=swap');
:root{--ivory:#ece6d8;--silver:#b4b8c8;--lav:#a9a6d6;--teal:#5fa8a0;--amber:#d9a441;}
*{box-sizing:border-box}
html,body{margin:0;color-scheme:dark;background:transparent;font-family:Inter,system-ui,sans-serif;color:var(--ivory)}
#wrap{border:1px solid rgba(236,230,216,.16);border-radius:18px;overflow:hidden;background:rgba(8,12,32,.92)}
#bar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;border-bottom:1px solid rgba(236,230,216,.12);font-size:13px;color:var(--silver)}
#toggle{font:inherit;color:var(--ivory);background:transparent;border:1px solid rgba(236,230,216,.35);border-radius:999px;padding:6px 18px;cursor:pointer}
#toggle:hover{border-color:var(--lav);background:rgba(169,166,214,.14)}
#toggle:focus-visible,#frame:focus-visible{outline:2px solid var(--lav);outline-offset:2px}
#frame{height:__H__px;overflow-y:auto;overflow-x:hidden;position:relative;scrollbar-color:rgba(169,166,214,.45) transparent}
#page{position:relative;padding:22px 26px 40px}
p{margin:0 0 16px;line-height:2.1;font-family:'Cormorant Garamond',Georgia,serif;font-size:19px;color:var(--silver)}
p.journal{color:var(--ivory)}
.w{display:inline-block;padding:0 3px}
.w.push{color:#f0c46c;text-decoration:underline dotted}
#cv{position:absolute;left:0;top:0;pointer-events:none;z-index:2}
.empty{color:var(--silver);padding:40px;text-align:center}
</style></head><body>
<div id="wrap">
  <div id="bar"><span id="count-wrap">Words explored: <b id="count">0</b></span>
    <button id="toggle" type="button">Stop</button></div>
  <div id="frame" tabindex="0" aria-label="Your responses, with the neuron animation">
    <div id="page"><canvas id="cv" aria-hidden="true"></canvas></div>
  </div>
</div>
<script>
(function(){
var DATA = __DATA__;
var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var frame=document.getElementById('frame'), page=document.getElementById('page');
var cv=document.getElementById('cv'), ctx=cv.getContext('2d');
var btn=document.getElementById('toggle'), countEl=document.getElementById('count');
var PALETTE=['#a9a6d6','#5fa8a0','#ece6d8','#d9a441'];
var words=[];

DATA.paras.forEach(function(p){
  var el=document.createElement('p');
  if(p.kind==='journal'){el.className='journal';}
  p.text.split(/\s+/).filter(Boolean).forEach(function(tok){
    var s=document.createElement('span'); s.className='w'; s.textContent=tok;
    var key=tok.toLowerCase().replace(/[^a-z']/g,'');
    if(p.kind==='journal' && DATA.weights && DATA.weights[key]>0.8){s.className+=' push';}
    el.appendChild(s); el.appendChild(document.createTextNode(' '));
    words.push({el:s,text:tok,x:0,y:0,w:0,h:0,cx:0,cy:0});
  });
  page.appendChild(el);
});
if(!words.length){
  page.innerHTML='<div class="empty">Nothing to show yet. Answer a few questions and your words will appear here.</div>';
  btn.style.display='none'; document.getElementById('count-wrap').style.display='none';
  return;
}

var running=!reduce, raf=null, last=0, t=0, laidOut=false, W=0, H=0;
var soma={x:0,y:0}, arms=[], cur=0, nextAt=0, reassignAt=0, measureAt=0, popped=false;
var seen={}, seenCount=0, touched={}, pops=[], client=null, userScrollUntil=0;
for(var i=0;i<8;i++){arms.push({x:0,y:0,tx:0,ty:0,word:-1});}

function rgba(hex,a){var n=parseInt(hex.slice(1),16);return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}
function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}

function assign(snap){
  var d=[],k;
  for(k=0;k<words.length;k++){var dx=words[k].cx-soma.x, dy=words[k].cy-soma.y; d.push([dx*dx+dy*dy,k]);}
  d.sort(function(a,b){return a[0]-b[0];});
  var cand=d.slice(0,Math.min(8,d.length)).map(function(e){return e[1];});
  arms.forEach(function(a){
    if(!cand.length){a.word=-1;a.tx=soma.x;a.ty=soma.y;if(snap){a.x=soma.x;a.y=soma.y;}return;}
    var best=0,bd=1e18;
    for(var j=0;j<cand.length;j++){var w=words[cand[j]],ex=w.cx-a.x,ey=w.cy-a.y,dd=ex*ex+ey*ey;if(dd<bd){bd=dd;best=j;}}
    var wi=cand.splice(best,1)[0];
    a.word=wi;a.tx=words[wi].cx;a.ty=words[wi].cy;
    if(snap){a.x=a.tx;a.y=a.ty;}
  });
}

function measure(){
  var pr=page.getBoundingClientRect();
  for(var i=0;i<words.length;i++){
    var w=words[i], r=w.el.getBoundingClientRect();
    w.x=r.left-pr.left; w.y=r.top-pr.top; w.w=r.width; w.h=r.height;
    w.cx=w.x+w.w/2; w.cy=w.y+w.h/2;
  }
}
function sizeCanvas(){
  var dpr=window.devicePixelRatio||1;
  W=page.clientWidth; H=page.offsetHeight;
  cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
  cv.style.width=W+'px'; cv.style.height=H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
}
function layout(){
  if(frame.clientWidth===0){laidOut=false;return;}
  sizeCanvas();
  measure();
  if(!laidOut){soma.x=words[0].cx;soma.y=words[0].cy;assign(true);}
  laidOut=true;
  if(!running){draw();}
}

function step(dt){
  t+=dt;
  if(t>=measureAt){                       /* the text can re-flow (fonts, scrollbar): measure again */
    if(page.clientWidth!==W||page.offsetHeight!==H){sizeCanvas();}
    measure(); measureAt=t+0.4;
  }
  var pr=page.getBoundingClientRect(), pointer=null;
  if(client){
    pointer={x:client.x-pr.left,y:client.y-pr.top};
    if(pointer.x<0||pointer.y<0||pointer.x>W||pointer.y>H){pointer=null;}
  }
  if(t>=nextAt){cur=(cur+1+Math.floor(Math.random()*5))%words.length;nextAt=t+1.5+Math.random()*0.9;popped=false;}
  var wt=words[cur], gx=wt.cx, gy=wt.cy;
  if(pointer){gx+=(pointer.x-gx)*0.3; gy+=(pointer.y-gy)*0.3;}   /* follows the cursor a little */
  var k=1-Math.exp(-dt*2.2);
  soma.x+=(gx-soma.x)*k; soma.y+=(gy-soma.y)*k;
  if(t>=reassignAt){assign(false);reassignAt=t+0.4;}
  var ka=1-Math.exp(-dt*7);
  arms.forEach(function(a,i){
    a.x+=(a.tx-a.x)*ka; a.y+=(a.ty-a.y)*ka;
    if(a.word>=0 && Math.abs(a.x-a.tx)<6 && Math.abs(a.y-a.ty)<6){
      if(!seen[a.word]){seen[a.word]=1;seenCount++;countEl.textContent=seenCount;}
      touched[a.word]={t:t,c:PALETTE[i%PALETTE.length]};
    }
  });
  if(!popped && Math.hypot(soma.x-wt.cx,soma.y-wt.cy)<22){
    pops.push({text:wt.text.replace(/[^\p{L}\p{N}']/gu,''),x:wt.cx,y:wt.y,t:t});
    popped=true; if(pops.length>4){pops.shift();}
  }
  if(performance.now()>userScrollUntil){
    var target=wt.cy-frame.clientHeight/2, max=frame.scrollHeight-frame.clientHeight;
    target=Math.max(0,Math.min(max,target));
    frame.scrollTop+=(target-frame.scrollTop)*(1-Math.exp(-dt*0.9));
  }
}

function draw(){
  ctx.clearRect(0,0,W,H);
  var key,w;
  for(key in touched){
    var v=touched[key], al=1-(t-v.t)/10;
    if(al<=0){delete touched[key];continue;}
    w=words[key]; rr(w.x-1,w.y+2,w.w+2,w.h-4,6);
    ctx.fillStyle=rgba(v.c,al*0.12); ctx.fill();
    ctx.strokeStyle=rgba(v.c,al*0.85); ctx.lineWidth=1.1; ctx.stroke();
  }
  var cw=words[cur]; rr(cw.x-1,cw.y+2,cw.w+2,cw.h-4,6);
  ctx.fillStyle='rgba(169,166,214,.22)'; ctx.fill();

  arms.forEach(function(a,i){
    var dx=a.x-soma.x, dy=a.y-soma.y, len=Math.hypot(dx,dy)||1;
    var nx=-dy/len, ny=dx/len, wob=Math.sin(t*1.4+i*1.7)*Math.min(18,len*0.18);
    var mx=(soma.x+a.x)/2+nx*wob, my=(soma.y+a.y)/2+ny*wob, c=PALETTE[i%PALETTE.length];
    ctx.beginPath(); ctx.moveTo(soma.x,soma.y); ctx.quadraticCurveTo(mx,my,a.x,a.y);
    ctx.strokeStyle=rgba(c,0.8); ctx.lineWidth=1.3; ctx.stroke();
    var ang=Math.atan2(a.y-my,a.x-mx);
    [-0.6,0.6].forEach(function(s){
      ctx.beginPath(); ctx.moveTo(a.x,a.y);
      ctx.lineTo(a.x+Math.cos(ang+s)*8,a.y+Math.sin(ang+s)*8); ctx.stroke();
    });
    ctx.beginPath(); ctx.arc(a.x,a.y,2.8,0,6.283); ctx.fillStyle=c; ctx.fill();
  });

  var g=ctx.createRadialGradient(soma.x,soma.y,2,soma.x,soma.y,22);
  g.addColorStop(0,'rgba(169,166,214,.55)'); g.addColorStop(1,'rgba(169,166,214,0)');
  ctx.fillStyle=g; ctx.beginPath(); ctx.arc(soma.x,soma.y,22,0,6.283); ctx.fill();
  ctx.beginPath(); ctx.arc(soma.x,soma.y,7,0,6.283); ctx.fillStyle='#dcd8f5'; ctx.fill();
  ctx.beginPath(); ctx.arc(soma.x,soma.y,2.6,0,6.283); ctx.fillStyle='#2b3260'; ctx.fill();

  pops=pops.filter(function(p){return t-p.t<2;});
  pops.forEach(function(p){
    var age=t-p.t, al=1-age/2;
    ctx.font='600 26px "Cormorant Garamond", Georgia, serif';
    var tw=ctx.measureText(p.text).width;
    var x=Math.max(14,Math.min(W-tw-24,p.x-tw/2)), y=Math.max(34,p.y-16-age*14);
    rr(x-10,y-26,tw+20,36,10);
    ctx.fillStyle=rgba('#5fa8a0',al*0.28); ctx.fill();
    ctx.strokeStyle=rgba('#5fa8a0',al*0.8); ctx.lineWidth=1; ctx.stroke();
    ctx.fillStyle=rgba('#ece6d8',al); ctx.fillText(p.text,x,y);
  });
}

function loop(ts){
  if(!running){return;}
  var now=ts/1000, dt=last?Math.min(0.05,now-last):0.016; last=now;
  if(!laidOut){layout();}
  if(laidOut){step(dt);draw();}
  raf=requestAnimationFrame(loop);
}
function start(){running=true;last=0;btn.textContent='Stop';raf=requestAnimationFrame(loop);}
function stop(){running=false;cancelAnimationFrame(raf);btn.textContent='Start';}
btn.onclick=function(){if(running){stop();}else{start();}};

frame.addEventListener('mousemove',function(e){client={x:e.clientX,y:e.clientY};});
frame.addEventListener('mouseleave',function(){client=null;});
frame.addEventListener('wheel',function(){userScrollUntil=performance.now()+4000;},{passive:true});
frame.addEventListener('touchmove',function(){userScrollUntil=performance.now()+4000;},{passive:true});
if(window.ResizeObserver){var ro=new ResizeObserver(function(){layout();});ro.observe(frame);ro.observe(page);}
window.addEventListener('resize',layout);
if(document.fonts){if(document.fonts.ready){document.fonts.ready.then(layout);}document.fonts.onloadingdone=layout;}

layout();
if(reduce){btn.textContent='Play animation';}else{start();}
})();
</script></body></html>'''


def build_html(paragraphs, weights=None, height=480):
    """paragraphs: list of {"kind": "answer" | "journal", "text": str}"""
    data = json.dumps({"paras": paragraphs, "weights": weights or {}})
    data = data.replace("</", "<\\/")            # keeps the text from closing the script tag
    return TEMPLATE.replace("__DATA__", data).replace("__H__", str(int(height)))


def show(paragraphs, weights=None, height=480):
    import streamlit.components.v1 as components
    components.html(build_html(paragraphs, weights, height), height=height + 64, scrolling=False)