(function () {
  const data = window.MVP_DASHBOARD_DATA || { runs: [], summary: {} };

  const state = {
    ourEntitySizeChart: null,
    theirEntitySizeChart: null,
  };

  function byId(id) {
    return document.getElementById(id);
  }

  function fmtInt(value) {
    return typeof value === 'number' ? value.toLocaleString('en-US') : 'n/a';
  }

  function fmtPct(value) {
    return typeof value === 'number' ? `${value.toFixed(2)}%` : 'n/a';
  }

  function fmtApproxHoursFromMinutes(value) {
    if (typeof value !== 'number') {
      return 'n/a';
    }
    const hours = value / 60;
    const roundedHours = Math.max(1, Math.round(hours));
    if (roundedHours === 1) {
      return '~1 hour';
    }
    return `~${roundedHours} hours`;
  }

  function fmtApproxRecords(value) {
    if (typeof value !== 'number') {
      return 'n/a';
    }
    if (value >= 950000 && value <= 1050000) {
      return '~1 million';
    }
    if (value >= 1000000) {
      return `~${(value / 1000000).toFixed(2)} million`;
    }
    return fmtInt(value);
  }

  function fmtSignedPct(value) {
    if (typeof value !== 'number') {
      return 'n/a';
    }
    const sign = value > 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
  }

  function fmtOutOf(value, total) {
    if (typeof value !== 'number' || typeof total !== 'number' || total < 0) {
      return 'n/a';
    }
    return `${fmtInt(value)} / ${fmtInt(total)}`;
  }

  function fmtPctOutOf(value, total) {
    if (typeof value !== 'number' || typeof total !== 'number' || total <= 0) {
      return 'n/a';
    }
    const pct = (value / total) * 100;
    return `${pct.toFixed(2)}%`;
  }

  function asNumber(value) {
    return typeof value === 'number' && Number.isFinite(value) ? value : null;
  }

  function ratioPct(num, den) {
    if (typeof num !== 'number' || typeof den !== 'number' || den <= 0) {
      return null;
    }
    return (num / den) * 100;
  }

  function escapeHtml(text) {
    return String(text)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function getOurMetricHelp(label, run) {
    const inputRecords = asNumber(run.records_input);
    const ourGroupedMembers = asNumber(run.our_grouped_members);
    const theirGroupedMembers = asNumber(run.their_grouped_members);
    const ourEntities = asNumber(run.our_entities_formed) ?? asNumber(run.our_resolved_entities);
    const theirEntities = asNumber(run.their_entities_formed) ?? asNumber(run.resolved_entities);
    const isPartial = asNumber(run.records_input_reported) > asNumber(run.records_input);

    const map = {
      'Match %': `Percentage of loaded records that Our reference (SOURCE_IPG_ID groups) considers matched, meaning records that belong to groups with at least 2 members.${isPartial ? ' This run is partial, so percentages refer only to loaded records.' : ''}`,
      'Entities Created': 'Total number of entities formed by Our reference grouping on the loaded records. Records with missing/blank IPG are treated as singleton entities (size 1).',
    };
    return map[label] || '';
  }

  function getTheirMetricHelp(label, run) {
    const inputRecords = asNumber(run.records_input);
    const ourGroupedMembers = asNumber(run.our_grouped_members);
    const theirGroupedMembers = asNumber(run.their_grouped_members);
    const ourEntities = asNumber(run.our_entities_formed) ?? asNumber(run.our_resolved_entities);
    const theirEntities = asNumber(run.their_entities_formed) ?? asNumber(run.resolved_entities);
    const isPartial = asNumber(run.records_input_reported) > asNumber(run.records_input);

    const map = {
      'Match %': `Percentage of loaded records that Their engine resolves into multi-record entities (at least 2 records per entity).${isPartial ? ' This run is partial, so percentages refer only to loaded records.' : ''}`,
      'Entities Created': 'Total number of entities resolved by Their engine on the loaded records.',
      'Match Gain/Loss %': 'Difference between Their and Our matched-record coverage on the same loaded population. Positive means Their side groups more records; negative means Our side groups more records.',
    };
    return map[label] || '';
  }

  function refreshTooltips() {
    if (!window.bootstrap || typeof window.bootstrap.Tooltip !== 'function') {
      return;
    }
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach((element) => {
      window.bootstrap.Tooltip.getOrCreateInstance(element, {
        container: 'body',
        trigger: 'hover focus',
      });
    });
  }

  function setTooltipText(element, text) {
    if (!element || typeof text !== 'string') {
      return;
    }
    element.setAttribute('data-bs-title', text);
    element.setAttribute('title', text);
    element.setAttribute('aria-label', text);
    if (window.bootstrap && typeof window.bootstrap.Tooltip === 'function') {
      const instance = window.bootstrap.Tooltip.getInstance(element);
      if (instance) {
        instance.dispose();
      }
    }
  }

  function getAllRuns() {
    return Array.isArray(data.runs) ? data.runs : [];
  }

  function getStatus(run) {
    return run && typeof run.run_status === 'string' ? run.run_status : 'incomplete';
  }

  function hasRenderableMetrics(run) {
    if (!run || typeof run !== 'object') {
      return false;
    }
    const inputRecords = asNumber(run.records_input);
    const ourEntities = asNumber(run.our_entities_formed) ?? asNumber(run.our_resolved_entities);
    const theirEntities = asNumber(run.their_entities_formed) ?? asNumber(run.resolved_entities);
    const ourMatchPct = asNumber(run.our_match_pct);
    const theirMatchPct = asNumber(run.their_match_pct);
    return (
      typeof inputRecords === 'number' &&
      (typeof ourMatchPct === 'number' ||
        typeof theirMatchPct === 'number' ||
        typeof ourEntities === 'number' ||
        typeof theirEntities === 'number')
    );
  }

  function getRenderableRuns() {
    return getAllRuns().filter(hasRenderableMetrics);
  }

  function getRun() {
    const renderable = getRenderableRuns();
    if (renderable.length) {
      return renderable[0];
    }
    const all = getAllRuns();
    return all.length ? all[0] : null;
  }


  function renderSelectedRunCards(run) {
    const inputRecords = asNumber(run.records_input);
    const ourEntities = asNumber(run.our_entities_formed) ?? asNumber(run.our_resolved_entities);
    const theirEntities = asNumber(run.their_entities_formed) ?? asNumber(run.resolved_entities);
    const ourGroupedMembers = asNumber(run.our_grouped_members);
    const theirGroupedMembers = asNumber(run.their_grouped_members);
    const ourMatchPct = asNumber(run.our_match_pct) ?? ratioPct(ourGroupedMembers, inputRecords);
    const theirMatchPct = asNumber(run.their_match_pct) ?? ratioPct(theirGroupedMembers, inputRecords);
    const theirMatchGainLossPct = asNumber(run.their_match_gain_loss_pct);

    const ourCards = [
      { label: 'Match %', value: fmtPct(ourMatchPct), help: getOurMetricHelp('Match %', run) },
      { label: 'Entities Created', value: fmtInt(ourEntities), help: getOurMetricHelp('Entities Created', run) },
    ];

    const theirCards = [
      { label: 'Match %', value: fmtPct(theirMatchPct), help: getTheirMetricHelp('Match %', run) },
      { label: 'Entities Created', value: fmtInt(theirEntities), help: getTheirMetricHelp('Entities Created', run) },
    ];

    byId('ourMetricCards').innerHTML = ourCards
      .map(
        (card) => `
          <div class="col-12 col-sm-6 col-xl-6 fade-up">
            <div class="card metric-card metric-card-our">
              <div class="card-body">
                <div class="metric-label">${escapeHtml(card.label)}</div>
                <span
                  class="metric-help-icon"
                  role="button"
                  tabindex="0"
                  data-help-text="${escapeHtml(card.help)}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  data-bs-title="${escapeHtml(card.help)}"
                  title="${escapeHtml(card.help)}"
                  aria-label="${escapeHtml(card.help)}"
                >i</span>
                <div class="metric-value">${escapeHtml(card.value)}</div>
              </div>
            </div>
          </div>
        `
      )
      .join('');

    byId('theirMetricCards').innerHTML = theirCards
      .map(
        (card) => `
          <div class="col-12 col-sm-6 col-xl-6 fade-up">
            <div class="card metric-card">
              <div class="card-body">
                <div class="metric-label">${escapeHtml(card.label)}</div>
                <span
                  class="metric-help-icon"
                  role="button"
                  tabindex="0"
                  data-help-text="${escapeHtml(card.help)}"
                  data-bs-toggle="tooltip"
                  data-bs-placement="top"
                  data-bs-title="${escapeHtml(card.help)}"
                  title="${escapeHtml(card.help)}"
                  aria-label="${escapeHtml(card.help)}"
                >i</span>
                <div class="metric-value">${escapeHtml(card.value)}</div>
              </div>
            </div>
          </div>
        `
      )
      .join('');

    const executionMinutes = asNumber(run.execution_minutes);
    const executionMinutesEstimated = asNumber(run.execution_minutes_estimated);
    byId('inputRecordsValue').textContent = fmtApproxRecords(run.records_input);
    byId('executionMinutesValue').textContent = fmtApproxHoursFromMinutes(
      executionMinutes !== null ? executionMinutes : executionMinutesEstimated
    );
    byId('theirMatchGainLossValue').textContent = fmtSignedPct(theirMatchGainLossPct);
    refreshTooltips();
  }

  function destroyChart(name) {
    if (state[name]) {
      state[name].destroy();
      state[name] = null;
    }
  }

  function toDistribution(obj) {
    const entries = Object.entries(obj || {})
      .map(([k, v]) => [String(k), Number(v)])
      .filter(([, v]) => Number.isFinite(v))
      .sort((a, b) => Number(a[0]) - Number(b[0]));
    return {
      labels: entries.map(([k]) => k),
      values: entries.map(([, v]) => v),
    };
  }

  function renderSelectedCharts(run) {
    destroyChart('ourEntitySizeChart');
    destroyChart('theirEntitySizeChart');

    const ourEntityAll = toDistribution(run.our_entity_size_distribution);
    const ourLabels = [];
    const ourValues = [];
    ourEntityAll.labels.forEach((label, index) => {
      const size = Number(label);
      if (Number.isFinite(size) && size <= 30) {
        ourLabels.push(label);
        ourValues.push(ourEntityAll.values[index]);
      }
    });
    state.ourEntitySizeChart = new Chart(byId('ourEntitySizeChart'), {
      type: 'bar',
      data: {
        labels: ourLabels,
        datasets: [
          {
            label: 'Entity count',
            data: ourValues,
            backgroundColor: '#ffffff',
            borderColor: '#ffffff',
            hoverBackgroundColor: '#ffffff',
            hoverBorderColor: '#ffffff',
            borderWidth: 1,
            minBarLength: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label(context) {
                const y = context.parsed && typeof context.parsed.y === 'number' ? context.parsed.y : null;
                return y === null ? 'n/a' : `Entity count: ${fmtInt(y)}`;
              },
            },
          },
        },
        scales: {
          x: {
            ticks: { color: '#e6edf8' },
            grid: { color: 'rgba(230,237,248,0.14)' },
          },
          y: {
            type: 'logarithmic',
            min: 1,
            title: {
              display: true,
              text: 'Entity count (log scale)',
              color: '#e6edf8',
            },
            ticks: {
              color: '#e6edf8',
              callback(value) {
                return fmtInt(Number(value));
              },
            },
            grid: { color: 'rgba(230,237,248,0.14)' },
          },
        },
      },
    });

    const theirEntityAll = toDistribution(run.entity_size_distribution);
    const theirLabels = [];
    const theirValues = [];
    theirEntityAll.labels.forEach((label, index) => {
      const size = Number(label);
      if (Number.isFinite(size) && size <= 30) {
        theirLabels.push(label);
        theirValues.push(theirEntityAll.values[index]);
      }
    });
    state.theirEntitySizeChart = new Chart(byId('theirEntitySizeChart'), {
      type: 'bar',
      data: {
        labels: theirLabels,
        datasets: [
          {
            label: 'Entity count',
            data: theirValues,
            backgroundColor: '#ffffff',
            borderColor: '#ffffff',
            hoverBackgroundColor: '#ffffff',
            hoverBorderColor: '#ffffff',
            borderWidth: 1,
            minBarLength: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label(context) {
                const y = context.parsed && typeof context.parsed.y === 'number' ? context.parsed.y : null;
                return y === null ? 'n/a' : `Entity count: ${fmtInt(y)}`;
              },
            },
          },
        },
        scales: {
          x: {
            ticks: { color: '#e6edf8' },
            grid: { color: 'rgba(230,237,248,0.14)' },
          },
          y: {
            type: 'logarithmic',
            min: 1,
            title: {
              display: true,
              text: 'Entity count (log scale)',
              color: '#e6edf8',
            },
            ticks: {
              color: '#e6edf8',
              callback(value) {
                return fmtInt(Number(value));
              },
            },
            grid: { color: 'rgba(230,237,248,0.14)' },
          },
        },
      },
    });
    renderTopMatchKeys(run);
  }

  function prettifyMatchKey(rawKey) {
    if (typeof rawKey !== 'string') {
      return '';
    }
    return rawKey
      .replace(/TAX[_-]?ID/gi, '<<TAXIDTOKEN>>')
      .replace(/[+_-]+/g, ', ')
      .replace(/<<TAXIDTOKEN>>/g, 'Tax ID')
      .replace(/\s*,\s*/g, ', ')
      .replace(/(,\s*){2,}/g, ', ')
      .replace(/^,\s*|\s*,$/g, '')
      .trim();
  }

  function renderTopMatchKeys(run) {
    const container = byId('matchKeyList');
    if (!container) {
      return;
    }
    const topKeys = Array.isArray(run.top_match_keys) ? run.top_match_keys : [];
    if (!topKeys.length) {
      container.innerHTML = '<div class="match-key-empty">No match keys available for this run.</div>';
      return;
    }

    const counts = topKeys.map((item) => (typeof item[1] === 'number' ? item[1] : 0));
    const maxCount = Math.max(...counts, 1);
    const top10Total = counts.reduce((acc, value) => acc + value, 0);

    container.innerHTML = topKeys
      .map((item, index) => {
        const rawLabel = typeof item[0] === 'string' ? item[0] : '';
        const count = typeof item[1] === 'number' ? item[1] : 0;
        const widthPct = (count / maxCount) * 100;
        const sharePct = top10Total > 0 ? (count / top10Total) * 100 : 0;
        return `
          <div class="match-key-row">
            <div class="match-key-rank">#${index + 1}</div>
            <div class="match-key-center">
              <div class="match-key-label-line">
                <span class="match-key-label" title="${escapeHtml(rawLabel)}">${escapeHtml(prettifyMatchKey(rawLabel))}</span>
                <span class="match-key-share">${sharePct.toFixed(1)}%</span>
              </div>
              <div class="match-key-track">
                <div class="match-key-fill" style="width:${widthPct.toFixed(2)}%"></div>
              </div>
            </div>
          </div>
        `;
      })
      .join('');
  }

  function renderCurrent() {
    const run = getRun();
    if (!run) {
      byId('inputRecordsValue').textContent = 'n/a';
      byId('executionMinutesValue').textContent = 'n/a';
      byId('theirMatchGainLossValue').textContent = 'n/a';
      byId('ourMetricCards').innerHTML =
        '<div class="col-12"><div class="alert alert-warning">No data available for selected run.</div></div>';
      byId('theirMetricCards').innerHTML =
        '<div class="col-12"><div class="alert alert-warning">No data available for selected run.</div></div>';
      return;
    }
    renderSelectedRunCards(run);
    renderSelectedCharts(run);
  }

  function renderEmptyState() {
    byId('inputRecordsValue').textContent = 'n/a';
    byId('executionMinutesValue').textContent = 'n/a';
    byId('theirMatchGainLossValue').textContent = 'n/a';
    byId('ourMetricCards').innerHTML =
      '<div class="col-12"><div class="alert alert-warning">Selected run details will appear here after the first successful run.</div></div>';
    byId('theirMetricCards').innerHTML =
      '<div class="col-12"><div class="alert alert-warning">Selected run details will appear here after the first successful run.</div></div>';
  }

  function boot() {
    if (!getAllRuns().length) {
      renderEmptyState();
      return;
    }
    renderCurrent();
  }

  boot();
})();
