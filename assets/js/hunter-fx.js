// Interactive Hunter FX, Scroll Observer & Dynamic Counters

function formatStatValue(value, format) {
  const num = Number(value);
  if (isNaN(num)) return String(value);

  if (format === 'percent') {
    // If it has decimals like 99.999, preserve up to 3 decimals
    const formatted = Number.isInteger(num) ? num.toString() : num.toFixed(3);
    return `${formatted}%`;
  }
  if (format === 'int') {
    return Math.round(num).toString();
  }
  return String(value);
}

function animateCounter(element, target, duration = 1200, format = 'int') {
  if (!element) return;
  const targetNum = parseFloat(target);
  if (isNaN(targetNum)) {
    element.textContent = target;
    return;
  }

  const startTime = performance.now();
  const startNum = 0;

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic curve
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const currentVal = startNum + (targetNum - startNum) * easeOut;

    element.textContent = formatStatValue(currentVal, format);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = formatStatValue(targetNum, format);
    }
  }

  requestAnimationFrame(update);
}

function initScrollObserver() {
  if (typeof document === 'undefined' || !('IntersectionObserver' in window)) return;

  const revealElements = document.querySelectorAll('.reveal-on-scroll');
  if (!revealElements.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');

        // Animate any counter values in this panel
        const counters = entry.target.querySelectorAll('.counter-val');
        counters.forEach(counter => {
          if (!counter.dataset.animated) {
            counter.dataset.animated = 'true';
            const targetVal = counter.getAttribute('data-target-val');
            const format = counter.getAttribute('data-format') || 'int';
            animateCounter(counter, targetVal, 1400, format);
          }
        });

        // Illuminate timeline nodes sequentially
        const timelineNodes = entry.target.querySelectorAll('.timeline-node');
        timelineNodes.forEach((node, idx) => {
          setTimeout(() => {
            node.classList.add('illuminated');
          }, idx * 180);
        });

        obs.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: '0px 0px -50px 0px',
    threshold: 0.15
  });

  revealElements.forEach(el => observer.observe(el));
}

function initPortraitFX() {
  if (typeof document === 'undefined') return;
  const portrait = document.querySelector('.portrait-container');
  if (!portrait) return;

  const triggerScan = () => {
    portrait.classList.remove('scanning');
    void portrait.offsetWidth; // Trigger reflow
    portrait.classList.add('scanning');
  };

  portrait.addEventListener('click', triggerScan);
  portrait.addEventListener('mouseenter', triggerScan);
}

function initCodeGridParallax() {
  if (typeof document === 'undefined' || typeof window === 'undefined') return;
  const backdrop = document.querySelector('.code-syntax-backdrop');
  if (!backdrop) return;

  // Reduced motion check
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  window.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    backdrop.style.transform = `translate3d(${x}px, ${y}px, 0)`;
  }, { passive: true });
}

function initHunterFx() {
  initScrollObserver();
  initPortraitFX();
  initCodeGridParallax();
}

// Universal export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatStatValue,
    animateCounter,
    initHunterFx,
    initScrollObserver,
    initPortraitFX,
    initCodeGridParallax
  };
}

if (typeof window !== 'undefined') {
  window.formatStatValue = formatStatValue;
  window.animateCounter = animateCounter;
  window.initHunterFx = initHunterFx;
}
