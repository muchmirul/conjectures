"""Build one playable page per chapter, so the reader can move the ideas around.

    cd multicolor-ramsey && make play

Writes ../docs/multicolor-ramsey/play/NN.html, one per chapter, plus an index.
Each page is self contained: no libraries, no network, one canvas and a few
controls.  Reading that six people cannot stay safe is weaker than trying to
keep them safe yourself and watching the triangle appear, so every chapter
that has a claim in it gets a control that pokes at that claim.

The mathematics in these pages is the same mathematics as `src/ramsey_guide`,
re-expressed in JavaScript.  `tests/test_interactive.py` checks the two
implementations against each other at a set of sample points, so the page and
the library cannot drift apart silently.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "multicolor-ramsey" / "play"

# --- shared maths, kept in one place so the checks can find it -------------

MATHS = r"""
// the shared edge palette: color 0 is always this red, in every page
const EDGE_COLORS=['#d03b3b','#2a78d6','#eda100','#4a3aa7','#00787a','#008300'];

// the pentagon table: ring pairs get color 0, star pairs color 1
function pentagonColoring(){
  const M=[...Array(5)].map(()=>Array(5).fill(-1));
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){
    const d=Math.min((j-i)%5,(i-j+5)%5);
    M[i][j]=M[j][i]=(d===1)?0:1;
  }
  return M;
}

// the sixteen-element field, built on x^4 = x + 1 over the two-element field
function gf16Mul(a,b){
  let out=0;
  while(b){ if(b&1)out^=a; a<<=1; if(a&16)a^=19; b>>=1; }
  return out;
}
function gf16Class(v){
  let x=1;
  for(let e=0;e<15;e++){ if(x===v)return e%3; x=gf16Mul(x,2); }
  return -1;
}
// the record table, or any first n people of it (a safe table stays safe
// when people leave)
function gf16Coloring(n){
  const M=[...Array(n)].map(()=>Array(n).fill(-1));
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)
    M[i][j]=M[j][i]=gf16Class(i^j);
  return M;
}

// the referee: every one-color triangle in a coloring matrix
function monoTriangles(M){
  const out=[],n=M.length;
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    const c=M[i][j]; if(c<0)continue;
    for(let k=j+1;k<n;k++)
      if(M[i][k]===c&&M[j][k]===c)out.push([i,j,k]);
  }
  return out;
}

// multiplying safe tables: rooms keep outer colors between them,
// fresh colors inside
function productColoring(outer,inner,outerColors){
  const no=outer.length,ni=inner.length,n=no*ni;
  const M=[...Array(n)].map(()=>Array(n).fill(-1));
  for(let a=0;a<n;a++)for(let b=a+1;b<n;b++){
    const pa=Math.floor(a/ni),ua=a%ni,pb=Math.floor(b/ni),ub=b%ni;
    M[a][b]=M[b][a]=(pa===pb)?outerColors+inner[ua][ub]:outer[pa][pb];
  }
  return M;
}

// the sorting staircase: forced(1)=3, forced(k)=k*(forced(k-1)-1)+2
function upperStaircase(k){
  const v=[3];
  for(let c=2;c<=k;c++)v.push(c*(v[v.length-1]-1)+2);
  return v;
}

const PENTAGON_BASE=Math.sqrt(5);
const GF16_BASE=Math.cbrt(16);
const PRE_2026_BASE=Math.pow(380,1/5);
// the honest floor: the best safe table provable by multiplying the record
// blocks (2 people per color, 5 per two, 16 per three, 50 per four)
function productLower(k){
  const blocks=[[1,2],[2,5],[3,16],[4,50]];
  const best=Array(k+1).fill(1);
  for(let i=1;i<=k;i++)for(const [c,s] of blocks)
    if(c<=i)best[i]=Math.max(best[i],best[i-c]*s);
  return best[k];
}
// the 2026 paper's explicit per-color base, constant deliberately unoptimized
function explicitNewBase(k){
  return Math.cbrt(k)/(6*Math.exp(38)*Math.log(k));
}

