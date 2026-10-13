const COLORS = {
  blue: '#4c8dff', green: '#4fd08a', gray: '#a8a8aa', grid: '#4a4e55', text: '#b9bcc2', white: '#f4f4f5', bg: '#202226'
};

const baseline = {
  nominal: 3.0,
  expectedInflation: 2.0,
  natural: 1.0,
  expectedOutput: 0.0,
  sigma: 1.0,
  beta: 0.99,
  kappa: 0.10
};

const state = {
  nominal: { label: '名目金利 iₜ', min: -1, max: 8, step: 0.1, value: 4.0, suffix: '%' },
  expectedInflation: { label: '期待インフレ率 Eₜπₜ₊₁', min: -1, max: 6, step: 0.1, value: 2.0, suffix: '%' },
  natural: { label: '自然利子率 rₜⁿ', min: -2, max: 4, step: 0.1, value: 1.0, suffix: '%' },
  expectedOutput: { label: '来期GDPギャップ Eₜxₜ₊₁', min: -4, max: 4, step: 0.1, value: 0.0, suffix: '%' },
  sigma: { label: 'σ', min: 0.4, max: 3.0, step: 0.1, value: 1.0, suffix: '' },
  beta: { label: 'β', min: 0.85, max: 1.0, step: 0.01, value: 0.99, suffix: '' },
  kappa: { label: 'κ', min: 0.02, max: 0.5, step: 0.01, value: 0.10, suffix: '' }
};

const taylor = {
  inflationGap: { label: 'インフレギャップ Δπ', min: -3, max: 4, step: 0.1, value: 1.0, suffix: '%pt' },
  phiPi: { label: 'φπ', min: 0, max: 3, step: 0.1, value: 1.5, suffix: '' },
  outputGap: { label: 'GDPギャップ xₜ', min: -4, max: 4, step: 0.1, value: 0.0, suffix: '%' },
  phiX: { label: 'φx', min: 0, max: 1.5, step: 0.1, value: 0.5, suffix: '' }
};

const pct = (v, d = 2) => `${v.toFixed(d)}%`;
const pt = (v, d = 2) => `${v.toFixed(d)}pt`;
const near = (v, eps = 1e-6) => Math.abs(v) < eps;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

function fmtControl(item) {
  const digits = item.step < 0.1 ? 2 : 1;
  return `${item.value.toFixed(digits)}${item.suffix}`;
}

function mountControls(targetId, keys, source, onInput) {
  const root = document.getElementById(targetId);
  root.innerHTML = '';
  keys.forEach(key => {
    const item = source[key];
    const label = document.createElement('label');
    label.className = 'control';
    const top = document.createElement('div');
    top.className = 'control-top';
    const name = document.createElement('span');
    name.textContent = item.label;
    const value = document.createElement('span');
    value.className = 'control-value';
    value.id = `${targetId}-${key}-value`;
    value.textContent = fmtControl(item);
    top.append(name, value);
    const input = document.createElement('input');
    input.type = 'range';
    input.min = item.min;
    input.max = item.max;
    input.step = item.step;
    input.value = item.value;
    input.addEventListener('input', () => {
      item.value = Number(input.value);
      value.textContent = fmtControl(item);
      onInput();
    });
    label.append(top, input);
    root.append(label);
  });
}

function calc(s) {
  const real = s.nominal - s.expectedInflation;
  const rateGap = real - s.natural;
  const output = s.expectedOutput - rateGap / s.sigma;
  const inflation = s.beta * s.expectedInflation + s.kappa * output;
  return { real, rateGap, output, inflation };
}

function direction(current, base, invertColor = false) {
  const diff = current - base;
  if (Math.abs(diff) < 0.005) return { arrow: '→', cls: 'flat' };
  const up = diff > 0;
  return { arrow: up ? '↑' : '↓', cls: invertColor ? (up ? 'down' : 'up') : (up ? 'up' : 'down') };
}

function svgHelpers(svg, dims) {
  const { W, H, L, R, T, B, xmin, xmax, ymin, ymax } = dims;
  const sx = x => L + (x - xmin) / (xmax - xmin) * (W - L - R);
  const sy = y => H - B - (y - ymin) / (ymax - ymin) * (H - T - B);
  const line = (x1,y1,x2,y2,cls,extra='') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}" ${extra}/>`;
  const text = (x,y,txt,cls='svg-label',anchor='middle',extra='') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}" ${extra}>${txt}</text>`;
  return { sx, sy, line, text };
}

