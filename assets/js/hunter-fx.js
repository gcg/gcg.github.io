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
  const streamLeft = document.querySelector('.code-stream-left');
  const streamRight = document.querySelector('.code-stream-right');
  const backdrop = document.querySelector('.code-syntax-backdrop');

  if (!streamLeft && !streamRight && !backdrop) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  let mouseX = 0, mouseY = 0, ticking = false;

  const updateStreams = () => {
    const scrollY = window.scrollY || window.pageYOffset || 0;
    const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const progress = Math.min(Math.max(scrollY / maxScroll, 0), 1);

    if (streamLeft || streamRight) {
      const vh = window.innerHeight;
      const leftH = streamLeft ? streamLeft.offsetHeight : 0;
      const rightH = streamRight ? streamRight.offsetHeight : 0;

      const maxLeftShift = Math.max(leftH - vh + 100, 160);
      const maxRightShift = Math.max(rightH - vh + 100, 160);

      const leftY = -progress * maxLeftShift + mouseY * 12;
      const rightY = -progress * maxRightShift + mouseY * 16;
      const leftX = mouseX * 8;
      const rightX = -mouseX * 8;

      if (streamLeft) streamLeft.style.transform = `translate3d(${leftX}px, ${leftY}px, 0)`;
      if (streamRight) streamRight.style.transform = `translate3d(${rightX}px, ${rightY}px, 0)`;
    } else if (backdrop) {
      const x = mouseX * 20;
      const y = mouseY * 20;
      backdrop.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    }
    ticking = false;
  };

  const requestUpdate = () => {
    if (!ticking) {
      requestAnimationFrame(updateStreams);
      ticking = true;
    }
  };

  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate, { passive: true });
  window.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5);
    mouseY = (e.clientY / window.innerHeight - 0.5);
    requestUpdate();
  }, { passive: true });

  requestUpdate();
}

function initBackdropSubsystems() {
  if (typeof document === 'undefined' || !('IntersectionObserver' in window)) return;
  const sections = document.querySelectorAll('main > section[data-subsystem]');
  const codeUnits = document.querySelectorAll('.code-block-unit[data-subsystem]');
  if (!sections.length || !codeUnits.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const activeSubsystem = entry.target.getAttribute('data-subsystem');
        codeUnits.forEach(unit => {
          if (unit.getAttribute('data-subsystem') === activeSubsystem) {
            unit.classList.add('active-subsystem');
          } else {
            unit.classList.remove('active-subsystem');
          }
        });
      }
    });
  }, {
    rootMargin: '-10% 0px -30% 0px',
    threshold: 0.15
  });

  sections.forEach(sec => observer.observe(sec));
}

function initChronicles() {
  if (typeof document === 'undefined') return;
  const toggles = document.querySelectorAll('.chronicle-toggle-btn');
  toggles.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const content = document.getElementById(targetId);
      if (!content) return;

      const isExpanded = content.classList.contains('expanded');
      if (isExpanded) {
        content.classList.remove('expanded');
        btn.innerHTML = `<span>Preview Chronicle</span> <span class="toggle-icon">▾</span>`;
        btn.setAttribute('aria-expanded', 'false');
      } else {
        content.classList.add('expanded');
        btn.innerHTML = `<span>Close Chronicle</span> <span class="toggle-icon">▴</span>`;
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

function initHunterFx() {
  initScrollObserver();
  initPortraitFX();
  initCodeGridParallax();
  initBackdropSubsystems();
  initChronicles();
}

// Universal export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    formatStatValue,
    animateCounter,
    initHunterFx,
    initScrollObserver,
    initPortraitFX,
    initCodeGridParallax,
    initBackdropSubsystems,
    initChronicles
  };
}

if (typeof window !== 'undefined') {
  window.formatStatValue = formatStatValue;
  window.animateCounter = animateCounter;
  window.initHunterFx = initHunterFx;
  window.initBackdropSubsystems = initBackdropSubsystems;
  window.initChronicles = initChronicles;
}
