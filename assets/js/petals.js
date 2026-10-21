// Falling plum petals and snowflakes, behind and in front of the chapter.

function initPetals(container, count, opts) {
  const front = !!(opts && opts.front);
  const pinks = ['var(--plum)', 'var(--plum-2)', 'var(--plum-3)'];
  const r = (a, b) => a + Math.random() * (b - a);

  for (let i = 0; i < count; i++) {
    const p = document.createElement('i');
    const snow = !front && Math.random() < 0.3;
    if (snow) p.className = 'snow';
    const size = front ? r(16, 26) : snow ? r(3, 6) : r(6, 13);
    p.style.cssText = [
      `--x:${r(-5, 100).toFixed(1)}%`,
      `--s:${size.toFixed(1)}px`,
      `--d:${(front ? r(7, 12) : r(9, 22)).toFixed(1)}s`,
      `--dl:-${r(0, 22).toFixed(1)}s`,
      `--dx:${r(-160, 80).toFixed(0)}px`,
      `--c:${pinks[i % pinks.length]}`,
      `--o:${(front ? 0.55 : r(0.55, 0.9)).toFixed(2)}`,
      `--b:${(front ? r(1.5, 3) : 0).toFixed(1)}px`,
    ].join(';');
    container.appendChild(p);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const back = document.getElementById('petals-back');
  const front = document.getElementById('petals-front');
  if (back) initPetals(back, 60, { front: false });
  if (front) initPetals(front, 6, { front: true });
});
