"""Build one playable page per chapter, for all three parts.

    cd condensed-math && make play

Writes ../docs/condensed-math/<part>/play/NN.html, one per chapter, plus an
index per part.  Each page is self contained: no libraries, no network, one
canvas and a few controls.

This topic is deliberately simulation-heavy.  Condensed mathematics is a
subject where the definitions look forbidding and the ideas underneath them
are concrete: a probe really is a branching tree, a measure really is a list
of weights that add up, and the reason an exponent cannot pass one really is
that merging two boxes would make a measure bigger.  Reading those sentences
is much weaker than moving them, so every chapter gets a control that pokes
at its own claim.

The mathematics in these pages mirrors `src/condensed_guide/core.py`,
re-expressed in JavaScript.  `tests/test_interactive.py` runs the pages'
JavaScript and compares it with the Python library at sample points, so the
two cannot drift apart silently.
"""

from __future__ import annotations

from condensed_guide.parts import DOCS, PARTS, Part

# --- shared maths, kept in one place so the checks can find it -------------

MATHS = r"""
// ---------------------------------------------------------------------
// probes, as honest inverse systems of finite sets
// ---------------------------------------------------------------------
function cantorProbe(depth){
  const levels=[[""]],parents=[];
  for(let i=0;i<depth;i++){
    const nxt=[];for(const s of levels[i]){nxt.push(s+"0");nxt.push(s+"1");}
    const par={};for(const s of nxt)par[s]=s.slice(0,-1);
    parents.push(par);levels.push(nxt);
  }
  return {name:"halving",levels:levels,parents:parents};
}
function branchProbe(depth,b){
  const levels=[[""]],parents=[];
  for(let i=0;i<depth;i++){
    const nxt=[];for(const s of levels[i])for(let k=0;k<b;k++)nxt.push(s+k);
    const par={};for(const s of nxt)par[s]=s.slice(0,-1);
    parents.push(par);levels.push(nxt);
  }
  return {name:"branching by "+b,levels:levels,parents:parents};
}
function sequenceProbe(depth){
  const levels=[["oo"]],parents=[];
  for(let i=0;i<depth;i++){
    const nxt=[];for(let k=0;k<=i;k++)nxt.push(String(k));nxt.push("oo");
    const par={};for(let k=0;k<=i;k++)par[String(k)]=(k===i?"oo":String(k));
    par["oo"]="oo";
    parents.push(par);levels.push(nxt);
  }
  return {name:"approaching",levels:levels,parents:parents};
}
function pAdicProbe(p,depth){
  const levels=[["0"]],parents=[];
  for(let i=0;i<depth;i++){
    const n=Math.pow(p,i+1),nxt=[];
    for(let k=0;k<n;k++)nxt.push(String(k));
    const par={};for(let k=0;k<n;k++)par[String(k)]=String(k%Math.pow(p,i));
    parents.push(par);levels.push(nxt);
  }
  return {name:"base-"+p,levels:levels,parents:parents};
}
function probeSizes(S){ return S.levels.map(l=>l.length); }
function project(S,label,frm,to){
  for(let i=frm-1;i>=to;i--) label=S.parents[i][label];
  return label;
}
function fibre(S,label,at,over){
  return S.levels[at].filter(x=>project(S,x,at,over)===label);
}

// ---------------------------------------------------------------------
// measures: one weight per box, a box's weight the total of what is inside
// ---------------------------------------------------------------------
function measureFromLeaves(S,leafWeights){
  const d=S.levels.length-1,weights=[Object.assign({},leafWeights)];
  for(let i=d-1;i>=0;i--){
    const coarse={};for(const l of S.levels[i])coarse[l]=0;
    for(const x of S.levels[i+1])coarse[S.parents[i][x]]+=weights[0][x];
    weights.unshift(coarse);
  }
  return weights;
}
function measureOk(S,weights){
  for(let i=0;i<weights.length-1;i++)
    for(const l of S.levels[i]){
      let inner=0;
      for(const x of S.levels[i+1])if(S.parents[i][x]===l)inner+=weights[i+1][x];
      if(Math.abs(weights[i][l]-inner)>1e-9)return false;
    }
  return true;
}
function integrate(S,weights,f,level){
  let s=0;for(const l of S.levels[level])s+=f[l]*weights[level][l];return s;
}
function refineFn(S,f,frm,to){
  const g={};for(const x of S.levels[to])g[x]=f[project(S,x,to,frm)];return g;
}

// ---------------------------------------------------------------------
// the p-adic size, and the doubling sum of part two
// ---------------------------------------------------------------------
function pValuation(n,p){ if(n===0)return Infinity;let v=0;
  while(n%p===0){n/=p;v++;}return v; }
function pAdicAbsInt(n,p){ return n===0?0:Math.pow(p,-pValuation(n,p)); }
function geomPartialSums(p,terms){
  const out=[];let s=0,t=1;
  for(let n=0;n<terms;n++){s+=t;t*=p;out.push(s);}
  return out;
}
function geomLimitTimes(p){ return 1/(1-p); }   // the value the sums close on

// ---------------------------------------------------------------------
// measure sizes: why the exponent must not pass one
// ---------------------------------------------------------------------
function lpSize(vals,p){
  let s=0;for(const v of vals)s+=Math.pow(Math.abs(v),p);
  return Math.pow(s,1/p);
}
function mergeBoxes(vals,groups){
  return groups.map(g=>g.reduce((a,i)=>a+vals[i],0));
}
function mergeRatio(vals,groups,p){
  const before=lpSize(vals,p);
  return before?lpSize(mergeBoxes(vals,groups),p)/before:0;
}
function worstMergeRatio(boxes,p){ return Math.pow(boxes,1-1/p); }
function lpBallPoint(theta,p){
  const c=Math.cos(theta),s=Math.sin(theta);
  const k=Math.pow(Math.pow(Math.abs(c),p)+Math.pow(Math.abs(s),p),1/p);
  return [c/k,s/k];
}

// ---------------------------------------------------------------------
// the completed tensor product of part two, section 7
// ---------------------------------------------------------------------
const ADIC={"Z":[],"Z_p":["p"],"Z_l":["l"],"Z[[T]]":["T"],"Z[[U]]":["U"],
            "Z_p[[T]]":["p","T"],"Z[[T,U]]":["T","U"],"R":null};
// a prime direction names the base ring; the rest are formal variables
function nameDirections(dirs){
  const all=Array.from(dirs).sort();
  const primes=all.filter(d=>d==="p"||d==="l");
  const vars=all.filter(d=>d!=="p"&&d!=="l");
  const base=primes.length?("Z_"+primes[0]):"Z";
  return vars.length?(base+"[["+vars.join(",")+"]]"):base;
}
function solidTensor(a,b){
  const da=ADIC[a],db=ADIC[b];
  if(da===null||db===null)return "0";
  const dirs=new Set(da.concat(db));
  const primes=Array.from(dirs).filter(d=>d==="p"||d==="l");
  if(primes.length>1)return "0";
  return nameDirections(dirs);
}
// only these five combinations are stated outright in the lectures
const QUOTED_TENSOR=[["Z_p","Z_l"],["Z_p","R"],["Z_p","Z_p"],
                     ["Z_p","Z[[T]]"],["Z[[U]]","Z[[T]]"]];
function quotedTensor(a,b){
  return QUOTED_TENSOR.some(pr=>(pr[0]===a&&pr[1]===b)||(pr[0]===b&&pr[1]===a));
}

// ---------------------------------------------------------------------
// holes, by Smith normal form over the whole numbers
// ---------------------------------------------------------------------
function smith(mat){
  if(!mat||!mat.length||!mat[0].length)return [];
  const m=mat.map(r=>r.slice());
  const rows=m.length,cols=m[0].length,divs=[];
  let t=0;
  while(t<rows&&t<cols){
    let pi=-1,pj=-1,best=Infinity;
    for(let i=t;i<rows;i++)for(let j=t;j<cols;j++)
      if(m[i][j]&&Math.abs(m[i][j])<best){best=Math.abs(m[i][j]);pi=i;pj=j;}
    if(pi<0)break;
    const tmp=m[t];m[t]=m[pi];m[pi]=tmp;
    for(const row of m){const v=row[t];row[t]=row[pj];row[pj]=v;}
    for(let guard=0;guard<400;guard++){
      for(let i=t+1;i<rows;i++)if(m[i][t]){
        const q=Math.trunc(m[i][t]/m[t][t]);
        for(let j=0;j<cols;j++)m[i][j]-=q*m[t][j];
      }
      let nz=-1;for(let i=t+1;i<rows;i++)if(m[i][t]){nz=i;break;}
      if(nz>=0){const s=m[t];m[t]=m[nz];m[nz]=s;continue;}
      for(let j=t+1;j<cols;j++)if(m[t][j]){
        const q=Math.trunc(m[t][j]/m[t][t]);
        for(const row of m)row[j]-=q*row[t];
      }
      let nc=-1;for(let j=t+1;j<cols;j++)if(m[t][j]){nc=j;break;}
      if(nc>=0){for(const row of m){const v=row[t];row[t]=row[nc];row[nc]=v;}continue;}
      break;
    }
    divs.push(Math.abs(m[t][t]));t++;
  }
  return divisibilityChain(divs);
}
// diagonalising is not quite the normal form: a diagonal 2, 3 describes the
// same group as 1, 6, so the chain is repaired the same way as in Python
function gcd(a,b){ while(b){const t=a%b;a=b;b=t;} return Math.abs(a); }
function divisibilityChain(divs){
  const d=divs.slice().sort((a,b)=>a-b);
  let changed=true;
  while(changed){
    changed=false;
    for(let i=0;i<d.length-1;i++){
      const a=d[i],b=d[i+1];
      if(b%a){const g=gcd(a,b);d[i]=g;d[i+1]=(a/g)*b;changed=true;}
    }
  }
  return d;
}
const SHAPES={
  "circle":{cells:[1,1],bd:{1:[[0]]}},
  "figure eight":{cells:[1,2],bd:{1:[[0,0]]}},
  "sphere":{cells:[1,0,1],bd:{2:[]}},
  "torus":{cells:[1,2,1],bd:{1:[[0],[0]],2:[[0],[0]]}},
  "klein bottle":{cells:[1,2,1],bd:{1:[[0],[0]],2:[[0],[2]]}}
};
function homology(name){
  const S=SHAPES[name],out=[];
  for(let k=0;k<S.cells.length;k++){
    const n=S.cells[k],dk=S.bd[k],dn=S.bd[k+1];
    const rankK=dk&&dk.length?smith(dk).length:0;
    const divs=dn&&dn.length?smith(dn):[];
    out.push({free:n-rankK-divs.length,torsion:divs.filter(d=>d>1)});
  }
  return out;
}
function binom(n,k){ let r=1;for(let i=0;i<k;i++)r=r*(n-i)/(i+1);
  return Math.round(r); }
function exteriorRanks(n){ const o=[];for(let i=0;i<=n;i++)o.push(binom(n,i));
  return o; }

// ---------------------------------------------------------------------
// functions near the edge, of part three
// ---------------------------------------------------------------------
function lineEdgeRank(top,tails){ return (top+tails+1)-(top+1); }
function crossEdgeRank(top,tails){ return 2*(top+tails+1)-(2*(top+1)-1); }

// ---------------------------------------------------------------------
// a very small plotting helper
// ---------------------------------------------------------------------
function Plot(canvas,xlo,xhi,ylo,yhi,pad){
  const ctx=canvas.getContext('2d'), W=canvas.width, H=canvas.height;
  pad=pad||{l:54,r:18,t:18,b:40};
  const X=x=>pad.l+(x-xlo)/(xhi-xlo)*(W-pad.l-pad.r);
  const Y=y=>H-pad.b-(y-ylo)/(yhi-ylo)*(H-pad.t-pad.b);
  return {ctx,X,Y,W,H,pad,
    clear(){ctx.clearRect(0,0,W,H);},
    axes(xlabel,ylabel){
      ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;ctx.beginPath();
      ctx.moveTo(pad.l,pad.t);ctx.lineTo(pad.l,H-pad.b);
      ctx.lineTo(W-pad.r,H-pad.b);ctx.stroke();
      ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='center';
      if(xlabel)ctx.fillText(xlabel,(pad.l+W-pad.r)/2,H-9);
      if(ylabel){ctx.save();ctx.translate(14,(pad.t+H-pad.b)/2);
        ctx.rotate(-Math.PI/2);ctx.fillText(ylabel,0,0);ctx.restore();}
    },
    curve(f,color,lw,n){n=n||400;ctx.strokeStyle=color;ctx.lineWidth=lw||2.2;
      ctx.beginPath();
      for(let i=0;i<=n;i++){const x=xlo+(xhi-xlo)*i/n,y=f(x);
        if(i===0)ctx.moveTo(X(x),Y(y));else ctx.lineTo(X(x),Y(y));}
      ctx.stroke();},
    line(xs,ys,color,lw){ctx.strokeStyle=color;ctx.lineWidth=lw||2;
      ctx.beginPath();
      for(let i=0;i<xs.length;i++){if(i===0)ctx.moveTo(X(xs[i]),Y(ys[i]));
        else ctx.lineTo(X(xs[i]),Y(ys[i]));}ctx.stroke();},
    dots(xs,ys,color,r){ctx.fillStyle=color;
      for(let i=0;i<xs.length;i++){ctx.beginPath();
        ctx.arc(X(xs[i]),Y(ys[i]),r||3.4,0,7);ctx.fill();}},
    hline(y,color,dash){ctx.save();ctx.strokeStyle=color;
      ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(pad.l,Y(y));
      ctx.lineTo(W-pad.r,Y(y));ctx.stroke();ctx.restore();},
    vline(x,color,dash){ctx.save();ctx.strokeStyle=color;
      ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(X(x),pad.t);
      ctx.lineTo(X(x),H-pad.b);ctx.stroke();ctx.restore();},
    label(x,y,text,color,align){ctx.fillStyle=color;ctx.font='12px system-ui';
      ctx.textAlign=align||'left';ctx.fillText(text,X(x),Y(y));}
  };
}

// draw a probe as a branching diagram; returns the positions used
function drawTree(ctx,S,depth,box,opts){
  opts=opts||{};
  const yStep=(box.h-24)/Math.max(1,depth);
  const pos={};
  for(let i=0;i<=depth;i++){
    const n=S.levels[i].length,step=box.w/n;
    for(let k=0;k<n;k++)
      pos[i+"|"+S.levels[i][k]]=[box.x+(k+0.5)*step,box.y+12+i*yStep];
  }
  ctx.strokeStyle=opts.edge||'#c3c2b7';ctx.lineWidth=1;
  for(let i=0;i<depth;i++)
    for(const l of S.levels[i+1]){
      const a=pos[(i+1)+"|"+l],b=pos[i+"|"+S.parents[i][l]];
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
    }
  for(let i=0;i<=depth;i++)
    for(const l of S.levels[i]){
      const p=pos[i+"|"+l];
      ctx.fillStyle=(opts.colour?opts.colour(i,l):null)||'#2a78d6';
      ctx.beginPath();ctx.arc(p[0],p[1],opts.r||4,0,7);ctx.fill();
    }
  return pos;
}
"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TITLE</title>
<style>
 :root{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
        --line:#e1e0d9;--blue:#2a78d6;--green:#008300;--red:#d03b3b;
        --violet:#4a3aa7;--teal:#00787a;--brown:#8a5a2c;}
 @media (prefers-color-scheme: dark){
   :root{--surface:#15150f;--ink:#f2f1ea;--ink2:#c9c7bd;--muted:#8d8b82;
         --line:#33322c;}
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
 canvas{width:100%;height:auto;display:block;border-radius:8px;
   background:var(--surface)}
 .controls{margin:18px 0 0}
 .row{display:flex;align-items:center;gap:12px;margin:10px 0}
 .row label{flex:0 0 200px;font-size:14px;color:var(--ink2)}
 input[type=range]{flex:1;accent-color:var(--blue)}
 .val{flex:0 0 120px;text-align:right;font-family:ui-monospace,monospace;
   font-size:13px}
 .pick{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
 .pick button{font:inherit;font-size:13.5px;padding:6px 12px;cursor:pointer;
   border:1px solid var(--line);border-radius:999px;background:transparent;
   color:var(--ink2)}
 .pick button:hover{border-color:var(--blue);color:var(--blue)}
 .pick button.on{background:var(--blue);border-color:var(--blue);color:#fff}
 .readout{margin-top:18px;padding:14px 16px;border:1px solid var(--line);
   border-radius:8px;font-family:ui-monospace,monospace;font-size:14px;
   white-space:pre-line}
 .verdict-ok{color:var(--green)} .verdict-no{color:var(--red)}
 .nav{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);
   font-size:14px}
 .nav a{color:var(--blue);text-decoration:none}
 .nav a:hover{text-decoration:underline}
 .note{margin-top:26px;font-size:13.5px;color:var(--muted)}
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
<canvas id="c" width="720" height="400"></canvas>
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


def picker(ident, label, options, chosen=0):
    buttons = "".join(
        f'<button data-v="{v}" class="{"on" if i == chosen else ""}">{t}</button>'
        for i, (v, t) in enumerate(options))
    return (f'<div class="row"><label>{label}</label>'
            f'<div class="pick" id="{ident}" style="flex:1">{buttons}</div></div>')


PICKER_JS = r"""
function pick(id,onChange){
  const box=document.getElementById(id);
  let cur=box.querySelector('button.on').dataset.v;
  box.addEventListener('click',e=>{
    if(e.target.tagName!=='BUTTON')return;
    box.querySelectorAll('button').forEach(b=>b.classList.remove('on'));
    e.target.classList.add('on');cur=e.target.dataset.v;onChange(cur);
  });
  return {get value(){return cur;}};
}
"""


# --- part one: shapes you can only see by probing them ---------------------

PART_ONE_CHAPTERS = [
    (0, "Build a probe",
     "A probe is one box, split, and split again, forever. Below the tree is "
     "the dust it cuts out: the points you reach by following the splits all "
     "the way down.",
     "Push the depth up one step at a time and watch the boxes halve. Every "
     "single stage is a finite picture. Only the whole endless stack is "
     "infinite, and it is the only infinite thing in the definition.",
     slider("depth", "how many splits", 0, 6, 1, 3) +
     slider("branch", "pieces per split", 2, 4, 1, 2),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const depth=document.getElementById('depth'),branch=document.getElementById('branch');
function draw(){
  const d=parseInt(depth.value),b=parseInt(branch.value);
  const S=branchProbe(d,b);
  ctx.clearRect(0,0,cv.width,cv.height);
  drawTree(ctx,S,d,{x:40,y:18,w:640,h:210},{r:4.2});
  // the dust: the intervals the deepest level cuts out
  const n=S.levels[d].length,y=300,W=640,seg=W/n;
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('the dust the splits cut out',40,278);
  for(let k=0;k<n;k++){
    const w=Math.max(1.2,seg*0.62);
    ctx.fillStyle='#4a3aa7';
    ctx.fillRect(40+k*seg+(seg-w)/2,y,w,26);
  }
  const sizes=probeSizes(S);
  depthv.textContent=String(d);branchv.textContent=String(b);
  document.getElementById('out').textContent=
    'boxes at each stage   '+sizes.join(', ')+'\n'+
    'boxes at the finest   '+sizes[sizes.length-1]+'\n'+
    'every stage is finite; only the endless stack is not';
}
depth.addEventListener('input',draw);branch.addEventListener('input',draw);draw();
""",
     "Splitting in two gives the Cantor set, the probe the guide calls the "
     "halving probe. Splitting in p gives the base-p probe of part two. The "
     "tree and the counts are built by the same code as the figures."),

    (1, "The two real lines",
     "The same numbers twice: as separated grains with no notion of nearness, "
     "and as a ruler where nearness is everything. The slider is how closely "
     "you look.",
     "Zoom in as far as you like. On the ruler, every window you open holds "
     "endlessly many other points. On the dust, every window eventually holds "
     "one point and nothing else. The two are the same list of numbers and "
     "different objects.",
     slider("zoom", "how closely you look", 0, 100, 1, 20),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const zoom=document.getElementById('zoom');
function draw(){
  const z=parseInt(zoom.value);
  const half=Math.pow(10,-z/25);       // half-width of the window
  ctx.clearRect(0,0,cv.width,cv.height);
  const x0=60,x1=680,cx=(x0+x1)/2;
  // the ruler
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the ruler: nearness kept',x0,42);
  ctx.strokeStyle='#4a3aa7';ctx.lineWidth=3;
  ctx.beginPath();ctx.moveTo(x0,70);ctx.lineTo(x1,70);ctx.stroke();
  ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(cx,70,6,0,7);ctx.fill();
  ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('every window holds endlessly many others',cx,96);
  // the dust
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the dust: nearness forgotten',x0,168);
  const grains=Math.max(1,Math.round(28*Math.min(1,half*40)));
  for(let k=0;k<=grains;k++){
    const x=grains===0?cx:x0+(x1-x0)*k/grains;
    ctx.fillStyle=(Math.abs(x-cx)<8)?'#d03b3b':'#8a5a2c';
    ctx.beginPath();ctx.arc(x,196,5,0,7);ctx.fill();
  }
  ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText(grains<=1?'the window now holds one grain and nothing else'
                        :'grains, each one alone',cx,224);
  // the matching
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('send each number to itself',x0,278);
  for(let k=0;k<=10;k++){
    const x=x0+(x1-x0)*k/10;
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(x,292);ctx.lineTo(x,326);ctx.stroke();
  }
  ctx.strokeStyle='#8a5a2c';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(x0,292);ctx.lineTo(x1,292);ctx.stroke();
  ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(x0,326);ctx.lineTo(x1,326);ctx.stroke();
  zoomv.textContent='window '+half.toExponential(1);
  const out=document.getElementById('out');
  out.textContent=
    'numbers left over at the front   0\n'+
    'numbers left over at the back    0\n'+
    'so the map kills nothing and misses nothing\n'+
    (grains<=1?'and yet: this window separates a grain but not a ruler point'
              :'keep zooming until one grain stands alone');
  out.className='readout '+(grains<=1?'verdict-no':'');
}
zoom.addEventListener('input',draw);draw();
""",
     "The kill-list and miss-list really are empty, which is why ordinary "
     "algebra concludes the two are the same object and is wrong. Part one, "
     "section 5, names what it is missing."),

    (2, "Switch the probe",
     "The three probes this guide uses. The tree is the stack of finite "
     "stages; click any box to light up everything inside it.",
     "Compare the counts. The halving probe doubles, the approaching probe "
     "adds one separated point per stage and keeps the rest in a single box, "
     "and the base-p probe multiplies by p. All three are built from finite "
     "stages only.",
     picker("kind", "which probe", [("cantor", "halving"),
                                    ("seq", "approaching"),
                                    ("padic", "base-p")]) +
     slider("depth2", "stages shown", 1, 5, 1, 4) +
     slider("pval", "p, for the base-p probe", 2, 5, 1, 3),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const depth2=document.getElementById('depth2'),pval=document.getElementById('pval');
let chosen=null,kind='cantor';
const K=pick('kind',v=>{kind=v;chosen=null;draw();});
function probe(){
  const d=parseInt(depth2.value);
  if(kind==='cantor')return cantorProbe(d);
  if(kind==='seq')return sequenceProbe(d);
  return pAdicProbe(parseInt(pval.value),d);
}
let POS={},CUR=null,DEPTH=0;
function draw(){
  const d=parseInt(depth2.value);DEPTH=d;
  const S=probe();CUR=S;
  ctx.clearRect(0,0,cv.width,cv.height);
  const inside=new Set();
  if(chosen){
    for(let i=chosen.lvl;i<=d;i++)
      for(const x of fibre(S,chosen.label,i,chosen.lvl))inside.add(i+'|'+x);
  }
  POS=drawTree(ctx,S,d,{x:40,y:20,w:640,h:250},
    {r:5,colour:(i,l)=>inside.has(i+'|'+l)?'#008300':'#2a78d6'});
  const sizes=probeSizes(S);
  // the counts as bars
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('boxes per stage',40,318);
  for(let i=0;i<sizes.length;i++){
    const w=Math.min(560,sizes[i]*10);
    ctx.fillStyle='#00787a';ctx.fillRect(120,328+i*13,Math.max(2,w),8);
    ctx.fillStyle='#52514e';ctx.font='11px system-ui';ctx.textAlign='right';
    ctx.fillText('stage '+i,112,336+i*13);
    ctx.textAlign='left';ctx.fillText(String(sizes[i]),126+Math.max(2,w),336+i*13);
  }
  depth2v.textContent=String(d);pvalv.textContent=String(pval.value);
  document.getElementById('out').textContent=
    S.name+' probe\n'+
    'boxes per stage   '+sizes.join(', ')+'\n'+
    (chosen?('clicked a stage-'+chosen.lvl+' box: '+
             fibre(S,chosen.label,d,chosen.lvl).length+
             ' of the finest boxes sit inside it')
           :'click a box to light up everything inside it');
}
cv.addEventListener('click',e=>{
  const r=cv.getBoundingClientRect();
  const mx=(e.clientX-r.left)*cv.width/r.width;
  const my=(e.clientY-r.top)*cv.height/r.height;
  let best=null,bd=1e9;
  for(const key in POS){
    const [lvl,label]=key.split('|');
    const p=POS[key],d2=(p[0]-mx)**2+(p[1]-my)**2;
    if(d2<bd){bd=d2;best={lvl:parseInt(lvl),label:label};}
  }
  if(bd<400){chosen=best;draw();}
});
depth2.addEventListener('input',draw);pval.addEventListener('input',draw);draw();
""",
     "These are the profinite sets of Definition 1.2. The counts and the "
     "boxes-inside-a-box are computed live by the same recipe as the Python "
     "library, and the tests compare the two."),

    (3, "Land a probe without tearing it",
     "The approaching probe on the left: points marching towards a limit. A "
     "target line on the right. You choose where the marching points head, "
     "and where the limit point lands.",
     "Set the two sliders apart and the chain snaps at the limit: the "
     "landing is refused. Bring them together and it is accepted. That gap, "
     "and nothing else, is what continuity means to a probe.",
     slider("tend", "where the marching points head", -100, 100, 1, 30) +
     slider("limit", "where the limit point lands", -100, 100, 1, 30),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const tend=document.getElementById('tend'),limit=document.getElementById('limit');
function draw(){
  const a=parseInt(tend.value)/100,b=parseInt(limit.value)/100;
  ctx.clearRect(0,0,cv.width,cv.height);
  const lx=110,rx=560,top=48,bot=340;
  const Y=v=>(top+bot)/2-v*((bot-top)/2-14);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText('the probe',lx,30);ctx.fillText('the target',rx,30);
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(rx,top);ctx.lineTo(rx,bot);ctx.stroke();
  const N=9;
  for(let k=0;k<N;k++){
    const py=top+18+k*22;                       // probe point k
    const val=a+0.85/(k+1);            // the marching landings
    ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(lx,py,5,0,7);ctx.fill();
    ctx.strokeStyle='rgba(42,120,214,0.45)';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(lx+8,py);ctx.lineTo(rx-4,Y(val));ctx.stroke();
    ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(rx,Y(val),4,0,7);ctx.fill();
  }
  // the limit point of the probe
  const py=top+18+N*22+18;
  ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(lx,py,7,0,7);ctx.fill();
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='right';
  ctx.fillText('the limit point',lx-12,py+4);
  ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(lx+9,py);ctx.lineTo(rx-4,Y(b));ctx.stroke();
  ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(rx,Y(b),6,0,7);ctx.fill();
  // where the march is heading
  ctx.strokeStyle='#008300';ctx.setLineDash([4,4]);ctx.lineWidth=1.6;
  ctx.beginPath();ctx.moveTo(rx-70,Y(a));ctx.lineTo(rx+70,Y(a));ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#008300';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('where the march heads',rx+14,Y(a)-8);
  const gap=Math.abs(a-b),ok=gap<0.02;
  if(!ok){
    ctx.strokeStyle='#d03b3b';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(rx+4,Y(a));ctx.lineTo(rx+4,Y(b));ctx.stroke();
    ctx.fillStyle='#d03b3b';ctx.textAlign='left';
    ctx.fillText('the chain snaps here',rx+14,(Y(a)+Y(b))/2+4);
  }
  tendv.textContent=a.toFixed(2);limitv.textContent=b.toFixed(2);
  const out=document.getElementById('out');
  out.textContent='the march heads to   '+a.toFixed(2)+'\n'+
    'the limit lands at   '+b.toFixed(2)+'\n'+
    'gap                  '+gap.toFixed(2)+'\n'+
    (ok?'accepted: nearby points of the probe go to nearby points'
       :'refused: the probe was torn at its limit');
  out.className='readout '+(ok?'verdict-ok':'verdict-no');
}
tend.addEventListener('input',draw);limit.addEventListener('input',draw);draw();
""",
     "Every space you can measure distance in is determined by which "
     "sequences converge, so this one probe already reads all of them. That "
     "is Remark 1.6 of the lectures."),

    (4, "Cut, then glue",
     "Two rules tie an answer sheet together. Cut: a probe in separate "
     "pieces is answered piece by piece. Glue: answers on a covering that "
     "agree on the overlap come from exactly one answer below.",
     "Set the two pieces to different values and the cut rule is happy, "
     "since nothing connects them. Then move to gluing and make the overlap "
     "disagree: the answers refuse to become one.",
     picker("rule", "which rule", [("cut", "cut"), ("glue", "glue")]) +
     slider("left", "answer on the left piece", 0, 5, 1, 2) +
     slider("right", "answer on the right piece", 0, 5, 1, 4),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const L=document.getElementById('left'),R=document.getElementById('right');
let mode='cut';
pick('rule',v=>{mode=v;draw();});
const COL=['#2a78d6','#00787a','#4a3aa7','#8a5a2c','#008300','#eda100'];
function band(x,y,w,h,c,txt){
  ctx.fillStyle=c;ctx.fillRect(x,y,w,h);
  ctx.fillStyle='#fff';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText(txt,x+w/2,y+h/2+5);
}
function draw(){
  const a=parseInt(L.value),b=parseInt(R.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  if(mode==='cut'){
    ctx.fillText('one probe, falling into two separate pieces',40,34);
    band(40,54,300,44,COL[a],'answer '+a);
    band(380,54,300,44,COL[b],'answer '+b);
    ctx.fillStyle='#52514e';ctx.textAlign='left';
    ctx.fillText('answering the whole probe',40,150);
    band(40,170,640,44,'#898781','the pair ('+a+', '+b+')');
    ctx.fillStyle='#008300';ctx.font='13px system-ui';
    ctx.fillText('accepted for every choice: nothing connects the pieces',40,246);
    document.getElementById('out').textContent=
      'left piece    '+a+'\nright piece   '+b+'\n'+
      'the whole     ('+a+', '+b+')\n'+
      'the cut rule accepts every pair, always';
    document.getElementById('out').className='readout verdict-ok';
  }else{
    ctx.fillText('a covering: two pieces, overlapping in the middle',40,34);
    band(40,54,400,44,COL[a],'answer '+a);
    band(280,116,400,44,COL[b],'answer '+b);
    ctx.strokeStyle='#0b0b0b';ctx.setLineDash([4,4]);ctx.lineWidth=1.4;
    ctx.strokeRect(280,50,160,114);ctx.setLineDash([]);
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('the overlap',360,182);
    const ok=(a===b);
    ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
    ctx.fillText('the probe underneath',40,224);
    if(ok){ band(40,244,640,44,COL[a],'exactly one answer: '+a); }
    else {
      ctx.strokeStyle='#d03b3b';ctx.lineWidth=2.5;ctx.setLineDash([6,5]);
      ctx.strokeRect(40,244,640,44);ctx.setLineDash([]);
      ctx.fillStyle='#d03b3b';ctx.textAlign='center';
      ctx.fillText('no answer below: the pieces disagree on the overlap',360,271);
    }
    document.getElementById('out').textContent=
      'left piece    '+a+'\nright piece   '+b+'\n'+
      (ok?'they agree on the overlap, so exactly one answer glues below'
         :'they disagree on the overlap, so nothing glues');
    document.getElementById('out').className='readout '+(ok?'verdict-ok':'verdict-no');
  }
  leftv.textContent=String(a);rightv.textContent=String(b);
}
L.addEventListener('input',draw);R.addEventListener('input',draw);draw();
""",
     "These are the two sheaf conditions listed under Definition 1.2. On an "
     "unfoldable probe the glue rule holds automatically, which is why part "
     "one, section 6, is worth its strangeness."),

    (5, "Build a ghost",
     "On the halving probe, choose how much each split shifts the value. The "
     "result is a landing the ruler allows and the dust does not, which is "
     "one entry of the group with no points.",
     "Set the wobble to zero: the landing is flat on every box, so the dust "
     "can do it too, and the ghost entry is zero. Turn the wobble up and no "
     "box is ever flat, however deep you look. The point count stays at "
     "zero throughout.",
     slider("wobble", "how much each split shifts", 0, 100, 1, 60) +
     slider("gdepth", "how deep you look", 1, 7, 1, 5),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const wob=document.getElementById('wobble'),gd=document.getElementById('gdepth');
function draw(){
  const w=parseInt(wob.value)/100,d=parseInt(gd.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const n=Math.pow(2,d),x0=40,W=640,y0=40,H=210;
  // the landing: a value per finest box, built by shifting at every split
  const vals=[];
  for(let k=0;k<n;k++){
    let v=0.5,step=0.5;
    for(let i=0;i<d;i++){
      const bit=(k>>(d-1-i))&1;step/=2;
      v+=(bit?step:-step)*w;
    }
    vals.push(v);
  }
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('the landing, box by box',x0,28);
  const seg=W/n;
  for(let k=0;k<n;k++){
    const h=vals[k]*H;
    ctx.fillStyle=w<0.01?'#008300':'#4a3aa7';
    ctx.fillRect(x0+k*seg,y0+H-h,Math.max(1,seg-0.6),h);
  }
  // how flat the finest boxes are
  let spread=0;
  for(let k=0;k<n;k+=2)spread=Math.max(spread,Math.abs(vals[k]-vals[k+1]));
  ctx.fillStyle='#52514e';ctx.fillText('what a single point can see',x0,300);
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(x0,326);ctx.lineTo(x0+W,326);ctx.stroke();
  ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('nothing: the ghost has no points at all',x0+W/2,348);
  wobblev.textContent=w.toFixed(2);gdepthv.textContent=String(d);
  const flat=spread<1e-9;
  const out=document.getElementById('out');
  out.textContent=
    'points the ghost has            0\n'+
    'widest gap inside a finest box  '+spread.toFixed(4)+'\n'+
    (flat?'flat on every box, so the dust can do it too: this entry is zero'
         :'never flat, however deep you look: a nonzero entry of the ghost');
  out.className='readout '+(flat?'':'verdict-ok');
}
wob.addEventListener('input',draw);gd.addEventListener('input',draw);draw();
""",
     "This is Example 1.9 of the lectures made concrete. The point count is "
     "zero for every setting; the probe entry is not, and that difference is "
     "exactly what topological groups could not express."),

    (6, "The lifting game",
     "A covering: two copies sit above every point of the probe. Choose one "
     "copy per point. On the approaching probe your choices must settle "
     "down, or the limit point cannot be lifted.",
     "Set the pattern to alternate and watch the limit fail: neither copy is "
     "what the choices are approaching. Then switch to the unfoldable probe, "
     "where nothing converges in the first place, so no choice is ever "
     "blocked.",
     picker("base", "which probe below",
            [("seq", "approaching"), ("ed", "unfoldable")]) +
     slider("period", "how often the choice flips", 1, 8, 1, 1),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const per=document.getElementById('period');
let base='seq';
pick('base',v=>{base=v;draw();});
function draw(){
  const P=parseInt(per.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const N=12,x0=60,step=48,yUp=90,yDn=250,yBase=250;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the covering: two copies above every point',20,30);
  ctx.fillText('the probe below',20,332);
  const choices=[];
  for(let k=0;k<N;k++)choices.push(Math.floor(k/P)%2);
  for(let k=0;k<N;k++){
    const x=x0+k*step;
    ctx.fillStyle='#c3c2b7';
    ctx.beginPath();ctx.arc(x,yUp,5,0,7);ctx.fill();
    ctx.beginPath();ctx.arc(x,yUp+70,5,0,7);ctx.fill();
    const y=choices[k]?yUp:yUp+70;
    ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(x,y,7,0,7);ctx.fill();
    ctx.strokeStyle='rgba(42,120,214,0.5)';ctx.lineWidth=1.4;
    ctx.beginPath();ctx.moveTo(x,y+8);ctx.lineTo(x,yBase-8);ctx.stroke();
    ctx.fillStyle=(base==='seq')?'#4a3aa7':'#8a5a2c';
    ctx.beginPath();ctx.arc(x,yBase,5,0,7);ctx.fill();
  }
  const settles=(P>=N);
  if(base==='seq'){
    const lx=x0+N*step+34;
    ctx.fillStyle='#4a3aa7';ctx.beginPath();ctx.arc(lx,yBase,8,0,7);ctx.fill();
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('the limit',lx,yBase+24);
    if(settles){
      const y=choices[N-1]?yUp:yUp+70;
      ctx.fillStyle='#008300';ctx.beginPath();ctx.arc(lx,y,8,0,7);ctx.fill();
      ctx.strokeStyle='#008300';ctx.lineWidth=2;
      ctx.beginPath();ctx.moveTo(lx,y+9);ctx.lineTo(lx,yBase-9);ctx.stroke();
    }else{
      ctx.strokeStyle='#d03b3b';ctx.lineWidth=2.5;
      ctx.beginPath();ctx.arc(lx,yUp,9,0,7);ctx.stroke();
      ctx.beginPath();ctx.arc(lx,yUp+70,9,0,7);ctx.stroke();
      ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';ctx.textAlign='center';
      ctx.fillText('neither copy works',lx,yUp+108);
    }
  }else{
    ctx.fillStyle='#8a5a2c';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText('nothing converges here, so no limit point can be blocked',
                 x0,yBase+42);
  }
  periodv.textContent=P>=N?'never':('every '+P);
  const ok=(base==='ed')||settles;
  const out=document.getElementById('out');
  out.textContent=(base==='seq'?'approaching probe below\n':'unfoldable probe below\n')+
    'choices flip   '+(P>=N?'never':'every '+P+' points')+'\n'+
    (base==='ed'
      ? 'every covering of an unfoldable probe lifts, whatever you choose'
      : (settles?'the choices settle, so the limit lifts too'
                :'the choices never settle, so the limit cannot be lifted'));
  out.className='readout '+(ok?'verdict-ok':'verdict-no');
}
per.addEventListener('input',draw);draw();
""",
     "Unfoldable is the guide's word for extremally disconnected, Definition "
     "2.4. The fact that nothing converges in one is Warning 2.6, and it is "
     "why the picture on the right looks so unlike anything you would draw."),

    (7, "The round trip",
     "Turn a space into its answer sheet, then read a space back out of it. "
     "On everything ordinary you get what you started with.",
     "Send each space around. The circle, the interval and the finite set "
     "return unchanged. The last one, where a point is not closed, never "
     "becomes an answer sheet at all, and the lectures flag it as the one "
     "genuine failure.",
     picker("space", "which space", [("circle", "circle"), ("seg", "interval"),
                                     ("two", "two points"),
                                     ("sier", "a point that is not closed")]),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let which='circle';
pick('space',v=>{which=v;draw();});
function shape(cx,cy,scale,dim){
  ctx.strokeStyle=dim?'#c3c2b7':'#4a3aa7';ctx.fillStyle=dim?'#c3c2b7':'#4a3aa7';
  ctx.lineWidth=3;
  if(which==='circle'){ctx.beginPath();ctx.arc(cx,cy,44*scale,0,7);ctx.stroke();}
  else if(which==='seg'){ctx.beginPath();ctx.moveTo(cx-54*scale,cy);
    ctx.lineTo(cx+54*scale,cy);ctx.stroke();
    ctx.beginPath();ctx.arc(cx-54*scale,cy,5,0,7);ctx.fill();
    ctx.beginPath();ctx.arc(cx+54*scale,cy,5,0,7);ctx.fill();}
  else if(which==='two'){ctx.beginPath();ctx.arc(cx-26,cy,8,0,7);ctx.fill();
    ctx.beginPath();ctx.arc(cx+26,cy,8,0,7);ctx.fill();}
  else{ctx.beginPath();ctx.arc(cx-26,cy,8,0,7);ctx.fill();
    ctx.strokeStyle=dim?'#c3c2b7':'#d03b3b';ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(cx+26,cy,9,0,7);ctx.stroke();
    ctx.fillStyle=dim?'#c3c2b7':'#d03b3b';ctx.font='11px system-ui';
    ctx.textAlign='center';ctx.fillText('not closed',cx+26,cy+26);}
}
function arrow(x0,y,x1,label,dead){
  ctx.strokeStyle=dead?'#d03b3b':'#008300';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(x0,y);ctx.lineTo(x1,y);ctx.stroke();
  ctx.beginPath();ctx.moveTo(x1,y);ctx.lineTo(x1-9,y-5);ctx.lineTo(x1-9,y+5);
  ctx.closePath();ctx.fillStyle=dead?'#d03b3b':'#008300';ctx.fill();
  ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText(label,(x0+x1)/2,y-12);
}
function draw(){
  const bad=(which==='sier');
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText('the space',110,50);shape(110,150,1,false);
  arrow(190,150,300,'read by probes',bad);
  // the answer sheet, drawn as a stack of probe entries
  ctx.fillText('the answer sheet',390,50);
  for(let i=0;i<5;i++){
    ctx.strokeStyle=bad?'#d03b3b':'#2a78d6';ctx.lineWidth=1.6;
    ctx.strokeRect(340,110+i*24,100,18);
    ctx.fillStyle=bad?'#d03b3b':'#2a78d6';ctx.font='11px system-ui';
    ctx.fillText('probe '+(i+1),390,123+i*24);
  }
  if(bad){
    ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';
    ctx.fillText('no answer sheet exists',390,250);
  }
  arrow(470,150,580,'points read back',bad);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';
  ctx.fillText('the space again',650,50);shape(650,150,1,bad);
  const out=document.getElementById('out');
  out.textContent=bad
    ? 'a point of this space is not closed\n'+
      'such a space never becomes an answer sheet, at any size bound\n'+
      'the lectures flag exactly this case as the failure'
    : 'sent out and read back: the same space\n'+
      'the continuous maps out of it are the same maps too';
  out.className='readout '+(bad?'verdict-no':'verdict-ok');
}
draw();
""",
     "The round trip working is Proposition 1.7 and Theorem 2.16; the "
     "failure is Warning 2.14. Every space with a distance on it, and every "
     "shape built from cells, is on the safe side."),

    (8, "Count the turns",
     "A closed path drawn on a ring. The only thing about it that survives "
     "wobbling is how many whole turns it makes, and that count is the "
     "ring's first hole count.",
     "Change the turns and watch the counter follow. Then push the wobble as "
     "far as it goes: the path deforms wildly and the count does not move. "
     "Switch to the doughnut and there are two counts to keep.",
     picker("holes", "which shape", [("ring", "ring"), ("torus", "doughnut")]) +
     slider("turns", "turns the path makes", -3, 3, 1, 2) +
     slider("turns2", "turns the second way, for the doughnut", -3, 3, 1, 1) +
     slider("wob2", "how much to wobble the path", 0, 100, 1, 0),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const T1=document.getElementById('turns'),T2=document.getElementById('turns2');
const WB=document.getElementById('wob2');
let mode='ring';
pick('holes',v=>{mode=v;draw();});
function draw(){
  const n1=parseInt(T1.value),n2=parseInt(T2.value),w=parseInt(WB.value)/100;
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=360,cy=190;
  if(mode==='ring'){
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=26;
    ctx.beginPath();ctx.arc(cx,cy,120,0,7);ctx.stroke();
    ctx.strokeStyle='#2a78d6';ctx.lineWidth=2.6;ctx.beginPath();
    const N=1400;
    for(let i=0;i<=N;i++){
      const t=i/N*2*Math.PI;
      const ang=n1*t+w*1.9*Math.sin(5*t);
      const rad=120+w*26*Math.sin(7*t);
      const x=cx+rad*Math.cos(ang),y=cy+rad*Math.sin(ang);
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
    // the running angle, unwrapped, is what the counter reads
    let total=0,prev=0;
    for(let i=1;i<=600;i++){
      const t=i/600*2*Math.PI,tp=(i-1)/600*2*Math.PI;
      const a=n1*t+w*1.9*Math.sin(5*t),b=n1*tp+w*1.9*Math.sin(5*tp);
      let d=a-b;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;
      total+=d;
    }
    const count=Math.round(total/(2*Math.PI));
    document.getElementById('out').textContent=
      'turns you asked for   '+n1+'\n'+
      'turns measured        '+count+'\n'+
      'wobble                '+w.toFixed(2)+'\n'+
      'the count is a whole number and the wobble cannot move it';
    document.getElementById('out').className='readout '+
      (count===n1?'verdict-ok':'verdict-no');
  }else{
    // a doughnut seen at an angle, with the two independent loops on it
    const R=132,r=48,tilt=0.42;
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
    for(let k=0;k<28;k++){
      const u=k/28*2*Math.PI;
      ctx.beginPath();
      for(let j=0;j<=40;j++){
        const v=j/40*2*Math.PI;
        const x=cx+(R+r*Math.cos(v))*Math.cos(u);
        const y=cy+((R+r*Math.cos(v))*Math.sin(u))*tilt+r*Math.sin(v)*0.86;
        if(j===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
      }
      ctx.stroke();
    }
    ctx.strokeStyle='#2a78d6';ctx.lineWidth=3;ctx.beginPath();
    for(let j=0;j<=400;j++){
      const u=j/400*2*Math.PI;
      const x=cx+(R+r)*Math.cos(u),y=cy+(R+r)*Math.sin(u)*tilt;
      if(j===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
    ctx.strokeStyle='#008300';ctx.lineWidth=3;ctx.beginPath();
    for(let j=0;j<=400;j++){
      const v=j/400*2*Math.PI;
      const x=cx+(R+r*Math.cos(v)),y=cy+(R+r*Math.cos(v))*0+r*Math.sin(v)*0.86;
      if(j===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
    ctx.fillStyle='#2a78d6';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('the long way round',cx,cy-124);
    ctx.fillStyle='#008300';
    ctx.fillText('through the hole',cx+R+r+2,cy+r+34);
    const ranks=exteriorRanks(2);
    document.getElementById('out').textContent=
      'turns the long way    '+n1+'\n'+
      'turns through the hole '+n2+'\n'+
      'hole counts by degree  '+ranks.join(', ')+'\n'+
      'two independent loops, and their combination in degree two';
    document.getElementById('out').className='readout verdict-ok';
  }
  turnsv.textContent=String(n1);turns2v.textContent=String(n2);
  wob2v.textContent=w.toFixed(2);
}
[T1,T2,WB].forEach(s=>s.addEventListener('input',draw));draw();
""",
     "The winding count is the first hole count of the circle. The doughnut "
     "row is the exterior pattern of Proposition 3.1, recomputed here; the "
     "tests check it against the same formula in Python."),
]


