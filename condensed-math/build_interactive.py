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
  if(grains<=1){
    // fully zoomed: exactly one grain stands alone in the window
    ctx.fillStyle='#d03b3b';
    ctx.beginPath();ctx.arc(cx,196,5,0,7);ctx.fill();
  }else for(let k=0;k<=grains;k++){
    const x=x0+(x1-x0)*k/grains;
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
     picker("rule", "rule", [("cut", "cut"), ("glue", "glue")]) +
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
    ctx.fillText('the construction stops',390,250);
  }
  arrow(470,150,580,'recover the topology',bad);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';
  ctx.fillText('the recovered space',650,50);shape(650,150,1,bad);
  const out=document.getElementById('out');
  out.textContent=bad
    ? 'a point of this space is not closed\n'+
      'A space with a nonclosed point does not define the required condensed set.\n'+
      'Warning 2.14 identifies this exact failure.'
    : 'The recovered topology is the original topology.\n'+
      'The translation also preserves all continuous maps.';
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
     picker("holes", "which shape", [("ring", "circle"), ("torus", "torus")]) +
     slider("turns", "turns the path makes", -3, 3, 1, 2) +
     slider("turns2", "turns the second way, for the doughnut", -3, 3, 1, 1) +
     slider("wob2", "wobble applied to the path", 0, 100, 1, 0),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const T1=document.getElementById('turns'),T2=document.getElementById('turns2');
const WB=document.getElementById('wob2');
let mode='ring';
pick('holes',v=>{mode=v;draw();});
// the running angle, unwrapped: how the turn counter reads any closed path
function windingCount(f){
  let total=0;
  for(let i=1;i<=600;i++){
    const a=f(i/600*2*Math.PI),b=f((i-1)/600*2*Math.PI);
    let d=a-b;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;
    total+=d;
  }
  return Math.round(total/(2*Math.PI));
}
function draw(){
  const n1=parseInt(T1.value),n2=parseInt(T2.value),w=parseInt(WB.value)/100;
  ctx.clearRect(0,0,cv.width,cv.height);
  const cx=360,cy=190;
  if(mode==='ring'){
    // a zero-turn path still has to be a visible closed loop, so it gets a
    // small non-winding circle to live on
    const ang=t=>n1*t+(n1===0?0.35*Math.sin(t):0)+w*1.9*Math.sin(5*t);
    const rad=t=>120+(n1===0?20*Math.cos(t):0)+w*26*Math.sin(7*t);
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=26;
    ctx.beginPath();ctx.arc(cx,cy,120,0,7);ctx.stroke();
    ctx.strokeStyle='#2a78d6';ctx.lineWidth=2.6;ctx.beginPath();
    const N=1400;
    for(let i=0;i<=N;i++){
      const t=i/N*2*Math.PI;
      const x=cx+rad(t)*Math.cos(ang(t)),y=cy+rad(t)*Math.sin(ang(t));
      if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
    }
    ctx.stroke();
    const count=windingCount(ang);
    document.getElementById('out').textContent=
      'turns you asked for   '+n1+'\n'+
      'turns measured        '+count+'\n'+
      'deformation           '+w.toFixed(2)+'\n'+
      (n1===0?'A zero-winding loop still has winding number zero after deformation.'
             :'The winding number is an integer and deformation does not change it.');
    document.getElementById('out').className='readout '+
      (count===n1?'verdict-ok':'verdict-no');
  }else{
    // a doughnut seen at an angle, with the chosen path drawn on it
    const R=132,r=48,tilt=0.42;
    const P=(u,v)=>[cx+(R+r*Math.cos(v))*Math.cos(u),
                    cy+((R+r*Math.cos(v))*Math.sin(u))*tilt
                      +r*Math.sin(v)*0.86];
    ctx.strokeStyle='#c3c2b7';ctx.lineWidth=1;
    for(let k=0;k<28;k++){
      const u=k/28*2*Math.PI;
      ctx.beginPath();
      for(let j=0;j<=40;j++){
        const q=P(u,j/40*2*Math.PI);
        if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
      }
      ctx.stroke();
    }
    // the two reference loops, drawn thin: the axes the counts are read on
    ctx.strokeStyle='rgba(42,120,214,0.55)';ctx.lineWidth=1.6;ctx.beginPath();
    for(let j=0;j<=200;j++){const q=P(j/200*2*Math.PI,0);
      if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);}
    ctx.stroke();
    ctx.strokeStyle='rgba(0,131,0,0.55)';ctx.lineWidth=1.6;ctx.beginPath();
    for(let j=0;j<=200;j++){const q=P(0,j/200*2*Math.PI);
      if(j===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);}
    ctx.stroke();
    // the path itself: n1 turns the long way, n2 through the hole, wobbled;
    // with both counts zero it becomes a small loop that goes nowhere
    const still=(n1===0&&n2===0);
    const U=t=>n1*t+(still?0.45*Math.sin(t):0)+w*1.1*Math.sin(3*t);
    const V=t=>n2*t+(still?0.45*Math.cos(t):0)+w*1.6*Math.sin(2*t+1);
    ctx.strokeStyle='#4a3aa7';ctx.lineWidth=2.8;ctx.beginPath();
    for(let i=0;i<=1600;i++){
      const t=i/1600*2*Math.PI,q=P(U(t),V(t));
      if(i===0)ctx.moveTo(q[0],q[1]);else ctx.lineTo(q[0],q[1]);
    }
    ctx.stroke();
    ctx.fillStyle='#2a78d6';ctx.font='12px system-ui';ctx.textAlign='center';
    ctx.fillText('the long way round',cx,cy-124);
    ctx.fillStyle='#008300';
    ctx.fillText('through the hole',cx+R+r+2,cy+r+34);
    const m1=windingCount(U),m2=windingCount(V);
    const ranks=exteriorRanks(2);
    document.getElementById('out').textContent=
      'turns the long way     asked '+n1+', measured '+m1+'\n'+
      'turns through the hole  asked '+n2+', measured '+m2+'\n'+
      'hole counts by degree  '+ranks.join(', ')+'\n'+
      (still?'a loop that goes nowhere counts zero both ways'
            :'two independent counts, and the wobble moves neither');
    document.getElementById('out').className='readout '+
      (m1===n1&&m2===n2?'verdict-ok':'verdict-no');
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
  // p-adic reading: nested boxes closing in
  const y0=250;
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText(p+'-adic distance: the totals approach a limit',40,y0-16);
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
  ctx.fillText('p-adic limit: '+lim.toFixed(4),x+w/2,y0+92);
  const ordDist=Math.abs(sums[n-1]-lim);
  const padic=Math.pow(p,-n);
  basev.textContent=String(p);termsv.textContent=String(n);
  document.getElementById('out').textContent=
    'terms added                '+n+'\n'+
    'last running total         '+sums[n-1]+'\n'+
    'ordinary distance to the value  '+ordDist.toFixed(1)+'\n'+
    p+'-adic distance to the limit    '+padic.toExponential(3)+'\n'+
    'The ordinary error grows by a factor of '+p+
    ', while the p-adic error shrinks by a factor of '+p+'.';
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
  ctx.fillText('coordinates read by the homomorphism',x0-4,116);
  // the divisibility argument, drawn as a shrinking bar
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';
  ctx.fillText('why the map cannot read infinitely many coordinates',20,168);
  for(let k=0;k<8;k++){
    const w=560/Math.pow(2,k);
    ctx.fillStyle='rgba(74,58,167,'+(0.85-0.09*k)+')';
    ctx.fillRect(44,186+k*17,Math.max(2,w),10);
    ctx.fillStyle='#52514e';ctx.font='11px ui-monospace,monospace';
    ctx.textAlign='left';
    ctx.fillText('divisible by 2^'+(k+1),612,196+k*17);
  }
  ctx.fillStyle='#d03b3b';ctx.font='12px system-ui';ctx.textAlign='left';
  ctx.fillText('An integer divisible by every power of two must be zero.',44,342);
  reachv.textContent=String(R);pokev.textContent='coordinate '+P;
  const seen=(P<=R);
  const out=document.getElementById('out');
  out.textContent=
    'the homomorphism reads   coordinate 1 to '+R+'\n'+
    'you change              coordinate '+P+'\n'+
    'the output              '+(seen?'moves':'does not move')+'\n'+
    (seen?'That coordinate is inside the finite range, so it changes the output.'
         :'That coordinate is outside the finite range, so it cannot change the output.');
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
             ("sum", "a direct sum of integer groups"), ("R", "the ruler")]),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