function gridSvg({ W,H,L,R,T,B,xmin,xmax,ymin,ymax,sx,sy,xTicks,yTicks,xLabel,yLabel }) {
  let out = '';
  xTicks.forEach(v => {
    const x = sx(v);
    out += `<line x1="${x}" y1="${T}" x2="${x}" y2="${H-B}" class="gridline"/>`;
    out += `<text x="${x}" y="${H-B+22}" class="svg-label" text-anchor="middle">${v}</text>`;
  });
  yTicks.forEach(v => {
    const y = sy(v);
    out += `<line x1="${L}" y1="${y}" x2="${W-R}" y2="${y}" class="gridline"/>`;
    out += `<text x="${L-10}" y="${y+4}" class="svg-label" text-anchor="end">${v}</text>`;
  });
  out += `<line x1="${L}" y1="${H-B}" x2="${W-R}" y2="${H-B}" class="axis"/>`;
  out += `<line x1="${L}" y1="${T}" x2="${L}" y2="${H-B}" class="axis"/>`;
  out += `<text x="${(L+W-R)/2}" y="${H-7}" class="svg-axis-label" text-anchor="middle">${xLabel}</text>`;
  out += `<text x="16" y="${(T+H-B)/2}" class="svg-axis-label" text-anchor="middle" transform="rotate(-90 16 ${(T+H-B)/2})">${yLabel}</text>`;
  return out;
}

function polylinePoints(fn, sx, sy, xmin, xmax, ymin, ymax, n = 90) {
  return Array.from({length:n+1}, (_,i) => {
    const x = xmin + (xmax-xmin)*i/n;
    return `${sx(x)},${sy(clamp(fn(x), ymin, ymax))}`;
  }).join(' ');
}

function drawIS(current, base) {
  const svg = document.getElementById('isChart');
  const dims = { W:560,H:340,L:58,R:18,T:20,B:48,xmin:-5,xmax:5,ymin:-2,ymax:6 };
  const { sx, sy } = svgHelpers(svg, dims);
  const { W,H,L,R,T,B,xmin,xmax,ymin,ymax } = dims;
  const isFn = x => state.natural.value + state.sigma.value * (state.expectedOutput.value - x);
  const baseFn = x => baseline.natural + baseline.sigma * (baseline.expectedOutput - x);
  let out = gridSvg({ ...dims, sx, sy, xTicks:[-4,-2,0,2,4], yTicks:[-2,0,2,4,6], xLabel:'GDPギャップ xₜ（%）', yLabel:'期待実質金利 rᵉ（%）' });
  out += `<polyline points="${polylinePoints(baseFn,sx,sy,xmin,xmax,ymin,ymax)}" class="baseline"/>`;
  out += `<polyline points="${polylinePoints(isFn,sx,sy,xmin,xmax,ymin,ymax)}" class="curve-blue"/>`;
  out += `<line x1="${L}" y1="${sy(current.real)}" x2="${sx(current.output)}" y2="${sy(current.real)}" class="policy-line"/>`;
  out += `<line x1="${L}" y1="${sy(state.natural.value)}" x2="${W-R}" y2="${sy(state.natural.value)}" class="natural-line"/>`;
  out += `<line x1="${sx(current.output)}" y1="${sy(current.real)}" x2="${sx(current.output)}" y2="${H-B}" class="guide" stroke="${COLORS.blue}"/>`;
  out += `<circle cx="${sx(base.output)}" cy="${sy(base.real)}" r="5" class="point-base"/>`;
  out += `<circle cx="${sx(current.output)}" cy="${sy(current.real)}" r="7" class="point-blue"/>`;
  out += `<text x="${L+8}" y="${sy(current.real)-8}" class="svg-label" text-anchor="start">rᵉ=${current.real.toFixed(1)}%</text>`;
  out += `<text x="${W-R-4}" y="${sy(state.natural.value)-8}" class="svg-label" text-anchor="end">rⁿ=${state.natural.value.toFixed(1)}%</text>`;
  svg.innerHTML = out;
}

