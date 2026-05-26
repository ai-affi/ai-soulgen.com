// Affiliate Configuration — AI SoulGen
const AFFILIATE_BASE = 'https://www.ourdreamersai.com/7S8HPQB/3QQG7/';
const OFFERS = {
  women:   AFFILIATE_BASE + '?source=soulgen_modal_women',
  men:     AFFILIATE_BASE + '?source=soulgen_modal_men',
  anime:   AFFILIATE_BASE + '?source=soulgen_modal_anime',
  default: AFFILIATE_BASE + '?source=soulgen_direct'
};

window.goToOffer = function(preference) {
  const url = OFFERS[preference] || OFFERS.default;
  window.open(url, '_blank');
};

// Modal logic
document.addEventListener('DOMContentLoaded', function() {
  const overlay = document.getElementById('modal-overlay');
  const modal = document.getElementById('preference-modal');
  const closeBtn = document.getElementById('modal-close');

  function openModal() {
    overlay.classList.add('active');
    modal.classList.add('active');
  }

  function closeModal() {
    overlay.classList.remove('active');
    modal.classList.remove('active');
  }

  // Auto-open after 3s, 1x per session
  if (!sessionStorage.getItem('modalShown')) {
    setTimeout(function() {
      openModal();
      sessionStorage.setItem('modalShown', 'true');
    }, 3000);
  }

  // Close handlers
  closeBtn.addEventListener('click', closeModal);
  overlay.addEventListener('click', closeModal);
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
  });

  // Preference buttons
  document.querySelectorAll('.pref-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var pref = this.getAttribute('data-preference');
      goToOffer(pref);
      closeModal();
    });
  });

  // All CTA buttons go direct
  document.querySelectorAll('[data-open-modal]').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      goToOffer('default');
    });
  });
});