// the referee's card this repository found and verified (13 rows, 8 columns)
const REFEREE=[[1,1,0,1,1,1,1,1],[1,0,0,1,0,0,1,0],[1,0,0,1,1,0,1,1],
  [1,0,1,1,1,0,0,0],[1,0,1,1,0,1,0,0],[0,0,0,1,0,0,1,1],[0,1,1,0,1,0,1,1],
  [0,1,1,0,1,0,0,0],[0,1,1,0,0,0,0,0],[0,1,1,0,0,1,1,1],[1,1,0,1,0,1,1,0],
  [0,0,1,0,0,1,0,1],[1,0,0,0,0,0,0,0]];
// the first row showing both symbols within the chosen columns, or -1
function saturatedRow(cols){
  for(let r=0;r<REFEREE.length;r++){
    const seen=new Set(cols.map(z=>REFEREE[r][z]));
    if(seen.size===2)return r;
  }
  return -1;
}

// the noisy five-symbol channel and the classic two-letter code
function confusable(a,b){ return a===b||((a-b+5)%5)===1||((a-b+5)%5)===4; }
function distinguishable(u,v){
  for(let d=0;d<u.length;d++)if(!confusable(u[d],v[d]))return d;
  return -1;
}
const CODEBOOK=[[0,0],[1,2],[2,4],[3,1],[4,3]];

// people on a circle, starting from the top
function ringPos(n,cx,cy,r){
  const out=[];
  for(let i=0;i<n;i++){
    const a=Math.PI/2+2*Math.PI*i/n;
    out.push([cx+r*Math.cos(a),cy-r*Math.sin(a)]);
  }
  return out;
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
    curve(f,color,lw){ctx.strokeStyle=color;ctx.lineWidth=lw||2.4;ctx.beginPath();
      for(let i=0;i<=400;i++){const x=xlo+(xhi-xlo)*i/400,y=f(x);
        if(i===0)ctx.moveTo(X(x),Y(y));else ctx.lineTo(X(x),Y(y));}ctx.stroke();},
    dots(xs,ys,color){ctx.fillStyle=color;
      for(let i=0;i<xs.length;i++){ctx.beginPath();ctx.arc(X(xs[i]),Y(ys[i]),3.4,0,7);ctx.fill();}},
    line(xs,ys,color,lw){ctx.strokeStyle=color;ctx.lineWidth=lw||2;ctx.beginPath();
      for(let i=0;i<xs.length;i++){if(i===0)ctx.moveTo(X(xs[i]),Y(ys[i]));
        else ctx.lineTo(X(xs[i]),Y(ys[i]));}ctx.stroke();},
    hline(y,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(pad.l,Y(y));ctx.lineTo(W-pad.r,Y(y));ctx.stroke();ctx.restore();},
    vline(x,color,dash){ctx.save();ctx.strokeStyle=color;ctx.setLineDash(dash||[]);
      ctx.beginPath();ctx.moveTo(X(x),pad.t);ctx.lineTo(X(x),H-pad.b);ctx.stroke();ctx.restore();},
    label(x,y,text,color,align){ctx.fillStyle=color;ctx.font='12px system-ui';
      ctx.textAlign=align||'left';ctx.fillText(text,X(x),Y(y));}
  };
}