function drawNKPC(current, base) {
  const svg = document.getElementById('nkpcChart');
  const center = state.beta.value * state.expectedInflation.value;
  const dims = { W:560,H:340,L:58,R:18,T:20,B:48,xmin:-5,xmax:5,ymin:center-2.6,ymax:center+2.6 };
  const { sx, sy } = svgHelpers(svg, dims);
  const { W,H,L,R,T,B,xmin,xmax,ymin,ymax } = dims;
  const fn = x => state.beta.value * state.expectedInflation.value + state.kappa.value * x;
  const baseFn = x => baseline.beta * baseline.expectedInflation + baseline.kappa * x;
  const yTicks = Array.from({length:5},(_,i)=> Number((ymin+(ymax-ymin)*i/4).toFixed(1)));
  let out = gridSvg({ ...dims, sx, sy, xTicks:[-4,-2,0,2,4], yTicks, xLabel:'GDPギャップ xₜ（%）', yLabel:'インフレ率 πₜ（%）' });
  out += `<polyline points="${polylinePoints(baseFn,sx,sy,xmin,xmax,ymin,ymax)}" class="baseline"/>`;
  out += `<polyline points="${polylinePoints(fn,sx,sy,xmin,xmax,ymin,ymax)}" class="curve-green"/>`;
  out += `<line x1="${sx(current.output)}" y1="${H-B}" x2="${sx(current.output)}" y2="${sy(current.inflation)}" class="guide" stroke="${COLORS.blue}"/>`;
  out += `<line x1="${L}" y1="${sy(current.inflation)}" x2="${sx(current.output)}" y2="${sy(current.inflation)}" class="guide" stroke="${COLORS.green}"/>`;
  out += `<line x1="${sx(0)}" y1="${T}" x2="${sx(0)}" y2="${H-B}" class="natural-line"/>`;
  out += `<circle cx="${sx(base.output)}" cy="${sy(clamp(base.inflation,ymin,ymax))}" r="5" class="point-base"/>`;
  out += `<circle cx="${sx(current.output)}" cy="${sy(clamp(current.inflation,ymin,ymax))}" r="7" class="point-green"/>`;
  out += `<text x="${L+8}" y="${sy(clamp(current.inflation,ymin,ymax))-8}" class="svg-label" text-anchor="start">π=${current.inflation.toFixed(2)}%</text>`;
  svg.innerHTML = out;
}

function updateTransmission() {
  const currentState = Object.fromEntries(Object.entries(state).map(([k,v]) => [k,v.value]));
  const current = calc(currentState);
  const base = calc(baseline);

  document.getElementById('mNominal').textContent = pct(state.nominal.value);
  document.getElementById('mReal').textContent = pct(current.real);
  document.getElementById('mRateGap').textContent = pt(current.rateGap);
  document.getElementById('mOutput').textContent = pct(current.output);
  document.getElementById('mInflation').textContent = pct(current.inflation);

  const dN = direction(state.nominal.value, baseline.nominal);
  const dR = direction(current.real, base.real);
  const dX = direction(current.output, base.output, true);
  const dP = direction(current.inflation, base.inflation, true);
  document.getElementById('flowText').innerHTML =
    `名目金利 <span class="${dN.cls}">${dN.arrow}</span>　→　期待実質金利 <span class="${dR.cls}">${dR.arrow}</span>　→　GDPギャップ <span class="${dX.cls}">${dX.arrow}</span>　→　インフレ率 <span class="${dP.cls}">${dP.arrow}</span>`;

  let explain;
  if (near(current.rateGap, .01)) {
    explain = `期待実質金利は自然利子率とほぼ同じです。この設定では、金利面からGDPギャップを押し上げたり押し下げたりする力はほぼ中立です。`;
  } else if (current.rateGap > 0) {
    explain = `期待実質金利は自然利子率を ${current.rateGap.toFixed(2)}pt 上回っています。IS曲線上ではGDPギャップを ${current.output.toFixed(2)}% へ押し下げ、そのGDPギャップがNKPCを通じてインフレ率に下押し圧力をかけます。`;
  } else {
    explain = `期待実質金利は自然利子率を ${Math.abs(current.rateGap).toFixed(2)}pt 下回っています。IS曲線上ではGDPギャップを ${current.output.toFixed(2)}% へ押し上げ、そのGDPギャップがNKPCを通じてインフレ率に上押し圧力をかけます。`;
  }
  if (state.nominal.value > baseline.nominal && current.real < base.real) {
    explain += ` 名目金利は基準より高いのに、期待インフレ率の上昇によって期待実質金利はむしろ低くなっています。`;
  }
  document.getElementById('transmissionExplain').textContent = explain;
  drawIS(current, base);
  drawNKPC(current, base);
}

