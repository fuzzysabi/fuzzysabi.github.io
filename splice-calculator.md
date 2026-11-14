---
layout: page
title: Splice Calculator
date: '2026-11-11'
permalink: /splice-calculator/
---

<style>
  .splice { max-width: 34rem; color-scheme: light dark; }
  .splice fieldset { border: 0; padding: 0; margin: 0 0 1rem; }
  .splice legend { font-weight: 600; margin-bottom: .4rem; padding: 0; }
  .splice fieldset label { display: block; margin: .2rem 0; cursor: pointer; }
  .splice input[type="text"], .splice input[type="number"], .splice select, .splice button {
    font: inherit; color: inherit; background: transparent;
    border: 1px solid rgba(128,128,128,.55); border-radius: 4px; padding: .4rem .55rem;
  }
  .splice input:focus-visible, .splice select:focus-visible, .splice button:focus-visible {
    outline: 2px solid currentColor; outline-offset: 2px;
  }
  .splice-row { display: flex; gap: .5rem; margin-bottom: .5rem; }
  .splice-row .splice-val { flex: 1; min-width: 0; }
  .splice-row .splice-val[aria-invalid="true"] { border-color: #c0392b; }
  .splice-count { margin-bottom: .75rem; }
  .splice-count input { width: 5rem; margin-left: .4rem; }
  .splice button { cursor: pointer; }
  .splice button:hover { background: rgba(128,128,128,.18); }
  .splice-remove { padding: .4rem .7rem; }
  .splice[data-mode="same"] .splice-row:not(:first-child),
  .splice[data-mode="same"] .splice-remove,
  .splice[data-mode="same"] #splice-add,
  .splice[data-mode="diff"] .splice-count { display: none; }
  #splice-out { margin-top: 1.25rem; padding-left: .9rem; border-left: 3px solid currentColor; line-height: 1.5; }
  #splice-out p { margin: 0 0 .35rem; }
  #splice-out .splice-answer { font-size: 1.35rem; font-weight: 600; }
  #splice-out .splice-error { color: #c0392b; }
  @media (prefers-color-scheme: dark) { #splice-out .splice-error, .splice-row .splice-val[aria-invalid="true"] { color: #ff8a7a; border-color: #ff8a7a; } }
    /* Phone-friendly: 16px inputs stop iOS zooming on focus */
  .splice input[type="text"], .splice input[type="number"], .splice select, .splice button { font-size: 16px; }

  @media (max-width: 520px) {
    .splice fieldset label { padding: .45rem 0; }
    .splice fieldset input[type="radio"] { width: 1.15rem; height: 1.15rem; margin-right: .4rem; vertical-align: -.15rem; }

    /* each wire becomes two lines: size on top, unit + remove below */
    .splice-row { flex-wrap: wrap; gap: .4rem .5rem; margin-bottom: .75rem; padding-bottom: .6rem; border-bottom: 1px solid rgba(128,128,128,.25); }
    .splice-row .splice-val { flex: 1 1 100%; }
    .splice-row .splice-unit { flex: 1 1 0; min-width: 0; }

    .splice input[type="text"], .splice input[type="number"], .splice select, .splice button { padding: .6rem .7rem; }
    .splice .splice-remove { padding: .6rem 1rem; }
    .splice-count input { width: 6rem; }
    #splice-add { width: 100%; }
    #splice-out .splice-answer { font-size: 1.5rem; }
  }
</style>

<div class="splice" id="splice" data-mode="same">
  <fieldset>
    <legend>Wires in the splice</legend>
    <label><input type="radio" name="splice-mode" value="same" checked> Multiple of the same gauge</label>
    <label><input type="radio" name="splice-mode" value="diff"> Different gauges</label>
  </fieldset>

  <div id="splice-rows"></div>

  <div class="splice-count">
    <label>Number of wires <input type="number" id="splice-n" min="1" step="1" value="2"></label>
  </div>

  <button type="button" id="splice-add">+ Add wire</button>

  <div id="splice-out" aria-live="polite"></div>
</div>

<script>
(function () {
  var CMIL_TO_MM2 = 5.067e-4; // same constant as fuzfunctions.py
  var MIN_AWG = -3;           // 4/0
  var MAX_AWG = 40;

  var root = document.getElementById('splice');
  var rowsEl = document.getElementById('splice-rows');
  var countEl = document.getElementById('splice-n');
  var outEl = document.getElementById('splice-out');

  // Circular mil area of an AWG size (same formula as area() in fuzfunctions.py)
  function area(awg) {
    return Math.pow(5 * Math.pow(92, (36 - awg) / 39), 2);
  }

  // First gauge whose area exceeds the total (same stepping as awgbyarea()).
  // Returns null if the total is larger than 4/0 AWG.
  function awgByArea(totalCmil) {
    var q = MAX_AWG;
    while (q >= MIN_AWG) {
      if (area(q) > totalCmil) return q;
      q = q > 2 ? q - 2 : q - 1;
    }
    return null;
  }

  // Accepts 12, 0, 00, 000, 0000, 1/0 ... 4/0. Returns NaN if invalid.
  function parseAwg(text) {
    var t = text.trim();
    var m;
    if ((m = /^(\d+)\/0$/.exec(t))) return -(parseInt(m[1], 10) - 1);
    if (/^0+$/.test(t)) return -(t.length - 1);
    if (/^-?\d+$/.test(t)) return parseInt(t, 10);
    return NaN;
  }

  function fmtAwg(q) {
    if (q <= 0) return (1 - q) + '/0 AWG';
    return q + ' AWG';
  }

  function fmtMm(x) { return x.toFixed(3) + ' mm²'; }
  function fmtCmil(x) { return Math.round(x).toLocaleString('en-US') + ' cmil'; }

  function addRow() {
    var row = document.createElement('div');
    row.className = 'splice-row';
    row.innerHTML =
      '<input type="text" class="splice-val" autocomplete="off" aria-label="Wire size">' +
      '<select class="splice-unit" aria-label="Unit">' +
      '<option value="awg">AWG</option><option value="mm">mm²</option></select>' +
      '<button type="button" class="splice-remove" aria-label="Remove wire">×</button>';
    rowsEl.appendChild(row);
    setPlaceholder(row);
    return row;
  }

  function setPlaceholder(row) {
    var unit = row.querySelector('.splice-unit').value;
    row.querySelector('.splice-val').placeholder = unit === 'awg' ? 'e.g. 12 or 2/0' : 'e.g. 2.5';
  }

  // Area in mm² for one row, or an error string, or null if the row is empty
  function rowArea(row) {
    var input = row.querySelector('.splice-val');
    var unit = row.querySelector('.splice-unit').value;
    var text = input.value.trim();
    input.removeAttribute('aria-invalid');
    if (text === '') return null;
    var result;
    if (unit === 'awg') {
      var g = parseAwg(text);
      if (isNaN(g) || g < MIN_AWG || g > MAX_AWG) {
        result = { error: 'Enter a gauge from 4/0 to 40 (e.g. 12, 0, 2/0).' };
      } else {
        result = { mm2: area(g) * CMIL_TO_MM2 };
      }
    } else {
      var v = Number(text);
      if (!isFinite(v) || v <= 0) result = { error: 'Enter an area greater than 0 mm².' };
      else result = { mm2: v };
    }
    if (result.error) input.setAttribute('aria-invalid', 'true');
    return result;
  }

  function line(cls, text) {
    var p = document.createElement('p');
    if (cls) p.className = cls;
    p.textContent = text;
    outEl.appendChild(p);
  }

  function calculate() {
    var same = root.dataset.mode === 'same';
    var rows = Array.prototype.slice.call(rowsEl.children);
    if (same) rows = rows.slice(0, 1);

    outEl.textContent = '';
    var total = 0, wires = 0, error = null;

    if (same) {
      var r = rowArea(rows[0]);
      var n = parseInt(countEl.value, 10);
      if (r && r.error) error = r.error;
      else if (r && (isNaN(n) || n < 1)) error = 'Enter a number of wires of 1 or more.';
      else if (r) { total = r.mm2 * n; wires = n; }
    } else {
      rows.forEach(function (row) {
        var r = rowArea(row);
        if (!r) return;
        if (r.error) { error = error || r.error; return; }
        total += r.mm2;
        wires += 1;
      });
    }

    if (error) { line('splice-error', error); return; }
    if (wires === 0) { line('', 'Enter a wire size to see the result.'); return; }

    var totalCmil = total / CMIL_TO_MM2;
    var q = awgByArea(totalCmil);

    if (q === null) {
      line('splice-answer', 'Larger than 4/0 AWG');
      line('', 'Total area ' + fmtMm(total) + ' (' + (totalCmil / 1000).toFixed(1) + ' kcmil). Use a kcmil-rated splice.');
      return;
    }

    line('splice-answer', 'Equivalent splice: ' + fmtAwg(q));
    line('', wires + (wires === 1 ? ' wire' : ' wires') + ', total ' + fmtMm(total) + ' (' + fmtCmil(totalCmil) + ')');
    line('', fmtAwg(q) + ' is ' + fmtMm(area(q) * CMIL_TO_MM2) + ' (' + fmtCmil(area(q)) + ')');
  }

  // Events
  root.addEventListener('input', calculate);
  root.addEventListener('change', function (e) {
    if (e.target.name === 'splice-mode') root.dataset.mode = e.target.value;
    if (e.target.classList.contains('splice-unit')) setPlaceholder(e.target.closest('.splice-row'));
    calculate();
  });
  root.addEventListener('click', function (e) {
    if (e.target.id === 'splice-add') {
      addRow().querySelector('.splice-val').focus();
      calculate();
    } else if (e.target.classList.contains('splice-remove') && rowsEl.children.length > 1) {
      e.target.closest('.splice-row').remove();
      calculate();
    }
  });

  addRow();
  addRow();
  calculate();
})();
</script>