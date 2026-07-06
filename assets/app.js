/* ============ Enterprise AI AgentOps Platform · App (API 연동) ============ */

/* ---------- Icon system ---------- */
const ICONS = {
  grid:'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  bot:'<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4m0 0h3"/><circle cx="9" cy="14" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="14" r="1.2" fill="currentColor" stroke="none"/>',
  book:'<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
  git:'<circle cx="6" cy="6" r="2.6"/><circle cx="6" cy="18" r="2.6"/><circle cx="18" cy="9" r="2.6"/><path d="M6 8.6v6.8M18 11.6c0 3-2.5 4.4-6 4.4"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
  pulse:'<path d="M3 12h4l2.5-7 4 14 2.5-7H21"/>',
  spark:'<path d="M12 2l1.9 5.8L20 9.7l-5 3.9 1.8 6.2L12 16.3 7.2 19.8 9 13.6 4 9.7l6.1-1.9z"/>',
  menu:'<path d="M4 7h16M4 12h16M4 17h16"/>',
  chev:'<path d="M9 6l6 6-6 6"/>',
  plus:'<path d="M12 5v14M5 12h14"/>',
  bell:'<path d="M18 9a6 6 0 1 0-12 0c0 6-2.5 7.5-2.5 7.5h17S18 15 18 9z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
  chat:'<path d="M21 12a8 8 0 0 1-8 8H4l2-3.5A8 8 0 1 1 21 12z"/>',
  thumb:'<path d="M7 10v11H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h3zm0 0l4.2-7.5a1.8 1.8 0 0 1 3.3 1.2L13.8 8H19a2 2 0 0 1 2 2.4l-1.4 7A2 2 0 0 1 17.6 19H7"/>',
  copy:'<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
  coin:'<circle cx="12" cy="12" r="9"/><path d="M14.8 9.2a3 3 0 0 0-2.8-1.7c-1.7 0-3 1-3 2.25S10.3 11.5 12 12s3 1 3 2.25-1.3 2.25-3 2.25a3 3 0 0 1-2.8-1.7M12 5.5v2M12 16.5v2"/>',
  shield:'<path d="M12 2l8 3.5V11c0 5.2-3.4 8.9-8 11-4.6-2.1-8-5.8-8-11V5.5L12 2z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
  confluence:'<path d="M3 18c2.5-4.5 5-6 8.5-4.2L20 18M21 6c-2.5 4.5-5 6-8.5 4.2L4 6"/>',
  pdf:'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8.5 15.5h7M8.5 12.5h7"/>',
  excel:'<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
  image:'<rect x="3" y="3" width="18" height="18" rx="2.5"/><circle cx="9" cy="9" r="2"/><path d="M21 15l-5-5-9 9"/>',
  arrow:'<path d="M5 12h14M13 6l6 6-6 6"/>',
  cycle:'<path d="M21 12a9 9 0 1 1-2.6-6.4M21 3v5h-5"/>',
  star:'<path d="M12 2.8l2.5 5.9 6.4.5-4.9 4.2 1.5 6.2L12 16.3 6.5 19.6 8 13.4 3.1 9.2l6.4-.5z"/>',
  play:'<path d="M6 4l14 8-14 8z"/>',
  download:'<path d="M12 3v12m0 0l-4.5-4.5M12 15l4.5-4.5"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>',
  check:'<path d="M20 6L9 17l-5-5"/>',
  send:'<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
  trash:'<path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>',
  gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
};
function hydrateIcons(root=document){
  root.querySelectorAll('i[data-i]').forEach(el=>{
    const n = el.dataset.i;
    if(!ICONS[n] || el.dataset.done) return;
    el.dataset.done = '1';
    el.innerHTML = `<svg viewBox="0 0 24 24" width="100%" height="100%" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">${ICONS[n]}</svg>`;
  });
}
const I = n => `<i data-i="${n}"></i>`;