let g='Z';
pick('grp',v=>{g=v;draw();});
const FACTS={
  "Z":[true,'the integers',
       'A finite integer weighting integrates to another integer.'],
  "prod":[true,'a product of integer groups',
       'Integration is performed in each integer coordinate.'],
  "Zp":[true,'the p-adic integers',
       'The p-adic completion supports the corresponding compatible sums.'],
  "ser":[true,'power series in one variable',
       'One coefficient for each power makes this an integer product.'],
  "sum":[false,'a direct sum allows only finite support',
       'A compatible weighting may use infinitely many coordinates, so the result '+
       'may have infinite support, which a direct sum does not allow.'],
  "R":[false,'the usual real line',
       'The real group is divisible, while the integer-product generators '+
       'receive no nonzero map from a divisible group.']
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
             ("Zp", "base-p numbers, with p = 2")]) +
     slider("steps", "how many divisions", 1, 10, 1, 5),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const steps=document.getElementById('steps');
let g='R';
pick('dgrp',v=>{g=v;draw();});
// how many times two divides a whole number
function val2(m){let v=0;while(m%2===0){m/=2;v++;}return v;}
function draw(){
  const n=parseInt(steps.value);
  ctx.clearRect(0,0,cv.width,cv.height);
  let v=720,inside=true,firstOut=-1,v2=val2(720);
  ctx.fillStyle='#52514e';ctx.font='13px system-ui';ctx.textAlign='left';
  ctx.fillText('start at 720, then divide by 2, 3, 4, ...',40,30);
  for(let k=0;k<n;k++){
    const d=k+2;const nv=v/d;
    let ok;
    if(g==='R')ok=true;
    else if(g==='Z')ok=Number.isInteger(nv);
    else {v2-=val2(d);ok=(v2>=0);}   // base-2: only factors of two matter
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
    (g==='R'?'the ruler':g==='Z'?'the whole numbers':'the base-two numbers')+'\n'+
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
  ctx.fillText('completion direction of each factor',40,262);
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
  ruler(288,fa,'#4a3aa7','first factor completes along '+(A==='R'?'no adic direction':fa));
  ruler(336,fb,'#8a5a2c','second factor completes along '+(B==='R'?'no adic direction':fb));
  const out=document.getElementById('out');
  const hasReal=A==='R'||B==='R';
  const source=quotedTensor(A,B)
    ? 'stated in the lectures'
    : hasReal ? 'follows from the vanishing of solidified real groups'
              : 'follows by relabelling the coordinate rule';
  const reason=res==='0'
    ? (hasReal
       ? 'The result is zero because the usual real line becomes zero under solidification.'
       : 'The result is zero because the two prime-completion directions are incompatible.')
    : 'The completion directions are compatible, so both remain in the result.';
  out.textContent=
    pretty(A)+'  combined with  '+pretty(B)+'\n'+
    'gives  '+pretty(res)+'   ('+source+')\n'+reason;
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
     picker("rule2", "measure rule",
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
    ctx.fillText('A direct sum fails as soon as infinitely many',40,150);
    ctx.fillText('coordinates are nonzero.',40,170);
    ctx.fillStyle='#008300';
    ctx.fillText('The solid completion allows all coordinates',40,214);
    ctx.fillText('and gives one compatible result.',40,234);
    for(let k=0;k<D;k++){
      ctx.fillStyle='#00787a';
      ctx.fillRect(48+k*36,270,22,Math.max(4,40/(1+k*0.5)));
    }
    document.getElementById('out').textContent=
      'coordinates set        '+n+' and rising\n'+
      'direct sum             fails when support is not finite\n'+
      'solid completion       contains one compatible result\n'+
      'The completion rule concerns modules over the ring, not only elements of the ring.';
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
     picker("op", "operation",
            [("pull", "pullback"), ("push", "ordinary pushforward"),
             ("shriek", "compactly supported pushforward"),
             ("upper", "upper shriek")]) +
     slider("proper", "does anything escape to the edge", 0, 1, 1, 1),
     PICKER_JS + r"""
const cv=document.getElementById('c'),ctx=cv.getContext('2d');
const pr=document.getElementById('proper');
let op='pull';
pick('op',v=>{op=v;draw();});
const INFO={
  pull:['pullback','transfer an object from the target to the source','standard'],
  push:['ordinary pushforward','transfer all sections from source to target','standard'],
  shriek:['compactly supported pushforward','transfer only the sections '+
          'controlled at the boundary','boundary operation'],
  upper:['upper shriek','right adjoint of compactly supported pushforward',
         'defined by adjunction']
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
    ctx.fillText(lost+' sections meet the boundary and are omitted',540,196);
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
  ctx.fillText('two required special cases',60,240);
  const rules=[
    ['the map is proper',
     'compactly supported pushforward equals ordinary pushforward',!escapes],
    ['the map is an open inclusion',
     'upper shriek equals pullback',true]];
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
      ? (escapes?'boundary behaviour changes the compactly supported result'
                :'for a proper map this equals ordinary pushforward')
      : 'this belongs to one of the two standard adjoint pairs');
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

# Keep the explanatory copy separate from the drawing code. This makes it
# possible to revise every activity in one pass without touching the numerical
# implementation that the JavaScript tests compare with Python.
REVISED_COPY = {
    "condensed-math01": [
        ("Build the finite stages",
         "A profinite probe is assembled from finite stages. This example starts with one box and divides every box into two at the next stage. A point of the completed probe is a compatible path through all the stages.",
         "Increase the depth one level at a time. Each displayed stage contains finitely many boxes, although there is no final stage in the completed probe. Select a box to see which finer boxes lie above it.",
         "Binary splitting gives the Cantor probe. Replacing two children by p children gives the base-p probe used in part two. The browser and Python code construct the same finite sets and transition maps."),
        ("Compare two topologies",
         "Both rows contain the same real numbers. The upper row gives them the discrete topology, so every point is isolated. The lower row uses the usual topology, where each interval contains more points.",
         "Move the inspection slider toward a smaller scale. A neighbourhood in the discrete row eventually contains one point, while every interval in the usual real line still contains infinitely many points.",
         "The identity map has zero kernel and zero cokernel when only individual values are checked, but it is not an isomorphism of topological groups. Example 1.9 explains how condensed groups retain the missing quotient."),
        ("Compare three probes",
         "The diagram shows finite stages of the halving probe, the approaching-sequence probe, and a base-p probe. Selecting a box highlights all finer boxes that map back to it.",
         "Compare the number of boxes at successive stages. Binary branching doubles the count, the sequence probe separates one additional point, and base-p branching multiplies the count by p.",
         "These are inverse systems of finite sets, the profinite sets used in Definition 1.2. The stage sizes and fibres are computed in the browser and checked against the Python implementation."),
        ("Test continuity with a sequence",
         "The points on the left approach a limit point. Their images on the target approach the value chosen by the first control, while the image of the limit is chosen independently by the second control.",
         "Choose different values and observe the break at the limit. Then make the values equal. The map is continuous precisely when the images of the sequence approach the image assigned to its limit.",
         "Remark 1.6 states that convergent sequences determine every metrizable space. The activity therefore shows a complete continuity test for spaces whose topology comes from a distance."),
        ("Test the cut and glue rules",
         "A condensed set must handle disjoint pieces independently and must combine compatible answers on a cover. These are the cut and glue forms of the sheaf condition.",
         "In cut mode, choose any two values; both are accepted because the pieces are disjoint. In glue mode, compare equal and unequal overlap values. A single answer below exists exactly when they agree.",
         "Definition 1.2 states these two conditions. Proposition 2.8 later shows that the glue condition is automatic on extremally disconnected probes because every cover of such a probe splits."),
        ("Inspect the point-invisible quotient",
         "A continuous real-valued function on the halving probe represents an element of the quotient from Example 1.9. It vanishes in the quotient only when it comes from a locally constant function.",
         "Set the variation to zero and the function becomes locally constant. Increase it and refine the probe. The function keeps varying at every visible depth even though the quotient still has no value on the one-point probe.",
         "Example 1.9 identifies this value as a continuous function modulo locally constant functions. The activity constructs one finite approximation; it does not prove that the pattern continues through every stage."),
        ("Try to choose a continuous section",
         "A cover places two possible lifts above each point of the probe. A section chooses one lift per point, and that choice must vary continuously.",
         "Use an alternating choice on the approaching-sequence probe. No value above the limit makes that section continuous. Then select the extremally disconnected case, where the defining property guarantees that some continuous section exists.",
         "Definition 2.4 calls a compact Hausdorff space extremally disconnected when every surjection onto it splits. Warning 2.6 states that every convergent sequence in such a space is eventually constant."),
        ("Translate a space and recover it",
         "The first step records every continuous map from a profinite probe into a space. The second step recovers a topology from those probe values.",
         "Run the circle, interval, and finite set through both steps. Each returns with its original topology. The final example has a nonclosed point and stops because Warning 2.14 excludes it.",
         "Proposition 1.7 proves full faithfulness on compactly generated spaces, and Theorem 2.16 identifies compact Hausdorff spaces with qcqs condensed sets. The rejected example lies outside their hypotheses."),
        ("Measure the winding number",
         "A closed path around a circle has an integer winding number. Continuous deformation may change the shape of the path, but it cannot change that integer without breaking the path.",
         "Change the number of turns, then increase the deformation. The measured winding number remains equal to the chosen integer, and a path with zero turns stays a small loop that goes nowhere. Switch to the torus and set both counts: the drawn loop follows them, and the deformation changes its shape without changing either count.",
         "The circle calculation gives its first cohomology generator. Proposition 3.1 describes products of circles by an exterior algebra; the displayed torus ranks are recomputed here from that formula."),
    ],
    "condensed-math02": [
        ("Distribute a compatible weight",
         "A weighting assigns a number to every box at every stage. The number on a coarse box must equal the sum of the numbers on the finer boxes inside it.",
         "Change the split and the number of stages. The weights on individual branches move, but the total at each level remains the initial value. This is the compatibility equation for a measure.",
         "Definition 5.1 constructs the free solid group as an inverse limit with one integer coordinate per finite-stage box. The activity uses real-valued display weights so that the split can move smoothly, while the compatibility calculation is the same."),
        ("Compare ordinary and p-adic distance",
         "The partial sums add one, p, p squared, and successive powers of p. They grow in ordinary distance but converge when distance is measured p-adically.",
         "Increase the term count for several bases. The ordinary error is multiplied by p at each step, while the p-adic error is divided by p. Compare the displayed limit with one divided by one minus p.",
         "The browser computes the partial sums and both errors live. The Python tests repeat the calculation with exact fractions. For base two, the p-adic limit is minus one."),
        ("Integrate at two stages",
         "A continuous integer-valued function is already constant on the boxes of some finite stage. It can be integrated there or repeated on every box of a finer stage.",
         "Change the stage at which the function is first read. The bars become finer after refinement, but the weighted total remains unchanged because the child weights add to the parent weight.",
         "Stage independence makes integration against a compatible weighting well defined. The tests calculate the same integral at coarse and fine stages and require exact agreement."),
        ("Build a function from a basis",
         "At a finite stage, the indicator of one box is one on that box and zero on the others. Integer combinations of these indicators reconstruct every integer-valued function on the stage.",
         "Add basis functions until the filled bars match the target outline. The labels are integer coefficients. No fractions are needed, and all boxes match when the final basis function is added.",
         "Nöbeling's theorem extends freeness to continuous integer-valued functions on the complete profinite probe. This activity verifies only a finite stage, where freeness is elementary."),
        ("Test the finite-coordinate property",
         "An element of an infinite product may have a nonzero value in every coordinate. Specker's theorem says that a homomorphism from this product to the integers can depend on only finitely many coordinates.",
         "Choose the coordinates read by the homomorphism, then change a coordinate inside or outside that range. A coordinate beyond the finite range cannot affect the output.",
         "Specker's theorem is quoted rather than tested by a finite model. Together with Nöbeling's theorem, it yields Corollary 5.5: the free solid group on a probe is a product of copies of the integers."),
        ("Check the unique-extension rule",
         "A condensed group is solid when every map from probe points extends uniquely to all compatible integer measures. The selector compares groups that satisfy or fail this condition.",
         "Select each group and read the reason for its result. The integers, their products, p-adic integers, and power-series groups pass. A direct sum and the usual real line fail for different reasons.",
         "Definition 5.1 gives the extension condition. Theorem 5.8 and Corollary 6.1 prove the structural results used for these examples; the activity presents their consequences rather than proving them."),
        ("Compare divisible and nondivisible groups",
         "A divisible group allows division by every positive integer. The additive real numbers are divisible, while the integers are not.",
         "Choose a group and increase the number of divisions. Record the first step that leaves the group: the integers leave at the first fraction, while the 2-adic integers survive division by odd numbers and leave only when the factors of two run out. The final line shows why a map from a divisible group to an integer coordinate must be zero.",
         "This arithmetic explains why the real line has no map to the compact projective generators of solid groups. Corollary 6.1 (iii), using Theorem 4.3, proves the stronger statement that derived solidification sends the real line to zero."),
        ("Read a completed tensor product",
         "The completed tensor product combines two solid groups while retaining compatible completion directions. The table lists the examples stated in Lecture VI and direct consequences of the coordinate rule.",
         "Select the p-adic groups for two distinct primes and observe the zero entry. Then compare equal prime directions and power-series directions, which remain in the result.",
         "Example 6.4 states five identities. Proposition 6.3 explains the power-series case by pairing coordinate sets. The readout distinguishes directly quoted entries from entries obtained by relabelling that rule."),
        ("Recover homology from solidification",
         "Derived solidification of the free condensed group on a CW complex recovers its integral homology. The bars separate free classes from finite-order torsion classes.",
         "Rotate the sphere and torus, then compare all five examples. For the Klein bottle, use the bars rather than the surface drawing: it has an order-two homology class that is killed when doubled.",
         "The homology groups are computed here from cellular boundary matrices using Smith normal form. Example 6.5 supplies the quoted theorem identifying those groups with derived solidification."),
    ],
    "condensed-math03": [
        ("Compare exponents",
         "The exponent determines both the unit region for the measure size and the effect of merging boxes. These are separate tests, and their boundaries meet at exponent one.",
         "Lower the exponent through one. The unit region stops being convex below one, while the merge ratio becomes no greater than one. Read both panels before deciding which exponents are allowed.",
         "For n equal boxes, the merge ratio is n raised to one minus the reciprocal of the exponent. The browser evaluates this expression, and the Python tests independently check the ratio and the convexity result."),
        ("Check the data of a measure rule",
         "A proposed rule consists of a condensed ring and one module of measures for every extremally disconnected probe. It must include point masses and turn finite disjoint unions into products.",
         "Toggle each requirement separately. Without Dirac measures, points cannot enter the measure module. Without the disjoint-union rule, independent pieces no longer receive independent data.",
         "Definition 7.1 gives these data. Definition 7.4 adds the derived compatibility test that defines an analytic ring. The finite toggles illustrate necessary inputs but cannot establish that derived condition."),
        ("Compare two analytic rules",
         "The p-adic rule and the solid rule over a discrete ring are both analytic. Each permits an infinite operation that ordinary algebra alone does not define.",
         "Increase the number of terms in each example. The p-adic panel follows a convergent series, while the discrete-ring panel allows a measure with entries in an unrestricted product.",
         "Proposition 7.8 proves that both rules are analytic. In the discrete-ring example the coefficient ring itself has no topology; completion is carried by the selected category of modules."),
        ("Measure the effect of merging",
         "A measure on the full probe must remain within the same size bound when fine boxes are merged into coarse boxes. The chart computes this change for equal weights.",
         "Choose an exponent above one and merge several boxes; the size can increase. Move to one or below and repeat. The ratio is then at most one, so the finite-stage bounds remain compatible.",
         "For equal weights the ratio is n raised to one minus one over p. The tests check this formula directly. Equal weights give the worst growth above one, while the general subadditivity inequality controls all weights at or below one."),
        ("Separate global terms from boundary terms",
         "Near infinity, a function is expanded in the inverse coordinate. Global polynomials form one part of this expansion, while negative powers describe the formal boundary tail.",
         "Move the observation point outward and compare the terms. Then form the quotient conceptually: polynomial terms are removed because they already extend globally, and inverse-power tails remain.",
         "The displayed calculation uses a finite truncation of the Laurent series. Increasing the allowed polynomial degree does not change the number of retained tail coordinates at a fixed tail depth."),
        ("Compute a boundary quotient",
         "Compactly supported pushforward is built from the difference between functions near the boundary and functions defined everywhere. The line and coordinate cross provide finite models of that quotient.",
         "Use the same truncation depth for both shapes. The line retains one tail. The cross retains one tail from each branch plus one contribution from the relation at their shared point.",
         "Remark 8.5 gives the exact dualizing-complex formula for the cross. The activity checks only the rank pattern of finite truncations and identifies the additional contribution from the crossing relation."),
        ("Match bounded functions with valuations",
         "A subring of functions declared to have size at most one determines a region in the valuation space. Proposition 9.2 says that, under its hypotheses, the region also recovers the subring.",
         "Add and remove boundedness conditions. Each condition removes valuations that assign the chosen function a size greater than one. Compare the remaining region after every change.",
         "The correspondence is Proposition 9.2. The two plotted directions are schematic independent valuation parameters, not coordinates on a specific ring, so the drawing illustrates inclusion rather than a particular valuation space."),
        ("Follow the six operations",
         "The six operations are tensor product, internal Hom, pullback, ordinary pushforward, compactly supported pushforward, and its right adjoint. They occur in three adjoint pairs.",
         "Choose compactly supported pushforward for a proper map and for a map with a boundary. In the proper case it agrees with ordinary pushforward; in the other case it removes contributions that escape through the boundary.",
         "Nagata compactification factors a separated finite-type map into an open immersion followed by a proper map. The stated rules determine the candidate compactly supported pushforward, while the theorem must prove independence of the chosen factorization."),
        ("Pair complementary degrees",
         "Coherent duality pairs a class with one in the complementary degree and applies a trace to obtain a scalar on the base. A perfect pairing identifies either side with the dual of the other.",
         "Rotate the surface to see its three-dimensional model, then change its genus. Compare the dimensions on the two sides and follow a paired class through the trace.",
         "The equal dimensions provide a finite classical model of the pairing. Theorem 11.1 constructs compactly supported pushforward, the trace, and the duality isomorphism for a separated smooth finite-type map; the activity does not prove that theorem."),
    ],
}


# Plain-language copy shown on the playable pages. Each entry contains the
# heading, short explanation, instruction, and source note for one chapter.
PLAIN_COPY = {
    "condensed-math01": [
        ("Build a probe from finite stages",
         "A probe begins with one box. Each new stage divides the boxes into smaller ones. A point in the finished probe is a path that makes one compatible choice at every stage.",
         "Add one stage at a time. Notice that every stage has finitely many boxes, even though the completed probe has no last stage. Change the number of pieces to compare different branching patterns.",
         "The standard name for this object is a profinite set. The browser builds the same finite sets and transition maps as the Python code, and the tests compare their results."),
        ("Compare two ideas of closeness",
         "The two rows contain the same real numbers. In the top row, every point stands alone. In the bottom row, the numbers have their usual distance, so nearby values remain close.",
         "Make the viewing window smaller. The discrete row eventually isolates one point. An interval in the usual real line always contains more points, however small the interval becomes.",
         "The identity map has zero point-level kernel and cokernel, but it is not an isomorphism of topological groups. Example 1.9 shows how condensed groups keep the quotient that the pointwise test misses."),
        ("Compare three kinds of probes",
         "These diagrams show finite stages of a halving probe, an approaching sequence, and a base-p probe. Every box has a precise parent in the stage above it.",
         "Choose a probe and add stages. Select a box to highlight all the smaller boxes inside it. Compare how the number of boxes changes from one stage to the next.",
         "Definition 1.2 describes these probes as inverse systems of finite sets. The activity calculates their stage sizes and fibres, and the tests compare those calculations with the Python implementation."),
        ("Check continuity with a sequence",
         "The sequence points approach a limit. A continuous map must send those points toward the value assigned to the limit point.",
         "Choose where the sequence images approach, then choose the image of the limit. Try unequal values first. Make them equal and see why the continuity result changes.",
         "Remark 1.6 says that convergent sequences determine the topology of every metrizable space. For spaces defined by a distance, this activity shows the full sequence test for continuity."),
        ("Use the cut and glue rules",
         "A condensed set treats separate pieces independently. It also joins answers on a cover when they agree wherever the cover repeats the same point.",
         "In cut mode, choose any value on each separate piece. In glue mode, try equal and unequal values on the overlap. A value below exists only when the overlap values match.",
         "These are the sheaf conditions in Definition 1.2. Proposition 2.8 says that gluing is automatic on extremally disconnected probes because every cover of such a probe has a section."),
        ("Find a quotient that points miss",
         "A probe can support a continuous real-valued function that is not locally constant. Such a function gives information that the one-point probe cannot detect.",
         "Set the variation to zero, then increase it and add finer stages. At zero, the map is locally constant. With variation, it keeps changing on smaller visible boxes.",
         "Example 1.9 identifies the quotient as continuous functions modulo locally constant functions. This activity shows finite approximations to one nonzero class and does not prove that the pattern continues forever."),
        ("Try to choose a continuous section",
         "A cover gives possible points above each point of a probe. A section chooses one point above each point, and those choices must vary continuously.",
         "Alternate between the two choices above the approaching sequence. No choice at the limit can make that section continuous. Then switch to the extremally disconnected case, where every cover has some continuous section.",
         "Definition 2.4 calls a compact Hausdorff space extremally disconnected when every surjection onto it splits. Warning 2.6 says that a convergent sequence in such a space must eventually be constant."),
        ("Recover a familiar space",
         "First record every continuous map from a profinite probe into a space. Then use those probe maps to recover a topology on its points.",
         "Send the circle, interval, and finite set through both steps. Each one returns with its original topology. The final example stops because it has a point that is not closed.",
         "Proposition 1.7 proves this recovery for compactly generated spaces, and Theorem 2.16 gives the compact Hausdorff case. Warning 2.14 explains why the rejected example lies outside the assumptions."),
        ("Keep track of winding",
         "A closed path around a circle has an integer winding number. A continuous deformation may change the path's shape, but it cannot change that number without breaking the path.",
         "Change the turn count and then deform the path. On the torus, choose both independent turn counts. The drawing changes shape while the selected winding data stay fixed.",
         "The circle gives one generator in first cohomology. Proposition 3.1 describes products of circles with an exterior algebra, and the activity recomputes the displayed torus ranks from that formula."),
    ],
    "condensed-math02": [
        ("Distribute compatible weights",
         "A measure gives a weight to every box at every stage. Each parent weight must equal the sum of the child weights inside it.",
         "Change the way the weight is divided and add more stages. Individual branch weights change, but every stage keeps the same total.",
         "Definition 5.1 builds the free solid group as an inverse limit of integer weights. The display uses movable real weights, but it checks the same addition rule between parent and child boxes."),
        ("Compare ordinary and p-adic distance",
         "Add 1, then p, then p squared, and continue with higher powers. The totals grow under ordinary distance but settle toward a limit under p-adic distance.",
         "Increase the number of terms for several bases. Compare the growing ordinary error with the shrinking p-adic error, then read the limit shown below the picture.",
         "The browser calculates both errors directly. The Python tests repeat the calculation with exact fractions. In base two, the p-adic limit is minus one."),
        ("Integrate at a coarse or fine stage",
         "A continuous integer-valued function is constant on the boxes of some finite stage. We can repeat its values on finer boxes without changing the function.",
         "Move the reading stage. The bars split into finer bars, but the weighted total stays fixed because the child weights add up to their parent weight.",
         "This stage independence makes integration against a compatible measure well defined. The tests compute the same integral at coarse and fine stages and require exact equality."),
        ("Build a function from simple pieces",
         "For each box, an indicator function is one on that box and zero on all the others. Integer multiples of these simple functions can build any integer-valued function on a finite stage.",
         "Add the basis functions until the filled bars match the target outline. Each label is an integer coefficient, and the final function uses no fractions.",
         "Nöbeling's theorem proves the stronger result for all continuous integer-valued functions on a complete profinite probe. This activity checks only one finite stage, where the basis is elementary."),
        ("See which coordinates a map can read",
         "A product may have a nonzero integer in every coordinate. Specker's theorem says that an additive map from a countable product to the integers can read only finitely many of them.",
         "Choose how many coordinates the map reads. Change one coordinate inside that range and one outside it. Only a coordinate inside the range can change the output.",
         "The finite picture illustrates Specker's conclusion but cannot prove the infinite theorem. Together with Nöbeling's theorem, it gives the product description of the free solid group in Corollary 5.5."),
        ("Check the unique-extension rule",
         "A condensed group is solid when every assignment on probe points extends in exactly one way to all compatible integer measures.",
         "Choose each example and read why it passes or fails. Pay attention to whether the problem is that an extension does not exist or that the group cannot contain all needed values.",
         "Definition 5.1 gives the extension rule. Theorem 5.8 and Corollary 6.1 prove the facts used to classify these examples, so the activity reports consequences rather than proving them."),
        ("Compare divisible groups",
         "A divisible group allows division by every positive integer. The additive real numbers have this property, but the integers do not.",
         "Choose a group and increase the number of divisions. Watch for the first result that leaves the group. The final line explains why every map from a divisible group to an integer coordinate is zero.",
         "This arithmetic explains an obstruction to mapping the reals into the projective building blocks of solid groups. Corollary 6.1 (iii), using Theorem 4.3, proves the stronger derived vanishing result."),
        ("Read a completed tensor product",
         "The completed tensor product combines two solid groups and keeps completion directions that are compatible with both sides.",
         "Choose p-adic groups for two different primes and observe the zero result. Then compare equal prime directions and power-series directions, which remain in the answer.",
         "Example 6.4 states five identities. Proposition 6.3 explains the power-series example by pairing coordinate sets. The readout distinguishes quoted identities from entries obtained by relabelling that rule."),
        ("Recover homology from solidification",
         "Derived solidification of the free condensed group on a space recovers its integral homology. The bars separate free classes from classes of finite order.",
         "Compare all five spaces and rotate the sphere or torus. For the Klein bottle, notice the order-two class: adding that class to itself gives zero.",
         "The activity computes homology from cellular boundary matrices using Smith normal form. Example 6.5 supplies the theorem that identifies these groups with derived solidification."),
    ],
    "condensed-math03": [
        ("Compare the two exponent tests",
         "An exponent controls both the shape of the unit region and the effect of merging boxes. Convexity and stable merging are different conditions, although both change at exponent one.",
         "Move the exponent through one. Below one, the unit region is not convex, but merging no longer increases the size. Read both results before deciding which condition has passed.",
         "For n equal boxes, the merge ratio is n raised to one minus the reciprocal of the exponent. The browser evaluates this formula, and the Python tests check both the ratio and the convexity result."),
        ("Check the parts of a measure rule",
         "A proposed rule needs a condensed ring and a module of allowed measures for every extremally disconnected probe. Point masses must be included, and separate pieces must receive independent data.",
         "Turn each requirement off and on. Without Dirac measures, points cannot enter the measure module. Without the disjoint-union rule, two separate pieces cannot be handled independently.",
         "Definition 7.1 lists these data. Definition 7.4 adds the derived condition that defines an analytic ring. The controls check necessary inputs but cannot prove that final condition."),
        ("Compare two analytic measure rules",
         "The p-adic rule and the solid rule over a discrete ring both pass the analytic test. They support different infinite operations because their coefficient rings and measure modules differ.",
         "Add terms in both examples. The p-adic side follows a convergent series. The discrete-ring side shows a measure with an unrestricted family of coordinates.",
         "Proposition 7.8 proves that both rules are analytic. In the discrete example, the ring itself has no topology; the completion is carried by the chosen category of modules."),
        ("Measure what happens when boxes merge",
         "A fine-stage measure must stay within its size limit after its boxes are merged at a coarser stage. This chart calculates the change for equal weights.",
         "Choose an exponent above one and merge several boxes. Then move to one or below. The ratio is now at most one, so the same size limit works at both stages.",
         "For equal weights, the ratio is n raised to one minus one over p. Equal weights give the worst growth above one, while subadditivity controls all weights at or below one."),
        ("Separate global and boundary terms",
         "Near infinity, functions are expanded in the reciprocal coordinate. Polynomial terms extend across the whole line, while negative powers describe a tail that lives near the boundary.",
         "Move farther toward infinity and compare the terms. In the quotient, remove every polynomial term because it is already global. The negative-power tail remains.",
         "The activity uses a finite part of a Laurent series. Increasing the allowed polynomial degree does not change the number of retained tail coordinates at a fixed tail depth."),
        ("Compute a boundary quotient",
         "Compactly supported pushforward compares functions near the boundary with functions defined everywhere. A line and a coordinate cross give small models of this quotient.",
         "Use the same truncation for both shapes. The line keeps one tail. The cross keeps a tail from each branch and one extra contribution from the relation at their shared point.",
         "Remark 8.5 gives the exact dualizing-complex formula for the cross. This activity checks only the ranks of finite truncations and identifies the extra contribution from the crossing relation."),
        ("Match bounded functions with valuations",
         "A chosen subring of bounded functions selects the valuations that give every one of those functions size at most one. Under the theorem's assumptions, the selected region also recovers the subring.",
         "Add one bound at a time. Each new condition removes valuations that make the selected function too large. Compare the remaining region after every change.",
         "This correspondence is Proposition 9.2. The plotted points are a simple model of independent valuation parameters, not the valuation space of a particular ring, so the picture shows inclusion only."),
        ("Follow the six operations",
         "The six operations are tensor product, internal Hom, pullback, ordinary pushforward, compactly supported pushforward, and its right adjoint. They form three adjoint pairs.",
         "Choose compactly supported pushforward for a proper map and then for a map with a boundary. In the proper case, it equals ordinary pushforward. Otherwise, it removes contributions that escape through the boundary.",
         "Nagata compactification factors a separated finite-type map into an open immersion followed by a proper map. These rules define a candidate operation, while the theorem proves that it is independent of the chosen factorization."),
        ("Pair complementary degrees",
         "Coherent duality pairs a class with one in the complementary degree. Their product reaches the top degree, and a trace map then produces a scalar on the base.",
         "Rotate the surface and change its genus. Compare the number of classes on both sides, then follow a paired class through the trace.",
         "Equal finite dimensions provide a classical model of a perfect pairing. Theorem 11.1 constructs compactly supported pushforward, the trace, and the duality isomorphism; this activity does not prove the theorem."),
    ],
}


WIDGET_TERMS = [
    ("the base-two numbers", "the 2-adic integers"),
    ("the base-three numbers", "the 3-adic integers"),
    ("the base-p numbers", "the p-adic integers"),
    ("the whole numbers", "the integers"),
    ("whole-number", "integer"),
    ("the ruler", "the usual real line"),
    ("the dust", "the discrete real line"),
    ("the ghost", "the quotient"),
    ("unfoldable", "extremally disconnected"),
    ("answer sheet", "probe data"),
    ("marching points", "sequence points"),
    ("the march", "the sequence"),
    ("chain snaps", "limits differ"),
    ("one answer glues below", "one answer descends"),
    ("doughnut", "torus"),
    ("plain ring", "discrete ring"),
    ("the counterweight", "the right adjoint"),
    ("dials", "coordinates"),
    ("dial", "coordinate"),
    ("a question", "a homomorphism"),
    ("the question", "the homomorphism"),
    ("switches", "basis functions"),
    ("switch", "basis function"),
    ("measurement", "function"),
    ("wobble", "deformation"),
]

# Labels and readouts share the drawing code with the calculations. These
# replacements keep that on-canvas copy direct and grammatical without changing
# any numerical behavior.
WIDGET_POLISH = [
    # Part one
    ("how many splits", "number of stages"),
    ("pieces per split", "children of each box"),
    ("the discrete real line the splits cut out", "points represented by the final stage"),
    ("boxes at the finest", "boxes in the final stage"),
    ("every stage is finite; only the endless stack is not", "Every displayed stage is finite. The completed probe has no final stage."),
    ("how closely you look", "size of the viewing window"),
    ("the usual real line: nearness kept", "usual real line: nearby values remain close"),
    ("every window holds endlessly many others", "every interval still contains infinitely many points"),
    ("the discrete real line: nearness forgotten", "discrete real line: every point is isolated"),
    ("the window now holds one grain and nothing else", "the window now contains one point"),
    ("grains, each one alone", "isolated points"),
    ("send each number to itself", "map each number to the same value"),
    ("numbers left over at the front   0", "point-level kernel      0"),
    ("numbers left over at the back    0", "point-level cokernel    0"),
    ("so the map kills nothing and misses nothing", "The pointwise map loses no values and misses no values."),
    ("and yet: this window separates a grain but not a ruler point", "However, this window isolates a point only in the discrete row."),
    ("keep zooming until one grain stands alone", "Reduce the window until one discrete point stands alone."),
    ("which probe", "probe"),
    ("stages shown", "number of stages"),
    ("p, for the base-p probe", "base p"),
    ("boxes per stage", "boxes at each stage"),
    ("clicked a stage-", "selected a stage-"),
    (" of the finest boxes sit inside it", " final-stage boxes lie inside it"),
    ("click a box to light up everything inside it", "Select a box to highlight all finer boxes inside it."),
    ("where the sequence points head", "limit approached by the sequence"),
    ("where the limit point lands", "image of the limit point"),
    ("where the sequence heads", "limit approached by the sequence"),
    ("the limits differ here", "the two limit values differ"),
    ("the sequence heads to", "the sequence approaches"),
    ("the limit lands at", "the limit maps to"),
    ("accepted: nearby points of the probe go to nearby points", "Continuous: the sequence approaches the image of its limit."),
    ("refused: the probe was torn at its limit", "Not continuous: the sequence and its limit have different images."),
    ("answer on the left piece", "value on the left piece"),
    ("answer on the right piece", "value on the right piece"),
    ("one probe, falling into two separate pieces", "one probe divided into two disjoint pieces"),
    ("answering the whole probe", "values on the whole probe"),
    ("accepted for every choice: nothing connects the pieces", "Every pair is valid because the pieces are disjoint."),
    ("the cut rule accepts every pair, always", "The cut rule accepts every pair of values."),
    ("a covering: two pieces, overlapping in the middle", "a cover with two pieces that overlap"),
    ("exactly one answer: ", "one value below: "),
    ("no answer below: the pieces disagree on the overlap", "No value exists below because the overlap values differ."),
    ("they agree on the overlap, so exactly one answer descends", "The overlap values agree, so exactly one value descends."),
    ("they disagree on the overlap, so nothing glues", "The overlap values differ, so they cannot be glued."),
    ("how much each split shifts", "variation at each split"),
    ("how deep you look", "number of stages"),
    ("the landing, box by box", "function values on the final-stage boxes"),
    ("what a single point can see", "value on the one-point probe"),
    ("nothing: the quotient has no points at all", "zero: one point detects no quotient value"),
    ("points the quotient has", "point-level quotient values"),
    ("widest gap inside a finest box", "largest variation in a final box"),
    ("flat on every box, so the discrete real line can do it too: this entry is zero", "The map is locally constant, so its quotient class is zero."),
    ("never flat, however deep you look: a nonzero entry of the quotient", "The map still varies at every visible stage. This is the finite pattern used for a nonzero quotient class."),
    ("which probe below", "probe below the cover"),
    ("how often the choice flips", "period of the alternating choice"),
    ("the covering: two copies above every point", "the cover: two possible lifts above each point"),
    ("neither copy works", "neither limit choice is continuous"),
    ("nothing converges here, so no limit point can be blocked", "there is no nonconstant convergent sequence to create this obstruction"),
    ("every covering of an extremally disconnected probe lifts, whatever you choose", "By definition, every cover of an extremally disconnected probe has at least one continuous section."),
    ("the choices settle, so the limit lifts too", "The choices eventually agree, so they extend continuously to the limit."),
    ("the choices never settle, so the limit cannot be lifted", "The choices keep alternating, so no value at the limit makes this section continuous."),
    ("which space", "space"),
    ("read by probes", "record all probe maps"),
    ("points read back", "recover the topology"),
    ("no probe data exists", "the construction stops"),
    ("the lectures flag exactly this case as the failure", "Warning 2.14 identifies this exact failure."),
    ("sent out and read back: the same space", "The recovered topology is the original topology."),
    ("the continuous maps out of it are the same maps too", "The translation also preserves all continuous maps."),
    ("which shape", "shape"),
    ("turns the path makes", "turns around the circle"),
    ("turns the second way, for the torus", "turns in the second torus direction"),
    ("deformation applied to the path", "amount of deformation"),
    ("the count is a whole number and the deformation cannot move it", "The winding number is an integer and deformation does not change it."),
    ("the long way round", "around the main opening"),
    ("through the hole", "around the tube"),
    ("turns the long way", "turns around the opening"),
    ("turns through the hole", "turns around the tube"),
    ("hole counts by degree", "cohomology ranks by degree"),
    ("a loop that goes nowhere counts zero both ways", "A contractible loop has zero winding in both directions."),
    ("two independent counts, and the deformation moves neither", "The torus has two independent winding numbers, and deformation preserves both."),
    # Part two
    ("how each split leans", "how the weight is divided"),
    ("the number at the top", "initial weight"),
    ("boxes at the finest", "boxes in the final stage"),
    ("every stage agrees: this is a legal weighting", "Every stage has the same total, so the weighting is compatible."),
    ("the stages disagree, so this is not a weighting", "The stage totals differ, so the weighting is not compatible."),
    ("the base p", "base p"),
    ("terms added", "number of terms"),
    ("the ordinary size: the totals run away", "ordinary distance: the totals grow"),
    (" size: the totals close in", "-adic distance: the totals approach a limit"),
    ("the value the totals reach", "p-adic limit"),
    ("last running total", "last partial sum"),
    ("ordinary distance to the value", "ordinary distance to the limit"),
    (" distance to the value", "-adic distance to the limit"),
    ("one climbs by a factor of ", "The ordinary error grows by a factor of "),
    (", the other falls by a factor of ", ", while the p-adic error shrinks by a factor of "),
    ("level the function is read at", "stage where the function is read"),
    ("the function's shape", "function pattern"),
    ("the level you read at makes no difference", "Both stages give the same integral."),
    ("the readings disagree, which cannot happen for a weighting", "The integrals differ, so the displayed weights are not compatible."),
    ("basis functions used", "number of basis functions"),
    ("which function", "target function"),
    ("the function you want (outline) and what the basis functions give", "target function (outline) and current reconstruction"),
    ("boxes still uncovered", "boxes not yet matched"),
    ("rebuilt exactly, with whole numbers and no fractions", "The integer coefficients rebuild the function exactly."),
    ("keep adding basis functions", "Add more basis functions to match every box."),
    ("how far the homomorphism reaches", "coordinates read by the homomorphism"),
    ("which coordinate you set", "coordinate to change"),
    ("the coordinates: every one may be set, forever", "the product: every coordinate may be nonzero"),
    ("what the homomorphism can reach", "coordinates read by the homomorphism"),
    ("why no question reaches the whole row", "why the map cannot read infinitely many coordinates"),
    ("an answer divisible by every power must be zero", "An integer divisible by every power of two must be zero."),
    ("the homomorphism reaches", "the homomorphism reads"),
    ("that coordinate is inside the reach", "That coordinate is inside the finite range, so it changes the output."),
    ("that coordinate is past the reach, so the homomorphism cannot see it", "That coordinate is outside the finite range, so it cannot change the output."),
    ("which group", "group"),
    ("a row of coordinates", "a product of integer groups"),
    ("base-p numbers", "p-adic integers"),
    ("a weighting has a finite total, so integrating lands back in it", "A finite integer weighting integrates to another integer."),
    ("integrate coordinate by coordinate: each one is the integers again", "Integration is performed in each integer coordinate."),
    ("this is exactly the group the base-p probe was built to complete", "The p-adic completion supports the corresponding compatible sums."),
    ("one coordinate per power, so it is a row of coordinates in disguise", "One coefficient for each power makes this an integer product."),
    ("a weighting can spread across infinitely many coordinates, and the total ", "A compatible weighting may use infinitely many coordinates, so the result "),
    ("then has infinitely many nonzero slots, which this group forbids", "may have infinite support, which a direct sum does not allow."),
    ("every real number can be divided by every whole number, and the ", "The real group is divisible, while the integer-product "),
    ("building blocks cannot receive anything divisible like that", "generators receive no nonzero map from a divisible group."),
    ("the extension exists, and only one does", "Exactly one extension exists."),
    ("no such extension", "The required extension does not exist."),
    ("weightings can be integrated here", "Compatible measures can be integrated here."),
    ("what the rule asks for", "Requirements of the solid rule"),
    ("how many divisions", "number of divisions"),
    ("start at 720, then divide by 2, 3, 4, ...", "start at 720 and divide successively by 2, 3, 4, and so on"),
    ("so what can this group send to a single coordinate?", "possible image in one integer coordinate"),
    ("nothing but zero", "only zero"),
    ("whatever you like", "a possible nonzero integer"),
    ("divisible by everything, so it maps to zero in every row of coordinates,", "This group is divisible, so every map to an integer product is zero."),
    ("which is every building block the solid world is assembled from", "Integer products are the compact projective generators of solid groups."),
    ("not divisible by everything, so it has room to map into coordinates", "This group is not divisible, so this particular obstruction does not apply."),
    ("first factor", "first solid group"),
    ("second factor", "second solid group"),
    ("nothing at all", "zero"),
    ("the nesting each side carries", "completion direction of each factor"),
    ("first factor shrinks by", "first factor completes along"),
    ("second factor shrinks by", "second factor completes along"),
    ("nothing survives: the two sides carry nestings that never agree", "The result is zero because the two completion directions are incompatible."),
    ("the nestings are compatible, so both are kept", "The completion directions are compatible, so both remain in the result."),
    ("turn the camera", "camera angle"),
    ("the holes that fall out", "computed homology"),
    ("computed from cell boundaries over the integers", "The groups are computed from cellular boundary maps over the integers."),
    # Part three
    ("the exponent", "exponent p"),
    ("the midpoint stays inside", "the midpoint is inside the unit region"),
    ("the midpoint escapes", "the midpoint is outside the unit region"),
    ("size after merging, over before", "size after merging divided by size before"),
    ("the ball is", "the unit region is"),
    ("allowed: merging never makes a measure bigger", "Compatible: merging does not increase the size."),
    ("forbidden: merging makes the measure bigger, so the stages cannot fit together", "Not compatible: merging increases the size, so one bound cannot work at every stage."),
    ("each point counts as a unit weight", "include every Dirac point mass"),
    ("separate pieces answered separately", "treat disjoint pieces independently"),
    ("the legal weightings on that probe", "the allowed measures on that probe"),
    ("nothing to integrate against", "no measure module has been chosen"),
    ("without it, no point of the probe can enter at all", "Without Dirac measures, probe points cannot enter the measure module."),
    ("without it, the pieces of a probe stop being independent", "Without the product rule, disjoint pieces cannot be handled independently."),
    ("both requirements met: a rule for sums is defined here", "Both basic requirements are present."),
    ("a requirement is missing, so there is no rule yet", "A basic requirement is missing, so this is not a measure rule."),
    ("whether the rule then passes the further test is what makes it analytic", "The separate derived test determines whether the rule is analytic."),
    ("adding 1, 2, 4, 8, and on", "adding 1, 2, 4, 8, and further powers"),
    ("the gap halves every step, so the sum lands", "the p-adic error halves at each step, so the sum converges"),
    ("ordinary answer        none, the totals run away", "ordinary limit         none; the partial sums grow"),
    ("answer under this rule", "limit under this rule"),
    ("the base-p rule is exactly what makes this sum legal", "The p-adic measure rule gives this series a limit."),
    ("the solid rule: a sum spread across every coordinate", "the solid rule: a compatible measure using many coordinates"),
    ("... and on, forever", "and further coordinates"),
    ("finitely many allowed  fails once the count passes any bound", "direct sum             fails when support is not finite"),
    ("the solid rule         accepts it, with exactly one total", "solid completion       contains one compatible result"),
    ("this is why the rule is stated about modules, not about the ring", "The completion rule concerns modules over the ring, not only elements of the ring."),
    ("boxes merged into one", "number of boxes merged"),
    ("how uneven the weights are", "difference among the weights"),
    ("the boxes merge, the weights add", "merging adds all the weights"),
    ("the size did not grow: the stages fit together", "The size did not grow, so the same bound works at both stages."),
    ("the size grew: these stages cannot be one weighting", "The size grew, so one bound cannot define a compatible measure at both stages."),
    ("forbidden: this is why the exponent must not pass one", "The size grows above exponent one, so the finite-stage bounds are not compatible."),
    ("how far out you stand", "distance toward infinity"),
    ("tails kept", "number of tail terms"),
    ("the edge", "the boundary"),
    ("you are here, at", "observation point"),
    ("how much each power matters where you stand", "size of each term at the observation point"),
    ("red: a polynomial part, thrown away in the quotient", "red: global polynomial terms removed by the quotient"),
    ("teal: the tails, which are what survives", "teal: boundary-tail terms that remain in the quotient"),
    ("standing at", "observation point"),
    ("surviving pieces", "terms left in the quotient"),
    ("the count is the number of tails, whatever the polynomial part reaches to", "At a fixed tail depth, changing the polynomial degree does not change the quotient rank."),
    ("how far the polynomials reach", "maximum polynomial degree"),
    ("one edge", "one boundary branch"),
    ("the crossing point", "shared origin"),
    ("pieces of a function near the edge", "truncated boundary functions"),
    ("pieces of a function everywhere", "truncated global functions"),
    ("what is left over", "quotient rank"),
    ("near the edge", "near the boundary"),
    ("left over", "quotient"),
    ("   (exactly the tails)", "   (one boundary tail)"),
    ("   (both branches' tails, plus one)", "   (two boundary tails plus one shared-origin contribution)"),
    ("stable: pushing the polynomials further out does not move it", "The rank is stable when the polynomial degree increases."),
    ("declare the coordinate small", "bound the coordinate by one"),
    ("declare its reciprocal small", "bound its reciprocal by one"),
    ("declare a prime small", "bound a prime by one"),
    ("every consistent way of measuring how big each function is", "possible valuations"),
    (" is small", " is bounded"),
    (" is free", " is unrestricted"),
    ("declarations made", "bounds selected"),
    ("valuations left in", "valuations remaining"),
    ("nothing left: these declarations are incompatible", "No valuation satisfies all the selected bounds."),
    ("each declaration cuts the region down, and the region determines the declarations back", "Each bound shrinks the valuation region. Under Proposition 9.2, the region recovers the bounded subring."),
    ("does anything escape to the edge", "does support reach the boundary"),
    ("transfer an object from the target to the source", "move an object from the target space to the source space"),
    ("transfer all sections from source to target", "move all sections from the source space to the target space"),
    ("transfer only the sections controlled at the boundary", "move only sections whose support is controlled at the boundary"),
    ("boundary operation", "right adjoint of compact support"),
    ("right adjoint of compactly supported pushforward", "the right adjoint of compactly supported pushforward"),
    ("the space above", "source space"),
    ("the space below", "target space"),
    (" sections meet the boundary and are omitted", " sections reach the boundary and are omitted"),
    ("two required special cases", "two special cases"),
    ("boundary behaviour changes the compactly supported result", "Boundary support makes compactly supported pushforward differ from ordinary pushforward."),
    ("for a proper map this equals ordinary pushforward", "For a proper map, compactly supported pushforward equals ordinary pushforward."),
    ("this belongs to one of the two standard adjoint pairs", "This operation belongs to one of the three adjoint pairs."),
    ("how many holes the surface has", "genus of the surface"),
    ("one side", "one vector space"),
    ("its partner", "the complementary vector space"),
    ("one number", "one scalar"),
    ("holes in the surface", "genus of the surface"),
    ("classes on one side", "dimension on one side"),
    ("classes on the partner side", "dimension on the other side"),
    ("the two sides match for every shape, which is what perfect means", "This finite model gives the same dimension on both sides."),
    ("the trace turns the top-degree classes into a single number", "The trace sends each top-degree result to one scalar."),
    # Corrections after broader substitutions above.
    ("whole numbers", "integers"),
    ("boxes in the final stage level", "boxes in the final stage"),
    ("a direct sum of integer groups at a time", "finitely many coordinates at a time"),
    ("first solid group shrinks by", "first factor completes along"),
    ("second solid group shrinks by", "second factor completes along"),
    ("forbidden: merging makes the measure bigger, so the stages ", "Not compatible: merging increases the size, so "),
    ("cannot fit together", "one bound cannot work at every stage."),
    ("forbidden: this is why exponent p must not pass one", "The size grows above exponent one, so the finite-stage bounds are not compatible."),
    ("with finitely many coordinates allowed, this leaves the group ", "A direct sum fails "),
    ("the moment", "as soon as "),
    ("more than finitely many are set", "infinitely many coordinates are nonzero."),
    ("with the solid rule, a weighting spreads across all of ", "The solid completion allows all of "),
    ("them and still", "these coordinates and "),
    ("has exactly one total", "gives one compatible result."),
    ("pieces of a function near the boundary", "truncated boundary functions"),
    ("   (both branches\\' tails, plus one)", "   (two boundary tails plus one shared-origin contribution)"),
    ("unexpected count", "The calculated rank does not match the expected formula."),
    ("each declaration cuts the region down, and the region determines ", "Each bound shrinks the valuation region. Under Proposition 9.2, the region "),
    ("the declarations back", "recovers the bounded subring."),
    ("which operation", "operation"),
    ("does anything escape to the boundary", "does support reach the boundary"),
    ("push with compact support", "compactly supported pushforward"),
    ("transfer only the sections ", "move only sections whose support is "),
    ("controlled at the boundary", "controlled at the boundary"),
    ("classes on one vector space", "dimension on one side"),
]


def _naturalize_widget_copy(text):
    for old, new in WIDGET_TERMS:
        text = text.replace(old, new)
    for old, new in WIDGET_POLISH:
        text = text.replace(old, new)
    return text


def _apply_revised_copy(slug, chapters):
    copy = PLAIN_COPY[slug]
    assert len(copy) == len(chapters)
    revised = []
    for chapter, words in zip(chapters, copy):
        num, _, _, _, controls, widget, _ = chapter
        heading, lede, prompt, note = words
        controls = _naturalize_widget_copy(controls)
        widget = _naturalize_widget_copy(widget)
        revised.append((num, heading, lede, prompt, controls, widget, note))
    return revised


CHAPTERS = {
    "condensed-math01": _apply_revised_copy("condensed-math01", PART_ONE_CHAPTERS),
    "condensed-math02": _apply_revised_copy("condensed-math02", PART_TWO_CHAPTERS),
    "condensed-math03": _apply_revised_copy("condensed-math03", PART_THREE_CHAPTERS),
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
            nav.append('<a href="index.html">all activities</a>')
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
                 .replace("TITLE", f"Activities · condensed mathematics, "
                                   f"part {part.number}")
                 .replace("HEADING", f"Activities for part {part.number}")
                 .replace("LEDE", "Choose a chapter activity below. Each page "
                                  "turns one mathematical idea into a finite "
                                  "example that you can change.")
                 .replace('<p class="try"><strong>Try this.</strong> TRY</p>', "")
                 .replace('<canvas id="c" width="720" height="400"></canvas>', "")
                 .replace('<div class="controls">CONTROLS</div>',
                          f'<ul class="list">{rows}</ul>')
                 .replace('<div class="readout" id="out"></div>', "")
                 .replace("NOTE", "Every activity is self-contained and uses no "
                                  "network connection or external library. You "
                                  "can therefore save and run the pages offline.")
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
