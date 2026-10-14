// Main Application Entry Point

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize the rotating @gcg beacon in top HUD
  if (typeof RotatingBeacon !== 'undefined') {
    const beacon = new RotatingBeacon({
      containerId: 'rotating-social-beacon',
      intervalMs: 3500
    });
    beacon.mount();
  }

  // 2. Initialize Hunter FX, Scroll Observers, and Stat Counters
  if (typeof initHunterFx === 'function') {
    initHunterFx();
  }
});
