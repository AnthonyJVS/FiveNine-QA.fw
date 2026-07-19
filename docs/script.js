/* ═══════════════════════════════════════════════
   FiveNine QA Framework — Landing Page Scripts
   ═══════════════════════════════════════════════ */

(function () {
  'use strict';

  // ── Navbar scroll effect ──
  const navbar = document.getElementById('navbar');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    lastScroll = currentScroll;
  }, { passive: true });

  // ── Mobile nav toggle ──
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
      });
    });
  }

  // ── Smooth scroll for anchor links ──
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // ── Intersection Observer for fade-in + stagger ──
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');

        // Animate counters in stats grid
        if (entry.target.id === 'statsGrid') {
          animateCounters();
        }

        // Animate pass rate ring
        if (entry.target.querySelector('#progressRing')) {
          animatePassRate();
        }

        // Animate suite bars
        entry.target.querySelectorAll('.suite-bar-fill').forEach(bar => {
          const width = bar.dataset.width;
          if (width) {
            setTimeout(() => { bar.style.width = width; }, 200);
          }
        });

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in, .stagger').forEach(el => {
    observer.observe(el);
  });

  // ── Counter animation ──
  function animateCounters() {
    document.querySelectorAll('[data-count]').forEach(el => {
      const target = parseInt(el.dataset.count, 10);
      const duration = 1500;
      const start = performance.now();

      function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased);

        if (progress < 1) {
          requestAnimationFrame(update);
        }
      }

      requestAnimationFrame(update);
    });
  }

  // ── Pass rate ring animation ──
  function animatePassRate() {
    const ring = document.getElementById('progressRing');
    const rateValue = document.getElementById('rateValue');
    if (!ring || !rateValue) return;

    const passRate = 89.2; // 58/65 * 100
    const circumference = 2 * Math.PI * 56; // r=56
    const offset = circumference - (passRate / 100) * circumference;

    // Animate the ring
    setTimeout(() => {
      ring.style.strokeDashoffset = offset;
    }, 300);

    // Animate the percentage text
    const duration = 1500;
    const start = performance.now();

    function updateRate(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      rateValue.textContent = (passRate * eased).toFixed(1) + '%';

      if (progress < 1) {
        requestAnimationFrame(updateRate);
      }
    }

    requestAnimationFrame(updateRate);
  }

  // ── Tab switching ──
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabGroup = btn.closest('section') || btn.closest('.container');

      // Deactivate all tabs and content within this group
      tabGroup.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      // Activate clicked tab
      btn.classList.add('active');
      const targetTab = document.getElementById('tab-' + btn.dataset.tab);
      if (targetTab) {
        targetTab.classList.add('active');
      }
    });
  });

  // ── Magnetic buttons (cinematic footer + pills) ──
  document.querySelectorAll('.magnetic').forEach(el => {
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      el.style.transform = `translate(${x * 0.35}px, ${y * 0.35}px)`;
    });

    el.addEventListener('mouseleave', () => {
      el.style.transform = 'translate(0, 0)';
    });
  });

  // ── Giant background text parallax (footer) ──
  const footerGiantText = document.getElementById('footerGiantText');
  const footerWrapper = document.querySelector('.footer-reveal-wrapper');

  if (footerGiantText && footerWrapper) {
    let ticking = false;

    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;

      requestAnimationFrame(() => {
        const rect = footerWrapper.getBoundingClientRect();
        const viewportH = window.innerHeight;
        // Progress 0 -> 1 as the footer wrapper enters the viewport
        const progress = Math.min(1, Math.max(0, (viewportH - rect.top) / (viewportH + rect.height)));
        const translateY = 10 - progress * 10; // 10vh -> 0vh
        footerGiantText.style.transform = `translate(-50%, ${translateY}vh)`;
        footerGiantText.style.opacity = String(Math.min(1, progress * 1.6));
        ticking = false;
      });
    }, { passive: true });
  }

  // ── Back to top (footer) ──
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Active nav link highlighting ──
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 100;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        document.querySelectorAll('.nav-links a').forEach(link => {
          link.style.color = '';
          if (link.getAttribute('href') === '#' + id) {
            link.style.color = 'var(--accent)';
          }
        });
      }
    });
  }, { passive: true });

})();
