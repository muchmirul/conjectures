"""Build one playable page per chapter, so the reader can move the ideas around.

    cd zeta-critical-line && make play

Writes ../docs/zeta-critical-line/play/NN.html, one per chapter, plus an
index.  Each page is self contained: no libraries, no network, one canvas and
a few controls.  Reading that the zeta path strikes the centre is weaker than
steering the height yourself and watching it strike, so every chapter with a
claim in it gets a control that pokes at that claim.

The mathematics in these pages is the same mathematics as `src/zeta_guide`,
re-expressed in JavaScript.  `tests/test_interactive.py` runs the pages'
JavaScript and compares it with the Python library at sample points, so the
page and the library cannot drift apart silently.
"""

from __future__ import annotations

from pathlib import Path

from zeta_guide.core import zero_heights

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "zeta-critical-line" / "play"

ZEROS_JS = ",".join(f"{g:.12f}" for g in zero_heights()[:50])

# --- shared maths, kept in one place so the checks can find it -------------

MATHS = r"""
// the first fifty zero heights, from the repository's shipped table
const ZEROS=[__ZEROS__];

// complex helpers: numbers are [re, im]
function cadd(a,b){ return [a[0]+b[0],a[1]+b[1]]; }
function cmul(a,b){ return [a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]]; }
function cdiv(a,b){ const d=b[0]*b[0]+b[1]*b[1];
  return [(a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d]; }
// n^(-s) for real n>0: exp(-s ln n)
function npow(n,s){ const ln=Math.log(n),m=Math.exp(-s[0]*ln),t=-s[1]*ln;
  return [m*Math.cos(t),m*Math.sin(t)]; }

// zeta by Euler-Maclaurin, the same recipe as zeta_guide.core.zeta_em
function zetaEM(sre,sim){
  const s=[sre,sim],N=Math.max(60,Math.floor(1.3*Math.abs(sim))+20);
  let out=[0,0];
  for(let n=1;n<N;n++) out=cadd(out,npow(n,s));
  out=cadd(out,cdiv(npow(N,[s[0]-1,s[1]]),[s[0]-1,s[1]]));
  out=cadd(out,cmul([0.5,0],npow(N,s)));
  out=cadd(out,cmul(cdiv(s,[12,0]),npow(N,[s[0]+1,s[1]])));
  const s12=cmul(s,cmul([s[0]+1,s[1]],[s[0]+2,s[1]]));
  out=cadd(out,cmul(cdiv(s12,[-720,0]),npow(N,[s[0]+3,s[1]])));
  const s34=cmul(s12,cmul([s[0]+3,s[1]],[s[0]+4,s[1]]));
  out=cadd(out,cmul(cdiv(s34,[30240,0]),npow(N,[s[0]+5,s[1]])));
  return out;
}

// primes and prime powers, as in zeta_guide.core
function primesUpTo(x){
  const s=new Array(x+1).fill(true);s[0]=s[1]=false;
  for(let p=2;p*p<=x;p++)if(s[p])for(let q=p*p;q<=x;q+=p)s[q]=false;
  const out=[];for(let n=2;n<=x;n++)if(s[n])out.push(n);
  return out;
}
function vmTerms(x){
  const out=[];
  for(const p of primesUpTo(x)){let q=p;while(q<=x){out.push([q,Math.log(p)]);q*=p;}}
  return out.sort((a,b)=>a[0]-b[0]);
}
function psiStair(x,terms){
  let s=0;for(const [n,w] of terms)if(n<=x)s+=w;return s;
}

// the explicit formula's rebuild from the first K zero-waves
function psiWaves(x,K){
  let out=x-Math.log(2*Math.PI)-0.5*Math.log1p(-Math.pow(x,-2));
  const lx=Math.log(x);
  for(let k=0;k<K;k++){
    const g=ZEROS[k],r=Math.hypot(0.5,g),ang=Math.atan2(g,0.5);
    out-=2*Math.sqrt(x)/r*Math.cos(g*lx-ang);
  }
  return out;
}

// the prime-built density pointing back at the zeros
function primeDensity(tau,xcut){
  let out=Math.log(tau/(2*Math.PI))/(2*Math.PI);
  for(const [n,w] of vmTerms(xcut))
    out-=w/(Math.PI*Math.sqrt(n))*Math.cos(tau*Math.log(n));
  return out;
}

// the paper's shape functions and constants (equation 1.3 and section 7.1)
function shapeH(lam){ return 2-1/lam-lam/3; }
function shapeHd(lam){ return (1+shapeH(lam))/2; }
function shapeF(lam){ return lam/(1+lam*lam/3); }
function energyPerCount(lam){ return 1/lam+lam/3; }
function mtConstant(){ const t=Math.tan(1/Math.SQRT2);
  return 2*t/(Math.SQRT2+t); }

// the whole-number trick
function charge(m){ return m*m; }
function floor3(m){ return 3*m-2; }

// the toy family's window transform (stretch 100 to 200, dial one), the
// same recipe as zeta_guide.core.ToyFamily.response, by direct integration
const TOY_L=Math.log(100/(2*Math.PI)),TOY_W=0.2*TOY_L/2,TOY_H=2*Math.PI/TOY_L;
function rampProfile(x){ x=Math.min(1,Math.max(0,x));
  return x-Math.sin(2*Math.PI*x)/(2*Math.PI); }
function toyResponse(r){
  const n=1500,du=(TOY_L/2)/n;let s=0;
  for(let i=0;i<=n;i++){
    const u=i*du,v=rampProfile((TOY_L/2-u)/TOY_W)*Math.cos(r*u);
    s+=(i===0||i===n)?v/2:v;
  }
  return 2*s*du;
}
// the array's constant total (the sampling identity's right-hand side)
const TOY_AL2=(function(){
  const n=1500,du=(TOY_L/2)/n;let s=0;
  for(let i=0;i<=n;i++){
    const u=i*du,p=rampProfile((TOY_L/2-u)/TOY_W);
    s+=(i===0||i===n)?p*p/2:p*p;
  }
  return 2*s*du*TOY_L;
})();

// eigenvalues of a symmetric 2x2 table [[a,b],[b,c]]
function eig2(a,b,c){
  const t=(a+c)/2,d=Math.sqrt(((a-c)/2)**2+b*b);
  return [t-d,t+d];
}

// --- a very small plotting helper -----------------------------------------
function Plot(canvas,xlo,xhi,ylo,yhi,pad){
  const ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  pad=pad||{l:52,r:16,t:16,b:38};
  const X=x=>pad.l+(x-xlo)/(xhi-xlo)*(W-pad.l-pad.r);
  const Y=y=>H-pad.b-(y-ylo)/(yhi-ylo)*(H-pad.t-pad.b);
  return {ctx,X,Y,W,H,pad,
    clear(){ctx.clearRect(0,0,W,H);},
    axes(xlabel,ylabel){
      ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;ctx.beginPath();
      ctx.moveTo(pad.l,pad.t);ctx.lineTo(pad.l,H-pad.b);ctx.lineTo(W-pad.r,H-pad.b);ctx.stroke();
      ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='center';
      if(xlabel)ctx.fillText(xlabel,(pad.l+W-pad.r)/2,H-8);
      if(ylabel){ctx.save();ctx.translate(13,(pad.t+H-pad.b)/2);ctx.rotate(-Math.PI/2);
        ctx.fillText(ylabel,0,0);ctx.restore();}
    },
    curve(f,color,lw,n){n=n||400;ctx.strokeStyle=color;ctx.lineWidth=lw||2.2;ctx.beginPath();
      for(let i=0;i<=n;i++){const x=xlo+(xhi-xlo)*i/n,y=f(x);
        if(i===0)ctx.moveTo(X(x),Y(y));else ctx.lineTo(X(x),Y(y));}ctx.stroke();},
    line(xs,ys,color,lw){ctx.strokeStyle=color;ctx.lineWidth=lw||2;ctx.beginPath();
      for(let i=0;i<xs.length;i++){if(i===0)ctx.moveTo(X(xs[i]),Y(ys[i]));
        else ctx.lineTo(X(xs[i]),Y(ys[i]));}ctx.stroke();},
    dots(xs,ys,color,r){ctx.fillStyle=color;
      for(let i=0;i<xs.length;i++){ctx.beginPath();ctx.arc(X(xs[i]),Y(ys[i]),r||3.4,0,7);ctx.fill();}},
    hline(y,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(pad.l,Y(y));ctx.lineTo(W-pad.r,Y(y));ctx.stroke();ctx.restore();},
    vline(x,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(X(x),pad.t);ctx.lineTo(X(x),H-pad.b);ctx.stroke();ctx.restore();},
    label(x,y,text,color,align){ctx.fillStyle=color;ctx.font='12px system-ui';
      ctx.textAlign=align||'left';ctx.fillText(text,X(x),Y(y));}
  };
}
""".replace("__ZEROS__", ZEROS_JS)

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITLE</title>
<style>
 :root{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
        --line:#e1e0d9;--blue:#2a78d6;--green:#008300;--red:#d03b3b;--violet:#4a3aa7;}
 @media (prefers-color-scheme: dark){
   :root{--surface:#15150f;--ink:#f2f1ea;--ink2:#c9c7bd;--muted:#8d8b82;--line:#33322c;}
 }
 *{box-sizing:border-box}
 body{margin:0;padding:28px 20px 56px;background:var(--surface);color:var(--ink);
   font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;}
 main{max-width:760px;margin:0 auto}
 .back{font-size:14px;color:var(--muted);text-decoration:none}
 .back:hover{color:var(--blue)}
 h1{font-size:24px;line-height:1.25;margin:14px 0 6px}
 .lede{color:var(--ink2);margin:0 0 22px}
 .try{border-left:3px solid var(--blue);padding:8px 0 8px 14px;margin:0 0 22px;
   color:var(--ink2);font-size:15px}
 canvas{width:100%;height:auto;display:block;border-radius:8px;background:var(--surface)}
 .controls{margin:18px 0 0}
 .row{display:flex;align-items:center;gap:12px;margin:10px 0}
 .row label{flex:0 0 190px;font-size:14px;color:var(--ink2)}
 input[type=range]{flex:1;accent-color:var(--blue)}
 .val{flex:0 0 90px;text-align:right;font-family:ui-monospace,monospace;font-size:13px}
 .readout{margin-top:18px;padding:14px 16px;border:1px solid var(--line);border-radius:8px;
   font-family:ui-monospace,monospace;font-size:14px;white-space:pre-line}
 .verdict-ok{color:var(--green)} .verdict-no{color:var(--red)}
 .nav{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);font-size:14px}
 .nav a{color:var(--blue);text-decoration:none} .nav a:hover{text-decoration:underline}
 .note{margin-top:26px;font-size:13.5px;color:var(--muted)}
 /* embedded in the article: drop the chrome the article already provides */
 body.embed{padding:14px 16px 18px}
 body.embed .back, body.embed h1, body.embed .lede, body.embed .nav{display:none}
 body.embed .try{margin-top:0}
</style>
</head>
<body>
<main>
<a class="back" href="../index.html">back to the article</a>
<h1>HEADING</h1>
<p class="lede">LEDE</p>
<p class="try"><strong>Try this.</strong> TRY</p>
<canvas id="c" width="720" height="380"></canvas>
<div class="controls">CONTROLS</div>
<div class="readout" id="out"></div>
<p class="note">NOTE</p>
<div class="nav">NAV</div>
</main>
<script>
if(location.search.indexOf('embed')>=0) document.body.classList.add('embed');
MATHS
WIDGET
</script>
</body>
</html>
"""


def slider(ident, label, lo, hi, step, value):
    return (f'<div class="row"><label for="{ident}">{label}</label>'
            f'<input type="range" id="{ident}" min="{lo}" max="{hi}" '
            f'step="{step}" value="{value}">'
            f'<span class="val" id="{ident}v"></span></div>')


CHAPTERS = [
    # (number, folder, heading, lede, try, controls, widget js, note)
    (0, "00-start-here", "Steer the zeta path",
     "The value of zeta along the critical line, drawn as a path in the "
     "plane. The slider is the height.",
     "Push the height upward slowly and watch the path swing around and "
     "strike the centre. Every strike is a zero; the first comes at height "
     "14.13, and they never stop.",
     slider("tmax", "height climbed so far", 5, 60, 0.25, 20),
     r"""
const cv=document.getElementById('c');
const tmax=document.getElementById('tmax');
const P=Plot(cv,-2.4,4.8,-3.0,3.2,{l:16,r:16,t:16,b:16});
function draw(){
  const T=parseFloat(tmax.value);
  P.clear();
  P.hline(0,'#c3c2b7');P.vline(0,'#c3c2b7');
  const n=Math.max(60,Math.round(T*22));
  const xs=[],ys=[];
  for(let i=0;i<=n;i++){
    const t=1+(T-1)*i/n,z=zetaEM(0.5,t);
    xs.push(z[0]);ys.push(z[1]);
  }
  P.line(xs,ys,'#2a78d6',1.5);
  P.dots([xs[n]],[ys[n]],'#2a78d6',5);
  const struck=ZEROS.filter(g=>g<=T);
  P.ctx.beginPath();P.ctx.arc(P.X(0),P.Y(0),8,0,7);
  P.ctx.strokeStyle='#008300';P.ctx.lineWidth=2.2;P.ctx.stroke();
  tmaxv.textContent=T.toFixed(2);
  const near=struck.length&&Math.abs(T-struck[struck.length-1])<0.6;
  const out=document.getElementById('out');
  out.textContent='height  '+T.toFixed(2)+'\n'+
    'zeros struck so far  '+struck.length+
    (struck.length?'\nlatest at height '+struck[struck.length-1].toFixed(2):'');
  out.className='readout '+(near?'verdict-ok':'');
}
tmax.addEventListener('input',draw);draw();
""",
     "Zeta is computed live in this page, by the same recipe as the "
     "repository's Python library, and the zero heights come from the same "
     "shipped table the tests re-verify."),

    (1, "01-the-primes", "Walk the staircase",
     "The prime count climbing, against the smooth curve Gauss guessed at "
     "fifteen.",
     "Stretch the range and watch the two curves. The staircase never "
     "strays far from the smooth guess, and never quite agrees with it "
     "either. The gap between them is the wobble the zeros orchestrate.",
     slider("xmax", "how far to count", 50, 2000, 25, 300),
     r"""
const cv=document.getElementById('c');
const xmax=document.getElementById('xmax');
function li(x){ // Gauss's curve: the area under 1/log t, from 2, plus li(2)
  let s=1.04516378,t=2;const dt=x/4000;
  while(t+dt<=x){s+=dt/Math.log(t+dt/2);t+=dt;}
  s+=(x-t)/Math.log((t+x)/2);
  return s;
}
function draw(){
  const X=parseInt(xmax.value);
  const ps=primesUpTo(X);
  const P=Plot(cv,0,X,0,Math.max(10,li(X)*1.08));
  P.clear();P.axes('numbers up to '+X,'primes seen so far');
  P.curve(x=>x<4?li(4)*x/4:li(x),'#898781',1.6);
  const xs=[0],ys=[0];let c=0;
  for(const p of ps){xs.push(p,p);ys.push(c,c+1);c++;}
  xs.push(X);ys.push(c);
  P.line(xs,ys,'#2a78d6',1.7);
  P.label(X*0.98,li(X)*0.9,'the smooth guess','#898781','right');
  xmaxv.textContent=String(X);
  document.getElementById('out').textContent=
    'primes up to '+X+'        '+c+'\n'+
    'the smooth guess there   '+li(X).toFixed(1)+'\n'+
    'the wobble               '+(c-li(X)).toFixed(1);
}
xmax.addEventListener('input',draw);draw();
""",
     "The smooth curve is Gauss's logarithmic-integral guess, computed here "
     "by direct integration. In this whole range the truth runs slightly "
     "under the guess; Littlewood proved the sign nevertheless flips "
     "infinitely often, unimaginably far out."),

    (2, "02-riemanns-map", "Slice the landscape",
     "The size of zeta along one vertical slice of the strip. The slider "
     "moves the slice sideways.",
     "Start away from the middle and watch the valley floor: it dips but "
     "never touches zero. Slide to one half and every dip lands exactly on "
     "the floor, at the marked heights. As far as anyone has ever computed, "
     "the touching happens only there.",
     slider("sig", "the slice's first coordinate", 0, 1, 0.01, 0.2),
     r"""
const cv=document.getElementById('c');
const sig=document.getElementById('sig');
const marks=ZEROS.filter(g=>g<=50);
function draw(){
  const s=parseFloat(sig.value);
  const P=Plot(cv,2,50,0,4.2);
  P.clear();P.axes('height along the slice','size of zeta');
  for(const g of marks)P.vline(g,'#f0b5b5');
  let mn=1e9;
  P.curve(t=>{
    const z=zetaEM(s,t),v=Math.hypot(z[0],z[1]);
    if(t>3&&v<mn)mn=v;
    return Math.min(v,4.2);
  },'#2a78d6',1.8,700);
  sigv.textContent=s.toFixed(2);
  const onLine=Math.abs(s-0.5)<0.005;
  const out=document.getElementById('out');
  out.textContent='slice at first coordinate  '+s.toFixed(2)+'\n'+
    'lowest point of the curve  '+mn.toFixed(4)+'\n'+
    (onLine?'on the critical line: the dips reach zero, at the marked heights'
           :'off the line: the curve dips but never reaches zero');
  out.className='readout '+(onLine?'verdict-ok':'');
}
sig.addEventListener('input',draw);draw();
""",
     "Zeta is computed live along the slice, by the same recipe as the "
     "repository's Python library, and the marked heights come from the "
     "shipped zero table. That the touching happens only at one half is "
     "the Riemann hypothesis, verified here only as far as the picture "
     "reaches."),

    (3, "03-the-music", "Add the waves yourself",
     "The prime staircase, and the explicit formula's rebuild from the "
     "first zero-waves.",
     "Add waves one at a time. With none, the rebuild is a featureless "
     "ramp; each wave adds one frequency, and by fifty the corners of the "
     "staircase have assembled themselves out of pure tones.",
     slider("waves", "zero-waves added", 0, 50, 1, 0),
     r"""
const cv=document.getElementById('c');
const waves=document.getElementById('waves');
const terms=vmTerms(60);
function draw(){
  const K=parseInt(waves.value);
  const P=Plot(cv,2,50,0,52);
  P.clear();P.axes('position along the numbers','weighted prime tally');
  P.curve(x=>psiStair(x,terms),'#898781',1.6,900);
  P.curve(x=>psiWaves(x,K),'#2a78d6',1.8,900);
  wavesv.textContent=String(K);
  let err=0,n=0;
  for(let x=2.5;x<=50;x+=0.5){err+=Math.abs(psiWaves(x,K)-psiStair(x,terms));n++;}
  const out=document.getElementById('out');
  out.textContent='zero-waves added      '+K+'\n'+
    'average miss          '+(err/n).toFixed(2);
  out.className='readout '+(K>=40?'verdict-ok':'');
}
waves.addEventListener('input',draw);draw();
""",
     "The gray curve steps up at every prime and prime power, weighted the "
     "standard way; the blue curve is the smooth ramp minus one cosine per "
     "zero. The identity behind the convergence is Riemann's explicit "
     "formula, and the tests check the miss really shrinks."),

    (5, "05-four-counts", "Tally a stretch four ways",
     "Eight pin slots on a stretch of the strip. Click a slot to cycle it: "
     "clean on the line, doubled, or a mirror pair.",
     "Make a few pins doubled and a few into mirror pairs, and watch which "
     "counters move apart. The theorems bound three of the counters "
     "against the first.",
     "",
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const N=8,kinds=new Array(N).fill(0); // 0 clean, 1 doubled, 2 pair
const hs=[...Array(N)].map((_,i)=>50+i*38);
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const x0=250,x1=470,mid=(x0+x1)/2;
  ctx.fillStyle='rgba(180,175,160,0.15)';ctx.fillRect(x0,20,x1-x0,340);
  ctx.strokeStyle='#2a78d6';ctx.lineWidth=2.4;
  ctx.beginPath();ctx.moveTo(mid,20);ctx.lineTo(mid,360);ctx.stroke();
  let full=0,dist=0,online=0,clean=0;
  kinds.forEach((k,i)=>{
    const y=hs[i];
    if(k===0){
      ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(mid,y,7,0,7);ctx.fill();
      full+=1;dist+=1;online+=1;clean+=1;
    }else if(k===1){
      ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.arc(mid,y,10,0,7);ctx.stroke();
      ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(mid,y,4,0,7);ctx.fill();
      full+=2;dist+=1;online+=1;
    }else{
      ctx.fillStyle='#d03b3b';
      ctx.beginPath();ctx.arc(mid-60,y,7,0,7);ctx.fill();
      ctx.beginPath();ctx.arc(mid+60,y,7,0,7);ctx.fill();
      ctx.strokeStyle='#d03b3b';ctx.setLineDash([3,4]);ctx.lineWidth=1;
      ctx.beginPath();ctx.moveTo(mid-53,y);ctx.lineTo(mid+53,y);ctx.stroke();
      ctx.setLineDash([]);
      full+=2;dist+=2;
    }
  });
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('click a pin to change its kind',30,30);
  const out=document.getElementById('out');
  out.textContent=
    'the full count        '+full+'\n'+
    'the distinct count    '+dist+'\n'+
    'the on-line count     '+online+'\n'+
    'the clean-line count  '+clean+'\n'+
    'theorems (in the limit): on-line and clean-line at least 2/3 of full,\n'+
    'distinct at least 5/6 of full';
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const y=(e.clientY-r.top)*cv.height/r.height;
  let best=0,bd=1e9;
  hs.forEach((h,i)=>{const d=Math.abs(y-h);if(d<bd){bd=d;best=i;}});
  if(bd<26){kinds[best]=(kinds[best]+1)%3;draw();}
});
draw();
""",
     "Doubled pins and mirror pairs are synthetic: every zero anyone has "
     "computed is clean and on the line. The counters here move exactly the "
     "way the paper's four counting functions do."),

    (6, "06-the-microphones", "Slide a zero along the array",
     "Seven microphones of the toy array, and one zero you can move. Each "
     "microphone's share changes; the array's total does not.",
     "Park the zero on a microphone, then exactly between two. The shares "
     "redistribute completely, and the total printed below never moves. "
     "This fair sharing is why the table's diagonal counts every zero "
     "once, wherever it sits.",
     slider("zp", "the zero's position, in spacings", 0, 6, 0.02, 1.5),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const zp=document.getElementById('zp');
const SHOW=7,peak=toyResponse(0);
// the bump curves never change, so they are sampled once
const rlo=-2.5,rhi=6*TOY_H+2.5,NPT=200;
const CURVES=[...Array(SHOW)].map((_,k)=>
  [...Array(NPT+1)].map((_,i)=>{
    const r=rlo+(rhi-rlo)*i/NPT;
    return toyResponse(r-k*TOY_H)/peak;
  }));
function draw(){
  const pos=parseFloat(zp.value)*TOY_H;
  ctx.clearRect(0,0,cv.width,cv.height);
  // the bumps, drawn across the top half
  const x0=40,x1=680,y0=120,amp=78;
  const X=r=>x0+(r-rlo)/(rhi-rlo)*(x1-x0);
  for(let k=0;k<SHOW;k++){
    ctx.strokeStyle=k%2?'#00787a':'#2a78d6';ctx.lineWidth=1.3;ctx.beginPath();
    for(let i=0;i<=NPT;i++){
      const r=rlo+(rhi-rlo)*i/NPT;
      const x=X(r),y=y0-CURVES[k][i]*amp;
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
  }
  ctx.strokeStyle='#d03b3b';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(X(pos),18);ctx.lineTo(X(pos),y0+26);ctx.stroke();
  // the shares, as bars across the bottom half
  let total=0;
  for(let k=-40;k<=46;k++){const v=toyResponse(pos-k*TOY_H);total+=v*v;}
  total/=TOY_AL2;
  for(let k=0;k<SHOW;k++){
    const share=Math.pow(toyResponse(pos-k*TOY_H),2)/TOY_AL2;
    const bx=70+k*88,bh=share*160;
    ctx.fillStyle=k%2?'#00787a':'#2a78d6';
    ctx.fillRect(bx,330-bh,52,Math.max(1.5,bh));
    ctx.fillStyle='#52514e';ctx.font='11px system-ui';ctx.textAlign='center';
    ctx.fillText('mic '+k,bx+26,348);
    ctx.fillText(share.toFixed(2),bx+26,326-bh);
  }
  ctx.strokeStyle='#008300';ctx.setLineDash([5,4]);ctx.beginPath();
  ctx.moveTo(55,330-160);ctx.lineTo(690,330-160);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle='#008300';ctx.font='11px system-ui';ctx.textAlign='right';
  ctx.fillText('one whole zero',688,330-166);
  zpv.textContent=parseFloat(zp.value).toFixed(2);
  document.getElementById('out').textContent=
    'total over the whole array  '+total.toFixed(4)+'  (constant)\n'+
    'the sampling identity behind the count of chapter 8';
  document.getElementById('out').className='readout verdict-ok';
}
zp.addEventListener('input',draw);draw();
""",
     "The window and spacing are the toy family's, the same ones the "
     "figures and tests use, and the identity is the paper's Lemma 2.2. "
     "The total drifts from one only when the zero approaches the ends of "
     "a finite array, which is the edge effect the paper bounds."),

    (7, "07-bowls-and-saddles", "Mix a bowl with a saddle",
     "A two-microphone table: a bowl from an on-line zero, plus an "
     "adjustable amount of saddle from a mirror pair.",
     "Slide the saddle in. The up-curving directions never exceed the "
     "number of contributions that curled up: one from the bowl, at most "
     "one from the saddle. That cap is the see-saw law.",
     slider("w", "how much saddle to add", -1.5, 1.5, 0.05, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const w=document.getElementById('w');
function draw(){
  const W=parseFloat(w.value);
  // the table: bowl [[1,0],[0,0]] plus W times saddle [[0,1],[1,0]]
  const a=1,b=W,c=0;
  ctx.clearRect(0,0,cv.width,cv.height);
  // left: the sign of the surface strength over all mixing recipes
  const S=300,x0=30,y0=40;
  const img=ctx.createImageData(S,S);
  for(let iy=0;iy<S;iy++)for(let ix=0;ix<S;ix++){
    const x=-1+2*ix/S,y=1-2*iy/S;
    const q=a*x*x+2*b*x*y+c*y*y;
    const k=4*(iy*S+ix);
    if(q>1e-9){img.data[k]=42;img.data[k+1]=120;img.data[k+2]=214;img.data[k+3]=Math.min(210,40+170*Math.abs(q));}
    else if(q<-1e-9){img.data[k]=208;img.data[k+1]=59;img.data[k+2]=59;img.data[k+3]=Math.min(210,40+170*Math.abs(q));}
    else{img.data[k+3]=0;}
  }
  ctx.putImageData(img,x0,y0);
  ctx.strokeStyle='#c3c2b7';ctx.strokeRect(x0,y0,S,S);
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('blue: the mix curves up.  red: it curves down.',x0+S/2,y0+S+18);
  // right: the two eigenvalue bars
  const ev=eig2(a,b,c);
  const bx=420,bw=90,base=220;
  ctx.fillStyle='#52514e';ctx.fillText('the two principal directions',bx+bw+20,52);
  ev.forEach((v,i)=>{
    const h=v*80,x=bx+i*(bw+40);
    ctx.fillStyle=v>1e-9?'#2a78d6':(v<-1e-9?'#d03b3b':'#898781');
    ctx.fillRect(x,h>0?base-h:base,bw,Math.max(2,Math.abs(h)));
    ctx.fillStyle='#52514e';
    ctx.fillText(v.toFixed(2),x+bw/2,base+(h>0?20:-Math.abs(h)-8));
  });
  ctx.strokeStyle='#898781';ctx.beginPath();ctx.moveTo(bx-20,base);
  ctx.lineTo(bx+2*bw+60,base);ctx.stroke();
  wv.textContent=W.toFixed(2);
  const up=ev.filter(v=>v>1e-9).length;
  const out=document.getElementById('out');
  out.textContent='saddle amount        '+W.toFixed(2)+'\n'+
    'up-curving directions  '+up+'  (the see-saw law caps this at 2:\n'+
    'one bowl plus at most one from the saddle)';
  out.className='readout '+(up<=2?'verdict-ok':'verdict-no');
}
w.addEventListener('input',draw);draw();
""",
     "With no saddle the table has one up-direction and one flat one. "
     "However hard the saddle is pushed, the up-count never passes two, and "
     "a downward direction appears the moment the saddle wins: counting "
     "directions counts contributions."),

    (8, "08-the-prime-side", "Find the zeros with primes",
     "The prime-built density over the heights 100 to 140, with the true "
     "zero heights marked.",
     "Add prime powers one at a time. The smooth average knows nothing; "
     "each wave sharpens the profile, and with all ten in, the spikes "
     "stand on the marks. The primes in this page reach only up to 13.",
     slider("np", "prime powers added", 0, 10, 1, 0),
     r"""
const cv=document.getElementById('c');
const np=document.getElementById('np');
const terms=vmTerms(16);
const marks=ZEROS.filter(g=>g>=100&&g<=140);
function densityK(tau,K){
  let out=Math.log(tau/(2*Math.PI))/(2*Math.PI);
  for(let i=0;i<K;i++){
    const n=terms[i][0],w=terms[i][1];
    out-=w/(Math.PI*Math.sqrt(n))*Math.cos(tau*Math.log(n));
  }
  return out;
}
function draw(){
  const K=parseInt(np.value);
  const P=Plot(cv,100,140,-1.1,1.8);
  P.clear();P.axes('height','prime-built density');
  for(const g of marks)P.vline(g,'#f0b5b5');
  P.curve(t=>densityK(t,K),'#4a3aa7',1.7,1500);
  npv.textContent=K===0?'none':String(K)+' ('+terms.slice(0,K).map(t=>t[0]).join(', ')+')';
  const out=document.getElementById('out');
  out.textContent='prime powers added   '+K+'\n'+
    'zero heights marked  '+marks.length+
    (K===10?'\nthe spikes stand on or between the marks: close zeros merge\n'+
           'into one broad spike at this resolution':'');
  out.className='readout '+(K===10?'verdict-ok':'');
}
np.addEventListener('input',draw);draw();
""",
     "This is the duet played in the prime-to-zero direction, the same "
     "density the paper integrates against. The tests check the alignment "
     "quantitatively, and the toy table built from it agrees with the "
     "zero-built table to about two parts in a hundred million."),

    (9, "09-the-whole-number-trick", "Expose the doubles with energy",
     "Ten pin locations; the slider doubles some of them. The energy is "
     "measured, the count is measured, and the trick deduces a floor on "
     "the clean pins.",
     "Double more pins and watch the energy climb: a double pays four for "
     "its two of count. The deduced floor, twice the count minus the "
     "energy, tracks the true number of clean pins exactly.",
     slider("dbl", "locations doubled", 0, 10, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const dbl=document.getElementById('dbl');
function draw(){
  const D=parseInt(dbl.value),L=10;
  const count=(L-D)+2*D;              // the full count, multiplicity in
  const energy=(L-D)*charge(1)+D*charge(2);
  const floorClean=2*count-energy;    // the scalar whole-number trick
  ctx.clearRect(0,0,cv.width,cv.height);
  // the pins
  for(let i=0;i<L;i++){
    const x=60+i*64,y=70;
    if(i<L-D){ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(x,y,8,0,7);ctx.fill();}
    else{ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2.6;
      ctx.beginPath();ctx.arc(x,y,11,0,7);ctx.stroke();
      ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(x,y,4.5,0,7);ctx.fill();}
  }
  // the bars
  const bars=[['the count',count,'#2a78d6',30],
              ['the energy',energy,'#4a3aa7',0],
              ['deduced floor on clean pins',floorClean,'#008300',0],
              ['true clean pins',L-D,'#898781',0]];
  bars.forEach(([name,v,color],i)=>{
    const y=150+i*52;
    ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
    ctx.fillText(name,60,y-6);
    ctx.fillStyle=color;ctx.fillRect(60,y,Math.max(2,v*13),20);
    ctx.fillStyle='#0b0b0b';ctx.fillText(String(v),70+Math.max(2,v*13),y+15);
  });
  dblv.textContent=String(D);
  const out=document.getElementById('out');
  out.textContent='clean pins '+(L-D)+' of '+L+' locations, full count '+count+
    ', energy '+energy+'\n'+
    'twice the count minus the energy = '+floorClean+
    '  (the floor is exact here)';
  out.className='readout verdict-ok';
}
dbl.addEventListener('input',draw);draw();
""",
     "In the paper the count and the energy come from the primes, and the "
     "scalar trick becomes the rank-trace inequality so it survives saddles "
     "and finite microphones. The arithmetic shown here is the trick's "
     "soul: a double pays four for two."),

    (10, "10-two-thirds", "Turn the dial",
     "Every constant in the paper, as the dial (the bandwidth) turns and "
     "the window switches.",
     "Pull the dial to one and watch all three certificates peak: two "
     "thirds on the line and clean, five sixths distinct. Then switch to "
     "the optimised window for the last half percent.",
     slider("lam", "the dial", 0.35, 1.0, 0.005, 0.7) +
     slider("opt", "window: 0 flat, 1 optimised", 0, 1, 1, 0),
     r"""
const cv=document.getElementById('c');
const lam=document.getElementById('lam'),opt=document.getElementById('opt');
function draw(){
  const l=parseFloat(lam.value),useOpt=parseInt(opt.value)===1;
  const P=Plot(cv,0.35,1.05,0,1.0);
  P.clear();P.axes('the dial','proportion certified');
  P.curve(x=>Math.max(0,shapeH(x)),'#2a78d6',2.2);
  P.curve(x=>Math.max(shapeHd(x),shapeF(x)),'#008300',2.2);
  P.curve(x=>shapeF(x),'#898781',1.4);
  P.vline(l,'#c3c2b7',[4,4]);
  P.dots([l,l],[Math.max(0,shapeH(l)),Math.max(shapeHd(l),shapeF(l))],'#0b0b0b',4);
  P.label(0.37,0.93,'green: distinct.  blue: on the line and clean.  gray: the weaker certificate','#52514e');
  const c=mtConstant();
  const onLine=useOpt&&l>0.999?2-1/c:shapeH(l);
  const distinct=useOpt&&l>0.999?(3-1/c)/2:Math.max(shapeHd(l),shapeF(l));
  lamv.textContent=l.toFixed(3);
  optv.textContent=useOpt?'optimised':'flat';
  const atPeak=l>0.999;
  const out=document.getElementById('out');
  out.textContent='on the line, and clean   '+Math.max(0,onLine).toFixed(5)+'\n'+
    'distinct                 '+Math.max(0,distinct).toFixed(5)+'\n'+
    (atPeak?(useOpt?'the optimised window: the Montgomery-Taylor constants'
                   :'the natural setting: 2/3 and 5/6')
           :'the certificates peak at dial one');
  out.className='readout '+(atPeak?'verdict-ok':'');
}
lam.addEventListener('input',draw);opt.addEventListener('input',draw);draw();
""",
     "The curves are the paper's shape functions, computed live; the "
     "optimised-window constants come from the closed form the paper "
     "states, which the tests pin to 0.67250 and 0.83625. The dial cannot "
     "pass one: beyond it the prime sums would need knowledge nobody has."),

    (12, "12-what-it-means", "Walk the proportion line",
     "The line from zero to one, with every landmark: the old record, the "
     "new constants, the method's ceiling, and the untouched hypothesis.",
     "Slide the hypothetical future bandwidth. The paper says what "
     "pair-correlation reach would be needed for 0.70, 0.80, 0.90; nobody "
     "can prove any bandwidth past one today, and no bandwidth short of "
     "infinity settles the hypothesis.",
     slider("bw", "hypothetical future bandwidth", 1.0, 1.8, 0.01, 1.0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const bw=document.getElementById('bw');
// the paper's anchors: bandwidth needed for each proportion (Remark 1.1)
const ANCHORS=[[1.0,0.67250],[1.04,0.70],[1.26,0.80],[1.70,0.90]];
function propAt(b){
  if(b<=ANCHORS[0][0])return ANCHORS[0][1];
  for(let i=1;i<ANCHORS.length;i++){
    const [b0,p0]=ANCHORS[i-1],[b1,p1]=ANCHORS[i];
    if(b<=b1)return p0+(p1-p0)*(b-b0)/(b1-b0);
  }
  return 0.90;
}
function draw(){
  const b=parseFloat(bw.value);
  const P=Plot(cv,0.35,1.05,0,1,{l:30,r:20,t:30,b:60});
  P.clear();
  // the proportion bar
  const y=0.5;
  P.ctx.fillStyle='rgba(0,131,0,0.25)';
  P.ctx.fillRect(P.X(0.35),P.Y(0.62),P.X(2/3)-P.X(0.35),P.Y(0.38)-P.Y(0.62));
  const marks=[[5/12,'5/12: the record until 2026','#2a78d6',0.78],
               [2/3,'2/3: 2026, flat window','#008300',0.20],
               [0.67250,'0.6725: best window','#008300',0.86],
               [0.68185,'0.68185: the method\'s ceiling','#d03b3b',0.08],
               [1.0,'1: the hypothesis, open','#52514e',0.78]];
  for(const [x,lab,color,ty] of marks){
    P.vline(x,color);
    P.ctx.fillStyle=color;P.ctx.font='11.5px system-ui';P.ctx.textAlign='center';
    P.ctx.fillText(lab,Math.min(Math.max(P.X(x),70),cv.width-90),P.Y(ty));
  }
  const p=propAt(b);
  P.dots([p],[y],'#0b0b0b',6);
  P.ctx.fillStyle='#52514e';P.ctx.font='12px system-ui';P.ctx.textAlign='center';
  P.ctx.fillText('what bandwidth '+b.toFixed(2)+' would certify',P.X(p),P.Y(0.44));
  bwv.textContent=b.toFixed(2);
  const out=document.getElementById('out');
  out.textContent='bandwidth '+b.toFixed(2)+
    '  would certify about  '+p.toFixed(3)+'\n'+
    (b<1.01?'bandwidth one is where knowledge ends today':
     'no bandwidth is provable past one today; the anchors 1.04, 1.26, 1.70\n'+
     'are the paper\'s, the line between them only guides the eye');
  out.className='readout '+(b<1.01?'verdict-ok':'');
}
bw.addEventListener('input',draw);draw();
""",
     "The green region is what is now certified unconditionally. The "
     "ceiling at 0.68185 binds this method's kind of certificate, not "
     "mathematics as a whole; a proof of the hypothesis would need inputs "
     "of a different nature entirely."),
]


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (num, folder, heading, lede, try_, controls, widget, note) in enumerate(CHAPTERS):
        nav = []
        if i > 0:
            nav.append(f'<a href="{CHAPTERS[i-1][0]:02d}.html">← previous</a>')
        nav.append('<a href="index.html">all of them</a>')
        if i + 1 < len(CHAPTERS):
            nav.append(f'<a href="{CHAPTERS[i+1][0]:02d}.html">next →</a>')
        page = (SHELL
                .replace("TITLE", f"{heading} · the critical line")
                .replace("HEADING", f"{num} · {heading}")
                .replace("LEDE", lede)
                .replace("TRY", try_)
                .replace("CONTROLS", controls)
                .replace("NOTE", note)
                .replace("NAV", "  ·  ".join(nav))
                .replace("MATHS", MATHS)
                .replace("WIDGET", widget))
        (OUT / f"{num:02d}.html").write_text(page)

    rows = "\n".join(
        f'<li><a href="{num:02d}.html">{num} · {heading}</a>'
        f'<span>{lede}</span></li>'
        for num, _, heading, lede, *_ in CHAPTERS)
    index = (SHELL
             .replace("TITLE", "Play with it · the critical line")
             .replace("HEADING", "Play with it")
             .replace("LEDE", "One page per chapter. Every number in the "
                              "article is a control on one of these.")
             .replace('<p class="try"><strong>Try this.</strong> TRY</p>', "")
             .replace('<canvas id="c" width="720" height="380"></canvas>', "")
             .replace('<div class="controls">CONTROLS</div>',
                      f'<ul class="list">{rows}</ul>')
             .replace('<div class="readout" id="out"></div>', "")
             .replace("NOTE", "Each page is self contained: no libraries and no "
                              "network, so they work offline and from a file.")
             .replace("NAV", '<a href="../index.html">back to the article</a>')
             .replace("MATHS", "").replace("WIDGET", "")
             .replace("</style>",
                      ".list{list-style:none;padding:0;margin:0}"
                      ".list li{padding:12px 0;border-bottom:1px solid var(--line)}"
                      ".list a{display:block;color:var(--blue);text-decoration:none;"
                      "font-size:16px}"
                      ".list span{display:block;color:var(--muted);font-size:13.5px;"
                      "margin-top:2px}</style>"))
    (OUT / "index.html").write_text(index)
    print(f"wrote {len(CHAPTERS)} playable pages plus an index in {OUT}")


if __name__ == "__main__":
    build()