// drawing a coloring onto a canvas, shared by several pages
function drawColoring(ctx,M,pos,lw,highlight){
  const n=M.length;
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
    const c=M[i][j]; if(c<0)continue;
    ctx.strokeStyle=EDGE_COLORS[c];ctx.lineWidth=lw||1.6;ctx.globalAlpha=0.8;
    ctx.beginPath();ctx.moveTo(pos[i][0],pos[i][1]);
    ctx.lineTo(pos[j][0],pos[j][1]);ctx.stroke();
  }
  ctx.globalAlpha=1;
  if(highlight)for(const [i,j,k] of highlight){
    ctx.strokeStyle=EDGE_COLORS[M[i][j]];ctx.lineWidth=6;
    for(const [a,b] of [[i,j],[j,k],[i,k]]){
      ctx.beginPath();ctx.moveTo(pos[a][0],pos[a][1]);
      ctx.lineTo(pos[b][0],pos[b][1]);ctx.stroke();
    }
  }
  for(const [x,y] of pos){
    ctx.beginPath();ctx.arc(x,y,6,0,7);
    ctx.fillStyle='#fff';ctx.fill();
    ctx.strokeStyle='#52514e';ctx.lineWidth=1.4;ctx.stroke();
  }
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
    (0, "00-start-here", "The record table, one color at a time",
     "The sixteen-person, three-color table from 1955, still unbeaten. The "
     "slider isolates one color's net.",
     "Pull the slider through the three colors. Each net on its own has no "
     "triangle of any kind, which is why the whole table has no one-color "
     "one.",
     slider("layer", "which net to show (0 = all)", 0, 3, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const layer=document.getElementById('layer');
const M=gf16Coloring(16),pos=ringPos(16,360,190,158);
function draw(){
  const L=parseInt(layer.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const shown=(L===0)?M:M.map((row,i)=>row.map((v,j)=>v===L-1?v:-1));
  drawColoring(ctx,shown,pos,1.4);
  document.getElementById('layerv').textContent=L===0?'all':('color '+L);
  document.getElementById('out').textContent=
    'people                 16\n'+
    'connections            120\n'+
    'one-color triangles    '+monoTriangles(M).length+'  (checked live, all 560 triples)';
}
layer.addEventListener('input',draw);draw();
""",
     "The coloring is rebuilt in this page from the same 1955 recipe the "
     "article draws, and the triangle count is computed here, not quoted."),

    (1, "01-the-game", "Try to break the pentagon",
     "The five-person table, safe with two colors. Click any string to swap "
     "its color.",
     "Swap a few strings and watch the count. Every swap that helps one "
     "triangle tends to hurt another; see if you can find a second safe "
     "coloring at all.",
     "",
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const M=pentagonColoring(),pos=ringPos(5,360,195,150);
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const bad=monoTriangles(M);
  drawColoring(ctx,M,pos,2.6,bad);
  const out=document.getElementById('out');
  out.textContent='one-color triangles   '+bad.length+'\n'+
    (bad.length===0?'safe':'not safe: the thick triangle is one-colored');
  out.className='readout '+(bad.length===0?'verdict-ok':'verdict-no');
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const x=(e.clientX-r.left)*cv.width/r.width,y=(e.clientY-r.top)*cv.height/r.height;
  let best=null,bd=14;
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){
    const [x0,y0]=pos[i],[x1,y1]=pos[j];
    const t=Math.max(0,Math.min(1,((x-x0)*(x1-x0)+(y-y0)*(y1-y0))/((x1-x0)**2+(y1-y0)**2)));
    const d=Math.hypot(x-(x0+t*(x1-x0)),y-(y0+t*(y1-y0)));
    if(d<bd){bd=d;best=[i,j];}
  }
  if(best){const [i,j]=best;M[i][j]=M[j][i]=1-M[i][j];draw();}
});
draw();
""",
     "Up to rotating and reflecting the circle and renaming the colors, the "
     "ring-and-star coloring is the only safe one, which is why your swaps "
     "keep failing in the same ways."),

    (2, "02-six-is-forced", "Six people, and no way out",
     "Six people, two colors, and every string clickable. The triangle "
     "count can never reach zero.",
     "Chase the count downward. The article's tests walk all 32768 "
     "colorings: none is safe, and the luckiest contain exactly two "
     "one-color triangles. See if you can find one of those.",
     "",
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const M=[...Array(6)].map(()=>Array(6).fill(-1));
for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)M[i][j]=M[j][i]=(i+j)%2;
const pos=ringPos(6,360,195,152);
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const bad=monoTriangles(M);
  drawColoring(ctx,M,pos,2.4,bad.slice(0,1));
  const out=document.getElementById('out');
  out.textContent='one-color triangles   '+bad.length+'\n'+
    (bad.length===2?'two: that is the proven minimum, you cannot do better'
                   :'the proven minimum is two');
  out.className='readout '+(bad.length===2?'verdict-ok':'verdict-no');
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const x=(e.clientX-r.left)*cv.width/r.width,y=(e.clientY-r.top)*cv.height/r.height;
  let best=null,bd=14;
  for(let i=0;i<6;i++)for(let j=i+1;j<6;j++){
    const [x0,y0]=pos[i],[x1,y1]=pos[j];
    const t=Math.max(0,Math.min(1,((x-x0)*(x1-x0)+(y-y0)*(y1-y0))/((x1-x0)**2+(y1-y0)**2)));
    const d=Math.hypot(x-(x0+t*(x1-x0)),y-(y0+t*(y1-y0)));
    if(d<bd){bd=d;best=[i,j];}
  }
  if(best){const [i,j]=best;M[i][j]=M[j][i]=1-M[i][j];draw();}
});
draw();
""",
     "Only the first offending triangle is thickened, so the picture stays "
     "readable while you work."),

    (3, "03-more-crayons", "Grow the table toward the record",
     "The first n people of the sixteen-person table. A safe table stays "
     "safe when people leave, so every size up to sixteen is safe.",
     "Walk n up to 16 and watch the triangle count stay at zero the whole "
     "way. Seventeen is impossible, but that is a theorem, not a screen: no "
     "computer sweep can reach it.",
     slider("n", "people at the table", 3, 16, 1, 8),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const n=document.getElementById('n');
function draw(){
  const N=parseInt(n.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const M=gf16Coloring(N);
  drawColoring(ctx,M,ringPos(N,360,195,152),1.6);
  const triples=N*(N-1)*(N-2)/6;
  document.getElementById('nv').textContent=N;
  document.getElementById('out').textContent=
    'people                 '+N+'\n'+
    'triples checked        '+triples+'\n'+
    'one-color triangles    '+monoTriangles(M).length;
}
n.addEventListener('input',draw);draw();
""",
     "Three colors force a triangle at seventeen people, by Greenwood and "
     "Gleason in 1955. That direction is quoted in the article, not checked, "
     "because seventeen-person colorings outnumber atoms."),

    (4, "04-the-question", "Measure any table in people per color",
     "The scoring rule behind the whole question: a table's rate is the "
     "number that, multiplied by itself once per color, gives the table "
     "size.",
     "Set size 5 at 2 colors and read 2.24. Set size 16 at 3 colors and "
     "read 2.52. Then push the size as high as you like and watch how "
     "slowly the rate responds: rates are hard currency.",
     slider("s", "table size", 2, 400, 1, 5) +
     slider("k", "colors spent", 1, 8, 1, 2),
     r"""
const cv=document.getElementById('c');
const s=document.getElementById('s'),k=document.getElementById('k');
function draw(){
  const S=parseInt(s.value),K=parseInt(k.value);
  const rate=Math.pow(S,1/K);
  const P=Plot(cv,0,5,0,4.6);
  P.clear();P.axes('','people per color');
  const bars=[[PENTAGON_BASE,'pentagon','#2a78d6'],[GF16_BASE,'sixteen table','#2a78d6'],
              [PRE_2026_BASE,'best fixed recipe','#4a3aa7'],[rate,'yours','#d03b3b']];
  bars.forEach(([v,name,col],i)=>{
    P.ctx.fillStyle=col;P.ctx.globalAlpha=(i===3)?0.95:0.55;
    P.ctx.fillRect(P.X(i+0.6),P.Y(v),P.X(i+1.3)-P.X(i+0.6),P.Y(0)-P.Y(v));
    P.ctx.globalAlpha=1;P.label(i+0.95,-0.32,name,'#52514e','center');
    P.label(i+0.95,v+0.14,v.toFixed(2),'#52514e','center');
  });
  document.getElementById('sv').textContent=S;
  document.getElementById('kv').textContent=K;
  document.getElementById('out').textContent=
    'your table    '+S+' people from '+K+' colors\n'+
    'your rate     '+rate.toFixed(3)+' people per color\n'+
    'the question: with unlimited colors, does the best possible\n'+
    'rate climb forever or level off?';
}
s.addEventListener('input',draw);k.addEventListener('input',draw);draw();
""",
     "Erdős offered 250 dollars for what the best rate approaches and 100 "
     "dollars for whether it is even finite. The 2026 answer: it climbs "
     "forever."),

    (5, "05-multiply", "Multiply two safe tables",
     "Pick the two factors. The product keeps outer colors between rooms "
     "and gives each room fresh inner colors, and this page re-checks every "
     "triangle of the result, live.",
     "Multiply the sixteen table by itself: 256 people, 6 colors, zero bad "
     "triangles out of 2.7 million checked. Then look at the rate: it never "
     "beats the better factor.",
     slider("a", "outer table (0 pentagon, 1 sixteen)", 0, 1, 1, 0) +
     slider("b", "inner table (0 pentagon, 1 sixteen)", 0, 1, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const a=document.getElementById('a'),b=document.getElementById('b');
function pick(v){ return v?{M:gf16Coloring(16),k:3,name:'sixteen'}:{M:pentagonColoring(),k:2,name:'pentagon'}; }
function draw(){
  const A=pick(parseInt(a.value)),B=pick(parseInt(b.value));
  const M=productColoring(A.M,B.M,A.k);
  const n=M.length,K=A.k+B.k;
  const bad=monoTriangles(M);
  ctx.clearRect(0,0,cv.width,cv.height);
  const outerPos=ringPos(A.M.length,360,190,A.M.length>5?128:118);
  for(let p=0;p<A.M.length;p++)for(let q=p+1;q<A.M.length;q++){
    ctx.strokeStyle=EDGE_COLORS[A.M[p][q]];ctx.lineWidth=1.1;ctx.globalAlpha=0.35;
    ctx.beginPath();ctx.moveTo(outerPos[p][0],outerPos[p][1]);
    ctx.lineTo(outerPos[q][0],outerPos[q][1]);ctx.stroke();
  }
  ctx.globalAlpha=1;
  for(const [cx,cy] of outerPos){
    const r=A.M.length>5?18:34;
    const inPos=ringPos(B.M.length,cx,cy,r);
    for(let u=0;u<B.M.length;u++)for(let v=u+1;v<B.M.length;v++){
      ctx.strokeStyle=EDGE_COLORS[A.k+B.M[u][v]];ctx.lineWidth=0.8;ctx.globalAlpha=0.8;
      ctx.beginPath();ctx.moveTo(inPos[u][0],inPos[u][1]);
      ctx.lineTo(inPos[v][0],inPos[v][1]);ctx.stroke();
    }
    ctx.globalAlpha=1;
  }
  document.getElementById('av').textContent=A.name;
  document.getElementById('bv').textContent=B.name;
  const out=document.getElementById('out');
  out.textContent=
    'product         '+n+' people, '+K+' colors\n'+
    'triples checked '+(n*(n-1)*(n-2)/6).toLocaleString()+'\n'+
    'one-color triangles '+bad.length+'\n'+
    'rate            '+Math.pow(n,1/K).toFixed(3)+' people per color';
  out.className='readout '+(bad.length===0?'verdict-ok':'verdict-no');
}
a.addEventListener('input',draw);b.addEventListener('input',draw);draw();
""",
     "The drawing shows rooms and the strings between them faintly; the "
     "verdict below is computed from the full product, every triple."),

    (8, "08-palettes", "Test the parity rule",
     "One color, three rooms. Toggle which rooms hold the color, and watch "
     "which walls a string of that color may cross.",
     "Search for a pattern that opens all three walls. There are only eight "
     "patterns, so you will be done soon, and none of them works: that is "
     "the whole proof that no triangle can touch three rooms.",
     slider("p", "room P holds the color", 0, 1, 1, 1) +
     slider("q", "room Q holds the color", 0, 1, 1, 0) +
     slider("r", "room R holds the color", 0, 1, 1, 1),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const els=['p','q','r'].map(id=>document.getElementById(id));
const centres=[[360,90],[210,290],[510,290]];
function draw(){
  const held=els.map(e=>parseInt(e.value));
  ctx.clearRect(0,0,cv.width,cv.height);
  const pairs=[[0,1],[1,2],[0,2]];
  let usable=0;
  for(const [i,j] of pairs){
    const ok=held[i]!==held[j]; if(ok)usable++;
    ctx.strokeStyle=EDGE_COLORS[2];ctx.lineWidth=ok?4:2;
    ctx.setLineDash(ok?[]:[6,6]);ctx.globalAlpha=ok?0.95:0.4;
    ctx.beginPath();ctx.moveTo(centres[i][0],centres[i][1]);
    ctx.lineTo(centres[j][0],centres[j][1]);ctx.stroke();
  }
  ctx.setLineDash([]);ctx.globalAlpha=1;
  centres.forEach(([x,y],i)=>{
    ctx.beginPath();ctx.arc(x,y,34,0,7);
    ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2;ctx.stroke();
    ctx.fillStyle=held[i]?EDGE_COLORS[2]:'#fff';
    ctx.strokeStyle=EDGE_COLORS[2];ctx.lineWidth=2;
    ctx.fillRect(x-9,y-9,18,18);ctx.strokeRect(x-9,y-9,18,18);
    ctx.fillStyle='#898781';ctx.font='13px system-ui';ctx.textAlign='center';
    ctx.fillText('PQR'[i],x,y-44);
  });
  els.forEach((e,i)=>document.getElementById(e.id+'v').textContent=
    parseInt(e.value)?'holds':'misses');
  const out=document.getElementById('out');
  out.textContent='usable walls   '+usable+' of 3\n'+
    (usable===3?'impossible, and yet here we are (this cannot happen)'
               :'a triangle needs all three: it cannot form');
  out.className='readout verdict-ok';
}
els.forEach(e=>e.addEventListener('input',draw));draw();
""",
     "A wall is usable for a color when exactly one of its two rooms holds "
     "that color. Around a triangle, held would have to alternate with "
     "missed three times, and three is odd."),

    (9, "09-the-trap", "Spring the trap, then obey the rule",
     "The pentagon room, its red net, and an outsider sending in two red "
     "strings. You choose where they land.",
     "Land both strings on teammates (the pairs 1 and 3, or 2 and 4, "
     "counting from the top) and the room absorbs them. Land them on any "
     "red-connected pair and the triangle snaps shut.",
     slider("u", "first landing spot", 1, 5, 1, 1) +
     slider("v", "second landing spot", 1, 5, 1, 3),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const u=document.getElementById('u'),v=document.getElementById('v');
const M=pentagonColoring();
const TEAMS=[0,1,0,1,2];
const pos=ringPos(5,250,195,140);
const OUT_POS=[590,195];
function draw(){
  const U=parseInt(u.value)-1,V=parseInt(v.value)-1;
  ctx.clearRect(0,0,cv.width,cv.height);
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){
    const c=M[i][j];
    ctx.strokeStyle=EDGE_COLORS[c];ctx.lineWidth=c===0?2.6:1.2;
    ctx.globalAlpha=c===0?0.95:0.35;
    ctx.beginPath();ctx.moveTo(pos[i][0],pos[i][1]);
    ctx.lineTo(pos[j][0],pos[j][1]);ctx.stroke();
  }
  ctx.globalAlpha=1;
  const sprung=(U!==V)&&M[U][V]===0;
  for(const t of [U,V]){
    ctx.strokeStyle=EDGE_COLORS[0];ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(OUT_POS[0],OUT_POS[1]);
    ctx.lineTo(pos[t][0],pos[t][1]);ctx.stroke();
  }
  if(sprung){
    ctx.strokeStyle=EDGE_COLORS[0];ctx.lineWidth=7;ctx.globalAlpha=0.7;
    for(const [a,b] of [[OUT_POS,pos[U]],[OUT_POS,pos[V]],[pos[U],pos[V]]]){
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
    }
    ctx.globalAlpha=1;
  }
  const teamFill=['#7fb0ea','#f2c063','#b9a6e8'];
  pos.forEach(([x,y],i)=>{
    ctx.beginPath();ctx.arc(x,y,11,0,7);
    ctx.fillStyle=teamFill[TEAMS[i]];ctx.fill();
    ctx.strokeStyle='#52514e';ctx.lineWidth=1.4;ctx.stroke();
    ctx.fillStyle='#0b0b0b';ctx.font='11px system-ui';ctx.textAlign='center';
    ctx.fillText(String(i+1),x,y+4);
  });
  ctx.beginPath();ctx.arc(OUT_POS[0],OUT_POS[1],11,0,7);
  ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#52514e';ctx.stroke();
  ctx.fillStyle='#898781';ctx.font='12px system-ui';
  ctx.fillText('outside',OUT_POS[0],OUT_POS[1]+30);
  document.getElementById('uv').textContent='person '+(U+1);
  document.getElementById('vv').textContent='person '+(V+1);
  const out=document.getElementById('out');
  out.textContent=(U===V)?'one landing spot: nothing to close'
    :sprung?'those two are red-connected: red triangle'
    :'those two are not red-connected: safe\n'+
     (TEAMS[U]===TEAMS[V]?'(and they are teammates, which is how the real '+
      'rule guarantees it without looking)':'(safe here, but only by luck: '+
      'the real rule would not allow this landing)');
  out.className='readout '+(sprung?'verdict-no':'verdict-ok');
}
u.addEventListener('input',draw);v.addEventListener('input',draw);draw();
""",
     "The vertex fills are the teams. The real construction never checks "
     "the room's strings; it lands every same-colored pair inside one team, "
     "and teams are never internally red-connected, so safety is automatic."),

    (10, "10-the-referee", "Interrogate the referee's card",
     "The actual thirteen-row card this repository found. Click columns to "
     "choose four of them.",
     "Choose any four columns you like, adversarially. Some row always "
     "shows both symbols inside your chosen columns; the tests check all "
     "seventy choices, and you will not find a counterexample.",
     "",
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let chosen=[0,3,4,7];
const CW=64,CH=24,X0=104,Y0=28;
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const win=chosen.length===4?saturatedRow(chosen):-1;
  for(let r=0;r<13;r++)for(let z=0;z<8;z++){
    ctx.fillStyle=EDGE_COLORS[REFEREE[r][z]];
    ctx.globalAlpha=chosen.includes(z)?0.95:0.3;
    ctx.fillRect(X0+z*CW,Y0+r*CH,CW-5,CH-5);
  }
  ctx.globalAlpha=1;
  for(const z of chosen){
    ctx.strokeStyle='#52514e';ctx.lineWidth=2;
    ctx.strokeRect(X0+z*CW-2,Y0-2,CW-1,13*CH-1);
  }
  if(win>=0){
    ctx.strokeStyle='#008300';ctx.lineWidth=3;
    ctx.strokeRect(X0-4,Y0+win*CH-3,8*CW,CH+1);
    ctx.fillStyle='#008300';ctx.font='12px system-ui';ctx.textAlign='right';
    ctx.fillText('row '+(win+1),X0-10,Y0+win*CH+15);
  }
  document.getElementById('out').textContent=
    chosen.length===4?
      'columns '+chosen.map(z=>z+1).join(', ')+'\n'+
      'row '+(saturatedRow(chosen)+1)+' shows both symbols within them\n'+
      'this holds for all 70 possible choices':
      'pick '+(4-chosen.length)+' more column'+(4-chosen.length>1?'s':'');
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const x=(e.clientX-r.left)*cv.width/r.width;
  const z=Math.floor((x-X0)/CW);
  if(z<0||z>7)return;
  if(chosen.includes(z))chosen=chosen.filter(c=>c!==z);
  else if(chosen.length<4)chosen.push(z);
  draw();
});
draw();
""",
     "Thirteen rows of coin flips suffice at this toy size, and almost any "
     "random card passes here. At the real sizes nothing can be checked "
     "case by case, and two counting arguments do the work instead."),

    (12, "12-what-it-means", "Beat the channel with longer words",
     "The noisy five-symbol channel: each symbol can be heard as either "
     "neighbour. Pick any two of the five two-letter codewords.",
     "Check every pair: some position always distinguishes them safely. "
     "Five safe words of length two beats the two safe words that single "
     "letters allow, and that surplus is what capacity measures.",
     slider("a", "first codeword", 1, 5, 1, 1) +
     slider("b", "second codeword", 1, 5, 1, 2),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const a=document.getElementById('a'),b=document.getElementById('b');
const SYM='abcde';
function draw(){
  const A=parseInt(a.value)-1,B=parseInt(b.value)-1;
  ctx.clearRect(0,0,cv.width,cv.height);
  const pos=ringPos(5,180,190,120);
  for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(confusable(i,j)){
    ctx.strokeStyle='#898781';ctx.lineWidth=5;ctx.globalAlpha=0.35;
    ctx.beginPath();ctx.moveTo(pos[i][0],pos[i][1]);
    ctx.lineTo(pos[j][0],pos[j][1]);ctx.stroke();
  }
  ctx.globalAlpha=1;
  pos.forEach(([x,y],i)=>{
    ctx.beginPath();ctx.arc(x,y,14,0,7);
    ctx.fillStyle='#fff';ctx.fill();ctx.strokeStyle='#52514e';ctx.lineWidth=1.5;ctx.stroke();
    ctx.fillStyle='#0b0b0b';ctx.font='13px system-ui';ctx.textAlign='center';
    ctx.fillText(SYM[i],x,y+4);
  });
  const d=distinguishable(CODEBOOK[A],CODEBOOK[B]);
  for(let row=0;row<5;row++){
    const yy=60+row*54;
    const active=(row===A||row===B);
    for(let col=0;col<2;col++){
      const xx=430+col*80;
      ctx.fillStyle='#fff';ctx.strokeStyle=(active&&col===d&&A!==B)?'#008300':'#c3c2b7';
      ctx.lineWidth=(active&&col===d&&A!==B)?3:1.4;
      ctx.globalAlpha=active?1:0.45;
      ctx.fillRect(xx,yy,60,40);ctx.strokeRect(xx,yy,60,40);
      ctx.fillStyle='#0b0b0b';ctx.font='16px ui-monospace';ctx.textAlign='center';
      ctx.fillText(SYM[CODEBOOK[row][col]],xx+30,yy+26);
      ctx.globalAlpha=1;
    }
  }
  document.getElementById('av').textContent='word '+(A+1);
  document.getElementById('bv').textContent='word '+(B+1);
  const out=document.getElementById('out');
  out.textContent=(A===B)?'pick two different words'
    :'position '+(d+1)+' distinguishes them: '+SYM[CODEBOOK[A][d]]+' and '+
     SYM[CODEBOOK[B][d]]+' are not confusable\n'+
     'all ten pairs pass; the tests re-check every one';
  out.className='readout '+(A===B?'':'verdict-ok');
}
a.addEventListener('input',draw);b.addEventListener('input',draw);draw();
""",
     "This is Shannon's 1956 example. The 2026 result plays the same trick "
     "with safe tables as the codebooks: because their rate climbs forever, "
     "there are channels where any three symbols contain a confusable pair "
     "and yet the capacity is as large as you like."),
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
                .replace("TITLE", f"{heading} · the triangle game")
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
             .replace("TITLE", "Play with it · the triangle game")
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
