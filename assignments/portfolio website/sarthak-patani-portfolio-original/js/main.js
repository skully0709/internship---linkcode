// ============================================
// SARTHAK PATANI — PORTFOLIO — SHARED JS
// ============================================

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Loader ---------- */
  const loader = document.querySelector('.loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => loader.classList.add('hidden'), 350);
    });
    // fallback in case load already fired
    setTimeout(() => loader.classList.add('hidden'), 1800);
  }

  /* ---------- Nav scroll state ---------- */
  const nav = document.querySelector('.nav');
  const onScroll = () => {
    if (!nav) return;
    nav.classList.toggle('scrolled', window.scrollY > 12);

    // scroll progress bar
    const bar = document.querySelector('.scroll-progress');
    if (bar) {
      const h = document.documentElement;
      const scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
      bar.style.width = scrolled + '%';
    }

    // back to top button
    const btt = document.querySelector('.back-to-top');
    if (btt) btt.classList.toggle('show', window.scrollY > 600);
  };
  document.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile nav toggle ---------- */
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      links.classList.toggle('open');
    });
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      toggle.classList.remove('open');
      links.classList.remove('open');
    }));
  }

  /* ---------- Back to top ---------- */
  const btt = document.querySelector('.back-to-top');
  if (btt) {
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });
    revealEls.forEach(el => io.observe(el));
  }

  /* ---------- Cursor glow (desktop only, pointer:fine) ---------- */
  if (window.matchMedia('(pointer: fine)').matches) {
    const glow = document.createElement('div');
    glow.className = 'cursor-glow';
    document.body.appendChild(glow);
    let gx = window.innerWidth / 2, gy = window.innerHeight / 2;
    let cx = gx, cy = gy;
    document.addEventListener('mousemove', (e) => { gx = e.clientX; gy = e.clientY; });
    const anim = () => {
      cx += (gx - cx) * 0.12;
      cy += (gy - cy) * 0.12;
      glow.style.left = cx + 'px';
      glow.style.top = cy + 'px';
      requestAnimationFrame(anim);
    };
    anim();
  }

  /* ---------- Typing role rotator (hero) ---------- */
  const roleEl = document.querySelector('[data-typing]');
  if (roleEl) {
    const words = JSON.parse(roleEl.getAttribute('data-typing'));
    let wi = 0, ci = 0, deleting = false;
    const textSpan = document.createElement('span');
    const cursorSpan = document.createElement('span');
    cursorSpan.className = 'cursor-char';
    cursorSpan.textContent = '|';
    roleEl.textContent = '';
    roleEl.appendChild(textSpan);
    roleEl.appendChild(cursorSpan);

    const tick = () => {
      const word = words[wi];
      if (!deleting) {
        ci++;
        textSpan.textContent = word.slice(0, ci);
        if (ci === word.length) {
          deleting = true;
          setTimeout(tick, 1400);
          return;
        }
      } else {
        ci--;
        textSpan.textContent = word.slice(0, ci);
        if (ci === 0) {
          deleting = false;
          wi = (wi + 1) % words.length;
        }
      }
      setTimeout(tick, deleting ? 40 : 75);
    };
    tick();
  }

  /* ---------- Hero bridge-scene: mouse-driven blend between design/circuit layers ---------- */
  const scene = document.querySelector('.bridge-scene');
  if (scene) {
    const designLayer = scene.querySelector('.bridge-layer.design');
    const circuitLayer = scene.querySelector('.bridge-layer.circuit');
    const setBlend = (ratio) => {
      // ratio 0 = full circuit, 1 = full design
      scene.style.setProperty('--design-opacity', 0.15 + ratio * 0.55);
      scene.style.setProperty('--circuit-opacity', 0.95 - ratio * 0.65);
    };
    setBlend(0.5);
    scene.addEventListener('mousemove', (e) => {
      const r = scene.getBoundingClientRect();
      const ratio = Math.min(Math.max((e.clientX - r.left) / r.width, 0), 1);
      setBlend(ratio);
    });
    scene.addEventListener('mouseleave', () => setBlend(0.5));
    // gentle ambient auto-blend on touch devices
    if (!window.matchMedia('(pointer: fine)').matches) {
      let t = 0;
      setInterval(() => {
        t += 0.02;
        setBlend((Math.sin(t) + 1) / 2);
      }, 60);
    }
  }

  /* ---------- Animated counters ---------- */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const io2 = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseFloat(el.getAttribute('data-count'));
        const decimals = (el.getAttribute('data-count').split('.')[1] || '').length;
        const suffix = el.getAttribute('data-suffix') || '';
        const dur = 1400;
        const start = performance.now();
        const step = (now) => {
          const p = Math.min((now - start) / dur, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          const val = target * eased;
          el.textContent = val.toFixed(decimals) + suffix;
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = target.toFixed(decimals) + suffix;
        };
        requestAnimationFrame(step);
        io2.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(c => io2.observe(c));
  }

  /* ---------- Skill bars fill on view ---------- */
  const fills = document.querySelectorAll('.skill-fill');
  if (fills.length) {
    const io3 = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.width = e.target.getAttribute('data-fill') + '%';
          io3.unobserve(e.target);
        }
      });
    }, { threshold: 0.4 });
    fills.forEach(f => io3.observe(f));
  }

  /* ---------- Skill tabs ---------- */
  const tabs = document.querySelectorAll('.skill-tab');
  if (tabs.length) {
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        document.querySelectorAll('.skill-panel').forEach(p => p.classList.remove('active'));
        const panel = document.querySelector(`#panel-${tab.dataset.tab}`);
        if (panel) {
          panel.classList.add('active');
          panel.querySelectorAll('.skill-fill').forEach(f => {
            f.style.width = '0%';
            requestAnimationFrame(() => requestAnimationFrame(() => {
              f.style.width = f.getAttribute('data-fill') + '%';
            }));
          });
        }
      });
    });
  }

  /* ---------- Project filter pills ---------- */
  const pills = document.querySelectorAll('.filter-pill');
  if (pills.length) {
    pills.forEach(pill => {
      pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const filter = pill.dataset.filter;
        document.querySelectorAll('.project-card').forEach(card => {
          const show = filter === 'all' || card.dataset.cat === filter;
          card.style.display = show ? '' : 'none';
        });
      });
    });
  }

  /* ---------- Contact form (front-end only demo) ---------- */
  const form = document.querySelector('.contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const status = form.querySelector('.form-status');
      const btn = form.querySelector('button[type="submit"]');
      const originalText = btn.textContent;
      btn.textContent = 'Sending…';
      btn.disabled = true;
      setTimeout(() => {
        status.textContent = '✓ Message received — thanks! I\'ll reply within a day or two.';
        btn.textContent = originalText;
        btn.disabled = false;
        form.reset();
      }, 900);
    });
  }

  /* ---------- Orbit sphere node placement (Tech Stack page) ---------- */
  document.querySelectorAll('.orbit-ring').forEach(ring => {
    const nodes = ring.querySelectorAll('.orbit-node');
    const count = nodes.length;
    nodes.forEach((node, i) => {
      const angle = (360 / count) * i;
      node.style.transform = `rotate(${angle}deg) translate(${ring.offsetWidth / 2}px) rotate(-${angle}deg)`;
      node.style.top = '50%';
      node.style.left = '50%';
      node.style.marginTop = '-26px';
      node.style.marginLeft = '-26px';
    });
  });

  /* ---------- Set active nav link based on current page ---------- */
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });

});
