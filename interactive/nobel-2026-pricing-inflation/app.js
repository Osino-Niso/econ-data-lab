const pct = (x, digits = 2) => `${x.toFixed(digits)}%`;

const transmission = {
  nominal: { label: '名目金利 iₜ', min: -1, max: 8, step: 0.1, value: 4.0, suffix: '%' },
  expectedInflation: { label: '期待インフレ率 Eₜπₜ₊₁', min: -1, max: 6, step: 0.1, value: 2.0, suffix: '%' },
  natural: { label: '自然利子率 rₜⁿ', min: -2, max: 4, step: 0.1, value: 1.0, suffix: '%' },
  expectedGap: { label: '予想される来期GDPギャップ Eₜxₜ₊₁', min: -4, max: 4, step: 0.1, value: 0.0, suffix: '%' },
  sigma: { label: 'σ', min: 0.4, max: 3, step: 0.1, value: 1.0, suffix: '' },
  beta: { label: 'β', min: 0.85, max: 1.0, step: 0.01, value: 0.99, suffix: '' },
  kappa: { label: 'κ', min: 0.02, max: 0.5, step: 0.01, value: 0.10, suffix: '' }
};

const taylor = {
  natural: { label: '自然利子率 rₜⁿ', min: -2, max: 4, step: 0.1, value: 1.0, suffix: '%' },
  target: { label: 'インフレ目標 π*', min: 0, max: 4, step: 0.1, value: 2.0, suffix: '%' },
  inflationGap: { label: '現在のインフレギャップ πₜ−π*', min: -3, max: 4, step: 0.1, value: 1.0, suffix: '%pt' },
  expectedGap: { label: '期待インフレの目標からの乖離 Eπₜ₊₁−π*', min: -3, max: 4, step: 0.1, value: 1.0, suffix: '%pt' },
  outputGap: { label: 'GDPギャップ xₜ', min: -4, max: 4, step: 0.1, value: 0.0, suffix: '%' },
  phiPi: { label: 'φπ', min: 0, max: 3, step: 0.1, value: 1.5, suffix: '' },
  phiX: { label: 'φx', min: 0, max: 1.5, step: 0.1, value: 0.5, suffix: '' }
};

function mountSliders(targetId, config, onInput) {
  const root = document.getElementById(targetId);
  Object.entries(config).forEach(([key, item]) => {
    const wrapper = document.createElement('label');
    const value = document.createElement('span');
    value.className = 'value';
    value.id = `${targetId}-${key}-value`;
    const input = document.createElement('input');
    input.type = 'range';
    input.min = item.min;
    input.max = item.max;
    input.step = item.step;
    input.value = item.value;
    input.dataset.key = key;
    input.addEventListener('input', () => {
      item.value = Number(input.value);
      value.textContent = `${item.value.toFixed(item.step < 0.1 ? 2 : 1)}${item.suffix}`;
      onInput();
    });
    wrapper.append(document.createTextNode(item.label), value, input);
    root.appendChild(wrapper);
    value.textContent = `${item.value.toFixed(item.step < 0.1 ? 2 : 1)}${item.suffix}`;
  });
}

