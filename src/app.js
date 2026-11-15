// Hash navigation lets every page work when this file is opened directly.
const main = document.getElementById('content');
const navigation = document.querySelectorAll('#sidebar a');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let stopWidget = null;

function fitCanvas(canvas) {
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const r = canvas.getBoundingClientRect();
  canvas.width = Math.max(1, Math.round(r.width * dpr));
  canvas.height = Math.max(1, Math.round(r.height * dpr));
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { ctx, w: r.width, h: r.height };
}

function animate(frame) {
  let id = 0, last = performance.now(), alive = true;
  const step = (t) => {
    if (!alive) return;
    frame(Math.min(48, t - last) / 16.67, t);
    last = t;
    id = requestAnimationFrame(step);
  };
  id = requestAnimationFrame(step);
  return () => { alive = false; cancelAnimationFrame(id); };
}

const widgets = {
  // Schelling's segregation model.
  schelling(fig) {
    const canvas = fig.querySelector('canvas');
    const readout = fig.querySelector('.readout');
    let view = fitCanvas(canvas);
    const cell = 9;
    let W = 0, H = 0, grid, tick = 0, settled = 0;
    function seed() {
      W = Math.max(20, Math.floor((view.w - 24) / cell));
      H = Math.max(12, Math.floor((view.h - 58) / cell));
      grid = new Int8Array(W * H);
      for (let i = 0; i < grid.length; i++) {
        const r = Math.random();
        grid[i] = r < 0.1 ? 0 : r < 0.55 ? 1 : 2;
      }
      tick = 0; settled = 0;
    }
    function likeShare(i) {
      const x = i % W, y = (i / W) | 0, t = grid[i];
      let same = 0, total = 0;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const v = grid[((y + dy + H) % H) * W + ((x + dx + W) % W)];
        if (v) { total++; if (v === t) same++; }
      }
      return total ? same / total : 1;
    }
    function step() {
      const unhappy = [], empty = [];
      for (let i = 0; i < grid.length; i++) {
        if (!grid[i]) empty.push(i);
        else if (likeShare(i) < 0.375) unhappy.push(i);
      }
      for (let k = unhappy.length - 1; k > 0; k--) {
        const j = (Math.random() * (k + 1)) | 0;
        [unhappy[k], unhappy[j]] = [unhappy[j], unhappy[k]];
      }
      for (const i of unhappy) {
        const e = (Math.random() * empty.length) | 0, j = empty[e];
        grid[j] = grid[i]; grid[i] = 0; empty[e] = i;
      }
      tick++;
      return unhappy.length;
    }
    function draw(unhappy) {
      const { ctx, w, h } = view;
      ctx.clearRect(0, 0, w, h);
      const ox = (w - W * cell) / 2, oy = 38 + (h - 38 - H * cell) / 2;
      for (let i = 0; i < grid.length; i++) {
        const v = grid[i];
        if (!v) continue;
        ctx.fillStyle = v === 1 ? '#c4b28a' : '#4f8fae';
        ctx.fillRect(ox + (i % W) * cell, oy + ((i / W) | 0) * cell, cell - 2, cell - 2);
      }
      const pct = (100 * unhappy / (grid.length * 0.9)).toFixed(1);
      readout.textContent = `tick ${String(tick).padStart(3, '0')} · unhappy ${pct}%`;
    }
    seed();
    let unhappy = grid.length;
    draw(unhappy);
    if (reduceMotion) {
      for (let k = 0; k < 60 && unhappy; k++) unhappy = step();
      draw(unhappy);
    }
    const timer = reduceMotion ? 0 : setInterval(() => {
      if (settled > 18) { seed(); }
      unhappy = step();
      if (unhappy === 0) settled++;
      draw(unhappy);
    }, 150);
    const reseed = () => { seed(); draw(grid.length); };
    canvas.addEventListener('click', reseed);
    const onResize = () => { view = fitCanvas(canvas); seed(); draw(grid.length); };
    window.addEventListener('resize', onResize);
    return () => { clearInterval(timer); window.removeEventListener('resize', onResize); };
  },

  // Objects in orbit around Earth.
  orbits(fig) {
    const canvas = fig.querySelector('canvas');
    let view = fitCanvas(canvas);
    const deg = Math.PI / 180;
    const incs = [53, 53, 53, 70, 97.6, 97.6, 86.4, 43, 65, 82];
    const objs = [];
    for (let i = 0; i < 1400; i++) {
      const r = Math.random();
      let a, inc;
      if (r < 0.84) { a = 1.07 + Math.random() * 0.24; inc = incs[(Math.random() * incs.length) | 0] + (Math.random() - 0.5) * 6; }
      else if (r < 0.92) { a = 1.85 + Math.random() * 0.35; inc = 55 + (Math.random() - 0.5) * 8; }
      else { a = 2.9 + Math.random() * 0.06; inc = Math.random() * 2; }
      objs.push({ a, inc: inc * deg, raan: Math.random() * Math.PI * 2, u: Math.random() * Math.PI * 2,
                  w: 0.0042 * Math.pow(a, -1.5), active: Math.random() < 0.2 });
    }
    const stars = Array.from({ length: 160 }, () => [Math.random(), Math.random(), Math.random() * 0.6 + 0.2]);
    const tilt = 0.38;
    let spin = 0;
    function frame(dt) {
      const { ctx, w, h } = view;
      ctx.clearRect(0, 0, w, h);
      for (const [sx, sy, b] of stars) { ctx.fillStyle = `rgba(200,215,230,${b * 0.5})`; ctx.fillRect(sx * w, sy * h, 1, 1); }
      const R = Math.min(w * 0.15, h * 0.24), cx = w / 2, cy = h / 2 + 6;
      spin += 0.0006 * dt;
      const back = [], front = [];
      for (const o of objs) {
        o.u += o.w * dt;
        const cu = Math.cos(o.u), su = Math.sin(o.u), cO = Math.cos(o.raan + spin), sO = Math.sin(o.raan + spin);
        const ci = Math.cos(o.inc), si = Math.sin(o.inc);
        const x = o.a * (cO * cu - sO * su * ci);
        const y = o.a * (sO * cu + cO * su * ci);
        const z = o.a * (su * si);
        const yv = y * Math.cos(tilt) - z * Math.sin(tilt);
        const zv = y * Math.sin(tilt) + z * Math.cos(tilt);
        (yv > 0 ? front : back).push([cx + x * R, cy - zv * R, o.active]);
      }
      const dot = (list) => {
        for (const [x, y, act] of list) {
          ctx.fillStyle = act ? 'rgba(214,190,140,.95)' : 'rgba(140,160,175,.55)';
          ctx.fillRect(x - 0.8, y - 0.8, act ? 1.9 : 1.5, act ? 1.9 : 1.5);
        }
      };
      dot(back);
      const g = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.35, R * 0.1, cx, cy, R);
      g.addColorStop(0, '#16303f'); g.addColorStop(0.7, '#0b1822'); g.addColorStop(1, '#060d13');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(95,168,199,.55)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(cx, cy, R + 0.5, 0, Math.PI * 2); ctx.stroke();
      ctx.strokeStyle = 'rgba(95,168,199,.12)'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(cx, cy, R + 4, 0, Math.PI * 2); ctx.stroke();
      dot(front);
    }
    frame(0);
    const stop = reduceMotion ? () => {} : animate(frame);
    const onResize = () => { view = fitCanvas(canvas); frame(0); };
    window.addEventListener('resize', onResize);
    return () => { stop(); window.removeEventListener('resize', onResize); };
  },

  // Dinoflagellates that flash when the water is disturbed.
  glow(fig) {
    const canvas = fig.querySelector('canvas');
    let view = fitCanvas(canvas);
    let cells = [];
    const make = () => {
      const n = Math.round(view.w * view.h / 260);
      cells = Array.from({ length: n }, () => ({ x: Math.random() * view.w, y: Math.random() * view.h,
        vx: (Math.random() - 0.5) * 0.12, vy: (Math.random() - 0.5) * 0.08, e: 0, ph: Math.random() * 6.28 }));
    };
    make();
    let px = -999, py = -999, pspeed = 0, wave = -200;
    const point = (ev) => {
      const r = canvas.getBoundingClientRect();
      const x = ev.clientX - r.left, y = ev.clientY - r.top;
      if (px > -900) pspeed = Math.min(40, Math.hypot(x - px, y - py));
      px = x; py = y;
    };
    canvas.addEventListener('pointermove', point);
    canvas.addEventListener('pointerleave', () => { px = py = -999; pspeed = 0; });
    function frame(dt, t) {
      const { ctx, w, h } = view;
      ctx.globalCompositeOperation = 'source-over';
      ctx.fillStyle = 'rgba(3,8,13,1)';
      ctx.fillRect(0, 0, w, h);
      wave += 2.2 * dt;
      if (wave > w + 400) wave = -300 - Math.random() * 400;
      const crest = (x) => h * 0.78 + Math.sin(x / 60 + t / 900) * 8;
      ctx.globalCompositeOperation = 'lighter';
      for (const c of cells) {
        c.x += c.vx * dt; c.y += c.vy * dt + Math.sin(t / 1400 + c.ph) * 0.03 * dt;
        if (c.x < 0) c.x += w; if (c.x > w) c.x -= w; if (c.y < 0) c.y += h; if (c.y > h) c.y -= h;
        if (pspeed > 1) {
          const d = Math.hypot(c.x - px, c.y - py);
          if (d < 46) c.e = Math.min(1, c.e + (1 - d / 46) * pspeed * 0.05);
        }
        if (Math.abs(c.x - wave) < 26 && Math.abs(c.y - crest(c.x)) < 22) c.e = Math.min(1, c.e + 0.18 * dt);
        c.e *= Math.pow(0.955, dt);
        ctx.fillStyle = 'rgba(70,120,150,.32)';
        ctx.fillRect(c.x, c.y, 1.1, 1.1);
        if (c.e > 0.03) {
          const r = 1.2 + c.e * 3.4;
          const g = ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, r * 2.4);
          g.addColorStop(0, `rgba(150,235,255,${c.e})`);
          g.addColorStop(0.35, `rgba(40,170,255,${c.e * 0.55})`);
          g.addColorStop(1, 'rgba(0,80,255,0)');
          ctx.fillStyle = g;
          ctx.fillRect(c.x - r * 2.4, c.y - r * 2.4, r * 4.8, r * 4.8);
        }
      }
      pspeed *= Math.pow(0.8, dt);
    }
    frame(1, 0);
    const stop = reduceMotion ? () => {} : animate(frame);
    const onResize = () => { view = fitCanvas(canvas); make(); };
    window.addEventListener('resize', onResize);
    return () => { stop(); window.removeEventListener('resize', onResize); };
  },
};

function mountWidgets() {
  if (stopWidget) { stopWidget(); stopWidget = null; }
  const stops = [];
  for (const fig of main.querySelectorAll('[data-widget]')) {
    const make = widgets[fig.dataset.widget];
    if (make) stops.push(make(fig));
  }
  if (stops.length) stopWidget = () => stops.forEach((f) => f());
}

function showPage() {
  const requested = location.hash.slice(1) || 'about';
  const template = document.getElementById('page-' + requested)
    || document.getElementById('page-about');
  const page = template.id.slice(5);
  main.replaceChildren(template.content.cloneNode(true));
  for (const link of navigation) {
    if (link.hash === '#' + page) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  }
  const active = document.querySelector('#sidebar a[aria-current="page"]');
  document.title = active.dataset.title + ' · Mahean Magamemnon';
  window.scrollTo(0, 0);
  mountWidgets();
}
window.addEventListener('hashchange', () => {
  showPage();
  main.focus({ preventScroll: true });
});
showPage();
