"""Build one playable page per chapter, so the reader can move the ideas around.

    cd sphere-packing && make play

Writes ../docs/sphere-packing/play/NN.html, one per chapter, plus an index.
Each page is self contained: no libraries, no network, one canvas and a few
sliders.  Reading about a certificate breaking when you turn a dial is weaker
than turning the dial, so every chapter that has a number in it gets a control
for that number.

The mathematics in these pages is the same mathematics as `src/sphere_packing_guide`,
re-expressed in JavaScript.  `tests/test_interactive.py` checks the two
implementations against each other at a set of sample points, so the page and
the library cannot drift apart silently.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "sphere-packing" / "play"

# --- shared maths, kept in one place so the checks can find it -------------

MATHS = r"""
// gamma, by Lanczos, so ball volumes work in any dimension
function lgamma(z){
  const g=7,p=[0.99999999999980993,676.5203681218851,-1259.1392167224028,
    771.32342877765313,-176.61502916214059,12.507343278686905,
    -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7];
  if(z<0.5) return Math.log(Math.PI/Math.sin(Math.PI*z))-lgamma(1-z);
  z-=1; let x=p[0];
  for(let i=1;i<g+2;i++) x+=p[i]/(z+i);
  const t=z+g+0.5;
  return 0.5*Math.log(2*Math.PI)+(z+0.5)*Math.log(t)-t+Math.log(x);
}
function logBallVolume(d){ return (d/2)*Math.log(Math.PI)-lgamma(d/2+1); }
function ballVolume(d){ return Math.exp(logBallVolume(d)); }
function ballFractionOfCube(d){ return Math.exp(logBallVolume(d)-d*Math.log(2)); }

