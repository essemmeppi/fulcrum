// Rebuild with: FULCRUM_MAP_TOOLS=/tmp/fulcrum-map-tools node output/research/build-map.mjs
// Dependencies: d3-geo@3.1.1 and sharp@0.34.5. Geometry: Natural Earth, public domain.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(path.join(process.env.FULCRUM_MAP_TOOLS || here, 'package.json'));
const {geoEqualEarth, geoPath} = await import(require.resolve('d3-geo'));
const sharp = require('sharp');
const read = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const rows = read(path.join(here, '../../process-mapper/survey/screening/countries.json'));
const registry = read(path.join(here, '../../process-mapper/survey/registry/countries.json')).countries;
const world = read(path.join(here, 'world-boundaries.geojson'));
const labels = read(path.join(here, 'country-label-points.json'));
const codes = {xk:'KOS', ps:'PSX', ss:'SDS'};
const iso = c => codes[c.id] || c.iso3;
const byCode = new Map(registry.map(c => [iso(c), rows.find(r=>r.id===c.id)]));
const palette = {
  strong_evidence: {color:'#167d76', label:'Detailed operational material'},
  promising_evidence: {color:'#e6b35b', label:'Promising, unresolved'},
  public_facing_only: {color:'#90b3d4', label:'Public-facing evidence only'},
  unknown: {color:'#c5cbd0', label:'Unknown'},
};
const esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const counts = Object.fromEntries(Object.keys(palette).map(k=>[k,rows.filter(c=>c.assessment===k).length]));
if(rows.length!==197 || new Set(rows.map(c=>c.id)).size!==197) throw Error('Expected 197 unique country rows');
const W=1600,H=1120;
const projection=geoEqualEarth().fitExtent([[40,275],[1560,950]],{type:'Sphere'});
const draw=geoPath(projection).digits(2);
const represented=new Set();
let marks='';
for(const f of world.features) {
  if(f.properties.ADM0_A3==='ATA') continue;
  const c=byCode.get(f.properties.ADM0_A3);
  if(c) represented.add(c.id);
  marks+=`<path ${c?`data-country="${c.id}"`:''} d="${draw(f)}" fill="${c?palette[c.assessment].color:'#edf0f2'}" stroke="#ffffff" stroke-width="0.65"><title>${esc(c?`${c.name}: ${palette[c.assessment].label}`:`${f.properties.ADMIN}: outside study registry`)}</title></path>`;
}
const markerIds=[];
for(const c of registry) {
  if(represented.has(c.id)) continue;
  const p=labels.find(p=>p.ADM0_A3===iso(c));
  if(!p) throw Error(`No published coordinate for ${c.name}`);
  const [x,y]=projection([p.LABEL_X,p.LABEL_Y]);
  const r=rows.find(r=>r.id===c.id);
  marks+=`<circle data-country="${c.id}" cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="4.4" fill="${palette[r.assessment].color}" stroke="#ffffff" stroke-width="1.15"><title>${esc(`${c.name}: ${palette[r.assessment].label}`)}</title></circle>`;
  represented.add(c.id);markerIds.push(c.id);
}
if(represented.size!==197) throw Error(`Only ${represented.size} countries represented`);
let legend='';
Object.entries(palette).forEach(([k,v],i)=>{
  const x=55+i*390;
  legend+=`<rect x="${x}" y="176" width="11" height="68" rx="3" fill="${v.color}"/><text x="${x+27}" y="208" font-size="39" font-weight="600">${counts[k]}</text><text x="${x+27}" y="239" font-size="19">${v.label}</text>`;
});
const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="map-title map-desc">
<title id="map-title">Public documents: a starting point in at least 86 countries</title>
<desc id="map-desc">All 197 countries screened at national level. 86 have detailed operational material, 41 promising but unresolved, 20 public-facing evidence only, 50 unknown. Publication evidence is not validated mapping accuracy. Small states shown as dots.</desc>
<rect width="1600" height="1120" fill="#fff"/>
<g font-family="Arial, Helvetica, sans-serif" fill="#182d35">
<text x="55" y="48" font-size="17" letter-spacing="2">FULCRUM / WORLDWIDE NATIONAL-GOVERNMENT SCREEN</text>
<text x="55" y="106" font-size="43" font-weight="600">Public documents: a starting point in at least 86 countries</text>
<text x="55" y="146" font-size="22" fill="#53636b">197 countries searched · selected sources verified · research conducted 31 October 2026</text>
${legend}
<g id="country-marks">${marks}</g>
<text x="55" y="997" font-size="22" font-weight="600">Of the 86: 46 have public-facing or regulatory workflows; 40 qualify through government operations.</text>
<text x="55" y="1032" font-size="19" fill="#53636b">Publication evidence, including historical manuals—not complete maps, current readiness or paying customers.</text>
<text x="55" y="1061" font-size="19" fill="#53636b">Unknown does not mean unsuitable. National level only. Small states shown as dots; other territories unclassified.</text>
<text x="55" y="1095" font-size="16" fill="#64747c">Source: Fulcrum 197-country screening and reviewed evidence · Boundaries/label points: Natural Earth (public domain)</text>
</g></svg>`;
fs.writeFileSync(path.join(here,'worldwide-findings.svg'),svg);
await sharp(Buffer.from(svg)).resize(2400).png().toFile(path.join(here,'worldwide-findings.png'));
const compact=rows.map(c=>({id:c.id,name:c.name,assessment:c.assessment,areas:c.verified_areas,services:c.verified_services,evidence:c.evidence.filter(e=>e.assessment===c.assessment).slice(0,2).map(e=>({title:e.title,url:e.url,finding:e.finding,limitations:e.limitations}))}));
const options=rows.map(c=>`<option value="${c.id}">${esc(c.name)}</option>`).join('');
const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fulcrum: worldwide publication evidence</title><style>
body{margin:0;background:#fff;color:#182d35;font:16px/1.55 Arial,Helvetica,sans-serif}main{max-width:1500px;margin:auto;padding:12px 20px 40px}svg{display:block;width:100%;height:auto}label{font-weight:600}select{font:inherit;padding:9px;margin:0 0 0 12px;max-width:100%}#detail{max-width:1000px;margin:16px 0}#detail h2{margin:8px 0;font-size:22px}a{color:#136b68}li{margin-bottom:14px}.selected{stroke:#122d36!important;stroke-width:2.4!important}p{margin:8px 0}footer{font-size:13px;color:#53636b;border-top:1px solid #e1e6e8;padding-top:12px}@media(max-width:600px){main{padding:8px 12px 24px}label{display:block}select{margin:6px 0;width:100%}svg{min-height:230px}}@media print{.controls,#detail,footer{display:none}main{padding:0}}
</style></head><body><main>${svg}<div class="controls"><label for="country">Inspect a country<select id="country"><option value="">Choose a country</option>${options}</select></label></div><section id="detail" aria-live="polite"><p>Select a country to inspect its saved evidence and limitations. Breadth is the number of areas with detailed examples actually inspected.</p></section><footer>Summary prepared 1 November 2026. <a href="one-pager.md">One-page summary</a> · <a href="../../process-mapper/survey/screening/countries.md">Complete country ledger</a> · <a href="../../process-mapper/survey/METHOD.md">Method</a>. Boundary depiction follows Natural Earth and does not express a position on territorial status.</footer></main>
<script>const countries=${JSON.stringify(compact).replace(/</g,'\\u003c')};const labels=${JSON.stringify(Object.fromEntries(Object.entries(palette).map(([k,v])=>[k,v.label])))};const select=document.getElementById('country');const detail=document.getElementById('detail');const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function show(id){select.value=id;document.querySelectorAll('.selected').forEach(el=>el.classList.remove('selected'));document.querySelectorAll('[data-country="'+id+'"]').forEach(el=>el.classList.add('selected'));const c=countries.find(c=>c.id===id);if(!c){detail.innerHTML='<p>Select a country to inspect its saved evidence and limitations.</p>';return;}detail.innerHTML='<h2>'+escape(c.name)+' — '+labels[c.assessment]+'</h2><p>Detailed examples inspected: '+c.services.length+' function(s), '+c.areas.length+' service area(s).</p>'+(c.evidence.length?'<ul>'+c.evidence.map(e=>'<li><a href="'+escape(e.url)+'" target="_blank" rel="noopener">'+escape(e.title)+'</a><p>'+escape(e.finding)+'</p><p><strong>Limitations:</strong> '+escape(e.limitations)+'</p></li>').join('')+'</ul>':'<p>Insufficient verified evidence to classify. This is not a finding that useful documents do not exist.</p>');}select.addEventListener('change',()=>show(select.value));document.querySelectorAll('[data-country]').forEach(el=>el.addEventListener('click',()=>show(el.dataset.country)));</script></body></html>`;
fs.writeFileSync(path.join(here,'worldwide-findings.html'),html);
fs.writeFileSync(path.join(here,'map-checks.json'),JSON.stringify({countries:rows.length,represented:represented.size,counts,small_state_markers:markerIds,source_date:'2026-10-31',prepared_at:'2026-11-01'},null,2)+'\n');
console.log(JSON.stringify({countries:rows.length,represented:represented.size,counts,small_state_markers:markerIds.length}));
