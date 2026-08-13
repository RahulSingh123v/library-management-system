/* =============================================================
   Library Management System — Main JS
   ============================================================= */

/* ── Sidebar Toggle ─────────────────────────────────────────── */
(function () {
  'use strict';

  const sidebar  = document.getElementById('lmsSidebar');
  const main     = document.getElementById('lmsMain');
  const toggleBtn = document.getElementById('sidebarToggle');
  const overlay  = document.getElementById('sidebarOverlay');

  if (!sidebar || !main) return;

  const COLLAPSED_KEY = 'lms_sidebar_collapsed';

  // Restore state
  if (window.innerWidth > 768 && localStorage.getItem(COLLAPSED_KEY) === '1') {
    sidebar.classList.add('collapsed');
    main.classList.add('sidebar-collapsed');
  }

  function toggle() {
    if (window.innerWidth <= 768) {
      // Mobile: slide in/out
      sidebar.classList.toggle('mobile-open');
      if (overlay) overlay.classList.toggle('active');
    } else {
      // Desktop: collapse/expand
      const isCollapsed = sidebar.classList.toggle('collapsed');
      main.classList.toggle('sidebar-collapsed', isCollapsed);
      localStorage.setItem(COLLAPSED_KEY, isCollapsed ? '1' : '0');
    }
  }

  if (toggleBtn) toggleBtn.addEventListener('click', toggle);
  if (overlay)   overlay.addEventListener('click', toggle);

  // Highlight active nav link
  const links = sidebar.querySelectorAll('.sidebar-link');
  const currentPath = window.location.pathname;
  links.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
})();

/* ── Toast Notification System ──────────────────────────────── */
window.LMSToast = (function () {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const icons = {
    success: 'fa-circle-check',
    danger:  'fa-circle-xmark',
    warning: 'fa-triangle-exclamation',
    info:    'fa-circle-info',
  };

  const titles = {
    success: 'Success',
    danger:  'Error',
    warning: 'Warning',
    info:    'Notice',
  };

  function show(message, type = 'info', duration = 4500) {
    const toast = document.createElement('div');
    toast.className = `lms-toast toast-${type}`;
    toast.innerHTML = `
      <i class="fas ${icons[type] || icons.info} toast-icon"></i>
      <div class="toast-body">
        <div class="toast-title">${titles[type] || 'Notice'}</div>
        <div class="toast-msg">${message}</div>
      </div>
      <button class="toast-close"><i class="fas fa-xmark"></i></button>
    `;

    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => dismiss(toast));

    container.appendChild(toast);

    if (duration > 0) {
      setTimeout(() => dismiss(toast), duration);
    }

    return toast;
  }

  function dismiss(toast) {
    if (!toast || !toast.parentNode) return;
    toast.classList.add('hiding');
    setTimeout(() => toast.remove(), 280);
  }

  return { show, dismiss };
})();

/* ── Convert Django Messages to Toasts ──────────────────────── */
(function () {
  const djangoAlerts = document.querySelectorAll('[data-lms-message]');
  djangoAlerts.forEach(el => {
    const type = el.dataset.lmsType || 'info';
    const msg  = el.dataset.lmsMessage;
    if (msg) window.LMSToast.show(msg, type);
    el.remove();
  });
})();

/* ── Confirmation Modal ──────────────────────────────────────── */
window.LMSConfirm = (function () {
  let backdrop = document.getElementById('lmsConfirmModal');

  if (!backdrop) {
    backdrop = document.createElement('div');
    backdrop.id = 'lmsConfirmModal';
    backdrop.className = 'lms-modal-backdrop';
    backdrop.innerHTML = `
      <div class="lms-modal">
        <div class="modal-icon danger-icon" id="confirmIcon"><i class="fas fa-triangle-exclamation"></i></div>
        <div class="modal-title" id="confirmTitle">Are you sure?</div>
        <div class="modal-msg" id="confirmMsg">This action cannot be undone.</div>
        <div class="modal-actions">
          <button class="btn-lms btn-outline-lms" id="confirmCancel">Cancel</button>
          <button class="btn-lms btn-danger-lms" id="confirmOk">Confirm</button>
        </div>
      </div>
    `;
    document.body.appendChild(backdrop);

    document.getElementById('confirmCancel').addEventListener('click', close);
    backdrop.addEventListener('click', e => { if (e.target === backdrop) close(); });
  }

  let resolveFn = null;

  function open(options = {}) {
    const title = options.title || 'Are you sure?';
    const msg   = options.message || 'This action cannot be undone.';
    const okLabel = options.okLabel || 'Confirm';
    const type  = options.type || 'danger';

    document.getElementById('confirmTitle').textContent = title;
    document.getElementById('confirmMsg').textContent   = msg;
    document.getElementById('confirmOk').textContent    = okLabel;

    const icon = document.getElementById('confirmIcon');
    icon.className = `modal-icon ${type === 'success' ? 'success-icon' : 'danger-icon'}`;
    icon.innerHTML = type === 'success'
      ? '<i class="fas fa-circle-check"></i>'
      : '<i class="fas fa-triangle-exclamation"></i>';

    const okBtn = document.getElementById('confirmOk');
    okBtn.className = `btn-lms ${type === 'success' ? 'btn-success-lms' : 'btn-danger-lms'}`;

    // Remove old listener
    const newOk = okBtn.cloneNode(true);
    okBtn.parentNode.replaceChild(newOk, okBtn);
    newOk.textContent = okLabel;
    newOk.addEventListener('click', () => { close(); if (resolveFn) resolveFn(true); });

    backdrop.classList.add('open');

    return new Promise(resolve => { resolveFn = resolve; });
  }

  function close() {
    backdrop.classList.remove('open');
    resolveFn = null;
  }

  return { open };
})();

/* ── Intercept Confirm Buttons ───────────────────────────────── */
document.addEventListener('click', function (e) {
  const btn = e.target.closest('[data-confirm]');
  if (!btn) return;

  e.preventDefault();

  const title   = btn.dataset.confirmTitle   || 'Are you sure?';
  const message = btn.dataset.confirm        || 'This action cannot be undone.';
  const okLabel = btn.dataset.confirmOk      || 'Confirm';
  const type    = btn.dataset.confirmType    || 'danger';

  window.LMSConfirm.open({ title, message, okLabel, type }).then(confirmed => {
    if (!confirmed) return;
    // Follow the href or submit the form
    if (btn.tagName === 'A' && btn.href) {
      window.location.href = btn.href;
    } else if (btn.form) {
      btn.form.submit();
    }
  });
});

/* ── Auto-dismiss legacy alerts ──────────────────────────────── */
document.querySelectorAll('.auto-dismiss').forEach(el => {
  setTimeout(() => {
    el.style.transition = 'opacity .4s';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 400);
  }, 4000);
});

/* ── Date input min = today ──────────────────────────────────── */
document.querySelectorAll('input[name="due_date"]').forEach(input => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  input.min = tomorrow.toISOString().split('T')[0];
});
