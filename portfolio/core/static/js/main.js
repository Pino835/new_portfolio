// ===== CYBERPUNK PORTFOLIO JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initSmoothScroll();
  initScrollIndicator();
});

// ===== MOBILE MENU =====
function initMobileMenu() {
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', function() {
      navLinks.classList.toggle('active');
    });

    // Cerrar menú al hacer clic en un enlace
    const links = navLinks.querySelectorAll('a');
    links.forEach(link => {
      link.addEventListener('click', function() {
        navLinks.classList.remove('active');
      });
    });
  }
}

// ===== SMOOTH SCROLL =====
function initSmoothScroll() {
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        const offsetTop = targetElement.offsetTop - 80; // Offset para el header fijo
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  });
}

// ===== SCROLL INDICATOR =====
function initScrollIndicator() {
  const scrollIndicator = document.querySelector('.scroll-indicator');
  
  if (scrollIndicator) {
    scrollIndicator.addEventListener('click', function() {
      const aboutSection = document.querySelector('#about');
      if (aboutSection) {
        const offsetTop = aboutSection.offsetTop - 80;
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }
    });
  }
}

// ===== LAZY LOADING IMAGES =====
if ('IntersectionObserver' in window) {
  const images = document.querySelectorAll('img[data-src]');
  
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// ===== GLITCH EFFECT ON HOVER =====
function addGlitchEffect() {
  const titles = document.querySelectorAll('.neon-cyan, .neon-magenta');
  
  titles.forEach(title => {
    title.addEventListener('mouseenter', function() {
      this.style.textShadow = `
        -2px 0 #ff00ff,
        2px 0 #00ffff,
        0 0 10px #00ffff,
        0 0 20px #00ffff
      `;
    });
    
    title.addEventListener('mouseleave', function() {
      this.style.textShadow = '';
    });
  });
}

// Inicializar efectos glitch cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', addGlitchEffect);

// ===== ANALYTICS (OPCIONAL) =====
function trackEvent(eventName, eventData) {
  if (window.gtag) {
    gtag('event', eventName, eventData);
  }
}

// Rastrear clics en enlaces externos
document.addEventListener('click', function(e) {
  if (e.target.tagName === 'A' && e.target.target === '_blank') {
    const href = e.target.href;
    trackEvent('external_link_click', {
      'link_url': href
    });
  }
});