/* ---------- utils ---------- */
const $ = s => document.querySelector(s);
const esc = s => String(s??'').replace(/[&<>"']/g, m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const OFFLINE = location.protocol === 'file:';
async function api(path, opts={}){
  if(OFFLINE) throw new Error('offline');
  const res = await fetch(path, {headers:{'Content-Type':'application/json'}, ...opts,
    body: opts.body ? JSON.stringify(opts.body) : undefined});
  if(!res.ok){
    let msg = res.statusText;
    try{ msg = (await res.json()).detail || msg; }catch(e){}
    throw new Error(msg);
  }
  return res.json();
}
function toast(msg, kind='ok'){
  let box = $('#toasts');
  if(!box){ box = document.createElement('div'); box.id='toasts'; document.body.appendChild(box); }
  const t = document.createElement('div');
  t.className = `toast ${kind}`;
  t.innerHTML = (kind==='ok' ? '✅ ' : '⚠️ ') + esc(msg);
  box.appendChild(t);
  setTimeout(()=>t.remove(), 4200);
}
function timeAgo(s){
  if(!s) return '—';
  const d = (Date.now() - new Date(s.replace(' ','T')).getTime())/1000;
  if(d < 60) return '방금';
  if(d < 3600) return `${Math.floor(d/60)}분 전`;
  if(d < 86400) return `${Math.floor(d/3600)}시간 전`;
  return `${Math.floor(d/86400)}일 전`;
}
const stChip = s => ({'운영':'ok','검수':'warn','개발':'info','점검':'danger'}[s]||'gray');
const stars = n => n ? Array.from({length:5},(_,i)=>`<i data-i="star" style="${i<n?'':'opacity:.22'}"></i>`).join('') : '<span class="mini">미평가</span>';
const SRC_ICON = {confluence:['confluence','#2563eb'], pdf:['pdf','#e03131'], excel:['excel','#16a34a'], image:['image','#8b7cff']};
const PIPE_STAGES = ['추출','전처리','가공','적재'];

function sparkline(points, color='#4b5cff', w=140, h=32){
  const max = Math.max(...points), min = Math.min(...points);
  const rng = (max-min)||1, step = w/(points.length-1);
  const coords = points.map((p,i)=>[i*step, h-3-((p-min)/rng)*(h-8)]);
  const line = coords.map((c,i)=>(i?'L':'M')+c[0].toFixed(1)+' '+c[1].toFixed(1)).join(' ');
  const id = 'sg'+Math.random().toString(36).slice(2,7);
  return `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
    <defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${color}" stop-opacity=".25"/><stop offset="1" stop-color="${color}" stop-opacity="0"/>
    </linearGradient></defs>
    <path d="${line} L${w} ${h} L0 ${h} Z" fill="url(#${id})"/>
    <path d="${line}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round"/></svg>`;
}
function barsChart(vals, labels, color='#4b5cff', h=150){
  const max = Math.max(...vals, 1);
  return `<div style="display:flex;align-items:flex-end;gap:8px;height:${h}px;padding-top:8px">${
    vals.map((v,i)=>`<div style="display:flex;flex-direction:column;align-items:center;gap:7px;flex:1">
      <div style="width:100%;max-width:34px;height:${Math.max(4,(v/max)*(h-34))}px;border-radius:8px 8px 4px 4px;background:linear-gradient(180deg,${color},${color}88)" title="${v}"></div>
      <span style="font-size:10.5px;color:#8a90a8;font-weight:600">${esc(labels[i])}</span></div>`).join('')}</div>`;
}
function stagePills(current){
  const idx = current==='완료' ? 99 : PIPE_STAGES.indexOf(current);
  return `<div class="stages">${PIPE_STAGES.map((s,i)=>
    `<span class="stage-pill ${i<idx?'done':i===idx?'now':''}">${s}</span>${i<3?'<span class="stage-arrow">▸</span>':''}`
  ).join('')}<span class="stage-arrow">▸</span><span class="stage-pill ${current==='완료'?'done':''}">RAG 동기화</span></div>`;
}
const offlineCard = () => `
<div class="view"><div class="offline">
  <h3>⚡ 백엔드 서버(ITCEN-API)가 필요합니다</h3>
  <p>이 화면은 FastAPI 백엔드의 실데이터로 동작합니다.<br/>프로젝트 폴더에서 아래를 실행한 뒤 <b>http://localhost:8000</b> 으로 접속하세요.</p>
  <div class="code"><span class="c"># Windows</span>
run.bat
<span class="c"># 또는</span>
py -m uvicorn server.main:app --port 8000</div>
</div></div>`;

/* ---------- state ---------- */
const state = { agents:[], selBot:null, chat:{}, pollTimer:null };

async function loadAgents(){
  state.agents = await api('/itcen/agents');
  if(!state.selBot || !state.agents.find(a=>a.bot_type===state.selBot))
    state.selBot = state.agents[0]?.bot_type || null;
  const b = $('#agentCount'); if(b) b.textContent = state.agents.length;
  return state.agents;
}
const botSelect = (id) => `<select class="inp" id="${id}">${
  state.agents.map(a=>`<option value="${a.bot_type}" ${a.bot_type===state.selBot?'selected':''}>${esc(a.name)} · ${a.bot_type}</option>`).join('')}</select>`;

/* ============================================================
   VIEWS
============================================================ */
const VIEWS = {};
const BIND  = {};

/* ===== 대시보드 ===== */
VIEWS.dashboard = async () => {
  let usage=null, sources=[], jobs=[];
  try{
    [usage, sources, jobs] = await Promise.all([api('/itcen/ops/usage'), api('/itcen/knowledge/sources'), api('/itcen/ops/jobs')]);
    await loadAgents();
  }catch(e){ return offlineCard(); }
  const agents = state.agents;
  const chunks = sources.reduce((s,x)=>s+(x.chunks||0),0);
  const stuck = jobs.filter(j=>j.stuck).length;
  const logs = await api('/itcen/ops/logs?limit=6');
  const fly = [
    { ic:'book',  tint:'#8b7cff', h:'Knowledge', p:'흩어진 사내 지식을 RAG 파이프라인으로 정제 (추출→전처리→가공→적재)' },
    { ic:'gear',  tint:'#4b5cff', h:'Agent Config', p:'bot_type 하나로 System Prompt와 검색 범위를 빚어 봇의 성격을 결정' },
    { ic:'bot',   tint:'#12b886', h:'AI Agent로 수렴', p:'ITCEN-API(REST)로 형상을 호출해 Agent가 동작' },
    { ic:'pulse', tint:'#f59f00', h:'운영 신호 회귀', p:'로그·피드백·사용량이 콘솔로 돌아와 다음 개선의 출발점' },
  ];
  return `
<div class="view">
  <div class="banner" style="margin-bottom:22px">
    <h2>Enterprise AI AgentOps Platform</h2>
    <p style="max-width:760px">같은 구조의 전처리, 같은 기능의 도메인만 다른 Agent가 사내 프로젝트마다 반복 제작됩니다 — 운영 체계 부재가 만든 구조적 결과입니다.<br>
    <b style="color:#ffe28a">⇒ AI Ready Data 필요</b><br>
    AI 프로젝트를 3회 이상 수행한 결과, 과정은 늘 동일했습니다.</p>
    <p style="max-width:760px;margin-top:14px">AI Agent 구축보다 더 어려운 것은, 지속적인 운영입니다.<br>
    프로젝트마다 반복되는 전처리 과정 — 전처리 시간만 줄여도 구축 속도는 빨라집니다.<br>
    형상 관리되지 않는 프롬프트 — 어떻게 운영되고 있는지 모르는 수많은 Agent들이 남습니다.<br>
    <b style="color:#ffe28a">⇒ AgentOps 플랫폼 필요</b>
    <span style="opacity:.75;font-size:.9em">(Feat. 삼성전자 레퍼런스 참조)</span></p>
    <div style="display:flex;gap:8px;margin-top:16px;flex-wrap:wrap;position:relative">
      <span class="chip" style="background:rgba(255,255,255,.14);color:#e8eaff">✓ 실제 운영 환경에서 검증된 모델</span>
      <span class="chip" style="background:rgba(255,255,255,.14);color:#e8eaff">✓ 프로젝트마다 반복되던 전처리 제거</span>
      <span class="chip" style="background:rgba(255,255,255,.14);color:#e8eaff">✓ 프로젝트 단위 → 플랫폼 기반 운영</span>
    </div>
    <div class="bstats">
      <div class="s"><b>${agents.length}</b><span>등록 Agent</span></div>
      <div class="s"><b>${chunks.toLocaleString()}</b><span>지식 청크</span></div>
      <div class="s"><b>${usage.total_calls}</b><span>답변 로그</span></div>
      <div class="s"><b>${usage.satisfaction}%</b><span>만족도</span></div>
    </div>
  </div>

  <div class="grid kpis" style="margin-bottom:18px">
    ${[
      ['bot','#4b5cff', agents.length, '운영 중 AI Agent', agents.filter(a=>a.config_complete).length+'개 형상 완성'],
      ['book','#8b7cff', chunks.toLocaleString(), 'RAG 지식 청크', sources.length+'개 데이터 소스'],
      ['chat','#12b886', usage.total_calls, '누적 답변 처리', '평균 '+usage.avg_latency_ms+'ms'],
      ['shield','#f59f00', stuck, '멈춘 작업 (4h+)', stuck?'정리 필요':'정상'],
    ].map(k=>`
    <div class="kpi">
      <div class="kpi-ico" style="background:linear-gradient(135deg,${k[1]},${k[1]}cc)">${I(k[0])}</div>
      <div class="val">${k[2]}</div><div class="lbl">${k[3]}</div>
      <div class="mini" style="margin-top:8px">${k[4]}</div>
    </div>`).join('')}
  </div>

  <div class="card" style="margin-bottom:18px">
    <div class="card-head">
      <div><h3>하나의 콘솔 · 선순환 구조</h3><div class="sub">지식 → Config → Agent → 운영 신호 → 개선</div></div>
      <span class="chip brand">${I('cycle')} 실데이터 연동 중</span>
    </div>
    <div class="card-pad"><div class="flywheel">
      ${fly.map((f,i)=>`
      <div style="display:flex;align-items:center;gap:0">
        <div class="fw-node" style="flex:1">
          <div class="ic" style="background:linear-gradient(135deg,${f.tint},${f.tint}cc)">${I(f.ic)}</div>
          <h4>${f.h}</h4><p>${f.p}</p>
        </div>
        ${i<3?`<div class="fw-arrow">${I('arrow')}</div>`:''}
      </div>`).join('')}
    </div></div>
  </div>

  <div class="grid" style="grid-template-columns:1fr 1fr">
    <div class="card">
      <div class="card-head"><div><h3>지식 파이프라인 현황</h3><div class="sub">RAG Index 동기화 상태</div></div><a class="link" data-go="knowledge">전체 보기 ${I('chev')}</a></div>
      <div class="card-pad"><div class="pipe">
        ${sources.slice(0,4).map(p=>{
          const [ic,tint] = SRC_ICON[p.type]||['pdf','#888'];
          return `<div class="pipe-row">
          <div class="pipe-ico" style="background:linear-gradient(135deg,${tint},${tint}cc)">${I(ic)}</div>
          <div class="stack"><h5>${esc(p.name)}</h5><span class="m">${p.docs.toLocaleString()} 문서 · ${p.chunks.toLocaleString()} 청크</span></div>
          <span class="chip ${p.stage==='완료'?'ok':'info'}"><span class="cd"></span>${p.stage==='완료'?'동기화 완료':p.stage+' '+p.progress+'%'}</span>
        </div>`;}).join('')}
      </div></div>
    </div>
    <div class="card">
      <div class="card-head"><div><h3>최근 답변 로그</h3><div class="sub">운영 신호는 콘솔로 되돌아옵니다</div></div><a class="link" data-go="operations">운영 대시보드 ${I('chev')}</a></div>
      <div class="feed">
        ${logs.map(l=>`
        <div class="feed-item">
          <div class="feed-ic" style="background:${l.rating&&l.rating<=2?'#fa525218':'#4b5cff18'};color:${l.rating&&l.rating<=2?'#fa5252':'#4b5cff'}">${I('chat')}</div>
          <div style="flex:1"><div class="t"><b>${esc(l.bot_type)}</b> · ${esc(l.question)}</div>
          <div class="time">${timeAgo(l.created_at)} · ${l.latency_ms}ms ${l.improvement_queue?'· <b style="color:#e03131">개선 큐</b>':''}</div></div>
          <div class="rate">${stars(l.rating)}</div>
        </div>`).join('')}
      </div>
    </div>
  </div>
</div>`;
};

/* ===== Knowledge · RAG 파이프라인 ===== */
VIEWS.knowledge = async () => {
  let sources, rules, indexes;
  try{ [sources, rules, indexes] = await Promise.all([
    api('/itcen/knowledge/sources'), api('/itcen/knowledge/rules'), api('/itcen/knowledge/indexes')]);
  }catch(e){ return offlineCard(); }
  return `
<div class="view">
  <div class="page-head">
    <div><h1>RAG 데이터 파이프라인</h1><p>Confluence · PDF · Excel · 이미지를 <b>추출 → 전처리 → 가공 → 적재</b>로 정제해 RAG Index와 동기화합니다. 각 소스의 [동기화] 버튼으로 파이프라인을 실제 실행해 보세요.</p></div>
    <div class="head-actions"><button class="ghost-btn primary" id="addSourceBtn">${I('plus')} 데이터 소스 연결</button></div>
  </div>

  <div class="grid" style="grid-template-columns:2fr 1fr;margin-bottom:18px">
    <div class="card">
      <div class="card-head"><div><h3>데이터 소스 · 파이프라인</h3><div class="sub">단계별 진행 상황 (실시간 갱신)</div></div></div>
      <div class="card-pad"><div class="pipe" id="srcList">
        ${sources.map(p=>srcRow(p)).join('')}
      </div></div>
    </div>

    <div style="display:flex;flex-direction:column;gap:18px">
      <div class="card">
        <div class="card-head"><div><h3>가공 단계 출력 규칙</h3><div class="sub">캡셔닝·요약·구조화 등 모든 LLM 출력에 강제 적용</div></div></div>
        <div class="card-pad">
          ${rules.map(r=>`<div style="display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-bottom:1px solid var(--line);font-size:12.5px;line-height:1.55">
            <span style="color:var(--ok);flex:0 0 16px;margin-top:1px">${I('check')}</span>${esc(r)}</div>`).join('')}
          <p class="mini" style="margin-top:12px;line-height:1.5">규칙 위반 출력은 적재 전 자동 반려되어 재생성됩니다.</p>
        </div>
      </div>
      <div class="card">
        <div class="card-head"><div><h3>RAG Index 현황</h3><div class="sub">Agent Config의 검색 범위로 연결됩니다</div></div></div>
        <table class="tbl">
          <thead><tr><th>Index</th><th>청크</th><th>사용 봇</th></tr></thead>
          <tbody>${indexes.map(x=>`<tr>
            <td><span class="tag v">${esc(x.index_name)}</span></td>
            <td class="mono">${(x.chunks||0).toLocaleString()}</td>
            <td>${x.used_by.length?x.used_by.map(b=>`<span class="tag">${esc(b)}</span>`).join(''):'<span class="muted">—</span>'}</td>
          </tr>`).join('')}</tbody>
        </table>
      </div>
    </div>
  </div>
</div>`;
};
function srcRow(p){
  const [ic,tint] = SRC_ICON[p.type]||['pdf','#888'];
  const running = p.stage!=='완료' && p.stage!=='대기';
  return `<div class="pipe-row" data-src="${p.id}" style="flex-wrap:wrap">
    <div class="pipe-ico" style="background:linear-gradient(135deg,${tint},${tint}cc)">${I(ic)}</div>
    <div class="stack" style="flex:1;min-width:200px">
      <h5>${esc(p.name)}</h5>
      <span class="m">${p.docs.toLocaleString()} 문서 · ${p.chunks.toLocaleString()} 청크 · ${I('cycle')} ${timeAgo(p.last_sync)} → <span class="tag v" style="margin:0">${esc(p.index_name)}</span></span>
    </div>
    <button class="ghost-btn sync-btn" data-id="${p.id}" style="height:32px;font-size:12px" ${running?'disabled':''}>
      ${running?'실행 중…':I('play')+' 동기화'}</button>
    <div style="flex-basis:100%;margin-top:10px">${stagePills(p.stage)}
      <div class="bar" style="margin-top:8px"><span style="width:${p.progress}%"></span></div>
    </div>
  </div>`;
}
BIND.knowledge = () => {
  wrap.querySelectorAll('.sync-btn').forEach(b=>b.addEventListener('click', async ()=>{
    b.disabled = true; b.textContent = '실행 중…';
    try{
      await api(`/itcen/knowledge/sources/${b.dataset.id}/sync`, {method:'POST'});
      toast('파이프라인 실행: 추출 → 전처리 → 가공 → 적재');
      startKnowledgePoll();
    }catch(e){ toast(e.message,'err'); b.disabled=false; }
  }));
  const addBtn = $('#addSourceBtn');
  if(addBtn) addBtn.addEventListener('click', openSourceModal);
  // 진행 중 소스가 있으면 폴링
  if(wrap.querySelector('.sync-btn[disabled]')) startKnowledgePoll();
};
function startKnowledgePoll(){
  clearInterval(state.pollTimer);
  state.pollTimer = setInterval(async ()=>{
    if(current!=='knowledge') return clearInterval(state.pollTimer);
    try{
      const sources = await api('/itcen/knowledge/sources');
      const list = $('#srcList');
      if(list){ list.innerHTML = sources.map(srcRow).join(''); hydrateIcons(list); BIND.knowledge(); }
      if(!sources.some(s=>s.stage!=='완료' && s.stage!=='대기')) clearInterval(state.pollTimer);
    }catch(e){ clearInterval(state.pollTimer); }
  }, 1200);
}
function openSourceModal(){
  openModal(`
    <div class="modal-head"><h3>데이터 소스 연결</h3><button class="x" data-close>✕</button></div>
    <div class="modal-body">
      <div class="form-row"><label>소스 이름</label><input class="inp" id="srcName" placeholder="예: 신제품 매뉴얼 PDF"/></div>
      <div class="form-2">
        <div class="form-row"><label>유형</label>
          <select class="inp" id="srcType"><option value="confluence">Confluence</option><option value="pdf">PDF</option><option value="excel">Excel</option><option value="image">이미지</option></select></div>
        <div class="form-row"><label>문서 수 <small>(시뮬레이션)</small></label><input class="inp" id="srcDocs" type="number" value="24"/></div>
      </div>
      <div class="form-row"><label>적재 대상 RAG Index</label><input class="inp" id="srcIndex" placeholder="예: product-manual"/>
        <p class="hint">같은 index_name을 쓰는 봇의 검색 범위에 즉시 반영됩니다.</p></div>
    </div>
    <div class="modal-foot"><span></span>
      <button class="ghost-btn primary" id="srcSave">${I('check')} 연결 후 파이프라인 실행</button></div>`);
  $('#srcSave').addEventListener('click', async ()=>{
    try{
      const r = await api('/itcen/knowledge/sources', {method:'POST', body:{
        name: $('#srcName').value||'새 데이터 소스', type: $('#srcType').value,
        index_name: $('#srcIndex').value||'default-index', docs: +$('#srcDocs').value||10 }});
      await api(`/itcen/knowledge/sources/${r.id}/sync`, {method:'POST'});
      closeModal(); toast('소스 연결 완료 — 파이프라인 실행 중'); go('knowledge');
    }catch(e){ toast(e.message,'err'); }
  });
}

/* ===== Agent Config ===== */
VIEWS.agents = async () => {
  try{ await loadAgents(); }catch(e){ return offlineCard(); }
  return `
<div class="view">
  <div class="page-head">
    <div><h1>AI Agent Config</h1>
      <p><b>bot_type</b>은 봇을 가리키는 고유 key id입니다. 에이전트를 만들 때 정한 이 키에 <b>System Prompt(말투·역할)</b>와 <b>벡터 검색 설정(지식 범위)</b>이 각각 매달립니다. 따라서 ①에이전트 → ②프롬프트 → ③검색 설정 순서로 진행하며, 외부에서 봇을 호출할 때도 bot_type으로 식별합니다.</p></div>
    <div class="head-actions"><button class="ghost-btn primary" id="wizBtn">${I('plus')} 새 Agent 생성 (3단계)</button></div>
  </div>

  <div class="grid" style="grid-template-columns:repeat(3,1fr);margin-bottom:18px">
    ${[['① 에이전트 생성','bot_type 키를 정하고 이름·도메인·담당자를 등록','bot','#4b5cff'],
       ['② System Prompt','말투와 역할 정의 — 버전으로 형상관리','git','#8b7cff'],
       ['③ 벡터 검색 설정','RAG Index와 검색 정책으로 지식 범위 결정','search','#12b886']]
    .map(s=>`<div class="kpi" style="display:flex;gap:14px;align-items:flex-start">
      <div class="kpi-ico" style="margin:0;background:linear-gradient(135deg,${s[3]},${s[3]}cc)">${I(s[2])}</div>
      <div><b style="font-size:14px">${s[0]}</b><p class="mini" style="margin-top:4px;line-height:1.5">${s[1]}</p></div>
    </div>`).join('')}
  </div>

  <div class="card">
    <table class="tbl">
      <thead><tr><th>Agent</th><th>bot_type (key)</th><th>도메인</th><th>형상</th><th>Prompt</th><th>Index</th><th>호출</th><th>만족도</th><th>상태</th><th></th></tr></thead>
      <tbody>
        ${state.agents.map(a=>`
        <tr>
          <td><div class="flex">
            <div class="ag-ico" style="background:linear-gradient(135deg,${a.tint},${a.tint}cc)">${a.icon}</div>
            <div class="stack"><span class="name">${esc(a.name)}</span><span class="muted">${esc(a.owner||'—')}</span></div>
          </div></td>
          <td><span class="key-badge">${esc(a.bot_type)}</span></td>
          <td>${esc(a.domain||'—')}</td>
          <td>${a.config_complete
              ?'<span class="chip ok">'+'✓ 완성 (3/3)'+'</span>'
              :'<span class="chip warn">미완성 '+(a.prompt_version?'2':'1')+'/3</span>'}</td>
          <td>${a.prompt_version?`<span class="tag v">${a.prompt_version}</span><div class="mini">${timeAgo(a.prompt_updated)}</div>`:'<span class="muted">—</span>'}</td>
          <td>${a.index_name?`<span class="tag v">${esc(a.index_name)}</span>`:'<span class="muted">—</span>'}</td>
          <td class="mono">${a.calls}</td>
          <td>${a.satisfaction!=null?`<div class="flex" style="gap:8px;min-width:100px"><div class="bar" style="flex:1"><span style="width:${a.satisfaction}%"></span></div><b style="font-size:12px">${a.satisfaction}%</b></div>`:'<span class="muted">—</span>'}</td>
          <td><span class="chip ${stChip(a.status)}"><span class="cd"></span>${a.status}</span></td>
          <td><button class="ghost-btn del-agent" data-bt="${a.bot_type}" title="삭제" style="height:30px;padding:0 9px">${I('trash')}</button></td>
        </tr>`).join('')}
      </tbody>
    </table>
  </div>
</div>`;
};
BIND.agents = () => {
  $('#wizBtn')?.addEventListener('click', openWizard);
  wrap.querySelectorAll('.del-agent').forEach(b=>b.addEventListener('click', async ()=>{
    if(!confirm(`'${b.dataset.bt}' 에이전트와 연결된 프롬프트·검색 설정을 모두 삭제할까요?`)) return;
    try{ await api(`/itcen/agents/${b.dataset.bt}`, {method:'DELETE'}); toast('삭제 완료'); go('agents'); }
    catch(e){ toast(e.message,'err'); }
  }));
};

/* ----- 3단계 생성 위저드 ----- */
function openWizard(){
  const wiz = { step:1, agent:{}, prompt:'', cfg:{} };
  const PROMPT_TMPL = `당신은 (역할)을 돕는 어시스턴트입니다.
- 모든 답변은 한국어로 작성한다.
- 불필요한 서론·결론·인사말을 포함하지 않는다.
- 사실 위주의 건조하고 명확한 문장으로 답한다.
- 근거 문서를 찾지 못하면 추측하지 않고 담당 채널을 안내한다.`;
  function render(){
    const s = wiz.step;
    openModal(`
    <div class="modal-head"><h3>새 Agent 생성</h3><button class="x" data-close>✕</button></div>
    <div class="modal-body">
      <div class="steps">
        <div class="step ${s===1?'on':s>1?'done':''}">① 에이전트 생성<small>bot_type 키 확정</small></div>
        <div class="step ${s===2?'on':s>2?'done':''}">② System Prompt<small>말투·역할</small></div>
        <div class="step ${s===3?'on':''}">③ 벡터 검색 설정<small>지식 범위</small></div>
      </div>
      ${s===1?`
        <div class="form-2">
          <div class="form-row"><label>bot_type <small>고유 key id · 소문자/숫자/하이픈</small></label>
            <input class="inp mono" id="wBt" placeholder="finance-report" value="${esc(wiz.agent.bot_type||'')}"/>
            <p class="hint">이 키에 프롬프트·검색 설정이 매달리며, 외부 호출 시 봇 식별자로 사용됩니다.</p></div>
          <div class="form-row"><label>이름</label><input class="inp" id="wName" placeholder="재무 리포트 Agent" value="${esc(wiz.agent.name||'')}"/></div>
        </div>
        <div class="form-2">
          <div class="form-row"><label>도메인</label><input class="inp" id="wDom" placeholder="재무" value="${esc(wiz.agent.domain||'')}"/></div>
          <div class="form-row"><label>담당자</label><input class="inp" id="wOwner" placeholder="이도현" value="${esc(wiz.agent.owner||'')}"/></div>
        </div>
        <div class="form-row"><label>설명</label><input class="inp" id="wDesc" placeholder="월별 재무 리포트 질의응답" value="${esc(wiz.agent.description||'')}"/></div>
        <div class="form-2">
          <div class="form-row"><label>아이콘</label>
            <select class="inp" id="wIcon">${['🤖','💰','📊','🧾','🏦','📈','🛠️','📦'].map(x=>`<option ${wiz.agent.icon===x?'selected':''}>${x}</option>`).join('')}</select></div>
          <div class="form-row"><label>테마 색</label>
            <select class="inp" id="wTint">${[['#4b5cff','블루'],['#12b886','그린'],['#8b7cff','퍼플'],['#f59f00','앰버'],['#fa5252','레드'],['#3b9dff','스카이']]
              .map(x=>`<option value="${x[0]}" ${wiz.agent.tint===x[0]?'selected':''}>${x[1]}</option>`).join('')}</select></div>
        </div>`
      : s===2?`
        <div class="form-row"><label>System Prompt <small>bot_type: <b class="mono">${esc(wiz.agent.bot_type)}</b> 에 v1.0으로 기록됩니다</small></label>
          <textarea class="inp" id="wPrompt">${esc(wiz.prompt||PROMPT_TMPL)}</textarea>
          <p class="hint">가공 파이프라인과 동일한 출력 규칙(한국어·서론/결론/추측 금지·건조하고 명확한 문장)이 기본 포함되어 있습니다.</p></div>`
      : `
        <div class="form-row"><label>RAG Index <small>지식 범위</small></label>
          <input class="inp mono" id="wIndex" placeholder="hr-knowledge" value="${esc(wiz.cfg.index_name||'')}"/>
          <p class="hint">Knowledge 메뉴의 Index 이름과 일치해야 검색이 동작합니다. (예: hr-knowledge, sales-docs, product-manual, security-policy, dev-wiki)</p></div>
        <div class="form-2">
          <div class="form-row"><label>Top-K: <b id="wTkV">${wiz.cfg.top_k||5}</b></label>
            <input type="range" id="wTk" min="1" max="20" value="${wiz.cfg.top_k||5}" style="--p:${((wiz.cfg.top_k||5)-1)/19*100}%"/></div>
          <div class="form-row"><label>유사도 임계값: <b id="wThV">${wiz.cfg.similarity_threshold||0.72}</b></label>
            <input type="range" id="wTh" min="50" max="95" value="${(wiz.cfg.similarity_threshold||0.72)*100}" style="--p:${(((wiz.cfg.similarity_threshold||0.72)*100)-50)/45*100}%"/></div>
        </div>
        ${[['rerank','Re-ranking (Cross-Encoder)',true],['citation_required','출처 인용 강제',true],['pii_masking','PII 마스킹',true],['multi_query','멀티-쿼리 확장',false]]
          .map(t=>`<div class="cfg-row" style="padding:12px 0">
            <div class="stack"><h5>${t[1]}</h5></div>
            <div class="switch wsw ${ (wiz.cfg[t[0]] ?? t[2]) ?'on':''}" data-k="${t[0]}"></div></div>`).join('')}`
      }
    </div>
    <div class="modal-foot">
      ${s>1?`<button class="ghost-btn" id="wPrev">← 이전</button>`:'<span></span>'}
      <button class="ghost-btn primary" id="wNext">${s<3?'다음 →':I('check')+' 생성 완료 (형상 3/3 등록)'}</button>
    </div>`);
    // bind
    if(s===3){
      const tk=$('#wTk'), th=$('#wTh');
      tk.addEventListener('input',()=>{ $('#wTkV').textContent=tk.value; tk.style.setProperty('--p',((tk.value-1)/19*100)+'%'); });
      th.addEventListener('input',()=>{ $('#wThV').textContent=(th.value/100).toFixed(2); th.style.setProperty('--p',((th.value-50)/45*100)+'%'); });
      wrapModal().querySelectorAll('.wsw').forEach(sw=>sw.addEventListener('click',()=>sw.classList.toggle('on')));
    }
    $('#wPrev')?.addEventListener('click',()=>{ save(); wiz.step--; render(); });
    $('#wNext').addEventListener('click', async ()=>{
      save();
      if(wiz.step===1){
        if(!/^[a-z0-9\-]{3,40}$/.test(wiz.agent.bot_type||'')) return toast('bot_type은 소문자·숫자·하이픈 3~40자입니다','err');
        if(!wiz.agent.name) return toast('이름을 입력하세요','err');
        wiz.step=2; return render();
      }
      if(wiz.step===2){
        if(!wiz.prompt.trim()) return toast('System Prompt를 입력하세요','err');
        wiz.step=3; return render();
      }
      if(!wiz.cfg.index_name) return toast('RAG Index를 입력하세요','err');
      try{
        await api('/itcen/agents',{method:'POST', body: wiz.agent});
        await api(`/itcen/agents/${wiz.agent.bot_type}/prompt`,{method:'PUT', body:{content:wiz.prompt, message:'최초 등록 (위저드)', author:wiz.agent.owner||'admin'}});
        await api(`/itcen/agents/${wiz.agent.bot_type}/rag-config`,{method:'PUT', body: wiz.cfg});
        closeModal();
        toast(`'${wiz.agent.bot_type}' 형상 3/3 등록 완료 — 즉시 호출 가능`);
        state.selBot = wiz.agent.bot_type;
        go('agents');
      }catch(e){ toast(e.message,'err'); }
    });
    function save(){
      if(wiz.step===1) wiz.agent = { bot_type:$('#wBt')?.value.trim(), name:$('#wName')?.value.trim(),
        domain:$('#wDom')?.value.trim(), owner:$('#wOwner')?.value.trim(), description:$('#wDesc')?.value.trim(),
        icon:$('#wIcon')?.value, tint:$('#wTint')?.value };
      if(wiz.step===2 && $('#wPrompt')) wiz.prompt = $('#wPrompt').value;
      if(wiz.step===3 && $('#wIndex')) wiz.cfg = { index_name:$('#wIndex').value.trim(), top_k:+$('#wTk').value,
        similarity_threshold:+($('#wTh').value/100).toFixed(2), bm25_weight:0.3,
        rerank: sw('rerank'), citation_required: sw('citation_required'),
        pii_masking: sw('pii_masking'), multi_query: sw('multi_query') };
      function sw(k){ const el = wrapModal()?.querySelector(`.wsw[data-k="${k}"]`); return el?el.classList.contains('on'):true; }
    }
  }
  render();
}

/* ===== System Prompt 형상관리 ===== */
VIEWS.prompts = async () => {
  try{ await loadAgents(); }catch(e){ return offlineCard(); }
  if(!state.selBot) return `<div class="view"><div class="offline"><h3>등록된 에이전트가 없습니다</h3><p>먼저 Agent Config에서 에이전트를 생성하세요.</p></div></div>`;
  const [detail, versions] = await Promise.all([
    api(`/itcen/agents/${state.selBot}`), api(`/itcen/agents/${state.selBot}/prompts`)]);
  const active = versions[0];
  return `
<div class="view">
  <div class="page-head">
    <div><h1>System Prompt 형상관리</h1><p>프롬프트를 코드처럼 버전으로 기록합니다. 저장 즉시 새 버전이 생성되고, <span class="mono">GET /agent/prompt/{bot_type}</span> 으로 외부에 제공됩니다.</p></div>
    <div class="head-actions">${botSelect('botSel')}</div>
  </div>
  <div class="toolbar">
    <span class="key-badge">bot_type: ${esc(state.selBot)}</span>
    <span class="chip brand">active → ${active?active.version:'없음'}</span>
    <span class="chip gray">외부 제공: <span class="mono" style="margin-left:4px">GET /agent/prompt/${esc(state.selBot)}</span></span>
  </div>

  <div class="grid" style="grid-template-columns:1.2fr 1fr">
    <div class="card">
      <div class="card-head"><div><h3>System Prompt 편집</h3><div class="sub">저장하면 새 버전으로 기록됩니다 (롤백 = 과거 버전 내용으로 재저장)</div></div></div>
      <div class="card-pad">
        <div class="form-row"><textarea class="inp" id="pContent" style="height:300px">${esc(active?active.content:'')}</textarea></div>
        <div class="form-2">
          <div class="form-row"><label>변경 메시지</label><input class="inp" id="pMsg" placeholder="예: 연차 규정 최신화 반영"/></div>
          <div class="form-row"><label>작성자</label><input class="inp" id="pAuthor" value="${esc(detail.owner||'admin')}"/></div>
        </div>
        <button class="ghost-btn primary" id="pSave">${I('git')} 새 버전으로 저장</button>
      </div>
    </div>
    <div class="card">
      <div class="card-head"><div><h3>버전 히스토리</h3><div class="sub">${esc(state.selBot)} · ${versions.length}개 버전</div></div></div>
      <div class="card-pad"><div class="vtree">
        ${versions.map((v,i)=>`
        <div class="vrow">
          <div class="vrail"><div class="vdot ${i===0?'tag':''}"></div></div>
          <div class="vcard">
            <div class="vh"><span class="vmsg">${esc(v.message||'변경')}</span><span class="tag v">${v.version}</span></div>
            <div class="vmeta"><span>👤 ${esc(v.author||'—')}</span><span>🕐 ${timeAgo(v.created_at)}</span>
              ${i===0?'<span class="chip ok" style="font-size:10.5px;padding:1px 8px">active</span>'
                     :`<button class="ghost-btn rollback" data-id="${v.id}" style="height:24px;font-size:11px;padding:0 9px">이 버전으로 롤백</button>`}</div>
          </div>
        </div>`).join('')}
      </div></div>
    </div>
  </div>
</div>`;
};
BIND.prompts = () => {
  $('#botSel')?.addEventListener('change', e=>{ state.selBot = e.target.value; go('prompts'); });
  $('#pSave')?.addEventListener('click', async ()=>{
    try{
      const r = await api(`/itcen/agents/${state.selBot}/prompt`, {method:'PUT', body:{
        content: $('#pContent').value, message: $('#pMsg').value||'변경 사항', author: $('#pAuthor').value||'admin'}});
      toast(`${r.version} 배포 — GET /agent/prompt/${state.selBot} 에 즉시 반영`);
      go('prompts');
    }catch(e){ toast(e.message,'err'); }
  });
  wrap.querySelectorAll('.rollback').forEach(b=>b.addEventListener('click', async ()=>{
    const versions = await api(`/itcen/agents/${state.selBot}/prompts`);
    const v = versions.find(x=>x.id==b.dataset.id);
    if(!v) return;
    try{
      const r = await api(`/itcen/agents/${state.selBot}/prompt`, {method:'PUT', body:{
        content: v.content, message: `롤백 ← ${v.version} (${v.message||''})`, author:'admin'}});
      toast(`${v.version} 내용으로 롤백 → 새 버전 ${r.version}`);
      go('prompts');
    }catch(e){ toast(e.message,'err'); }
  }));
};

/* ===== 벡터 검색 설정 ===== */
VIEWS.search = async () => {
  try{ await loadAgents(); }catch(e){ return offlineCard(); }
  if(!state.selBot) return `<div class="view"><div class="offline"><h3>등록된 에이전트가 없습니다</h3><p>먼저 Agent Config에서 에이전트를 생성하세요.</p></div></div>`;
  let cfg;
  try{ cfg = await api(`/agent/rag-config/${state.selBot}`); }
  catch(e){ cfg = {index_name:'', top_k:5, similarity_threshold:0.72, bm25_weight:0.3, rerank:true, citation_required:true, pii_masking:true, multi_query:false}; }
  const idx = await api('/itcen/knowledge/indexes');
  return `
<div class="view">
  <div class="page-head">
    <div><h1>벡터 검색 설정</h1><p>bot_type의 지식 범위(RAG Index)와 검색 정책을 중앙에서 관리합니다. 저장 즉시 <span class="mono">GET /agent/rag-config/{bot_type}</span> 과 <span class="mono">POST /agent/chat</span> 동작에 반영됩니다.</p></div>
    <div class="head-actions">${botSelect('botSel')}</div>
  </div>
  <div class="toolbar">
    <span class="key-badge">bot_type: ${esc(state.selBot)}</span>
    <span class="chip gray">외부 제공: <span class="mono" style="margin-left:4px">GET /agent/rag-config/${esc(state.selBot)}</span></span>
  </div>

  <div class="grid" style="grid-template-columns:1.3fr 1fr">
    <div class="card">
      <div class="card-head"><div><h3>검색 파라미터</h3></div>
        <button class="ghost-btn primary" id="cfgSave" style="height:34px">${I('check')} 저장 · 즉시 반영</button></div>
      <div class="cfg-row">
        <div class="stack"><h5>RAG Index (지식 범위)</h5><p>Knowledge 파이프라인이 적재한 인덱스를 선택합니다</p></div>
        <select class="inp" id="cIndex" style="min-width:200px">
          ${idx.map(x=>`<option ${x.index_name===cfg.index_name?'selected':''}>${esc(x.index_name)}</option>`).join('')}
        </select>
      </div>
      <div class="cfg-row">
        <div class="stack"><h5>Top-K: <b id="cTkV">${cfg.top_k}</b></h5><p>검색해 컨텍스트에 넣을 문서 수</p></div>
        <div class="slider-wrap"><input type="range" id="cTk" min="1" max="20" value="${cfg.top_k}" style="--p:${(cfg.top_k-1)/19*100}%"/></div>
      </div>
      <div class="cfg-row">
        <div class="stack"><h5>유사도 임계값: <b id="cThV">${cfg.similarity_threshold}</b></h5><p>이 값 미만의 문서는 컨텍스트에서 제외</p></div>
        <div class="slider-wrap"><input type="range" id="cTh" min="50" max="95" value="${cfg.similarity_threshold*100}" style="--p:${(cfg.similarity_threshold*100-50)/45*100}%"/></div>
      </div>
      <div class="cfg-row">
        <div class="stack"><h5>하이브리드 가중치 (BM25): <b id="cBmV">${cfg.bm25_weight}</b></h5><p>키워드 매칭 비중 — 나머지는 Vector</p></div>
        <div class="slider-wrap"><input type="range" id="cBm" min="0" max="100" value="${cfg.bm25_weight*100}" style="--p:${cfg.bm25_weight*100}%"/></div>
      </div>
      ${[['rerank','Re-ranking (Cross-Encoder)','1차 검색 결과를 재정렬해 상위 정확도 개선'],
         ['citation_required','출처 인용 강제','근거 미발견 시 추측 대신 정보 없음 반환'],
         ['pii_masking','PII 마스킹','응답 내 전화번호·이메일·주민번호 자동 마스킹'],
         ['multi_query','멀티-쿼리 확장','질문을 하위 질의로 확장 (비용 증가)']]
      .map(t=>`<div class="cfg-row">
        <div class="stack"><h5>${t[1]}</h5><p>${t[2]}</p></div>
        <div class="switch csw ${cfg[t[0]]?'on':''}" data-k="${t[0]}"></div></div>`).join('')}
    </div>

    <div style="display:flex;flex-direction:column;gap:18px">
      <div class="card">
        <div class="card-head"><div><h3>설정 미리보기 (JSON)</h3><div class="sub">외부 Agent가 받는 실제 응답</div></div></div>
        <div class="card-pad"><div class="code" id="cfgPreview"></div></div>
      </div>
      <div class="card card-pad" style="background:linear-gradient(135deg,#f6f4ff,#eef1ff);border-color:#ddd9ff">
        <div class="flex" style="align-items:flex-start;gap:13px">
          <div class="pipe-ico" style="background:var(--grad)">${I('spark')}</div>
          <div><b style="font-size:13.5px">저장 = 배포</b>
            <p class="mini" style="margin-top:5px;line-height:1.55">이 화면의 저장은 실제 형상 저장입니다. 저장 직후 ITCEN-API의 <span class="mono">/agent/chat</span> 호출부터 새 설정이 적용됩니다. Chat 테스트 메뉴에서 바로 확인해 보세요.</p></div>
        </div>
      </div>
    </div>
  </div>
</div>`;
};
BIND.search = () => {
  $('#botSel')?.addEventListener('change', e=>{ state.selBot = e.target.value; go('search'); });
  const tk=$('#cTk'), th=$('#cTh'), bm=$('#cBm');
  const upd = ()=>{
    $('#cTkV').textContent = tk.value;
    $('#cThV').textContent = (th.value/100).toFixed(2);
    $('#cBmV').textContent = (bm.value/100).toFixed(1);
    tk.style.setProperty('--p',((tk.value-1)/19*100)+'%');
    th.style.setProperty('--p',((th.value-50)/45*100)+'%');
    bm.style.setProperty('--p',bm.value+'%');
    preview();
  };
  [tk,th,bm].forEach(x=>x.addEventListener('input',upd));
  wrap.querySelectorAll('.csw').forEach(sw=>sw.addEventListener('click',()=>{ sw.classList.toggle('on'); preview(); }));
  $('#cIndex').addEventListener('change', preview);
  function body(){
    const sw = k => wrap.querySelector(`.csw[data-k="${k}"]`).classList.contains('on');
    return { index_name:$('#cIndex').value, top_k:+tk.value,
      similarity_threshold:+(th.value/100).toFixed(2), bm25_weight:+(bm.value/100).toFixed(2),
      rerank:sw('rerank'), citation_required:sw('citation_required'),
      pii_masking:sw('pii_masking'), multi_query:sw('multi_query') };
  }
  function preview(){
    const b = {bot_type: state.selBot, ...body()};
    $('#cfgPreview').textContent = JSON.stringify(b, null, 2);
  }
  preview();
  $('#cfgSave').addEventListener('click', async ()=>{
    try{
      await api(`/itcen/agents/${state.selBot}/rag-config`, {method:'PUT', body: body()});
      toast(`'${state.selBot}' 검색 설정 저장 — /agent/chat 에 즉시 반영`);
    }catch(e){ toast(e.message,'err'); }
  });
};

/* ===== 운영 대시보드 ===== */
VIEWS.operations = async () => {
  let usage, logs, jobs;
  try{ [usage, logs, jobs] = await Promise.all([
    api('/itcen/ops/usage'), api('/itcen/ops/logs?limit=12'), api('/itcen/ops/jobs')]); }
  catch(e){ return offlineCard(); }
  const stuck = jobs.filter(j=>j.stuck);
  const days = usage.daily.map(d=>d.day.slice(5));
  return `
<div class="view">
  <div class="page-head">
    <div><h1>운영 대시보드</h1><p>답변 로그·사용자 피드백·사용량 트렌드를 모니터링하고, 개선 신호를 다시 콘솔로 되돌립니다. <b>4시간 이상 running 상태로 멈춘 작업은 강제 종료</b>할 수 있습니다.</p></div>
    <div class="head-actions">
      <button class="ghost-btn" id="simStuck">${I('plus')} 멈춘 작업 재현(데모)</button>
      <button class="ghost-btn primary" id="cleanup">${I('shield')} 멈춘 작업 정리 ${stuck.length?`(${stuck.length}건)`:''}</button>
    </div>
  </div>

  <div class="grid kpis" style="margin-bottom:18px">
    ${[
      ['chat','#4b5cff', usage.total_calls, '누적 답변 수'],
      ['clock','#12b886', usage.avg_latency_ms+'ms', '평균 응답 시간'],
      ['thumb','#f59f00', usage.satisfaction+'%', '만족도 (피드백 기반)'],
      ['shield','#fa5252', stuck.length+'건', '멈춘 작업 (4h+ running)'],
    ].map(k=>`<div class="kpi">
      <div class="kpi-ico" style="background:linear-gradient(135deg,${k[1]},${k[1]}cc)">${I(k[0])}</div>
      <div class="val">${k[2]}</div><div class="lbl">${k[3]}</div></div>`).join('')}
  </div>

  <div class="grid" style="grid-template-columns:1.5fr 1fr;margin-bottom:18px">
    <div class="card">
      <div class="card-head"><div><h3>답변 로그 & 피드백</h3><div class="sub">★2 이하는 개선 큐로 자동 이관 · Chat 테스트에서 보낸 대화도 여기 기록됩니다</div></div></div>
      ${logs.map(l=>`
      <div class="log-item" style="${l.improvement_queue?'background:rgba(250,82,82,.04)':''}">
        <div>
          <div class="log-q">Q. ${esc(l.question)}</div>
          <div class="log-a">${esc(l.answer).slice(0,220)}${l.answer.length>220?'…':''}</div>
          <div class="log-meta">
            <span class="tag">${esc(l.bot_type)}</span>
            <span class="chip ${l.citations.length?'ok':'danger'}" style="font-size:10.5px">${l.citations.length?'✓ 출처 '+l.citations.length+'건':'✕ 인용 실패'}</span>
            <span class="mini">⏱ ${l.latency_ms}ms</span><span class="mini">${timeAgo(l.created_at)}</span>
            ${l.improvement_queue?'<span class="chip warn" style="font-size:10.5px">개선 큐 이관</span>':''}
            ${l.feedback?`<span class="mini">💬 ${esc(l.feedback)}</span>`:''}
          </div>
        </div>
        <div class="rate">${stars(l.rating)}</div>
      </div>`).join('')}
    </div>

    <div style="display:flex;flex-direction:column;gap:18px">
      <div class="card">
        <div class="card-head"><div><h3>실행 작업</h3><div class="sub">4시간 초과 running = 멈춤으로 판정</div></div></div>
        <div class="card-pad">
          ${jobs.slice(0,8).map(j=>`
          <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)">
            <div class="stack" style="flex:1"><b style="font-size:12.5px">${esc(j.name)}</b>
              <span class="mini mono">${j.status==='running'?`실행 ${j.running_for_min}분`:j.status} ${j.bot_type?'· '+esc(j.bot_type):''}</span></div>
            <span class="chip ${j.stuck?'danger':j.status==='running'?'info':j.status==='killed'?'warn':'ok'}" style="font-size:10.5px">
              ${j.stuck?'멈춤 (4h+)':j.status==='running'?'실행 중':j.status==='killed'?'강제 종료됨':'완료'}</span>
          </div>`).join('')}
        </div>
      </div>
      <div class="card">
        <div class="card-head"><div><h3>일별 사용량</h3></div></div>
        <div class="card-pad">${barsChart(usage.daily.map(d=>d.calls), days, '#4b5cff', 130)}</div>
      </div>
      <div class="card">
        <div class="card-head"><div><h3>봇별 호출</h3></div></div>
        <div class="card-pad">
          ${usage.per_bot.map(b=>{
            const max = usage.per_bot[0].calls||1;
            return `<div style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:5px"><b>${esc(b.bot_type)}</b><span class="mono">${b.calls}건 ${b.rating?'· ★'+b.rating.toFixed(1):''}</span></div>
            <div class="bar"><span style="width:${b.calls/max*100}%"></span></div></div>`;}).join('')}
        </div>
      </div>
    </div>
  </div>
</div>`;
};
BIND.operations = () => {
  $('#cleanup')?.addEventListener('click', async ()=>{
    try{
      const r = await api('/itcen/ops/jobs/cleanup', {method:'POST'});
      toast(r.killed ? `4시간 이상 멈춘 작업 ${r.killed}건 강제 종료` : '정리할 멈춘 작업이 없습니다');
      go('operations');
    }catch(e){ toast(e.message,'err'); }
  });
  $('#simStuck')?.addEventListener('click', async ()=>{
    await api('/itcen/ops/jobs/simulate-stuck', {method:'POST'});
    toast('5시간 전 시작된 멈춘 작업을 추가했습니다 (데모)');
    go('operations');
  });
};

/* ===== 지속 개선 ===== */
VIEWS.improve = async () => {
  let sig, usage;
  try{ [sig, usage] = await Promise.all([api('/itcen/ops/signals'), api('/itcen/ops/usage')]); }
  catch(e){ return offlineCard(); }
  return `
<div class="view">
  <div class="page-head">
    <div><h1>지속 개선</h1><p>운영 신호(낮은 평가·인용 실패)가 콘솔로 되돌아와 개선 큐를 형성합니다. 개선은 Prompt 새 버전 또는 검색 설정 변경으로 이어지고, 다시 형상 이력에 기록됩니다.</p></div>
  </div>

  <div class="grid" style="grid-template-columns:repeat(4,1fr);margin-bottom:18px">
    ${[['개선 신호 (낮은 평가)', sig.low_rated.length+'건', '#fa5252'],
       ['개선 신호 (인용 실패)', sig.citation_failed.length+'건', '#f59f00'],
       ['전체 만족도', usage.satisfaction+'%', '#12b886'],
       ['인용 성공률', usage.citation_rate+'%', '#4b5cff']]
    .map(s=>`<div class="kpi"><div class="val" style="font-size:24px;color:${s[2]}">${s[1]}</div><div class="lbl" style="margin-top:5px">${s[0]}</div></div>`).join('')}
  </div>

  <div class="grid" style="grid-template-columns:1fr 1fr;margin-bottom:18px">
    <div class="card">
      <div class="card-head"><div><h3>개선 큐 · 낮은 평가 (★2 이하)</h3><div class="sub">피드백이 프롬프트 개선의 출발점이 됩니다</div></div></div>
      ${sig.low_rated.length ? sig.low_rated.map(l=>`
      <div class="log-item">
        <div>
          <div class="log-q">Q. ${esc(l.question)}</div>
          <div class="log-meta">
            <span class="tag">${esc(l.bot_type)}</span><span class="rate">${stars(l.rating)}</span>
            <span class="mini">${timeAgo(l.created_at)}</span>
            ${l.feedback?`<span class="mini">💬 ${esc(l.feedback)}</span>`:''}
          </div>
        </div>
        <button class="ghost-btn fix-prompt" data-bt="${esc(l.bot_type)}" style="height:32px;font-size:12px">${I('git')} Prompt 개선</button>
      </div>`).join('') : '<div class="card-pad mini">개선 신호가 없습니다. Chat 테스트에서 👎 피드백을 남기면 여기로 이관됩니다.</div>'}
    </div>
    <div class="card">
      <div class="card-head"><div><h3>개선 큐 · 인용 실패</h3><div class="sub">지식 공백 → Knowledge 파이프라인 보강 대상</div></div></div>
      ${sig.citation_failed.length ? sig.citation_failed.map(l=>`
      <div class="log-item">
        <div>
          <div class="log-q">Q. ${esc(l.question)}</div>
          <div class="log-meta"><span class="tag">${esc(l.bot_type)}</span><span class="mini">${timeAgo(l.created_at)}</span>
            <span class="chip danger" style="font-size:10.5px">근거 문서 없음</span></div>
        </div>
        <button class="ghost-btn go-knowledge" style="height:32px;font-size:12px">${I('book')} 지식 보강</button>
      </div>`).join('') : '<div class="card-pad mini">인용 실패 신호가 없습니다.</div>'}
    </div>
  </div>

  <div class="card">
    <div class="card-head"><div><h3>선순환 흐름</h3><div class="sub">신호 → 조치 → 형상 기록</div></div></div>
    <div class="card-pad" style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
      ${[['① 신호 수집','낮은 평가·인용 실패·지연이 자동으로 큐에 쌓임','pulse','#fa5252'],
         ['② 조치','Prompt 새 버전 배포 또는 검색 설정 변경, 지식 재수집','gear','#4b5cff'],
         ['③ 형상 기록','모든 조치는 버전 이력으로 남아 효과를 전후 비교','git','#12b886']]
      .map(s=>`<div style="border:1px solid var(--line);border-radius:12px;padding:16px">
        <div class="pipe-ico" style="background:linear-gradient(135deg,${s[3]},${s[3]}cc);margin-bottom:10px">${I(s[2])}</div>
        <b style="font-size:13.5px">${s[0]}</b><p class="mini" style="margin-top:5px;line-height:1.5">${s[1]}</p></div>`).join('')}
    </div>
  </div>
</div>`;
};
BIND.improve = () => {
  wrap.querySelectorAll('.fix-prompt').forEach(b=>b.addEventListener('click',()=>{ state.selBot=b.dataset.bt; go('prompts'); }));
  wrap.querySelectorAll('.go-knowledge').forEach(b=>b.addEventListener('click',()=>go('knowledge')));
};

/* ===== ITCEN-API · Chat 테스트 ===== */
VIEWS.api = async () => {
  try{ await loadAgents(); }catch(e){ return offlineCard(); }
  const host = location.origin;
  const eps = [
    ['GET','/agent/prompt/{bot_type}','System Prompt 조회'],
    ['GET','/agent/rag-config/{bot_type}','RAG 검색 설정 조회'],
    ['POST','/agent/chat','형상 적용 대화 호출'],
    ['POST','/agent/feedback','답변 피드백 등록'],
    ['GET','/itcen/agents','에이전트 목록'],
    ['POST','/itcen/agents','① 에이전트 생성'],
    ['PUT','/itcen/agents/{bot_type}/prompt','② Prompt 등록/개정'],
    ['PUT','/itcen/agents/{bot_type}/rag-config','③ 검색 설정 등록'],
    ['POST','/itcen/knowledge/sources/{id}/sync','RAG 파이프라인 실행'],
    ['POST','/itcen/ops/jobs/cleanup','멈춘 작업 정리 (4h+)'],
  ];
  return `
<div class="view">
  <div class="page-head">
    <div><h1>ITCEN-API · Chat 테스트</h1><p>콘솔(ITCEN)에 등록한 형상을 <b>REST 방식으로 자유롭게 호출</b>해 AI Agent 개발에 사용합니다. 자세한 스키마와 테스트 호출은 <a class="link" href="/docs" target="_blank">Swagger UI ↗</a> 에서 제공합니다.</p></div>
    <div class="head-actions"><a class="ghost-btn primary" href="/docs" target="_blank">${I('book')} Swagger UI 열기</a></div>
  </div>

  <div class="grid" style="grid-template-columns:1fr 1.1fr">
    <div style="display:flex;flex-direction:column;gap:18px">
      <div class="card">
        <div class="card-head"><div><h3>주요 엔드포인트</h3><div class="sub">${esc(host)}</div></div></div>
        <div class="card-pad">
          ${eps.map(e=>`<a class="ep" href="/docs" target="_blank">
            <span class="m ${e[0].toLowerCase()}">${e[0]}</span><span class="p">${e[1]}</span><span class="d">${e[2]}</span></a>`).join('')}
        </div>
      </div>
      <div class="card">
        <div class="card-head"><div><h3>호출 예시</h3><div class="sub">외부 Agent 개발 코드에서</div></div></div>
        <div class="card-pad"><div class="code"><span class="c"># 1) 형상 가져오기</span>
curl ${esc(host)}/agent/prompt/<span class="y">hr-assistant</span>
curl ${esc(host)}/agent/rag-config/<span class="y">hr-assistant</span>

<span class="c"># 2) 대화 호출</span>
curl -X POST ${esc(host)}/agent/chat \\
  -H <span class="g">"Content-Type: application/json"</span> \\
  -d <span class="g">'{"bot_type":"hr-assistant","message":"육아휴직은 최대 얼마나 쓸 수 있나요?"}'</span>

<span class="c"># 3) 피드백 회귀 (운영 신호)</span>
curl -X POST ${esc(host)}/agent/feedback \\
  -d <span class="g">'{"log_id":1,"rating":5}'</span></div></div>
      </div>
    </div>

    <div class="card chat-box">
      <div class="card-head">
        <div><h3>Chat 테스트 (POST /agent/chat)</h3><div class="sub">등록된 형상(Prompt+검색 설정)이 실제 적용됩니다</div></div>
        ${botSelect('chatBot')}
      </div>
      <div class="chat-scroll" id="chatScroll">
        <div class="msg bot">bot_type을 선택하고 질문해 보세요.\n예) 육아휴직은 최대 얼마나 쓸 수 있나요? / X-200 초기화 절차 알려줘 / 경쟁사 가격 포지셔닝 요약해줘</div>
      </div>
      <div class="chat-input">
        <input id="chatInput" placeholder="질문을 입력하세요… (Enter 전송)"/>
        <button class="pill-btn" id="chatSend">${I('send')} 전송</button>
      </div>
    </div>
  </div>
</div>`;
};
BIND.api = () => {
  const scroll = $('#chatScroll'), input = $('#chatInput');
  $('#chatBot')?.addEventListener('change', e=>{ state.selBot = e.target.value; });
  async function send(){
    const q = input.value.trim();
    if(!q) return;
    input.value='';
    const bot = $('#chatBot').value;
    scroll.insertAdjacentHTML('beforeend', `<div class="msg user">${esc(q)}</div>`);
    const tid = 't'+Date.now();
    scroll.insertAdjacentHTML('beforeend', `<div class="msg bot" id="${tid}"><span class="typing"><span></span><span></span><span></span></span></div>`);
    scroll.scrollTop = scroll.scrollHeight;
    try{
      const r = await api('/agent/chat', {method:'POST', body:{bot_type: bot, message: q}});
      $('#'+tid).outerHTML = `<div class="msg bot">${esc(r.answer)}
        ${r.citations.length?`<div class="cites">${r.citations.map(c=>`<span class="tag v" title="${esc(c.snippet)}">📄 ${esc(c.doc)} · ${c.score}</span>`).join('')}</div>`:''}
        <div class="meta"><span>⏱ ${r.latency_ms}ms</span><span>prompt ${r.config_version}</span><span>log #${r.log_id}</span>
          <span class="fb" data-log="${r.log_id}">
            <button data-r="5" title="만족">👍</button><button data-r="1" title="불만족">👎</button>
          </span></div></div>`;
      bindFb();
    }catch(e){
      $('#'+tid).outerHTML = `<div class="msg bot" style="border-color:var(--danger)">⚠️ ${esc(e.message)}</div>`;
    }
    scroll.scrollTop = scroll.scrollHeight;
  }
  function bindFb(){
    scroll.querySelectorAll('.fb button:not([data-b])').forEach(b=>{
      b.dataset.b='1';
      b.addEventListener('click', async ()=>{
        const logId = +b.parentElement.dataset.log, rating = +b.dataset.r;
        try{
          const r = await api('/agent/feedback',{method:'POST', body:{log_id: logId, rating}});
          b.parentElement.querySelectorAll('button').forEach(x=>x.classList.remove('sel'));
          b.classList.add('sel');
          toast(rating<=2 && r.routed_to_improvement_queue
            ? '피드백 기록 — 개선 큐로 이관되었습니다 (지속 개선 메뉴 확인)'
            : '피드백이 운영 대시보드로 되돌아갑니다');
        }catch(e){ toast(e.message,'err'); }
      });
    });
  }
  $('#chatSend')?.addEventListener('click', send);
  input?.addEventListener('keydown', e=>{ if(e.key==='Enter') send(); });
};

/* ---------- modal helpers ---------- */
function wrapModal(){ return $('.modal'); }
function openModal(inner){
  closeModal();
  const bg = document.createElement('div');
  bg.className='modal-bg';
  bg.innerHTML = `<div class="modal">${inner}</div>`;
  document.body.appendChild(bg);
  hydrateIcons(bg);
  bg.addEventListener('click', e=>{ if(e.target===bg) closeModal(); });
  bg.querySelectorAll('[data-close]').forEach(x=>x.addEventListener('click', closeModal));
}
function closeModal(){ $('.modal-bg')?.remove(); }

/* ---------- Router ---------- */
const CRUMB = {
  dashboard:['하나의 콘솔','대시보드'], knowledge:['Knowledge','RAG 데이터 파이프라인'],
  agents:['Config','AI Agent Config'], prompts:['Config','System Prompt'], search:['Config','벡터 검색 설정'],
  operations:['운영','운영 대시보드'], improve:['운영','지속 개선'], api:['개발 연동','ITCEN-API · Chat 테스트'],
};
const wrap = document.getElementById('viewWrap');
let current = 'dashboard';
async function go(view){
  if(!VIEWS[view]) return;
  current = view;
  clearInterval(state.pollTimer);
  wrap.innerHTML = '<div class="view" style="padding:60px;text-align:center;color:var(--ink-3)">불러오는 중…</div>';
  let html;
  try{ html = await VIEWS[view](); }
  catch(e){ html = offlineCard(); }
  if(current!==view) return; // 이동 중 다른 뷰로 전환됨
  wrap.innerHTML = html;
  hydrateIcons(wrap);
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active', n.dataset.view===view));
  const c = CRUMB[view];
  document.getElementById('crumbRoot').textContent = c[0];
  document.getElementById('crumbLeaf').textContent = c[1];
  wrap.scrollTop = 0;
  document.getElementById('sidebar').classList.remove('open');
  wrap.querySelectorAll('[data-go]').forEach(a=>a.addEventListener('click',()=>go(a.dataset.go)));
  wrap.querySelectorAll('.seg').forEach(seg=>seg.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    seg.querySelectorAll('button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
  }));
  BIND[view]?.();
}
document.querySelectorAll('.nav-item').forEach(n=>n.addEventListener('click',()=>go(n.dataset.view)));
document.getElementById('menuBtn').addEventListener('click',()=>document.getElementById('sidebar').classList.toggle('open'));
document.getElementById('newAgentBtn')?.addEventListener('click', async ()=>{
  try{ await loadAgents(); }catch(e){ return toast('백엔드 서버를 먼저 실행하세요 (run.bat)','err'); }
  openWizard();
});
hydrateIcons(document);
// 딥링크: ?view=knowledge 등으로 특정 화면 바로 진입 (스크린샷/공유용)
const _initView = new URLSearchParams(location.search).get('view');
go(_initView && VIEWS[_initView] ? _initView : 'dashboard');
