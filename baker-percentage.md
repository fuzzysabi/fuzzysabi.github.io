---
layout: page
title: Baker's Percentage
date: '2026-11-11'
permalink: /bread-calculator/
---

# Baker's percentage calculator

Includes sourdough if you've got it, this is my basic weekly long sandwich loaf 
of molasses sourdough. Baked in [this pan](https://www.amazon.com/dp/B0FBRDZJL5?th=1), 
12 1/2 x 5 1/2 (about 1-1/2 times longer than a normal loaf pan).

<div id="bp-calc">
  <style>
    #bp-calc { max-width: 560px; margin: 0 auto; font-family: inherit; line-height: 1.4; }
    #bp-calc * { box-sizing: border-box; }
    #bp-calc .bp-top { display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-end; margin-bottom: 1rem; }
    #bp-calc label { display: flex; flex-direction: column; font-size: .85rem; gap: .25rem; }
    #bp-calc input[type=text], #bp-calc input[type=number], #bp-calc select {
      font: inherit; padding: .4rem .5rem; border: 1px solid rgba(128,128,128,.5);
      border-radius: 4px; background: transparent; color: inherit; min-width: 0;
    }
    #bp-calc input:focus-visible, #bp-calc select:focus-visible, #bp-calc button:focus-visible { outline: 2px solid currentColor; outline-offset: 2px; }
    #bp-calc input[type=number] { width: 5.5rem; }
    #bp-calc .bp-row { display: grid; grid-template-columns: 1fr 5rem 4.5rem 1.8rem; gap: .5rem; align-items: center; margin-bottom: .4rem; }
    #bp-calc .bp-row input[type=number] { width: 100%; }
    #bp-calc .bp-head { font-size: .8rem; opacity: .7; margin-bottom: .25rem; }
    #bp-calc .bp-g { text-align: right; font-variant-numeric: tabular-nums; font-weight: 600; }
    #bp-calc .bp-g small { display: block; font-weight: 400; opacity: .65; font-size: .72rem; }
    #bp-calc .bp-row[hidden] { display: none; }
    #bp-calc .bp-sdrow { padding: .45rem .5rem; margin: .2rem -.5rem .8rem; border: 1px solid rgba(128,128,128,.5); border-radius: 6px; background: rgba(128,128,128,.12); }
    #bp-calc .bp-sdrow > span:first-child { font-weight: 600; }
    #bp-calc .bp-sdrow small { display: block; font-weight: 400; opacity: .7; font-size: .78rem; }
    #bp-calc .bp-x { border: 0; background: transparent; color: inherit; opacity: .55; cursor: pointer; font-size: 1.1rem; }
    #bp-calc .bp-x:hover { opacity: 1; }
    #bp-calc .bp-btn { font: inherit; padding: .35rem .75rem; border: 1px solid rgba(128,128,128,.6); border-radius: 4px; background: transparent; color: inherit; cursor: pointer; margin: .3rem .4rem .8rem 0; }
    #bp-calc .bp-btn:hover { background: rgba(128,128,128,.15); }
    #bp-calc h3 { margin: 1.2rem 0 .4rem; font-size: 1rem; }
    #bp-calc .bp-sd { border: 1px solid rgba(128,128,128,.4); border-radius: 6px; padding: .8rem; margin: .5rem 0 1rem; }
    #bp-calc .bp-sd-fields { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: .6rem; }
    #bp-calc .bp-sd-fields[hidden] { display: none; }
    #bp-calc .bp-inline { flex-direction: row; align-items: center; gap: .5rem; font-size: 1rem; }
    #bp-calc .bp-note { font-size: .85rem; opacity: .8; margin: .3rem 0; }
    #bp-calc .bp-warn { font-size: .85rem; color: #b45309; margin: .3rem 0; }
    @media (prefers-color-scheme: dark) { #bp-calc .bp-warn { color: #fbbf24; } }
  </style>

  <div class="bp-top">
    <label>Dough weight per piece (g)
      <input type="number" id="bp-total" value="1500" min="1" step="50">
    </label>
    <label>Pieces
      <input type="number" id="bp-pieces" value="1" min="1" step="1">
    </label>
    <label>Round to
      <select id="bp-round">
        <option value="1">1 g</option>
        <option value="5" selected>5 g</option>
        <option value="10">10 g</option>
      </select>
    </label>
  </div>

  <div class="bp-row bp-head"><span>Flours</span><span>Percent</span><span style="text-align:right">Grams</span><span></span></div>
  <div id="bp-flours"></div>
  <button type="button" class="bp-btn" id="bp-add-flour">+ add flour</button>
  <div class="bp-warn" id="bp-flour-warn" hidden></div>

  <div class="bp-row bp-sdrow" id="bp-sd-row" hidden>
    <span>Sourdough starter<small id="bp-sd-split"></small></span>
    <span id="bp-sd-pctshow"></span>
    <div class="bp-g" id="bp-sd-g"></div>
    <span></span>
  </div>

  <div class="bp-row bp-head"><span>Other ingredients</span><span>Percent</span><span style="text-align:right">Grams</span><span></span></div>
  <div id="bp-others"></div>
  <button type="button" class="bp-btn" id="bp-add-other">+ add ingredient</button>

  <div class="bp-sd">
    <label class="bp-inline">
      <input type="checkbox" id="bp-sd-on" checked> Use sourdough starter
    </label>
    <div class="bp-sd-fields" id="bp-sd-fields" hidden>
      <label>Starter (% of flour)
        <input type="number" id="bp-sd-pct" value="30" min="0" step="5">
      </label>
      <label>Starter hydration (%)
        <input type="number" id="bp-sd-hyd" value="100" min="1" step="5">
      </label>
    </div>
    <div class="bp-note" id="bp-sd-out" hidden></div>
  </div>

  <div class="bp-note" id="bp-summary"></div>
  <div class="bp-note">Amounts of 50 g or more are rounded to the step you choose; smaller amounts to the nearest gram. Percentages are of total flour weight.</div>

  <script>
  (function () {
    var flours = [
      { name: 'Wheat Flour', pct: 50 },
      { name: 'White flour', pct: 50 }
    ];
    var others = [
      { name: 'Water', pct: 65, water: true },
      { name: 'Fat', pct: 10 },
      { name: 'Molasses', pct: 5 },
      { name: 'Salt', pct: 2 }
    ];
    var $ = function (id) { return document.getElementById(id); };
    var gEls = [];   // output elements, rebuilt on render

    function step() { return +$('bp-round').value || 1; }
    function rnd(x) { return x < 50 ? Math.round(x) : Math.round(x / step()) * step(); }
    function num(v) { v = parseFloat(v); return isFinite(v) && v >= 0 ? v : 0; }

    function buildRows(list, host, canRemoveFn, type) {
      host.innerHTML = '';
      list.forEach(function (item, i) {
        var row = document.createElement('div');
        row.className = 'bp-row';

        var name = document.createElement('input');
        name.type = 'text'; name.value = item.name; name.placeholder = 'Name';
        name.setAttribute('aria-label', 'Ingredient name');
        name.oninput = function () { item.name = name.value; update(); };

        var pct = document.createElement('input');
        pct.type = 'number'; pct.value = item.pct; pct.min = 0; pct.step = 1;
        pct.setAttribute('aria-label', (item.name || 'Ingredient') + ' percent');
        pct.oninput = function () { item.pct = num(pct.value); update(); };

        var g = document.createElement('div');
        g.className = 'bp-g';
        gEls.push({ item: item, el: g, type: type });

        var x = document.createElement('button');
        x.type = 'button'; x.className = 'bp-x'; x.textContent = '×';
        x.setAttribute('aria-label', 'Remove ' + (item.name || 'ingredient'));
        if (canRemoveFn(item)) {
          x.onclick = function () { list.splice(i, 1); render(); };
        } else { x.style.visibility = 'hidden'; }

        row.appendChild(name); row.appendChild(pct); row.appendChild(g); row.appendChild(x);
        host.appendChild(row);
      });
    }

    function render() {
      gEls = [];
      buildRows(flours, $('bp-flours'), function () { return flours.length > 1; }, 'flour');
      buildRows(others, $('bp-others'), function (it) { return !it.water; }, 'other');
      update();
    }

    function update() {
      var pieces = Math.max(Math.round(num($('bp-pieces').value)), 1);
      var total = num($('bp-total').value) * pieces;
      var flourPct = flours.reduce(function (s, f) { return s + f.pct; }, 0);
      var allPct = flourPct + others.reduce(function (s, o) { return s + o.pct; }, 0);
      var F = allPct ? total / allPct : 0; // grams per 1%
      function amt(p) { return rnd(F * p); }

      var warn = $('bp-flour-warn');
      if (Math.abs(flourPct - 100) > 0.01) {
        warn.hidden = false;
        warn.textContent = 'Flours add up to ' + (Math.round(flourPct * 10) / 10) + '%. In a baker\'s formula they should total 100%.';
      } else { warn.hidden = true; }

      // sourdough
      var on = $('bp-sd-on').checked;
      $('bp-sd-fields').hidden = !on;
      var sdOut = $('bp-sd-out');
      var sdFlour = 0, sdWater = 0, sdTotal = 0;
      if (on) {
        var hyd = Math.max(num($('bp-sd-hyd').value), 1) / 100;
        var totalFlour = amt(flourPct);
        sdTotal = rnd(totalFlour * num($('bp-sd-pct').value) / 100);
        sdFlour = Math.round(sdTotal / (1 + hyd));
        sdWater = sdTotal - sdFlour;
        sdOut.hidden = false;
        sdOut.textContent = 'Starter: ' + sdTotal + ' g (' + sdFlour + ' g flour + ' + sdWater + ' g water). The flour comes out of the first flour listed, the water out of the water below.';
      } else { sdOut.hidden = true; }

      $('bp-sd-row').hidden = !on;
      if (on) {
        $('bp-sd-pctshow').textContent = num($('bp-sd-pct').value) + '%';
        $('bp-sd-g').textContent = sdTotal + ' g';
        $('bp-sd-split').textContent = sdFlour + ' g flour + ' + sdWater + ' g water';
      }

      var sum = 0, short = false, remaining = sdFlour;
      gEls.forEach(function (o) {
        var full = amt(o.item.pct), out = full, note = '';
        if (on && o.type === 'flour') {
          // starter flour comes out of the first flour listed;
          // only if that runs out does the rest come from the next one
          var take = Math.min(remaining, full);
          out = full - take;
          remaining -= take;
        } else if (on && o.item.water) {
          out = full - sdWater;
        }
        if (out < 0) { out = 0; short = true; }
        if (on && out !== full) note = '<small>of ' + full + ' g</small>';
        o.el.innerHTML = out + ' g' + note;
        sum += out;
      });
      if (remaining > 0) short = true;
      if (on) sum += sdTotal;
      var msg = 'Total: ' + sum + ' g' + (pieces > 1 ? ' for ' + pieces + ' pieces (about ' + Math.round(sum / pieces) + ' g each)' : '') + (sum !== Math.round(total) ? ', rounding makes this differ slightly from ' + Math.round(total) + ' g' : '');
      if (short) msg += '. The starter is more flour or water than the formula has; lower the starter percentage.';
      $('bp-summary').textContent = msg;
    }

    $('bp-add-flour').onclick = function () { flours.push({ name: 'Flour ' + (flours.length + 1), pct: 0 }); render(); };
    $('bp-add-other').onclick = function () { others.push({ name: '', pct: 0 }); render(); };
    ['bp-total', 'bp-pieces', 'bp-round', 'bp-sd-on', 'bp-sd-pct', 'bp-sd-hyd'].forEach(function (id) {
      $(id).addEventListener('input', update);
      $(id).addEventListener('change', update);
    });
    render();
  })();
  </script>
</div>