// generalised Laguerre, the building blocks certificates are made of
function laguerre(k,alpha,y){
  let total=0;
  for(let i=0;i<=k;i++){
    const c=Math.exp(lgamma(k+alpha+1)-lgamma(i+alpha+1)-lgamma(k-i+1));
    let fact=1; for(let j=2;j<=i;j++) fact*=j;
    total+=c*Math.pow(-y,i)/fact;
  }
  return total;
}
// the sign carrying factor: the Gaussian is positive and cannot change a sign
function polyPart(coeffs,d,r){
  const y=2*Math.PI*r*r; let s=0;
  for(let k=0;k<coeffs.length;k++) s+=coeffs[k]*laguerre(k,d/2-1,y);
  return s;
}
function value(coeffs,d,r){ return polyPart(coeffs,d,r)*Math.exp(-Math.PI*r*r); }
function transformCoeffs(coeffs){ return coeffs.map((c,k)=>k%2?-c:c); }
function admissible(coeffs,d){
  const hat=transformCoeffs(coeffs);
  if(polyPart(hat,d,0)<=0) return false;
  for(let i=0;i<=1200;i++){ const r=1+i*(7/1200); if(polyPart(coeffs,d,r)>1e-12) return false; }
  for(let i=0;i<=1200;i++){ const r=i*(8/1200); if(polyPart(hat,d,r)<-1e-12) return false; }
  return true;
}
function densityBound(coeffs,d){
  const hat=transformCoeffs(coeffs);
  return ballVolume(d)*value(coeffs,d,0)/(Math.pow(2,d)*value(hat,d,0));
}
const ALPHA_STAR=0.5*Math.log2(2*Math.PI/Math.E);
const KL_EXPONENT=0.59905576;
const LP_RATE=Math.sqrt(Math.E/(2*Math.PI));
const SIGN_RADIUS=1/Math.PI;

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
    hline(y,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(pad.l,Y(y));ctx.lineTo(W-pad.r,Y(y));ctx.stroke();ctx.restore();},
    vline(x,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(X(x),pad.t);ctx.lineTo(X(x),H-pad.b);ctx.stroke();ctx.restore();},
    curve(f,color,lw){ctx.strokeStyle=color;ctx.lineWidth=lw||2.4;ctx.beginPath();
      for(let i=0;i<=400;i++){const x=xlo+(xhi-xlo)*i/400,y=f(x);
        if(i===0)ctx.moveTo(X(x),Y(y));else ctx.lineTo(X(x),Y(y));}ctx.stroke();},
    band(x0,x1,color){ctx.fillStyle=color;ctx.fillRect(X(x0),pad.t,X(x1)-X(x0),H-pad.t-pad.b);},
    label(x,y,text,color,align){ctx.fillStyle=color;ctx.font='12px system-ui';
      ctx.textAlign=align||'left';ctx.fillText(text,X(x),Y(y));},
    tick(x,y,text){ctx.fillStyle='#898781';ctx.font='11px system-ui';ctx.textAlign='center';
      ctx.fillText(text,X(x),Y(y));}
  };
}
"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITLE</title>
<style>
 :root{{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
        --line:#e1e0d9;--blue:#2a78d6;--green:#008300;--red:#d03b3b;--violet:#4a3aa7;}}
 @media (prefers-color-scheme: dark){{
   :root{{--surface:#15150f;--ink:#f2f1ea;--ink2:#c9c7bd;--muted:#8d8b82;--line:#33322c;}}
 }}
 *{{box-sizing:border-box}}
 body{{margin:0;padding:28px 20px 56px;background:var(--surface);color:var(--ink);
   font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif;}}
 main{{max-width:760px;margin:0 auto}}
 .back{{font-size:14px;color:var(--muted);text-decoration:none}}
 .back:hover{{color:var(--blue)}}
 h1{{font-size:24px;line-height:1.25;margin:14px 0 6px}}
 .lede{{color:var(--ink2);margin:0 0 22px}}
 .try{{border-left:3px solid var(--blue);padding:8px 0 8px 14px;margin:0 0 22px;
   color:var(--ink2);font-size:15px}}
 canvas{{width:100%;height:auto;display:block;border-radius:8px;background:var(--surface)}}
 .controls{{margin:18px 0 0}}
 .row{{display:flex;align-items:center;gap:12px;margin:10px 0}}
 .row label{{flex:0 0 190px;font-size:14px;color:var(--ink2)}}
 input[type=range]{{flex:1;accent-color:var(--blue)}}
 .val{{flex:0 0 90px;text-align:right;font-family:ui-monospace,monospace;font-size:13px}}
 .readout{{margin-top:18px;padding:14px 16px;border:1px solid var(--line);border-radius:8px;
   font-family:ui-monospace,monospace;font-size:14px;white-space:pre-line}}
 .verdict-ok{{color:var(--green)}} .verdict-no{{color:var(--red)}}
 .nav{{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);font-size:14px}}
 .nav a{{color:var(--blue);text-decoration:none}} .nav a:hover{{text-decoration:underline}}
 .note{{margin-top:26px;font-size:13.5px;color:var(--muted)}}
 /* embedded in the article: drop the chrome the article already provides */
 body.embed{{padding:14px 16px 18px}}
 body.embed .back, body.embed h1, body.embed .lede, body.embed .nav{{display:none}}
 body.embed .try{{margin-top:0}}
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
    (0, "00-start-here", "Turn the stack yourself",
     "The greengrocer's stack of equal balls, in three dimensions. Drag it.",
     "Drag left and right. Count how many balls touch the one in the middle, "
     "and notice that the gaps never close.",
     "",
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let az=0.6,el=0.35,drag=null;
const pts=[];
for(let i=-1;i<=1;i++)for(let j=-1;j<=1;j++)for(let k=-1;k<=1;k++)
  if((i+j+k)%2===0) pts.push([i,j,k]);
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=cv.width/2, cy=cv.height/2, s=78;
  const ca=Math.cos(az),sa=Math.sin(az),ce=Math.cos(el),se=Math.sin(el);
  const proj=p=>{
    const x=p[0]*ca-p[1]*sa, y=p[0]*sa+p[1]*ca, z=p[2];
    return [cx+x*s, cy-(z*ce-y*se)*s, y*ce+z*se];
  };
  const drawn=pts.map(p=>({p,q:proj(p)})).sort((a,b)=>a.q[2]-b.q[2]);
  for(const {p,q} of drawn){
    const centre=p[0]===0&&p[1]===0&&p[2]===0;
    const r=s*Math.SQRT2/4;
    const g=ctx.createRadialGradient(q[0]-r*0.3,q[1]-r*0.3,r*0.1,q[0],q[1],r);
    g.addColorStop(0, centre?'#8f84dd':'#7fb0ea');
    g.addColorStop(1, centre?'#4a3aa7':'#2a78d6');
    ctx.fillStyle=g; ctx.globalAlpha=centre?0.95:0.8;
    ctx.beginPath(); ctx.arc(q[0],q[1],r,0,7); ctx.fill();
  }
  ctx.globalAlpha=1;
  document.getElementById('out').textContent=
    'twelve balls touch the middle one\nthey fill 74.05 % of space';
}
cv.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];cv.setPointerCapture(e.pointerId);});
cv.addEventListener('pointerup',()=>drag=null);
cv.addEventListener('pointermove',e=>{
  if(!drag)return; az+=(e.clientX-drag[0])*0.01; el+=(e.clientY-drag[1])*0.006;
  el=Math.max(-1.4,Math.min(1.4,el)); drag=[e.clientX,e.clientY]; draw();});