function drawTaylor() {
  const svg = document.getElementById('taylorChart');
  const dims = { W:680,H:360,L:64,R:20,T:24,B:50,xmin:-3,xmax:4,ymin:-4,ymax:6 };
  const { sx, sy } = svgHelpers(svg, dims);
  const { H,L,R,T,B,xmin,xmax,ymin,ymax,W } = dims;
  const phiPi = taylor.phiPi.value;
  const phiX = taylor.phiX.value;
  const x = taylor.outputGap.value;
  const gap = taylor.inflationGap.value;
  const nominalFn = g => phiPi * g + phiX * x;
  const expectedFn = g => g;
  const realFn = g => (phiPi - 1) * g + phiX * x;
  let out = gridSvg({ ...dims, sx, sy, xTicks:[-3,-2,-1,0,1,2,3,4], yTicks:[-4,-2,0,2,4,6], xLabel:'インフレギャップ Δπ（%pt）', yLabel:'反応幅（%pt）' });
  out += `<polyline points="${polylinePoints(nominalFn,sx,sy,xmin,xmax,ymin,ymax)}" class="curve-blue"/>`;
  out += `<polyline points="${polylinePoints(expectedFn,sx,sy,xmin,xmax,ymin,ymax)}" class="baseline" style="stroke:${COLORS.gray};opacity:.95"/>`;
  out += `<polyline points="${polylinePoints(realFn,sx,sy,xmin,xmax,ymin,ymax)}" class="curve-green"/>`;
  out += `<line x1="${sx(gap)}" y1="${H-B}" x2="${sx(gap)}" y2="${sy(clamp(realFn(gap),ymin,ymax))}" class="guide" stroke="${COLORS.green}"/>`;
  out += `<circle cx="${sx(gap)}" cy="${sy(clamp(nominalFn(gap),ymin,ymax))}" r="6" class="point-blue"/>`;
  out += `<circle cx="${sx(gap)}" cy="${sy(clamp(realFn(gap),ymin,ymax))}" r="6" class="point-green"/>`;
  out += `<text x="${W-R-4}" y="${sy(clamp(nominalFn(xmax),ymin,ymax))-8}" class="svg-label" text-anchor="end">名目金利</text>`;
  out += `<text x="${W-R-4}" y="${sy(clamp(expectedFn(xmax),ymin,ymax))+16}" class="svg-label" text-anchor="end">期待インフレ</text>`;
  svg.innerHTML = out;

  const nominalResponse = nominalFn(gap);
  const realResponse = realFn(gap);
  const badge = document.getElementById('principleBadge');
  if (phiPi > 1) {
    badge.className = 'principle-badge good';
    badge.textContent = `Taylor principle を満たす：φπ = ${phiPi.toFixed(1)} > 1`;
  } else if (near(phiPi - 1, .001)) {
    badge.className = 'principle-badge edge';
    badge.textContent = `境界：φπ = 1`;
  } else {
    badge.className = 'principle-badge bad';
    badge.textContent = `Taylor principle を満たさない：φπ = ${phiPi.toFixed(1)} < 1`;
  }

  document.getElementById('taylorFlow').innerHTML =
    `インフレギャップ ${gap >= 0 ? '<span class="up">↑</span>' : '<span class="down">↓</span>'} ${Math.abs(gap).toFixed(1)}pt　→　名目金利 ${nominalResponse >= 0 ? '<span class="up">↑</span>' : '<span class="down">↓</span>'} ${Math.abs(nominalResponse).toFixed(2)}pt　→　期待実質金利ギャップ ${realResponse >= 0 ? '<span class="up">↑</span>' : '<span class="down">↓</span>'} ${Math.abs(realResponse).toFixed(2)}pt`;

  const text = phiPi > 1
    ? `インフレが1pt上がると名目金利は ${phiPi.toFixed(1)}pt 反応します。期待インフレが1対1で上がると仮定しても、実質金利は上がる方向なので需要を冷やすフィードバックになります。`
    : phiPi < 1
      ? `インフレが1pt上がっても名目金利の反応は ${phiPi.toFixed(1)}pt です。期待インフレが1対1で上がるなら、実質金利は下がる方向になり、需要を刺激する逆向きのフィードバックが起こり得ます。`
      : `名目金利と期待インフレが1対1で動く境界です。実質金利をインフレに対して強く上げる力はありません。`;
  document.getElementById('taylorExplain').textContent = text;
}

mountControls('mainControls', ['nominal','expectedInflation','natural'], state, updateTransmission);
mountControls('advancedControls', ['expectedOutput','sigma','beta','kappa'], state, updateTransmission);
mountControls('taylorControls', ['inflationGap','phiPi','outputGap','phiX'], taylor, drawTaylor);
updateTransmission();
drawTaylor();