# --- part two: infinite sums that finally land -----------------------------

PART_TWO_CHAPTERS = [
    (0, "Hand out the weights",
     "One number at the top, split down the tree. The only rule is that a "
     "box's number is always the total of the boxes inside it.",
     "Move the bias and watch the weight slide between the branches. The "
     "totals along every stage stay equal, because nothing was created or "
     "destroyed by splitting. That, and nothing else, is what a weighting is.",
     slider("bias", "how each split leans", 0, 100, 1, 50) +
     slider("wdepth", "stages shown", 1, 5, 1, 4) +
     slider("start", "the number at the top", 1, 64, 1, 32),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const bias=document.getElementById('bias'),wd=document.getElementById('wdepth');
const st=document.getElementById('start');
function draw(){
  const b=parseInt(bias.value)/100,d=parseInt(wd.value),top=parseInt(st.value);
  const S=cantorProbe(d);
  // hand the weight down, leaning by the bias at every split
  const w=[{"":top}];
  for(let i=0;i<d;i++){
    const nxt={};
    for(const l of S.levels[i]){
      const v=w[i][l];nxt[l+"0"]=v*(1-b);nxt[l+"1"]=v*b;
    }
    w.push(nxt);
  }
  ctx.clearRect(0,0,cv.width,cv.height);
  const yStep=250/Math.max(1,d);
  for(let i=0;i<=d;i++){
    const n=S.levels[i].length,step=640/n;
    for(let k=0;k<n;k++){
      const l=S.levels[i][k],x=40+(k+0.5)*step,y=34+i*yStep;
      if(i>0){
        const px=40+(Math.floor(k/2)+0.5)*(640/(n/2)),py=34+(i-1)*yStep;
        ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(px,py);ctx.stroke();
      }
      const r=Math.max(2.5,Math.min(16,Math.sqrt(w[i][l])*2.6));
      ctx.fillStyle='#00787a';ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.fill();
      if(n<=8){ctx.fillStyle='#52514e';ctx.font='11px system-ui';
        ctx.textAlign='center';ctx.fillText(w[i][l].toFixed(1),x,y-r-5);}
    }
    let tot=0;for(const l of S.levels[i])tot+=w[i][l];
    ctx.fillStyle='#008300';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText('stage '+i+' total  '+tot.toFixed(2),596,34+i*yStep+4);
  }
  biasv.textContent=b.toFixed(2);wdepthv.textContent=String(d);
  startv.textContent=String(top);
  const totals=[];
  for(let i=0;i<=d;i++){let t=0;for(const l of S.levels[i])t+=w[i][l];
    totals.push(t.toFixed(2));}
  const same=totals.every(t=>Math.abs(parseFloat(t)-top)<1e-6);
  const out=document.getElementById('out');
  out.textContent='totals, stage by stage   '+totals.join(', ')+'\n'+
    'boxes at the finest      '+S.levels[d].length+'\n'+
    (same?'every stage agrees: this is a legal weighting'
         :'the stages disagree, so this is not a weighting');
  out.className='readout '+(same?'verdict-ok':'verdict-no');
}
[bias,wd,st].forEach(s=>s.addEventListener('input',draw));draw();
""",
     "This is the free solid group of Definition 5.1, built the way the "
     "lectures build it: one copy of the whole numbers per box at each stage, "
     "fitting together down the levels."),

    (1, "The same sum, two sizes",
     "Adding one, then p, then p squared, and on. On the ordinary ruler the "
     "running totals fly apart. Under the base-p size they close in on a "
     "single point.",
     "Add terms and watch the two readings pull apart. The ordinary distance "
     "multiplies by p every step; the base-p distance divides by p every "
     "step. The value they close in on is a negative number, which is not a "
     "trick but what the sum genuinely equals under this size.",
     slider("base", "the base p", 2, 7, 1, 2) +
     slider("terms", "terms added", 1, 12, 1, 6),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const base=document.getElementById('base'),terms=document.getElementById('terms');
function draw(){
  const p=parseInt(base.value),n=parseInt(terms.value);
  const sums=geomPartialSums(p,n),lim=geomLimitTimes(p);
  ctx.clearRect(0,0,cv.width,cv.height);
  // ordinary reading: a log-scale ladder running away
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the ordinary size: the totals run away',40,30);
  const maxv=sums[sums.length-1];
  for(let k=0;k<n;k++){
    const frac=Math.log(sums[k]+1)/Math.log(maxv+1);
    const w=Math.max(3,frac*600);
    ctx.fillStyle='#d03b3b';ctx.fillRect(40,44+k*15,w,9);
    ctx.fillStyle='#52514e';ctx.font='11px system-ui';ctx.textAlign='left';
    ctx.fillText(String(sums[k]),46+w,52+k*15);
  }
  // base-p reading: nested boxes closing in
  const y0=250;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the base-'+p+' size: the totals close in',40,y0-16);
  let x=40,w=620;
  for(let k=0;k<n;k++){
    ctx.strokeStyle='#00787a';ctx.lineWidth=1.6;
    ctx.strokeRect(x,y0,w,120-k*0);
    ctx.fillStyle='rgba(0,120,122,'+(0.05+0.05*k)+')';
    ctx.fillRect(x,y0,w,120);
    const nw=w/p;x=x+ (k%2? (w-nw) : 0);w=nw;
  }
  ctx.fillStyle='#008300';ctx.beginPath();ctx.arc(x+w/2,y0+60,6,0,7);ctx.fill();
  ctx.fillStyle='#008300';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('the value the totals reach: '+lim.toFixed(4),x+w/2,y0+92);
  const ordDist=Math.abs(sums[n-1]-lim);
  const padic=Math.pow(p,-n);
  basev.textContent=String(p);termsv.textContent=String(n);
  document.getElementById('out').textContent=
    'terms added                '+n+'\n'+
    'last running total         '+sums[n-1]+'\n'+
    'ordinary distance to the value  '+ordDist.toFixed(1)+'\n'+
    'base-'+p+' distance to the value    '+padic.toExponential(3)+'\n'+
    'one climbs by a factor of '+p+', the other falls by a factor of '+p;
  document.getElementById('out').className='readout verdict-ok';
}
base.addEventListener('input',draw);terms.addEventListener('input',draw);draw();
""",
     "The running totals and both distances are computed live, and the "
     "Python library recomputes them in exact fractions. The value the sums "
     "reach is one over one minus the base, which for base two is minus one."),

    (2, "Read it at two levels",
     "A weighting on the halving probe, and a measurement to integrate "
     "against it. The same measurement can be read on coarse boxes or on "
     "fine ones.",
     "Change the level the measurement is read at. The picture gets finer "
     "and the total does not move. That is what makes a weighting an honest "
     "way to add up infinitely many things.",
     slider("readlvl", "level the measurement is read at", 1, 4, 1, 2) +
     slider("shape", "the measurement's shape", 0, 100, 1, 40),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const rl=document.getElementById('readlvl'),sh=document.getElementById('shape');
const DEPTH=5;
function draw(){
  const lvl=parseInt(rl.value),s=parseInt(sh.value)/100;
  const S=cantorProbe(DEPTH);
  const leaves={};
  for(const l of S.levels[DEPTH])leaves[l]=1;      // one unit per finest box
  const w=measureFromLeaves(S,leaves);
  // a measurement decided at `lvl`, then read at every finer level too
  const f={};
  S.levels[lvl].forEach((l,k)=>{
    f[l]=Math.round(1+9*Math.abs(Math.sin(3.1*s*(k+1))));
  });
  const totals=[];
  for(let j=lvl;j<=DEPTH;j++)
    totals.push(integrate(S,w,refineFn(S,f,lvl,j),j));
  ctx.clearRect(0,0,cv.width,cv.height);
  // the measurement, drawn at the read level and at the finest level
  function bars(y,level,fn,colour,caption){
    const n=S.levels[level].length,seg=640/n;
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText(caption,40,y-8);
    for(let k=0;k<n;k++){
      const v=fn[S.levels[level][k]],h=v*9;
      ctx.fillStyle=colour;
      ctx.fillRect(40+k*seg,y+100-h,Math.max(1,seg-1),h);
    }
  }
  bars(40,lvl,f,'#00787a','the measurement, read on '+S.levels[lvl].length+' boxes');
  bars(190,DEPTH,refineFn(S,f,lvl,DEPTH),'#4a3aa7',
       'the same measurement, read on '+S.levels[DEPTH].length+' boxes');
  ctx.fillStyle='#008300';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('total, level by level: '+totals.join('  =  '),40,346);
  readlvlv.textContent=String(lvl);shapev.textContent=s.toFixed(2);
  const same=totals.every(t=>t===totals[0]);
  const out=document.getElementById('out');
  out.textContent=
    'weight on each finest box   1\n'+
    'boxes at the finest level   '+S.levels[DEPTH].length+'\n'+
    'total, read at each level   '+totals.join(', ')+'\n'+
    (same?'the level you read at makes no difference'
         :'the readings disagree, which cannot happen for a weighting');
  out.className='readout '+(same?'verdict-ok':'verdict-no');
}
rl.addEventListener('input',draw);sh.addEventListener('input',draw);draw();
""",
     "The independence of the level is the property that makes integrating "
     "against a weighting well posed, and the tests recompute both readings "
     "in Python and compare them."),

    (3, "Take a measurement apart",
     "A whole-number measurement on the probe, and the switch functions it "
     "is built from. Each switch is one box on and everything else off.",
     "Add switches one at a time and watch the outline close on the "
     "measurement. The coefficients are whole numbers and never fractions, "
     "which is exactly the statement that the measurements form a free "
     "group.",
     slider("used", "switches used", 0, 16, 1, 0) +
     slider("target", "which measurement", 0, 100, 1, 35),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const used=document.getElementById('used'),tgt=document.getElementById('target');
const D=4;
function draw(){
  const k=parseInt(used.value),t=parseInt(tgt.value)/100;
  const S=cantorProbe(D),n=S.levels[D].length;
  const target=[];
  for(let i=0;i<n;i++)
    target.push(Math.round(2+5*Math.abs(Math.sin(2.3+7*t*(i+1)/n))));
  // the switches: one box each, taken in order, with whole coefficients
  const built=new Array(n).fill(0);
  for(let i=0;i<k&&i<n;i++)built[i]=target[i];
  ctx.clearRect(0,0,cv.width,cv.height);
  const seg=640/n,base=250;
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('the measurement you want (outline) and what the switches give',
               40,30);
  for(let i=0;i<n;i++){
    ctx.fillStyle=(i<k)?'#00787a':'rgba(0,120,122,0.16)';
    ctx.fillRect(40+i*seg,base-built[i]*26,seg-1.5,Math.max(0,built[i]*26));
    ctx.strokeStyle='#4a3aa7';ctx.lineWidth=1.8;
    ctx.strokeRect(40+i*seg,base-target[i]*26,seg-1.5,target[i]*26);
  }
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(40,base);ctx.lineTo(680,base);ctx.stroke();
  // the coefficients used
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('whole-number coefficients used so far',40,290);
  for(let i=0;i<k&&i<n;i++){
    ctx.fillStyle='#008300';ctx.font='12px ui-monospace,monospace';
    ctx.fillText(String(built[i]),40+i*seg+seg/2-4,312);
  }
  usedv.textContent=k+' of '+n;targetv.textContent=t.toFixed(2);
  const done=(k>=n);
  const out=document.getElementById('out');
  out.textContent=
    'boxes at this level      '+n+'\n'+
    'switches used            '+k+'\n'+
    'boxes still uncovered    '+Math.max(0,n-k)+'\n'+
    (done?'rebuilt exactly, with whole numbers and no fractions'
         :'keep adding switches');
  out.className='readout '+(done?'verdict-ok':'');
}
used.addEventListener('input',draw);tgt.addEventListener('input',draw);draw();
""",
     "That the switches always form a basis, for every probe including the "
     "infinite ones, is Nöbeling's theorem, given in the lectures with "
     "Bergman's proof. The construction is run in Python by the tests; at a "
     "finite level like this one the result is not surprising, and the "
     "theorem's content is the limit."),

    (4, "How far can a question reach",
     "An endless row of dials. A question adds up some of them and returns "
     "one whole number. The slider is how far the question is allowed to "
     "reach.",
     "Set a dial far out along the row, past the question's reach, and the "
     "answer does not move. Then ask why no question can reach all the way: "
     "the tail is divisible by every power of the base, so its answer would "
     "have to be too, and only zero is.",
     slider("reach", "how far the question reaches", 1, 20, 1, 6) +
     slider("poke", "which dial you set", 1, 20, 1, 12),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const reach=document.getElementById('reach'),poke=document.getElementById('poke');
function draw(){
  const R=parseInt(reach.value),P=parseInt(poke.value),N=20;
  ctx.clearRect(0,0,cv.width,cv.height);
  const x0=44,seg=630/N;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the dials: every one may be set, forever',20,30);
  for(let k=0;k<N;k++){
    const on=(k+1===P);
    const x=x0+k*seg;
    ctx.strokeStyle=(k<R)?'#2a78d6':'#c3c2b7';ctx.lineWidth=1.6;
    ctx.beginPath();ctx.arc(x+seg/2-2,72,11,0,7);ctx.stroke();
    if(on){ctx.fillStyle='#4a3aa7';
      ctx.beginPath();ctx.arc(x+seg/2-2,72,6,0,7);ctx.fill();}
  }
  ctx.fillStyle='#898781';ctx.font='11px system-ui';ctx.textAlign='center';
  ctx.fillText('...',x0+N*seg+8,76);
  // the reach window
  ctx.strokeStyle='#2a78d6';ctx.setLineDash([5,4]);ctx.lineWidth=1.6;
  ctx.strokeRect(x0-4,50,R*seg,46);ctx.setLineDash([]);
  ctx.fillStyle='#2a78d6';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('what the question can reach',x0-4,116);
  // the divisibility argument, drawn as a shrinking bar
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';
  ctx.fillText('why no question reaches the whole row',20,168);
  for(let k=0;k<8;k++){
    const w=560/Math.pow(2,k);
    ctx.fillStyle='rgba(74,58,167,'+(0.85-0.09*k)+')';
    ctx.fillRect(44,186+k*17,Math.max(2,w),10);
    ctx.fillStyle='#52514e';ctx.font='11px ui-monospace,monospace';
    ctx.textAlign='left';
    ctx.fillText('divisible by 2^'+(k+1),612,196+k*17);
  }
  ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('an answer divisible by every power must be zero',44,342);
  reachv.textContent=String(R);pokev.textContent='dial '+P;
  const seen=(P<=R);
  const out=document.getElementById('out');
  out.textContent=
    'the question reaches   dial 1 to '+R+'\n'+
    'you set                dial '+P+'\n'+
    'the answer             '+(seen?'moves':'does not move')+'\n'+
    (seen?'that dial is inside the reach'
         :'that dial is past the reach, so the question cannot see it');
  out.className='readout '+(seen?'':'verdict-ok');
}
reach.addEventListener('input',draw);poke.addEventListener('input',draw);draw();
""",
     "The reach of a question being finite is Specker's theorem of 1950, and "
     "it is what makes the weightings on a probe come out as a plain row of "
     "dials, which is Corollary 5.5 of the lectures."),

    (5, "Which groups obey the rule",
     "A group is solid when every placement of a probe's points into it "
     "extends, in exactly one way, so that weightings can be integrated. "
     "Pick a group and watch the test run.",
     "Try each in turn. The whole numbers pass, a row of dials passes, the "
     "base-p numbers pass. The ruler fails, and the reason is the one the "
     "next section is about.",
     picker("grp", "which group",
            [("Z", "whole numbers"), ("prod", "a row of dials"),
             ("Zp", "base-p numbers"), ("ser", "power series"),
             ("sum", "finitely many dials"), ("R", "the ruler")]),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let g='Z';
pick('grp',v=>{g=v;draw();});
const FACTS={
  "Z":[true,'the whole numbers',
       'a weighting has a finite total, so integrating lands back in it'],
  "prod":[true,'a row of dials',
       'integrate dial by dial: each one is the whole numbers again'],
  "Zp":[true,'the base-p numbers',
       'this is exactly the group the base-p probe was built to complete'],
  "ser":[true,'power series in one variable',
       'one dial per power, so it is a row of dials in disguise'],
  "sum":[false,'finitely many dials at a time',
       'a weighting can spread across infinitely many dials, and the total '+
       'then has infinitely many nonzero slots, which this group forbids'],
  "R":[false,'the ruler',
       'every real number can be divided by every whole number, and the '+
       'building blocks cannot receive anything divisible like that']
};
function draw(){
  const [ok,name,why]=FACTS[g];
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('a probe',60,34);
  const S=cantorProbe(3);
  drawTree(ctx,S,3,{x:40,y:44,w:250,h:140},{r:3.6});
  ctx.fillText('placed into '+name,380,34);
  ctx.strokeStyle=ok?'#008300':'#d03b3b';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(300,120);ctx.lineTo(370,120);ctx.stroke();
  ctx.beginPath();ctx.moveTo(370,120);ctx.lineTo(361,115);ctx.lineTo(361,125);
  ctx.closePath();ctx.fillStyle=ok?'#008300':'#d03b3b';ctx.fill();
  ctx.strokeStyle=ok?'#008300':'#d03b3b';ctx.lineWidth=2;
  ctx.strokeRect(390,52,290,136);
  ctx.fillStyle=ok?'#008300':'#d03b3b';ctx.font='14px system-ui';
  ctx.textAlign='center';
  ctx.fillText(ok?'the extension exists, and only one does'
                 :'no such extension',535,110);
  ctx.fillText(ok?'weightings can be integrated here':'the rule fails',535,134);
  // the two halves of the rule
  ctx.textAlign='left';ctx.font='13px system-ui';ctx.fillStyle='#52514e';
  ctx.fillText('what the rule asks for',60,240);
  const items=[['an extension exists',ok],['only one extension exists',ok]];
  items.forEach(([t,good],i)=>{
    ctx.fillStyle=good?'#008300':'#d03b3b';
    ctx.beginPath();ctx.arc(72,268+i*30,8,0,7);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText(good?'y':'n',72,272+i*30);
    ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
    ctx.fillText(t,90,272+i*30);
  });
  const out=document.getElementById('out');
  out.textContent=name+'\n'+(ok?'solid':'not solid')+'\n'+why;
  out.className='readout '+(ok?'verdict-ok':'verdict-no');
}
draw();
""",
     "The rule is Definition 5.1 of the lectures. That the solid groups form "
     "a self-contained setting with rows of dials as building blocks is "
     "Theorem 5.8 and Corollary 6.1, quoted here rather than computed."),

    (6, "Divide forever",
     "Take a number and divide it, by two, then three, then four, and on "
     "without end. Whether you stay inside the group is what decides the "
     "previous section's last row.",
     "Run the ruler and it never leaves. Run the whole numbers and it leaves "
     "at the first step. The consequence is at the bottom: a group that can "
     "always be divided has nothing to say to a dial, because the answer "
     "would have to be divisible by everything.",
     picker("dgrp", "which group",
            [("R", "the ruler"), ("Z", "whole numbers"),
             ("Zp", "base-p numbers")]) +
     slider("steps", "how many divisions", 1, 10, 1, 5),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const steps=document.getElementById('steps');
let g='R';
pick('dgrp',v=>{g=v;draw();});
function draw(){
  const n=parseInt(steps.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  let v=720,inside=true,firstOut=-1;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('start at 720, then divide by 2, 3, 4, ...',40,30);
  for(let k=0;k<n;k++){
    const d=k+2;const nv=v/d;
    let ok;
    if(g==='R')ok=true;
    else if(g==='Z')ok=Number.isInteger(nv);
    else ok=Number.isInteger(nv);      // the base-p numbers still need whole
    if(!ok&&inside){inside=false;firstOut=k;}
    const y=56+k*30;
    ctx.fillStyle=(ok&&inside)?'#008300':'#d03b3b';
    ctx.fillRect(40,y,Math.max(3,Math.min(600,Math.abs(nv)*0.9)),16);
    ctx.fillStyle='#52514e';ctx.font='12px ui-monospace,monospace';
    ctx.textAlign='left';
    ctx.fillText('÷ '+d+'  →  '+(Number.isInteger(nv)?nv:nv.toFixed(4)),
                 650,y+13);
    v=nv;
  }
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('so what can this group send to a single dial?',40,368);
  const divisible=(g==='R');
  ctx.fillStyle=divisible?'#d03b3b':'#008300';ctx.font='13px system-ui';
  ctx.fillText(divisible?'nothing but zero':'whatever you like',400,368);
  stepsv.textContent=String(n);
  const out=document.getElementById('out');
  out.textContent=
    (g==='R'?'the ruler':g==='Z'?'the whole numbers':'the base-p numbers')+'\n'+
    'divisions survived   '+(inside?n:firstOut)+' of '+n+'\n'+
    (divisible
      ? 'divisible by everything, so it maps to zero in every row of dials,\n'+
        'which is every building block the solid world is assembled from'
      : 'not divisible by everything, so it has room to map into dials');
  out.className='readout '+(divisible?'verdict-no':'verdict-ok');
}
steps.addEventListener('input',draw);draw();
""",
     "The divisibility shown here settles the building blocks: the ruler "
     "reaches none of them. Going from that to the full statement, "
     "that the solidified ruler is zero, is Corollary 6.1 (iii) of "
     "the lectures, and needs the computation of Theorem 4.3."),

    (7, "The multiplication table",
     "Two solid groups combined into one that handles pairs. Pick a row and "
     "a column, and read off what the combination is.",
     "Find the entry where the base-two numbers meet the base-three numbers. "
     "It is zero, and the two rulers beneath show why: the nestings shrink "
     "by different factors and never share a scale.",
     picker("ta", "first factor",
            [("Z_p", "base-p"), ("Z_l", "base-l"), ("Z[[T]]", "series in T"),
             ("Z[[U]]", "series in U"), ("R", "the ruler")]) +
     picker("tb", "second factor",
            [("Z_p", "base-p"), ("Z_l", "base-l"), ("Z[[T]]", "series in T"),
             ("Z[[U]]", "series in U"), ("R", "the ruler")], 1),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const NAMES=[["Z_p","base-p"],["Z_l","base-l"],["Z[[T]]","series in T"],
             ["Z[[U]]","series in U"],["R","the ruler"]];
function pretty(k){
  if(k==="0")return "nothing at all";
  if(k==="R")return "the ruler";
  if(k==="Z")return "whole numbers";
  const m=k.match(/^Z(?:_([pl]))?(?:\[\[(.+)\]\])?$/);
  if(!m)return k;
  const base=m[1]?("base-"+m[1]):"whole numbers";
  return m[2]?(base+" series in "+m[2].split(",").join(" and ")):base;
}
let A='Z_p',B='Z_l';
pick('ta',v=>{A=v;draw();});
pick('tb',v=>{B=v;draw();});
function draw(){
  ctx.clearRect(0,0,cv.width,cv.height);
  const x0=150,y0=54,cw=104,ch=34;
  ctx.font='12px system-ui';
  for(let j=0;j<NAMES.length;j++){
    ctx.fillStyle='#52514e';ctx.textAlign='center';
    ctx.fillText(NAMES[j][1],x0+j*cw+cw/2,y0-10);
  }
  for(let i=0;i<NAMES.length;i++){
    ctx.fillStyle='#52514e';ctx.textAlign='right';
    ctx.fillText(NAMES[i][1],x0-10,y0+i*ch+22);
    for(let j=0;j<NAMES.length;j++){
      const r=solidTensor(NAMES[i][0],NAMES[j][0]);
      const hit=(NAMES[i][0]===A&&NAMES[j][0]===B);
      ctx.fillStyle=hit?'#2a78d6':(r==='0'?'rgba(208,59,59,0.13)'
                                          :'rgba(0,120,122,0.13)');
      ctx.fillRect(x0+j*cw+2,y0+i*ch+2,cw-4,ch-4);
      ctx.fillStyle=hit?'#fff':(r==='0'?'#d03b3b':'#00787a');
      ctx.textAlign='center';ctx.font='12px ui-monospace,monospace';
      ctx.fillText(r==='0'?'0':r,x0+j*cw+cw/2,y0+i*ch+22);
      ctx.font='12px system-ui';
    }
  }
  // the two nestings, as rulers that never share a scale
  const res=solidTensor(A,B);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the nesting each side carries',40,262);
  function ruler(y,factor,colour,label){
    ctx.fillStyle=colour;ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText(label,40,y-6);
    let w=600;
    for(let k=0;k<6;k++){
      ctx.strokeStyle=colour;ctx.lineWidth=1.4;
      ctx.strokeRect(60,y,Math.max(3,w),16);
      w/=factor;
    }
  }
  const fa=(A==='Z_p')?2:(A==='Z_l')?3:(A==='R')?1:2;
  const fb=(B==='Z_p')?2:(B==='Z_l')?3:(B==='R')?1:2;
  ruler(288,fa,'#4a3aa7','first factor shrinks by '+(A==='R'?'nothing':fa));
  ruler(336,fb,'#8a5a2c','second factor shrinks by '+(B==='R'?'nothing':fb));
  const out=document.getElementById('out');
  out.textContent=
    pretty(A)+'  combined with  '+pretty(B)+'\n'+
    'gives  '+pretty(res)+
    (quotedTensor(A,B)?'   (stated in the lectures)':'   (the same rule, relabelled)')+'\n'+
    (res==='0'
      ? 'nothing survives: the two sides carry nestings that never agree'
      : 'the nestings are compatible, so both are kept');
  out.className='readout '+(res==='0'?'verdict-no':'verdict-ok');
}
draw();
""",
     "The grid is Example 6.4 of the lectures, transcribed. The one entry "
     "derived rather than quoted is the series row, which follows from index "
     "sets multiplying, Proposition 6.3, and the tests check that pairing."),

    (8, "Solidify a shape",
     "A shape, turned into a group the cheapest possible way and then made "
     "solid. What falls out is the shape's holes, in every degree, torsion "
     "and all.",
     "Turn the camera so the surface is genuinely three-dimensional, then "
     "switch shapes. The Klein bottle is the interesting one: it has a hole "
     "you have to go round twice to close, and the bars show it as a piece "
     "of order two.",
     picker("shp", "which shape",
            [("torus", "doughnut"), ("sphere", "sphere"), ("circle", "circle"),
             ("figure eight", "figure eight"),
             ("klein bottle", "klein bottle")]) +
     slider("spin", "turn the camera", 0, 360, 1, 35),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const spin=document.getElementById('spin');
let shape='torus';
pick('shp',v=>{shape=v;draw();});
function rot(p,a,b){
  let [x,y,z]=p;
  let x1=x*Math.cos(a)-z*Math.sin(a),z1=x*Math.sin(a)+z*Math.cos(a);
  let y1=y*Math.cos(b)-z1*Math.sin(b);z1=y*Math.sin(b)+z1*Math.cos(b);
  return [x1,y1,z1];
}
function proj(p,cx,cy,s){ return [cx+p[0]*s,cy+p[1]*s]; }
function draw(){
  const a=parseInt(spin.value)*Math.PI/180,b=0.52;
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=250,cy=170,s=64;
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
  if(shape==='torus'||shape==='klein bottle'){
    for(let i=0;i<24;i++){
      ctx.beginPath();
      for(let j=0;j<=36;j++){
        const u=i/24*2*Math.PI,v=j/36*2*Math.PI;
        const R=1.4,r=0.55;
        const p=rot([(R+r*Math.cos(v))*Math.cos(u),
                     (R+r*Math.cos(v))*Math.sin(u),r*Math.sin(v)],a,b);
        const q=proj(p,cx,cy,s);
        if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
    for(let j=0;j<14;j++){
      ctx.beginPath();
      for(let i=0;i<=48;i++){
        const u=i/48*2*Math.PI,v=j/14*2*Math.PI;
        const R=1.4,r=0.55;
        const p=rot([(R+r*Math.cos(v))*Math.cos(u),
                     (R+r*Math.cos(v))*Math.sin(u),r*Math.sin(v)],a,b);
        const q=proj(p,cx,cy,s);
        if(i===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
  }else if(shape==='sphere'){
    for(let i=0;i<18;i++){
      ctx.beginPath();
      for(let j=0;j<=36;j++){
        const th=i/18*Math.PI,ph=j/36*2*Math.PI;
        const p=rot([1.5*Math.sin(th)*Math.cos(ph),1.5*Math.sin(th)*Math.sin(ph),
                     1.5*Math.cos(th)],a,b);
        const q=proj(p,cx,cy,s);
        if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
  }else if(shape==='circle'){
    ctx.strokeStyle='#4a3aa7';ctx.lineWidth=3;ctx.beginPath();
    for(let j=0;j<=90;j++){
      const t=j/90*2*Math.PI;
      const p=rot([1.4*Math.cos(t),1.4*Math.sin(t),0],a,b);
      const q=proj(p,cx,cy,s);
      if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
    }
    ctx.stroke();
  }else{
    ctx.strokeStyle='#4a3aa7';ctx.lineWidth=3;
    for(const dx of [-0.8,0.8]){
      ctx.beginPath();
      for(let j=0;j<=90;j++){
        const t=j/90*2*Math.PI;
        const p=rot([dx+0.8*Math.cos(t),0.8*Math.sin(t),0],a,b);
        const q=proj(p,cx,cy,s);
        if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
  }
  if(shape==='klein bottle'){
    ctx.fillStyle='#8a5a2c';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('drawn as a doughnut: the gluing, not the picture,',cx,300);
    ctx.fillText('is what makes it a Klein bottle',cx,316);
  }
  // the holes that fall out
  const H=homology(shape);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the holes that fall out',450,44);
  H.forEach((h,k)=>{
    const y=70+k*54;
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText('degree '+k,450,y);
    for(let i=0;i<h.free;i++){
      ctx.fillStyle='#00787a';ctx.fillRect(450+i*30,y+8,24,20);
    }
    h.torsion.forEach((t,i)=>{
      ctx.fillStyle='#8a5a2c';
      ctx.fillRect(450+(h.free+i)*30,y+8,24,20);
      ctx.fillStyle='#fff';ctx.font='11px system-ui';ctx.textAlign='center';
      ctx.fillText('/'+t,462+(h.free+i)*30,y+23);
    });
    if(!h.free&&!h.torsion.length){
      ctx.fillStyle='#c3c2b7';ctx.font='12px system-ui';ctx.textAlign='left';
      ctx.fillText('none',450,y+23);
    }
  });
  spinv.textContent=spin.value+'°';
  const desc=H.map((h,k)=>'degree '+k+': '+h.free+
    (h.torsion.length?' plus order '+h.torsion.join(' and '):'')).join('\n');
  const out=document.getElementById('out');
  out.textContent=shape+'\n'+desc+'\n'+
    'computed from cell boundaries over the whole numbers';
  out.className='readout verdict-ok';
}
spin.addEventListener('input',draw);draw();
""",
     "The holes are computed here by Smith normal form over the whole "
     "numbers, so the Klein bottle's order-two piece is genuine and not "
     "rounded away. That solidification returns exactly these is Example 6.5 "
     "of the lectures, quoted."),
]


# --- part three: rings that know how to integrate --------------------------

PART_THREE_CHAPTERS = [
    (0, "Turn the exponent",
     "The measures of size at most one, drawn as a shape. The exponent "
     "decides the shape, and the shape decides whether the theory exists.",
     "Turn the exponent down through one and watch the ball cave inward. "
     "The chord drawn across it is the convexity test: above one it stays "
     "inside, below one it escapes. The merge reading underneath is the "
     "constraint that actually forces the answer.",
     slider("expo", "the exponent", 30, 250, 5, 100),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const expo=document.getElementById('expo');
function draw(){
  const p=parseInt(expo.value)/100;
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=210,cy=196,s=126;
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(cx-s-16,cy);ctx.lineTo(cx+s+16,cy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx,cy-s-16);ctx.lineTo(cx,cy+s+16);ctx.stroke();
  ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2.6;ctx.beginPath();
  for(let i=0;i<=720;i++){
    const t=i/720*2*Math.PI,q=lpBallPoint(t,p);
    const x=cx+q[0]*s,y=cy-q[1]*s;
    if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
  }
  ctx.closePath();ctx.stroke();
  // the convexity test: a chord between two points of the ball
  const A=lpBallPoint(Math.PI*0.18,p),B=lpBallPoint(Math.PI*0.82,p);
  const mid=[(A[0]+B[0])/2,(A[1]+B[1])/2];
  const midSize=lpSize(mid,p),convex=midSize<=1+1e-9;
  ctx.strokeStyle=convex?'#008300':'#d03b3b';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(cx+A[0]*s,cy-A[1]*s);
  ctx.lineTo(cx+B[0]*s,cy-B[1]*s);ctx.stroke();
  ctx.fillStyle=convex?'#008300':'#d03b3b';
  ctx.beginPath();ctx.arc(cx+mid[0]*s,cy-mid[1]*s,5,0,7);ctx.fill();
  ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText(convex?'the midpoint stays inside':'the midpoint escapes',
               cx,cy-s-28);
  // the merge reading
  const P=Plot(cv,0.3,2.5,0,3.2,{l:470,r:24,t:40,b:60});
  P.axes('the exponent','size after merging, over before');
  P.curve(x=>Math.min(3.2,worstMergeRatio(4,x)),'#00787a',2.2);
  P.hline(1,'#c3c2b7',[4,4]);
  P.vline(1,'#008300',[4,4]);
  P.dots([p],[Math.min(3.2,worstMergeRatio(4,p))],'#0b0b0b',5);
  P.label(0.34,3.0,'merging four equal boxes','#52514e');
  expov.textContent=p.toFixed(2);
  const ratio=worstMergeRatio(4,p);
  const allowed=(p<=1+1e-9);
  const out=document.getElementById('out');
  out.textContent=
    'the exponent               '+p.toFixed(2)+'\n'+
    'merging four equal boxes   size changes by '+ratio.toFixed(3)+'\n'+
    'the ball is                '+(convex?'convex':'not convex')+'\n'+
    (allowed?'allowed: merging never makes a measure bigger'
            :'forbidden: merging makes the measure bigger, so the stages '+
             'cannot fit together');
  out.className='readout '+(allowed?'verdict-ok':'verdict-no');
}
expo.addEventListener('input',draw);draw();
""",
     "The merge curve is the closed form: merging a number of equal boxes "
     "changes the size by that number raised to one minus the reciprocal of "
     "the exponent. The tests recompute both the curve and the convexity "
     "verdict in Python."),

    (1, "Assemble a rule",
     "A ring with a rule for sums needs three things. Switch each one on and "
     "off and watch which parts of the machinery survive.",
     "Turn off the requirement that each point counts as a unit weight, and "
     "the probe's points stop being able to enter at all. Turn off the "
     "splitting requirement and separate pieces stop being answered "
     "separately. Both are needed before anything can be integrated.",
     picker("ring", "the ring",
            [("Z", "whole numbers"), ("Zp", "base-p numbers"),
             ("A", "any plain ring")]) +
     slider("dirac", "each point counts as a unit weight", 0, 1, 1, 1) +
     slider("split", "separate pieces answered separately", 0, 1, 1, 1),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const dirac=document.getElementById('dirac'),split=document.getElementById('split');
let R='Z';
pick('ring',v=>{R=v;draw();});
const RN={"Z":"the whole numbers","Zp":"the base-p numbers",
          "A":"a plain ring with no topology"};
function draw(){
  const d=parseInt(dirac.value),s=parseInt(split.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the ring',60,32);
  ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2;ctx.strokeRect(46,44,180,52);
  ctx.fillStyle='#4a3aa7';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText(RN[R],136,75);
  ctx.fillStyle='#52514e';ctx.textAlign='left';ctx.font='13px system-ui';
  ctx.fillText('a probe',60,142);
  const S=cantorProbe(3);
  drawTree(ctx,S,3,{x:46,y:152,w:180,h:120},{r:3.4});
  // the arrow: the rule
  ctx.strokeStyle=(d&&s)?'#008300':'#d03b3b';ctx.lineWidth=2.4;
  ctx.beginPath();ctx.moveTo(250,166);ctx.lineTo(392,166);ctx.stroke();
  ctx.beginPath();ctx.moveTo(392,166);ctx.lineTo(382,161);ctx.lineTo(382,171);
  ctx.closePath();ctx.fillStyle=(d&&s)?'#008300':'#d03b3b';ctx.fill();
  ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('the rule',321,154);
  // the module of legal weightings
  ctx.strokeStyle=(d&&s)?'#00787a':'#c3c2b7';ctx.lineWidth=2;
  ctx.strokeRect(410,90,270,150);
  ctx.fillStyle=(d&&s)?'#00787a':'#c3c2b7';ctx.font='13px system-ui';
  ctx.fillText('the legal weightings on that probe',545,116);
  for(let k=0;k<8&&d&&s;k++){
    ctx.fillStyle='#00787a';
    ctx.fillRect(432+k*30,140,20,Math.max(6,14+9*Math.sin(k)));
  }
  if(!(d&&s)){
    ctx.fillStyle='#d03b3b';ctx.font='13px system-ui';ctx.textAlign='center';
    ctx.fillText('nothing to integrate against',545,180);
  }
  // the two switches, shown as their consequences
  const rows=[
    ['each point counts as a unit weight',d,
     'without it, no point of the probe can enter at all'],
    ['separate pieces answered separately',s,
     'without it, the pieces of a probe stop being independent']];
  rows.forEach(([t,on,why],i)=>{
    const y=290+i*40;
    ctx.fillStyle=on?'#008300':'#d03b3b';
    ctx.beginPath();ctx.arc(60,y,9,0,7);ctx.fill();
    ctx.fillStyle='#fff';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText(on?'y':'n',60,y+4);
    ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
    ctx.fillText(t,80,y+4);
    if(!on){ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';
      ctx.fillText(why,80,y+20);}
  });
  diracv.textContent=d?'on':'off';splitv.textContent=s?'on':'off';
  const out=document.getElementById('out');
  out.textContent='ring   '+RN[R]+'\n'+
    (d&&s?'both requirements met: a rule for sums is defined here'
         :'a requirement is missing, so there is no rule yet')+'\n'+
    'whether the rule then passes the further test is what makes it analytic';
  out.className='readout '+(d&&s?'verdict-ok':'verdict-no');
}
[dirac,split].forEach(x=>x.addEventListener('input',draw));draw();
""",
     "The two requirements are Definition 7.1 of the lectures: a functor to "
     "modules taking separate pieces to products, and the unit weights. "
     "Passing the further test is Definition 7.4, and which pairs pass is "
     "the content of the lecture."),

    (2, "What each rule lets you add",
     "Two rules that work, and one thing each of them can sum that ordinary "
     "algebra cannot.",
     "Push the term count up. The base-p rule swallows the doubling sum of "
     "part two. The solid rule over a plain ring swallows a sum spread "
     "across infinitely many dials. Neither has a finite answer in ordinary "
     "algebra.",
     picker("rule2", "which rule",
            [("padic", "the base-p rule"), ("solid", "the solid rule")]) +
     slider("nterm", "terms added", 1, 14, 1, 7),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const nt=document.getElementById('nterm');
let mode='padic';
pick('rule2',v=>{mode=v;draw();});
function draw(){
  const n=parseInt(nt.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  if(mode==='padic'){
    const sums=geomPartialSums(2,n),lim=geomLimitTimes(2);
    ctx.fillText('the base-p rule: adding 1, 2, 4, 8, and on',40,30);
    for(let k=0;k<n;k++){
      const gap=Math.pow(2,-(k+1));
      const w=Math.max(3,gap*600*8);
      ctx.fillStyle='#00787a';ctx.fillRect(40,52+k*20,Math.min(600,w),12);
      ctx.fillStyle='#52514e';ctx.font='11px ui-monospace,monospace';
      ctx.fillText('total '+sums[k]+'   still '+gap.toExponential(1)+
                   ' away',Math.min(610,w)+48,62+k*20);
    }
    ctx.fillStyle='#008300';ctx.font='13px system-ui';
    ctx.fillText('the gap halves every step, so the sum lands: '+lim,40,
                 68+n*20+16);
    document.getElementById('out').textContent=
      'terms added            '+n+'\n'+
      'ordinary answer        none, the totals run away\n'+
      'answer under this rule '+lim+'\n'+
      'the base-p rule is exactly what makes this sum legal';
  }else{
    ctx.fillText('the solid rule: a sum spread across every dial',40,30);
    const D=18;
    for(let k=0;k<D;k++){
      const on=(k<n);
      ctx.strokeStyle=on?'#2a78d6':'#c3c2b7';ctx.lineWidth=1.6;
      ctx.beginPath();ctx.arc(58+k*36,84,13,0,7);ctx.stroke();
      if(on){ctx.fillStyle='#4a3aa7';
        ctx.beginPath();ctx.arc(58+k*36,84,7,0,7);ctx.fill();}
    }
    ctx.fillStyle='#898781';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText('... and on, forever',58+D*36-18,88);
    ctx.fillStyle='#52514e';ctx.font='13px system-ui';
    ctx.fillText('with finitely many dials allowed, this leaves the group '+
                 'the moment',40,150);
    ctx.fillText('more than finitely many are set',40,170);
    ctx.fillStyle='#008300';
    ctx.fillText('with the solid rule, a weighting spreads across all of '+
                 'them and still',40,214);
    ctx.fillText('has exactly one total',40,234);
    for(let k=0;k<D;k++){
      ctx.fillStyle='#00787a';
      ctx.fillRect(48+k*36,270,22,Math.max(4,40/(1+k*0.5)));
    }
    document.getElementById('out').textContent=
      'dials set              '+n+' and rising\n'+
      'finitely many allowed  fails once the count passes any bound\n'+
      'the solid rule         accepts it, with exactly one total\n'+
      'this is why the rule is stated about modules, not about the ring';
  }
  document.getElementById('out').className='readout verdict-ok';
  
  ntermv.textContent=String(n);
}
nt.addEventListener('input',draw);draw();
""",
     "That both of these pass the test is Proposition 7.8 of the lectures. "
     "The second is the workhorse: the ring carries no topology, and all the "
     "topology lives in the modules."),

    (3, "Merge the boxes",
     "Weights in boxes, and the same weights after neighbouring boxes are "
     "merged. A weighting exists at every stage at once, so merging must "
     "never make it bigger.",
     "Set the exponent above one and merge: the size goes up, and the stages "
     "can no longer fit together. Bring the exponent to one or below and "
     "merging is safe. This one reading is what fixes the whole theory.",
     slider("expo2", "the exponent", 30, 250, 5, 200) +
     slider("group", "boxes merged into one", 2, 8, 1, 4) +
     slider("spread", "how uneven the weights are", 0, 100, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const e2=document.getElementById('expo2'),gp=document.getElementById('group');
const sp=document.getElementById('spread');
function draw(){
  const p=parseInt(e2.value)/100,g=parseInt(gp.value),u=parseInt(sp.value)/100;
  const vals=[];
  for(let k=0;k<g;k++)vals.push(1+u*Math.sin(2.1*k)*0.9);
  const groups=[[...Array(g).keys()]];
  const before=lpSize(vals,p),after=lpSize(mergeBoxes(vals,groups),p);
  ctx.clearRect(0,0,cv.width,cv.height);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the fine stage: '+g+' boxes',40,32);
  const w=520/g;
  for(let k=0;k<g;k++){
    ctx.fillStyle='#00787a';
    ctx.fillRect(40+k*w,120-vals[k]*46,w-4,vals[k]*46);
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
    ctx.strokeRect(40+k*w,44,w-4,76);
  }
  ctx.fillStyle='#00787a';ctx.font='12px system-ui';
  ctx.fillText('size '+before.toFixed(3),580,120);
  // the arrow down a level
  ctx.strokeStyle='#8a5a2c';ctx.lineWidth=2.2;
  ctx.beginPath();ctx.moveTo(300,140);ctx.lineTo(300,178);ctx.stroke();
  ctx.beginPath();ctx.moveTo(300,178);ctx.lineTo(295,169);ctx.lineTo(305,169);
  ctx.closePath();ctx.fillStyle='#8a5a2c';ctx.fill();
  ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('the boxes merge, the weights add',312,164);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';
  ctx.fillText('the coarse stage: one box',40,204);
  const total=vals.reduce((a,b)=>a+b,0);
  ctx.fillStyle='#4a3aa7';
  ctx.fillRect(40,300-total*46*0.55,516,total*46*0.55);
  ctx.strokeStyle='#c3c2b7';ctx.strokeRect(40,216,516,84);
  ctx.fillStyle='#4a3aa7';ctx.font='12px system-ui';
  ctx.fillText('size '+after.toFixed(3),580,300);
  const ratio=after/before,ok=ratio<=1+1e-9;
  ctx.fillStyle=ok?'#008300':'#d03b3b';ctx.font='14px system-ui';
  ctx.textAlign='left';
  ctx.fillText(ok?'the size did not grow: the stages fit together'
                 :'the size grew: these stages cannot be one weighting',40,344);
  expo2v.textContent=p.toFixed(2);groupv.textContent=String(g);
  spreadv.textContent=u.toFixed(2);
  const out=document.getElementById('out');
  out.textContent=
    'the exponent        '+p.toFixed(2)+'\n'+
    'size before merging '+before.toFixed(4)+'\n'+
    'size after merging  '+after.toFixed(4)+'\n'+
    'ratio               '+ratio.toFixed(4)+'\n'+
    (ok?'allowed' :'forbidden: this is why the exponent must not pass one');
  out.className='readout '+(ok?'verdict-ok':'verdict-no');
}
[e2,gp,sp].forEach(x=>x.addEventListener('input',draw));draw();
""",
     "With equal weights the ratio is the box count raised to one minus the "
     "reciprocal of the exponent, which the tests check in closed form. At "
     "or below exponent one, merging shrinks the size whatever the weights "
     "are. Above it, merging can grow the size, and equal weights are the "
     "case that grows most."),

    (4, "Slide out to the edge",
     "An endless line, and a function on it. Slide the viewpoint outward and "
     "watch which terms of the function still matter out there.",
     "Far out, the coordinate is huge and its reciprocal is tiny, so the "
     "natural terms to keep are the negative powers. The positive ones "
     "become the part you are allowed to throw away, and what is left is the "
     "tail.",
     slider("far", "how far out you stand", 0, 100, 1, 30) +
     slider("tails", "tails kept", 1, 8, 1, 4),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const far=document.getElementById('far'),tails=document.getElementById('tails');
function draw(){
  const f=parseInt(far.value)/100,m=parseInt(tails.value);
  const T=1+f*24;
  ctx.clearRect(0,0,cv.width,cv.height);
  // the line, with the viewpoint sliding out
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(40,72);ctx.lineTo(660,72);ctx.stroke();
  ctx.beginPath();ctx.moveTo(660,72);ctx.lineTo(648,66);ctx.lineTo(648,78);
  ctx.closePath();ctx.fillStyle='#8a5a2c';ctx.fill();
  ctx.fillStyle='#8a5a2c';ctx.font='12px system-ui';ctx.textAlign='right';
  ctx.fillText('the edge',644,60);
  const x=40+f*580;
  ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(x,72,8,0,7);ctx.fill();
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText('you are here, at '+T.toFixed(1),x,100);
  // the terms of a function, sized by how much they matter out there
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('how much each power matters where you stand',40,140);
  const powers=[];
  for(let e=2;e>=-m;e--)powers.push(e);
  const bw=600/powers.length;
  powers.forEach((e,i)=>{
    const size=Math.pow(T,e);
    const h=Math.max(2,Math.min(150,Math.log10(size+1e-12)*38+80));
    const keep=(e<0);
    ctx.fillStyle=keep?'#00787a':'rgba(208,59,59,0.55)';
    ctx.fillRect(44+i*bw,310-h,bw-5,h);
    ctx.fillStyle='#52514e';ctx.font='11px ui-monospace,monospace';
    ctx.textAlign='center';
    ctx.fillText((e>=0?'x^'+e:'1/x^'+(-e)),44+i*bw+bw/2-2,328);
  });
  ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('red: a polynomial part, thrown away in the quotient',44,352);
  ctx.fillStyle='#00787a';
  ctx.fillText('teal: the tails, which are what survives',420,352);
  farv.textContent=T.toFixed(1);tailsv.textContent=String(m);
  const out=document.getElementById('out');
  out.textContent=
    'standing at            '+T.toFixed(1)+'\n'+
    'tails kept             '+m+'\n'+
    'surviving pieces       '+lineEdgeRank(2,m)+'\n'+
    'the count is the number of tails, whatever the polynomial part reaches to';
  out.className='readout verdict-ok';
}
far.addEventListener('input',draw);tails.addEventListener('input',draw);draw();
""",
     "The count is computed by truncation and does not depend on how far up "
     "the polynomial part is allowed to reach, which is the point: only the "
     "tails survive."),

    (5, "Form the quotient",
     "Functions near the edge, functions everywhere, and what is left when "
     "you divide one by the other. The line has one edge; the coordinate "
     "cross has two.",
     "Compare the two shapes at the same depth. The line keeps exactly its "
     "tails. The cross keeps both branches' tails and one extra piece, and "
     "that extra piece is the crossing point showing up in the arithmetic.",
     picker("geom", "which shape", [("line", "the line"), ("cross", "the cross")]) +
     slider("tails2", "tails kept", 1, 8, 1, 4) +
     slider("top2", "how far the polynomials reach", 1, 8, 1, 3),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const t2=document.getElementById('tails2'),tp=document.getElementById('top2');
let shape='line';
pick('geom',v=>{shape=v;draw();});
function bar(y,n,colour,label){
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText(label,40,y-6);
  for(let k=0;k<n;k++){
    ctx.fillStyle=colour;ctx.fillRect(40+k*26,y,22,22);
  }
  ctx.fillStyle='#52514e';ctx.font='12px ui-monospace,monospace';
  ctx.fillText(String(n),48+n*26,y+16);
}
function draw(){
  const m=parseInt(t2.value),top=parseInt(tp.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  // the shape itself
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2.4;
  if(shape==='line'){
    ctx.beginPath();ctx.moveTo(420,58);ctx.lineTo(680,58);ctx.stroke();
    ctx.fillStyle='#8a5a2c';ctx.beginPath();ctx.arc(680,58,6,0,7);ctx.fill();
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('one edge',680,80);
  }else{
    ctx.beginPath();ctx.moveTo(430,58);ctx.lineTo(680,58);ctx.stroke();
    ctx.beginPath();ctx.moveTo(555,10);ctx.lineTo(555,106);ctx.stroke();
    ctx.fillStyle='#8a5a2c';
    ctx.beginPath();ctx.arc(680,58,6,0,7);ctx.fill();
    ctx.beginPath();ctx.arc(555,10,6,0,7);ctx.fill();
    ctx.fillStyle='#2a78d6';ctx.beginPath();ctx.arc(555,58,6,0,7);ctx.fill();
    ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='left';
    ctx.fillText('the crossing point',566,74);
  }
  const nearEdge=(shape==='line')?(top+m+1):2*(top+m+1);
  const everywhere=(shape==='line')?(top+1):(2*(top+1)-1);
  const left=(shape==='line')?lineEdgeRank(top,m):crossEdgeRank(top,m);
  bar(150,nearEdge,'#4a3aa7','pieces of a function near the edge');
  bar(224,everywhere,'#c3c2b7','pieces of a function everywhere');
  bar(298,left,'#00787a','what is left over');
  tails2v.textContent=String(m);top2v.textContent=String(top);
  const expected=(shape==='line')?m:(2*m+1);
  const out=document.getElementById('out');
  out.textContent=
    (shape==='line'?'the line':'the coordinate cross')+'\n'+
    'near the edge   '+nearEdge+'\n'+
    'everywhere      '+everywhere+'\n'+
    'left over       '+left+
    (shape==='line'?'   (exactly the tails)'
                   :'   (both branches\' tails, plus one)')+'\n'+
    (left===expected?'stable: pushing the polynomials further out does not move it'
                    :'unexpected count');
  out.className='readout '+(left===expected?'verdict-ok':'verdict-no');
}
[t2,tp].forEach(x=>x.addEventListener('input',draw));draw();
""",
     "This is the counting side of the formula Remark 8.5 of the lectures "
     "computes for the cross. The extra piece is the crossing point: the two "
     "branches share one value there, so one constant is not free."),

    (6, "Choose what counts as small",
     "A ring's valuations, and the region cut out by deciding which "
     "functions have size at most one. Every such decision is a region, and "
     "every region is such a decision.",
     "Switch each function in and out. Each one you declare small cuts the "
     "region down. The correspondence runs exactly both ways, which is what "
     "lets a space be described by patches at all.",
     slider("g1", "declare the coordinate small", 0, 1, 1, 1) +
     slider("g2", "declare its reciprocal small", 0, 1, 1, 0) +
     slider("g3", "declare a prime small", 0, 1, 1, 0),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const G=[document.getElementById('g1'),document.getElementById('g2'),
         document.getElementById('g3')];
function draw(){
  const a=parseInt(G[0].value),b=parseInt(G[1].value),c=parseInt(G[2].value);
  ctx.clearRect(0,0,cv.width,cv.height);
  const x0=70,y0=54,W=560,H=240;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('every consistent way of measuring how big each function is',
               x0,36);
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1.4;ctx.strokeRect(x0,y0,W,H);
  // the region left after each declaration
  let lo=0,hi=1,bot=0,topf=1;
  if(a){hi=Math.min(hi,0.62);}          // the coordinate small: cuts the right
  if(b){lo=Math.max(lo,0.38);}          // its reciprocal small: cuts the left
  if(c){topf=Math.min(topf,0.55);}      // a prime small: cuts the top
  if(hi>lo&&topf>bot){
    ctx.fillStyle='rgba(0,131,0,0.18)';
    ctx.fillRect(x0+lo*W,y0+(1-topf)*H,(hi-lo)*W,(topf-bot)*H);
    ctx.strokeStyle='#008300';ctx.lineWidth=2;
    ctx.strokeRect(x0+lo*W,y0+(1-topf)*H,(hi-lo)*W,(topf-bot)*H);
  }
  // scattered valuation points, lit when inside
  let inside=0,total=0;
  for(let i=0;i<26;i++)for(let j=0;j<11;j++){
    const fx=(i+0.5)/26,fy=(j+0.5)/11;
    const px=x0+fx*W,py=y0+(1-fy)*H;
    const ok=(fx>=lo&&fx<=hi&&fy>=bot&&fy<=topf);
    total++;if(ok)inside++;
    ctx.fillStyle=ok?'#008300':'#c3c2b7';
    ctx.beginPath();ctx.arc(px,py,2.6,0,7);ctx.fill();
  }
  const labels=[[a,'the coordinate'],[b,'its reciprocal'],[c,'a prime']];
  ctx.font='12px system-ui';ctx.textAlign='left';
  labels.forEach(([on,t],i)=>{
    ctx.fillStyle=on?'#008300':'#c3c2b7';
    ctx.beginPath();ctx.arc(x0+i*190,y0+H+34,7,0,7);ctx.fill();
    ctx.fillStyle='#52514e';
    ctx.fillText(t+(on?' is small':' is free'),x0+i*190+14,y0+H+38);
  });
  G.forEach((s,i)=>{document.getElementById(s.id+'v').textContent=
    parseInt(s.value)?'small':'free';});
  const empty=!(hi>lo&&topf>bot);
  const out=document.getElementById('out');
  out.textContent=
    'declarations made   '+[a,b,c].reduce((x,y)=>x+y,0)+'\n'+
    'valuations left in  '+inside+' of '+total+'\n'+
    (empty?'nothing left: these declarations are incompatible'
          :'each declaration cuts the region down, and the region determines '+
           'the declarations back');
  out.className='readout '+(empty?'verdict-no':'verdict-ok');
}
G.forEach(s=>s.addEventListener('input',draw));draw();
""",
     "The exact two-way correspondence between the subring you declare small "
     "and the region it cuts out is Proposition 9.2 of the lectures. The "
     "picture here is schematic: the axes stand for two independent ways a "
     "valuation can vary, not for particular coordinates."),

    (7, "Move a sheaf",
     "Six operations, in three pairs. Pick one and watch where a sheaf on "
     "one space ends up on the other.",
     "Try pushing forward with compact support on a map where something "
     "escapes to the edge, and again on one where nothing does. When nothing "
     "escapes, it is the same as ordinary pushforward. That coincidence is "
     "what pins the whole formalism down.",
     picker("op", "which operation",
            [("pull", "pull back"), ("push", "push forward"),
             ("shriek", "push with compact support"),
             ("upper", "the counterweight")]) +
     slider("proper", "does anything escape to the edge", 0, 1, 1, 1),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const pr=document.getElementById('proper');
let op='pull';
pick('op',v=>{op=v;draw();});
const INFO={
  pull:['pull back','drag a sheaf backwards along the map','easy'],
  push:['push forward','send a sheaf forwards, keeping everything','easy'],
  shriek:['push with compact support','send forwards, discarding what runs '+
          'off the edge','the hard one'],
  upper:['the counterweight','the exact partner of the compactly supported '+
         'pushforward','defined by being the partner']
};
function draw(){
  const escapes=parseInt(pr.value)===1;
  ctx.clearRect(0,0,cv.width,cv.height);
  const [name,what,hard]=INFO[op];
  // two spaces and the map between them
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText('the space above',180,34);ctx.fillText('the space below',540,34);
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=2;
  ctx.strokeRect(70,50,220,120);ctx.strokeRect(430,50,220,120);
  // the sheaf, drawn as a cloud of sections
  const src=(op==='pull'||op==='upper')?1:0;      // 0 above, 1 below
  const dst=1-src;
  const boxes=[[70,50],[430,50]];
  for(let k=0;k<12;k++){
    const bx=boxes[src][0]+22+ (k%4)*52,by=boxes[src][1]+26+Math.floor(k/4)*34;
    ctx.fillStyle='#4a3aa7';ctx.fillRect(bx,by,30,18);
  }
  const lost=(op==='shriek'&&escapes)?4:0;
  for(let k=0;k<12-lost;k++){
    const bx=boxes[dst][0]+22+(k%4)*52,by=boxes[dst][1]+26+Math.floor(k/4)*34;
    ctx.fillStyle='#00787a';ctx.fillRect(bx,by,30,18);
  }
  if(lost){
    ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText(lost+' sections ran off the edge and were discarded',540,196);
  }
  // the arrow
  const ax=src===0?300:420,bx2=src===0?420:300;
  ctx.strokeStyle='#008300';ctx.lineWidth=2.6;
  ctx.beginPath();ctx.moveTo(ax,110);ctx.lineTo(bx2,110);ctx.stroke();
  ctx.beginPath();ctx.moveTo(bx2,110);
  ctx.lineTo(bx2+(src===0?-10:10),105);ctx.lineTo(bx2+(src===0?-10:10),115);
  ctx.closePath();ctx.fillStyle='#008300';ctx.fill();
  ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText(name,360,96);
  // the two rules that force the definition
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('the two rules that force the compactly supported one',60,240);
  const rules=[
    ['nothing escapes to the edge',
     'compactly supported pushforward is ordinary pushforward',!escapes],
    ['the map is an open inclusion',
     'the counterweight is just the pullback',true]];
  rules.forEach(([a,b,on],i)=>{
    const y=270+i*36;
    ctx.fillStyle=on?'#008300':'#c3c2b7';
    ctx.beginPath();ctx.arc(72,y,8,0,7);ctx.fill();
    ctx.fillStyle='#52514e';ctx.font='12.5px system-ui';
    ctx.fillText('if '+a+', then '+b,90,y+4);
  });
  properv.textContent=escapes?'yes':'no';
  const out=document.getElementById('out');
  out.textContent=name+'\n'+what+'\n'+
    (op==='shriek'
      ? (escapes?'sections that run off the edge are discarded here'
                :'nothing escapes, so this is exactly ordinary pushforward')
      : 'this one is among the four that are easy to build');
  out.className='readout '+(op==='shriek'&&escapes?'':'verdict-ok');
}
pr.addEventListener('input',draw);draw();
""",
     "The two rules really do force the compactly supported pushforward "
     "everywhere, by factoring any reasonable map into an open inclusion "
     "followed by a proper one. The lectures note that the work is then in "
     "checking the answer does not depend on the factoring."),

    (8, "Pair, and trace",
     "Duality is a perfect pairing: a class in one degree, a partner in the "
     "complementary degree, and a single number out. Change the shape and "
     "the two sides move together.",
     "Turn the camera so the surface is genuinely three-dimensional, then "
     "change the number of holes. The two columns always match, which is "
     "what perfect means, and the trace is the one canonical way of "
     "collapsing the pairing to a number.",
     slider("genus", "how many holes the surface has", 1, 4, 1, 2) +
     slider("spin3", "turn the camera", 0, 360, 1, 40),
     r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const gs=document.getElementById('genus'),sp3=document.getElementById('spin3');
function rot(p,a,b){
  let [x,y,z]=p;
  let x1=x*Math.cos(a)-z*Math.sin(a),z1=x*Math.sin(a)+z*Math.cos(a);
  let y1=y*Math.cos(b)-z1*Math.sin(b);z1=y*Math.sin(b)+z1*Math.cos(b);
  return [x1,y1,z1];
}
function draw(){
  const g=parseInt(gs.value),a=parseInt(sp3.value)*Math.PI/180,b=0.5;
  ctx.clearRect(0,0,cv.width,cv.height);
  // g doughnuts in a row, turned together
  const cx=230,cy=170,s=30;
  ctx.strokeStyle='#c3c2b7';ctx.lineWidth=0.9;
  for(let h=0;h<g;h++){
    const off=(h-(g-1)/2)*3.1;
    for(let i=0;i<18;i++){
      ctx.beginPath();
      for(let j=0;j<=28;j++){
        const u=i/18*2*Math.PI,v=j/28*2*Math.PI;
        const R=1.3,r=0.5;
        const p=rot([off+(R+r*Math.cos(v))*Math.cos(u),
                     (R+r*Math.cos(v))*Math.sin(u),r*Math.sin(v)],a,b);
        const q=[cx+p[0]*s,cy+p[1]*s];
        if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
  }
  ctx.fillStyle='#52514e';ctx.font='12px system-ui';ctx.textAlign='center';
  ctx.fillText(g+(g===1?' hole':' holes'),cx,300);
  // the two columns of the pairing
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('one side',430,44);ctx.fillText('its partner',560,44);
  for(let k=0;k<g;k++){
    ctx.fillStyle='#4a3aa7';ctx.fillRect(430,58+k*30,72,22);
    ctx.fillStyle='#00787a';ctx.fillRect(560,58+k*30,72,22);
    ctx.strokeStyle='#008300';ctx.lineWidth=1.4;
    ctx.beginPath();ctx.moveTo(506,69+k*30);ctx.lineTo(556,69+k*30);ctx.stroke();
  }
  const y=58+g*30+30;
  ctx.strokeStyle='#008300';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(466,y-16);ctx.lineTo(531,y+6);ctx.stroke();
  ctx.beginPath();ctx.moveTo(596,y-16);ctx.lineTo(531,y+6);ctx.stroke();
  ctx.fillStyle='#008300';ctx.font='13px system-ui';ctx.textAlign='center';
  ctx.fillText('the trace',531,y+26);
  ctx.strokeStyle='#008300';ctx.lineWidth=2;ctx.strokeRect(496,y+34,70,28);
  ctx.fillStyle='#008300';ctx.fillText('one number',531,y+52);
  genusv.textContent=String(g);spin3v.textContent=sp3.value+'°';
  const out=document.getElementById('out');
  out.textContent=
    'holes in the surface        '+g+'\n'+
    'classes on one side         '+g+'\n'+
    'classes on the partner side '+g+'\n'+
    'the two sides match for every shape, which is what perfect means\n'+
    'the trace turns the top-degree classes into a single number';
  out.className='readout verdict-ok';
}
[gs,sp3].forEach(x=>x.addEventListener('input',draw));draw();
""",
     "The matching dimensions shown here are the classical statement of "
     "Serre duality on a curve. What the lectures add is that the dualizing "
     "object is not constructed but defined as the counterweight, so the "
     "duality is an adjointness rather than a theorem to be proved."),
]

CHAPTERS = {
    "condensed-math01": PART_ONE_CHAPTERS,
    "condensed-math02": PART_TWO_CHAPTERS,
    "condensed-math03": PART_THREE_CHAPTERS,
}


def build() -> None:
    total = 0
    for part in PARTS:
        chapters = CHAPTERS[part.slug]
        out = DOCS / part.slug / "play"
        out.mkdir(parents=True, exist_ok=True)
        for i, (num, heading, lede, try_, controls, widget, note) in \
                enumerate(chapters):
            nav = []
            if i > 0:
                nav.append(f'<a href="{chapters[i-1][0]:02d}.html">← previous</a>')
            nav.append('<a href="index.html">all of them</a>')
            if i + 1 < len(chapters):
                nav.append(f'<a href="{chapters[i+1][0]:02d}.html">next →</a>')
            page = (SHELL
                    .replace("TITLE", f"{heading} · condensed mathematics, "
                                      f"part {part.number}")
                    .replace("HEADING", f"{num} · {heading}")
                    .replace("LEDE", lede)
                    .replace("TRY", try_)
                    .replace("CONTROLS", controls)
                    .replace("NOTE", note)
                    .replace("NAV", "  ·  ".join(nav))
                    .replace("MATHS", MATHS)
                    .replace("WIDGET", widget))
            (out / f"{num:02d}.html").write_text(page)
        total += len(chapters)

        rows = "\n".join(
            f'<li><a href="{num:02d}.html">{num} · {heading}</a>'
            f"<span>{lede}</span></li>"
            for num, heading, lede, *_ in chapters)
        index = (SHELL
                 .replace("TITLE", f"Play with it · condensed mathematics, "
                                   f"part {part.number}")
                 .replace("HEADING", f"Play with part {part.number}")
                 .replace("LEDE", "One page per chapter. Every claim in the "
                                  "article is a control on one of these.")
                 .replace('<p class="try"><strong>Try this.</strong> TRY</p>', "")
                 .replace('<canvas id="c" width="720" height="400"></canvas>', "")
                 .replace('<div class="controls">CONTROLS</div>',
                          f'<ul class="list">{rows}</ul>')
                 .replace('<div class="readout" id="out"></div>', "")
                 .replace("NOTE", "Each page is self contained: no libraries "
                                  "and no network, so they work offline and "
                                  "from a file.")
                 .replace("NAV", '<a href="../index.html">back to the article</a>')
                 .replace("MATHS", "").replace("WIDGET", "")
                 .replace("</style>",
                          ".list{list-style:none;padding:0;margin:0}"
                          ".list li{padding:12px 0;border-bottom:1px solid var(--line)}"
                          ".list a{display:block;color:var(--blue);"
                          "text-decoration:none;font-size:16px}"
                          ".list span{display:block;color:var(--muted);"
                          "font-size:13.5px;margin-top:2px}</style>"))
        (out / "index.html").write_text(index)
        print(f"  {part.slug}: {len(chapters)} playable pages plus an index")
    print(f"wrote {total} playable pages under {DOCS}")


if __name__ == "__main__":
    build()