draw();
""",
     "This is the same face centred cubic arrangement as the opening animation, "
     "drawn live so you can choose the angle."),

    (1, "01-the-question", "Slide the rows together",
     "Circles of the same size, arranged in rows. The slider staggers the rows "
     "and pulls them closer.",
     "Push the slider all the way. The circles never change size and none is "
     "removed, yet the covered fraction climbs from 78.54 % to 90.69 %.",
     slider("t", "how staggered the rows are", 0, 1, 0.01, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const t=document.getElementById('t');
function draw(){
  const f=parseFloat(t.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const rowGap=1-(1-Math.sqrt(3)/2)*f, s=46, R=s/2;
  for(let j=-1;j<9;j++)for(let i=-1;i<18;i++){
    const x=40+(i+0.5*f*(((j%2)+2)%2))*s, y=24+j*s*rowGap;
    if(y<-s||y>cv.height+s)continue;
    ctx.beginPath();ctx.arc(x,y,R,0,7);
    ctx.fillStyle='rgba(42,120,214,0.55)';ctx.fill();
  }
  const dens=Math.PI/4*(1/rowGap);
  document.getElementById('tv').textContent=f.toFixed(2);
  document.getElementById('out').textContent=
    'covered   '+(dens*100).toFixed(2)+' %\n'+
    (f>0.995?'this is the best any arrangement of equal circles can do'
            :'keep going');
}
t.addEventListener('input',draw);draw();
""",
     "The covered fraction is computed from the row spacing, which is why it "
     "lands exactly on 90.69 % when the rows are fully staggered."),

    (2, "02-room-runs-out", "Add dimensions and watch the room go",
     "One ball, and the box that just holds it. The slider changes the "
     "dimension.",
     "Take the dimension up to 20. The ball keeps its width the whole way, and "
     "the fraction of the box it fills falls off a cliff.",
     slider("d", "dimension", 1, 30, 1, 3),
     r"""
const cv=document.getElementById('c');
const P=Plot(cv,0,31,-0.04,1.06);
const d=document.getElementById('d');
function draw(){
  const D=parseInt(d.value);
  P.clear();P.axes('dimension','fraction of the box the ball fills');
  P.ctx.fillStyle='rgba(42,120,214,0.75)';
  for(let k=1;k<=30;k++){
    const f=ballFractionOfCube(k), x0=P.X(k-0.36), x1=P.X(k+0.36);
    P.ctx.globalAlpha=(k===D)?1:0.35;
    P.ctx.fillStyle=(k===D)?'#4a3aa7':'#2a78d6';
    P.ctx.fillRect(x0,P.Y(f),x1-x0,P.Y(0)-P.Y(f));
  }
  P.ctx.globalAlpha=1;
  const frac=ballFractionOfCube(D), vol=ballVolume(D);
  document.getElementById('dv').textContent=D;
  document.getElementById('out').textContent=
    'dimension            '+D+'\n'+
    'ball fills           '+(frac*100).toPrecision(3)+' % of its box\n'+
    'volume of the ball   '+vol.toPrecision(4)+'\n'+
    'corners of the box   '+(D<=20?Math.pow(2,D).toLocaleString():'2^'+D);
}
d.addEventListener('input',draw);draw();
""",
     "The ball's own volume is largest in dimension five, which you can see by "
     "reading the volume line as you move the slider."),

    (3, "03-cannot-check", "Try to settle it by hand",
     "Click to drop circles. They refuse to overlap, and the packing you build "
     "is one of infinitely many.",
     "Fill the box as densely as you can, then press reset and try again. Your "
     "best attempt is evidence, and evidence is not a proof about every "
     "arrangement.",
     '<div class="row"><label>&nbsp;</label>'
     '<button id="reset" style="flex:1;padding:8px;border:1px solid var(--line);'
     'border-radius:6px;background:transparent;color:inherit;cursor:pointer">'
     'clear and start again</button><span class="val"></span></div>',
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const R=22; let placed=[], best=0;
function area(){ return placed.length*Math.PI*R*R/(cv.width*cv.height); }
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.strokeStyle='#c3c2b7';ctx.strokeRect(0.5,0.5,cv.width-1,cv.height-1);
  for(const p of placed){ctx.beginPath();ctx.arc(p[0],p[1],R,0,7);
    ctx.fillStyle='rgba(42,120,214,0.55)';ctx.fill();}
  const a=area(); if(a>best) best=a;
  document.getElementById('out').textContent=
    'circles placed   '+placed.length+'\n'+
    'covered          '+(a*100).toFixed(2)+' %\n'+
    'your best so far '+(best*100).toFixed(2)+' %\n'+
    'the true best is 90.69 %, and no amount of clicking proves it';
}
cv.addEventListener('click',e=>{
  const b=cv.getBoundingClientRect();
  const x=(e.clientX-b.left)*cv.width/b.width, y=(e.clientY-b.top)*cv.height/b.height;
  if(x<R||y<R||x>cv.width-R||y>cv.height-R) return;
  for(const p of placed) if(Math.hypot(p[0]-x,p[1]-y)<2*R) return;
  placed.push([x,y]);draw();});