function svgLineChart(svg, { xmin, xmax, ymin, ymax, fn, currentX, currentY, xLabel, yLabel }) {
  const W = 640, H = 250, L = 58, R = 18, T = 16, B = 38;
  const sx = x => L + (x - xmin) / (xmax - xmin) * (W - L - R);
  const sy = y => H - B - (y - ymin) / (ymax - ymin) * (H - T - B);
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const pts = Array.from({ length: 81 }, (_, i) => {
    const x = xmin + (xmax - xmin) * i / 80;
    return `${sx(x)},${sy(clamp(fn(x), ymin, ymax))}`;
  }).join(' ');
  const x0 = sx(clamp(0, xmin, xmax));
  const y0 = sy(clamp(0, ymin, ymax));
  const cx = sx(clamp(currentX, xmin, xmax));
  const cy = sy(clamp(currentY, ymin, ymax));
  svg.innerHTML = `
    <line class="guide" x1="${L}" y1="${y0}" x2="${W-R}" y2="${y0}" />
    <line class="guide" x1="${x0}" y1="${T}" x2="${x0}" y2="${H-B}" />
    <line class="axis" x1="${L}" y1="${H-B}" x2="${W-R}" y2="${H-B}" />
    <line class="axis" x1="${L}" y1="${T}" x2="${L}" y2="${H-B}" />
    <polyline class="curve" points="${pts}" />
    <circle class="point" cx="${cx}" cy="${cy}" r="5" />
    <text class="svg-label" x="${W/2}" y="${H-8}" text-anchor="middle">${xLabel}</text>
    <text class="svg-label" x="15" y="${H/2}" transform="rotate(-90 15 ${H/2})" text-anchor="middle">${yLabel}</text>
    <text class="svg-label" x="${L}" y="${H-22}">${xmin.toFixed(0)}</text>
    <text class="svg-label" x="${W-R-18}" y="${H-22}">${xmax.toFixed(0)}</text>
    <text class="svg-label" x="${L+4}" y="${T+10}">${ymax.toFixed(0)}</text>
    <text class="svg-label" x="${L+4}" y="${H-B-5}">${ymin.toFixed(0)}</text>`;
}

function updateTransmission() {
  const i = transmission.nominal.value;
  const ePi = transmission.expectedInflation.value;
  const rn = transmission.natural.value;
  const eX = transmission.expectedGap.value;
  const sigma = transmission.sigma.value;
  const beta = transmission.beta.value;
  const kappa = transmission.kappa.value;

  const realRate = i - ePi;
  const rateGap = realRate - rn;
  const x = eX - rateGap / sigma;
  const pi = beta * ePi + kappa * x;
  const stance = rateGap > 0.001 ? '引き締め方向' : rateGap < -0.001 ? '緩和方向' : 'ほぼ中立';

  document.getElementById('realRate').textContent = pct(realRate);
  document.getElementById('rateGap').textContent = pct(rateGap);
  document.getElementById('outputGap').textContent = pct(x);
  document.getElementById('inflation').textContent = pct(pi);
  document.getElementById('stance').textContent = stance;

  const yCenter = beta * ePi;
  const ySpread = Math.max(2.5, Math.abs(kappa) * 6 + 1.5);
  svgLineChart(document.getElementById('nkpcChart'), {
    xmin: -5, xmax: 5, ymin: yCenter - ySpread, ymax: yCenter + ySpread,
    fn: gap => beta * ePi + kappa * gap,
    currentX: x, currentY: pi,
    xLabel: 'GDPギャップ x（%）', yLabel: 'インフレ率 π（%）'
  });
}

function updateTaylor() {
  const rn = taylor.natural.value;
  const target = taylor.target.value;
  const piGap = taylor.inflationGap.value;
  const ePiGap = taylor.expectedGap.value;
  const x = taylor.outputGap.value;
  const phiPi = taylor.phiPi.value;
  const phiX = taylor.phiX.value;

  const neutralNominal = rn + target;
  const i = neutralNominal + phiPi * piGap + phiX * x;
  const expectedInflation = target + ePiGap;
  const realRate = i - expectedInflation;
  const gap = realRate - rn;

  document.getElementById('policyRate').textContent = pct(i);
  document.getElementById('taylorRealRate').textContent = pct(realRate);
  document.getElementById('taylorGap').textContent = pct(gap);
  document.getElementById('principle').textContent = phiPi > 1 ? '満たす（φπ > 1）' : Math.abs(phiPi - 1) < 1e-9 ? '境界（φπ = 1）' : '満たさない（φπ < 1）';

  // For the graph only, assume the expected-inflation gap moves one-for-one
  // with the current inflation gap, while holding x constant.
  const fn = inflationGap => (phiPi - 1) * inflationGap + phiX * x;
  const currentY = fn(piGap);
  svgLineChart(document.getElementById('taylorChart'), {
    xmin: -3, xmax: 4, ymin: -4, ymax: 5,
    fn, currentX: piGap, currentY,
    xLabel: 'インフレギャップ π−π*（%pt）', yLabel: '実質金利ギャップ（%pt）'
  });
}

mountSliders('transmissionInputs', transmission, updateTransmission);
mountSliders('taylorInputs', taylor, updateTaylor);
updateTransmission();
updateTaylor();
