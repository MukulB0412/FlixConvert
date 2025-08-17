// Tabs
document.addEventListener('DOMContentLoaded', () => {
  const btns = Array.from(document.querySelectorAll('.tab-button'));
  const tabs = Array.from(document.querySelectorAll('.tab'));
  btns.forEach(b => b.addEventListener('click', () => {
    btns.forEach(x => x.classList.remove('active'));
    tabs.forEach(t => t.classList.remove('active'));
    b.classList.add('active');
    document.getElementById(b.dataset.tab).classList.add('active');
    window.location.hash = 'convert';
  }));

  // Reveal on scroll
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // Drag & drop / preview for images
  const dropzone = document.getElementById('dropzone');
  const input = document.getElementById('img-input');
  const thumbs = document.getElementById('thumbs');
  const orderInput = document.getElementById('images_order');
  const form = document.getElementById('img-form');
  const layoutSelect = document.getElementById('layout');

  const state = { files: [] };

  const openPicker = () => input.click();
  dropzone.addEventListener('click', openPicker);

  const prevent = (e) => { e.preventDefault(); e.stopPropagation(); };
  ['dragenter','dragover'].forEach(evt => dropzone.addEventListener(evt, (e)=>{
    prevent(e); dropzone.classList.add('dragover');
  }));
  ;['dragleave','drop'].forEach(evt => dropzone.addEventListener(evt, (e)=>{
    prevent(e); dropzone.classList.remove('dragover');
  }));
  dropzone.addEventListener('drop', (e) => {
    const files = Array.from(e.dataTransfer.files || []).filter(f => f.type.startsWith('image/'));
    pushFiles(files);
  });
  input.addEventListener('change', (e) => {
    const files = Array.from(input.files || []);
    pushFiles(files);
  });

  function pushFiles(files) {
    for (const f of files) {
      state.files.push(f);
    }
    renderThumbs();
    // sync to hidden file input by constructing a new DataTransfer
    const dt = new DataTransfer();
    state.files.forEach(f => dt.items.add(f));
    input.files = dt.files;
    writeOrder();
  }

  function renderThumbs() {
    thumbs.innerHTML = '';
    state.files.forEach((f, idx) => {
      const url = URL.createObjectURL(f);
      const card = document.createElement('div');
      card.className = 'thumb';
      card.draggable = true;
      card.dataset.idx = String(idx);
      card.innerHTML = `<span class="handle">drag</span><img src="${url}" alt=""><span class="idx">#${idx+1}</span>`;
      thumbs.appendChild(card);
    });
  }

  // drag reorder
  let dragIdx = null;
  thumbs.addEventListener('dragstart', (e) => {
    const target = e.target.closest('.thumb'); if(!target) return;
    dragIdx = parseInt(target.dataset.idx);
    e.dataTransfer.effectAllowed = 'move';
  });
  thumbs.addEventListener('dragover', (e) => { e.preventDefault(); });
  thumbs.addEventListener('drop', (e) => {
    e.preventDefault();
    const target = e.target.closest('.thumb'); if(!target) return;
    const dropIdx = parseInt(target.dataset.idx);
    if (dragIdx===null || dropIdx===null || dragIdx===dropIdx) return;
    const arr = state.files;
    const [moved] = arr.splice(dragIdx,1);
    arr.splice(dropIdx,0,moved);
    renderThumbs();
    // reassign input files order
    const dt = new DataTransfer();
    arr.forEach(f => dt.items.add(f));
    input.files = dt.files;
    writeOrder();
  });

  function writeOrder() {
    const order = Array.from(input.files).map((_, i) => i).join(',');
    orderInput.value = order;
    // refresh indices
    document.querySelectorAll('.thumb').forEach((el, i) => {
      const idxBadge = el.querySelector('.idx');
      if (idxBadge) idxBadge.textContent = `#${i+1}`;
      el.dataset.idx = String(i);
    });
  }

  // Reset
  document.getElementById('img-reset').addEventListener('click', () => {
    state.files = [];
    thumbs.innerHTML = '';
    input.value = '';
    orderInput.value = '';
  });

  // toggle grid-only inputs
  const gridOnly = () => {
    const isGrid = layoutSelect.value === 'grid';
    document.querySelectorAll('.grid-only').forEach(el => el.style.display = isGrid ? 'block' : 'none');
  };
  layoutSelect.addEventListener('change', gridOnly);
  gridOnly();
});