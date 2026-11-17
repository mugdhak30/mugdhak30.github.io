/* Maps at the top of /talks/ and /year-archive/: a dot per place, and a panel listing what happened
   there when a dot is clicked. Markup and data come from _includes/place-map.html. */
(function () {
  var roots = document.querySelectorAll('.place-map');
  if (!roots.length || !window.jsVectorMap) return;

  // Where each map is centred and how far it is zoomed in.
  var VIEW = {
    // Talks reach from California to Melbourne and no further north than Copenhagen.
    talks: { coords: [10, 12], scale: 1.2 },
    // The blog map keeps room up to Lapland (~68°N).
    blog:  { coords: [17, 10], scale: 1.15 }
  };
  // Dot colour for each talk badge (from talks.yml); posters count with conferences.
  var GROUP = {
    'pub-asew': 'conf', 'pub-mobilesoft': 'conf', 'pub-icse': 'conf', 'pub-asejournal': 'conf',
    'workshop': 'conf', 'poster': 'conf',
    'invited-talk': 'invited', 'industry-talk': 'invited'
  };

  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  };
  var month = function (d) {
    var p = String(d).split('-');
    if (!p[1]) return p[0];
    return new Date(+p[0], +p[1] - 1).toLocaleString('en-GB', { month: 'short', year: 'numeric' });
  };
  var plural = function (n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); };
  function indexArg(args) {
    for (var i = 0; i < args.length; i++) {
      var x = args[i];
      if (typeof x === 'number' || (typeof x === 'string' && /^\d+$/.test(x))) return +x;
    }
  }

  function setup(root) {
    var D = JSON.parse(root.querySelector('.place-map-data').textContent);
    var talks = D.kind === 'talks';
    var canvas = root.querySelector('.place-map-canvas');
    var detail = root.querySelector('.place-map-detail');
    var css = function (n) { return getComputedStyle(root).getPropertyValue(n).trim(); };
    var place = function (k) { return D.places[k]; };
    var country = function (k) { return D.countries[place(k).cc] || { name: place(k).cc, flag: '' }; };

    // One list of items per place. Talks newest first, posts oldest first.
    var by = {};
    D.items.forEach(function (it) {
      (it.places || []).forEach(function (k) {
        if (!place(k)) {
          if (window.console) console.warn('place-map: unknown place "' + k + '" (' + (it.url || it.title) + '); add it to _data/places.yml');
          return;
        }
        (by[k] = by[k] || []).push(it);
      });
    });
    var keys = Object.keys(by);
    keys.forEach(function (k) {
      by[k].sort(function (a, b) { return talks ? b.date.localeCompare(a.date) : a.date.localeCompare(b.date); });
    });
    var countries = {};
    keys.forEach(function (k) { countries[place(k).cc] = 1; });

    var stats = talks
      ? [[D.items.length, 'presentations'], [keys.length, 'cities'], [Object.keys(countries).length, 'countries']]
      : [[D.items.length, 'posts'], [Object.keys(countries).length, 'countries']];
    root.querySelector('.place-map-stats').innerHTML = stats.map(function (s) {
      return '<div><b>' + s[0] + '</b><span>' + s[1] + '</span></div>';
    }).join('');

    // A place with several kinds of talk takes the colour of the most recent one.
    var color = function (k) { return css(talks ? '--pm-' + (GROUP[by[k][0].badge] || 'conf') : '--pm-written'); };
    var tip = function (k) { return plural(by[k].length, talks ? 'presentation' : 'blog post'); };
    var row = function (it) {
      var body = talks
        ? '<span class="pub-abbr ' + esc(it.badge) + '">' + esc(it.abbr) + '</span> ' + esc(it.title) +
          (it.venue ? '<br><span class="place-map-venue">' + esc(it.venue) + '</span>' : '')
        : '<a href="' + esc(it.url) + '">' + esc(it.title) + '</a>';
      return '<li><span class="place-map-when">' + month(it.date) + '</span><span>' + body + '</span></li>';
    };

    var map = null, selected = null, builtSize = '';
    function renderDetail() {
      if (!selected) { detail.hidden = true; detail.innerHTML = ''; return; }
      var c = country(selected);
      detail.innerHTML = '<div class="place-map-detail-head"><span>' + c.flag + ' <b>' + esc(place(selected).name) + '</b>, ' + esc(c.name) + '</span>' +
        '<button type="button" class="place-map-close" aria-label="Close">×</button></div><ul>' + by[selected].map(row).join('') + '</ul>';
      detail.hidden = false;
    }
    function build() {
      if (map) { try { map.destroy(); } catch (e) {} }
      canvas.innerHTML = '';
      builtSize = canvas.clientWidth + 'x' + canvas.clientHeight;
      // Smaller dots on phone-sized maps, so clusters (Germany, California) don't merge into one blob.
      var small = canvas.clientWidth < 500;
      var r = small ? 3 : 4.5, rSel = small ? 4.5 : 6.5, ring = small ? 0.8 : 1.2;
      map = new jsVectorMap({
        selector: canvas,
        map: 'world',
        zoomButtons: true,
        zoomOnScroll: false,
        zoomMax: 40,
        selectedRegions: Object.keys(countries),
        regionsSelectable: false,
        markersSelectable: false,
        regionStyle: {
          initial: { fill: css('--pm-land'), stroke: css('--pm-land-stroke'), strokeWidth: 0.3, fillOpacity: 1 },
          hover: { fillOpacity: 1, cursor: 'grab' },
          selected: { fill: css('--pm-visited') }
        },
        markerStyle: {
          initial: { stroke: css('--pm-bg'), strokeWidth: ring, r: r, fillOpacity: 0.95 },
          hover: { cursor: 'pointer', stroke: css('--pm-fg') }
        },
        markers: keys.map(function (k) {
          var style = { fill: color(k) };
          if (k === selected) { style.stroke = css('--pm-fg'); style.strokeWidth = small ? 1.8 : 2.5; style.r = rSel; }
          return { name: place(k).name, coords: [place(k).lat, place(k).lng], style: style };
        }),
        onRegionTooltipShow: function () {
          var t = [].slice.call(arguments).filter(function (x) { return x && typeof x.hide === 'function'; })[0];
          if (t) t.hide();
        },
        onMarkerTooltipShow: function () {
          var args = [].slice.call(arguments);
          var t = args.filter(function (x) { return x && typeof x.text === 'function'; })[0];
          var i = indexArg(args);
          if (t && i !== undefined) {
            var k = keys[i];
            t.text('<b>' + country(k).flag + ' ' + esc(place(k).name) + '</b><br>' + tip(k), true);
          }
        },
        onMarkerClick: function () {
          var i = indexArg(arguments);
          if (i === undefined) return;
          select(keys[i]);
        }
      });
      var v = VIEW[D.kind] || VIEW.blog;
      try { map.setFocus({ coords: v.coords, scale: v.scale }); } catch (e) {}
    }
    // Clicking a dot opens its panel below the map; clicking it again closes it.
    function select(k) {
      selected = selected === k ? null : k;
      renderDetail();
      build();
      if (selected) detail.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    detail.addEventListener('click', function (e) { if (e.target.closest('.place-map-close')) select(selected); });

    build();
    // Repaint when the site's theme toggle changes.
    new MutationObserver(build).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    // The library keeps the size the map had when it was drawn, so redraw when the box changes size.
    var t;
    function sizeChanged() {
      if (canvas.clientWidth + 'x' + canvas.clientHeight === builtSize) return;
      clearTimeout(t);
      t = setTimeout(build, 150);
    }
    if (window.ResizeObserver) new ResizeObserver(sizeChanged).observe(canvas);
    else window.addEventListener('resize', sizeChanged);
  }

  // The map library only draws once the page has finished loading.
  function start() { [].forEach.call(roots, setup); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