document.getElementById('reset').addEventListener('click',()=>{placed=[];draw();});
draw();
""",
     "The circles here have a fixed radius and simply refuse to overlap, which "
     "is the same rule the article's packings obey."),

    (4, "04-the-certificate", "Break a certificate yourself",
     "A working certificate in the plane. Each slider changes one of its parts.",
     "Move any slider until the green curve dips below zero. The moment it "
     "does, rule two is broken and the certificate proves nothing at all.",
     slider("a", "first part", -0.30, 0.30, 0.005, 0.035) +
     slider("b", "second part", -0.30, 0.30, 0.005, -0.097) +
     slider("cc", "third part", -0.30, 0.30, 0.005, 0.037),
     r"""
const cv=document.getElementById('c');
const A=document.getElementById('a'),B=document.getElementById('b'),C=document.getElementById('cc');
function draw(){
  const co=[1,parseFloat(A.value),parseFloat(B.value),parseFloat(C.value)];
  const hat=transformCoeffs(co), d=2;
  const P=Plot(cv,0,2.6,-0.45,1.15);
  P.clear();
  P.band(1,2.6,'rgba(208,59,59,0.07)');
  P.axes('distance from the centre, and frequency','');
  P.hline(0,'#c3c2b7');
  P.curve(r=>value(co,d,r),'#2a78d6');
  const ok=admissible(co,d);
  P.curve(r=>value(hat,d,r),ok?'#008300':'#d03b3b');
  P.label(1.06,1.02,'rule one applies from here out','#d03b3b');
  P.label(2.5,0.62,'blue: the function','#2a78d6','right');
  P.label(2.5,0.50,'green: its transform',ok?'#008300':'#d03b3b','right');
  document.getElementById('av').textContent=(+A.value).toFixed(3);
  document.getElementById('bv').textContent=(+B.value).toFixed(3);
  document.getElementById('ccv').textContent=(+C.value).toFixed(3);
  const out=document.getElementById('out');
  if(ok){
    out.innerHTML='<span class="verdict-ok">both rules hold</span>\n'+
      'this proves no packing of circles beats  '+(densityBound(co,d)*100).toFixed(2)+' %\n'+
      'the best that can actually be built is   90.69 %';
  } else {
    out.innerHTML='<span class="verdict-no">a rule is broken</span>\n'+
      'this certificate proves nothing at all';
  }
}
[A,B,C].forEach(s=>s.addEventListener('input',draw));draw();
""",
     "The sign rules are checked on a grid here, exactly as `is_admissible` "
     "does in the repository, so this page and the tests agree."),

    (5, "05-count-twice", "Count the same total twice",
     "A small packing on the left, its frequencies on the right. Step through "
     "the count.",
     "Step forward. Every pair of distinct centres pulls the total down, and "
     "every frequency pushes it up. The packing is trapped between them.",
     slider("k", "how far through the count", 0, 100, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const k=document.getElementById('k');
const n=5, C=[]; for(let i=0;i<n;i++)for(let j=0;j<n;j++)C.push([i,j]);
const F=[]; for(let i=-2;i<=2;i++)for(let j=-2;j<=2;j++)F.push([i,j]);
function draw(){
  const t=parseInt(k.value); ctx.clearRect(0,0,cv.width,cv.height);
  const s=52, ox=70, oy=60;
  ctx.fillStyle='#898781';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText('pairs of centres',ox+2*s,26); ctx.fillText('frequencies',470+2*s/2,26);
  for(const p of C){ctx.beginPath();ctx.arc(ox+p[0]*s,oy+p[1]*s,7,0,7);
    ctx.fillStyle='#e1e0d9';ctx.fill();}
  const half=Math.min(t,50), pairsShown=Math.floor(half/50*(C.length*C.length-1));
  if(t<=50){
    const a=C[pairsShown%C.length], b=C[Math.floor(pairsShown/C.length)%C.length];
    ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2;ctx.beginPath();
    ctx.moveTo(ox+a[0]*s,oy+a[1]*s);ctx.lineTo(ox+b[0]*s,oy+b[1]*s);ctx.stroke();
    for(const p of [a,b]){ctx.beginPath();ctx.arc(ox+p[0]*s,oy+p[1]*s,8,0,7);
      ctx.fillStyle='#4a3aa7';ctx.fill();}
  }
  const fx=470, fy=60, fs=42, lit=t<=50?0:Math.round((t-50)/50*F.length);
  for(let i=0;i<F.length;i++){
    const p=F[i];
    ctx.beginPath();ctx.arc(fx+(p[0]+2)*fs/1.6,fy+(p[1]+2)*fs/1.6,7,0,7);
    ctx.fillStyle=i<lit?'#008300':'#e1e0d9';ctx.fill();
  }
  document.getElementById('kv').textContent=t+'%';
  document.getElementById('out').textContent = t<=50
    ? 'counting over pairs of centres\nevery pair beyond a centre with itself sits at\n'+
      'distance one or more, where rule one makes it\nat or below zero: it can only pull the total down'
    : 'counting over frequencies\nrule two makes every one of them at or above zero:\n'+
      'they can only push the total up\n\none total, squeezed from both sides';
}
k.addEventListener('input',draw);draw();
""",
     "Poisson summation is the identity that makes the two counts equal. This "
     "page shows the two counts, not the proof of the identity."),

    (6, "06-best-so-far", "The gap nobody has closed",
     "What can be built, against what has been proved impossible, in the "
     "dimensions where this repository has a certificate.",
     "Switch between the two dimensions. The bar is what exists; the line is "
     "the ceiling. Everything unknown lives between them.",
     slider("d", "dimension", 2, 3, 1, 2),
     r"""
const cv=document.getElementById('c');
const d=document.getElementById('d');
const TRUE={2:0.9068996821171089,3:0.7404804896930611};
const BOUND={2:0.911648,3:0.784806};
function draw(){
  const D=parseInt(d.value),t=TRUE[D],b=BOUND[D];
  const P=Plot(cv,0,2,0.6,1.0);
  P.clear();P.axes('','fraction of space filled');
  P.ctx.fillStyle='rgba(42,120,214,0.75)';
  P.ctx.fillRect(P.X(0.55),P.Y(t),P.X(1.45)-P.X(0.55),P.Y(0.6)-P.Y(t));
  P.ctx.fillStyle='rgba(74,58,167,0.18)';
  P.ctx.fillRect(P.X(0.55),P.Y(b),P.X(1.45)-P.X(0.55),P.Y(t)-P.Y(b));
  P.ctx.strokeStyle='#008300';P.ctx.lineWidth=3;P.ctx.beginPath();
  P.ctx.moveTo(P.X(0.5),P.Y(b));P.ctx.lineTo(P.X(1.5),P.Y(b));P.ctx.stroke();
  P.label(1.55,b,'proved impossible above this','#008300');
  P.label(1.55,t,'actually reached','#2a78d6');
  document.getElementById('dv').textContent=D;
  document.getElementById('out').textContent=
    'dimension              '+D+'\n'+
    'can be built           '+(t*100).toFixed(2)+' %\n'+
    'proved impossible above '+(b*100).toFixed(2)+' %\n'+
    'the gap                '+((b-t)*100).toFixed(2)+' percentage points';
}
d.addEventListener('input',draw);draw();
""",
     "Both bounds come from certificates found by the search in this "
     "repository, and both are re-checked in the test suite."),

    (8, "08-balancing", "Stretch until the two agree",
     "A certificate and its Fourier transform. The slider stretches the "
     "certificate.",
     "Find the stretch where the two curves meet at the centre. That is the "
     "only stretch for which subtracting them gives a function that is zero "
     "there, and the whole rest of the proof needs it.",
     slider("a", "how much it is stretched", 0.6, 1.6, 0.005, 0.75),
     r"""
const cv=document.getElementById('c');
const A=document.getElementById('a');
const co=[1,0.03530634,-0.09737948,0.03676317], d=2;
const hat=transformCoeffs(co);
const perfect=Math.pow(value(hat,d,0)/value(co,d,0),1/d);
function draw(){
  const a=parseFloat(A.value);
  const h=r=>value(co,d,r*a);
  const hh=r=>Math.pow(a,-d)*value(hat,d,r/a);
  const P=Plot(cv,0,2.6,-0.35,1.35);
  P.clear();P.axes('distance from the centre','');
  P.hline(0,'#c3c2b7');
  P.curve(h,'#2a78d6'); P.curve(hh,'#008300');
  P.curve(r=>hh(r)-h(r),'#4a3aa7',3);
  P.label(2.5,1.22,'blue: stretched function','#2a78d6','right');
  P.label(2.5,1.10,'green: its transform','#008300','right');
  P.label(2.5,0.98,'violet: the difference','#4a3aa7','right');
  const gap=hh(0)-h(0);
  document.getElementById('av').textContent=a.toFixed(3);
  const near=Math.abs(gap)<0.004;
  document.getElementById('out').innerHTML=
    'difference at the centre   '+gap.toFixed(4)+'\n'+
    (near?'<span class="verdict-ok">balanced: the difference starts at zero, '+
          'and it now turns into minus itself under the Fourier transform</span>'
        :'not yet balanced, keep moving the slider');
}
A.addEventListener('input',draw);draw();
""",
     "The exact stretch is the ratio of the two values at the centre, taken to "
     "the power one over the dimension. Here that is about " +
     "0.75, and the page recomputes it rather than assuming it."),

    (9, "09-the-wall", "Push the radius into the wall",
     "The negative half of the balanced function has to fit inside a ball. The "
     "slider shrinks that ball.",
     "Shrink the radius past the dashed line. The room left for the negative "
     "half collapses, and half of the weight cannot possibly fit.",
     slider("r", "radius, per square root of the dimension", 0.15, 0.65, 0.005, 0.5),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const R=document.getElementById('r');
function allowed(c){ return c>=SIGN_RADIUS?0.5:0.5*Math.exp(-14*(SIGN_RADIUS-c)/SIGN_RADIUS); }
function draw(){
  const c=parseFloat(R.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=190,cy=190,s=250;
  ctx.beginPath();ctx.arc(cx,cy,SIGN_RADIUS*s,0,7);
  ctx.strokeStyle='#4a3aa7';ctx.setLineDash([5,5]);ctx.lineWidth=2;ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();ctx.arc(cx,cy,c*s,0,7);
  ctx.fillStyle='rgba(208,59,59,0.18)';ctx.fill();
  ctx.strokeStyle='#d03b3b';ctx.lineWidth=2;ctx.stroke();
  ctx.fillStyle='#4a3aa7';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('the wall',cx,cy-SIGN_RADIUS*s-10);
  const P=Plot(cv,0.15,0.65,0,0.62,{l:420,r:20,t:30,b:38});
  P.axes('radius','weight that can fit');
  P.hline(0.5,'#2a78d6',[4,4]);
  P.vline(SIGN_RADIUS,'#4a3aa7',[4,4]);
  P.curve(allowed,'#d03b3b');
  P.label(0.17,0.53,'half: what is demanded','#2a78d6');
  document.getElementById('rv').textContent=c.toFixed(3);
  const a=allowed(c);
  document.getElementById('out').innerHTML=
    'radius        '+c.toFixed(3)+'   (the wall is at '+SIGN_RADIUS.toFixed(3)+')\n'+
    'can fit       '+(a*100).toFixed(2)+' % of the weight\n'+
    'is demanded   50.00 %\n'+
    (c>=SIGN_RADIUS?'<span class="verdict-ok">still possible</span>'
                   :'<span class="verdict-no">impossible: no certificate can '+
                    'have a radius here</span>');
}
R.addEventListener('input',draw);draw();
""",
     "The collapse drawn here is exponential, which is the shape the proof "
     "gives. The rate of that curve is chosen for legibility and is not the "
     "constant from the paper."),

    (11, "11-they-meet", "Watch the two halves close",
     "One direction rules every certificate out below a rate. The other builds "
     "one that reaches it. The slider raises the dimension.",
     "Raise the dimension. The two curves squeeze together on one number, and "
     "that number is the exact strength of the method.",
     slider("d", "dimension", 4, 4000, 4, 20),
     r"""
const cv=document.getElementById('c');
const d=document.getElementById('d');
function draw(){
  const D=parseInt(d.value);
  const P=Plot(cv,4,4000,0.55,0.80);
  P.clear();P.axes('dimension','rate the bound decays at');
  P.hline(LP_RATE,'#4a3aa7',[4,4]);
  P.label(2200,LP_RATE+0.012,'the exact rate','#4a3aa7');
  const rate=x=>Math.exp(logBallVolume(Math.round(x))/Math.round(x))/2*(Math.sqrt(x)*SIGN_RADIUS);
  P.ctx.lineWidth=2.6;
  for(const [sgn,col] of [[1,'#008300'],[-1,'#2a78d6']]){
    P.ctx.strokeStyle=col;P.ctx.beginPath();
    for(let i=0;i<=200;i++){const x=4+(D-4)*i/200;
      const y=rate(x)*(1+sgn*0.55/Math.sqrt(x));
      if(i===0)P.ctx.moveTo(P.X(x),P.Y(y));else P.ctx.lineTo(P.X(x),P.Y(y));}
    P.ctx.stroke();
  }
  document.getElementById('dv').textContent=D;
  document.getElementById('out').textContent=
    'dimension                    '+D+'\n'+
    'gap between the two halves   '+(2*0.55/Math.sqrt(D)).toFixed(4)+'\n'+
    'the exact rate               '+LP_RATE.toFixed(10)+'\n'+
    'as halvings per dimension    '+ALPHA_STAR.toFixed(10);
}
d.addEventListener('input',draw);draw();
""",
     "The two curves are drawn closing at a rate chosen for legibility. The "
     "real error terms are the ones the theorem writes as vanishing "
     "corrections."),

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
                .replace("TITLE", f"{heading} · sphere packing")
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
             .replace("TITLE", "Play with it · sphere packing")
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
