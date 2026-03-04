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

  function fmtMinutes(value, isEstimate) {
    if (typeof value !== 'number') {
      return 'n/a';
    }
    if (isEstimate) {
      return `~${value.toFixed(2)} min`;
    }
    return `${value.toFixed(2)} min`;
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
      'Match Gain/Loss %': 'Difference between Our and Their matched-record coverage on the same loaded population. Positive means Our side groups more records; negative means Their side groups more records.',
      'Entity Gain/Loss %': 'Difference between Our and Their entity counts on the same loaded population. Positive means Our side forms more entities (typically more fragmented); negative means Their side forms more entities.',
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
      'Entity Gain/Loss %': 'Difference between Their and Our entity counts on the same loaded population. Positive means Their side forms more entities (typically more fragmented); negative means Our side forms more entities.',
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
    const ourMatchPct = asNumber(run.our_match_pct);
    const theirMatchPct = asNumber(run.their_match_pct);
    return typeof inputRecords === 'number' && (typeof ourMatchPct === 'number' || typeof theirMatchPct === 'number');
  }

  function getRenderableRuns() {
    return getAllRuns().filter(hasRenderableMetrics);
  }

  function getRun() {
    const runs = getRenderableRuns();
    return runs.length ? runs[0] : null;
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
    const theirEntityGainLossPct = asNumber(run.their_entity_gain_loss_pct);

    const ourCards = [
      { label: 'Match %', value: fmtPct(ourMatchPct), help: getOurMetricHelp('Match %', run) },
      { label: 'Entities Created', value: fmtInt(ourEntities), help: getOurMetricHelp('Entities Created', run) },
    ];

    const theirCards = [
      { label: 'Match %', value: fmtPct(theirMatchPct), help: getTheirMetricHelp('Match %', run) },
      { label: 'Entities Created', value: fmtInt(theirEntities), help: getTheirMetricHelp('Entities Created', run) },
      { label: 'Match Gain/Loss %', value: fmtSignedPct(theirMatchGainLossPct), help: getTheirMetricHelp('Match Gain/Loss %', run) },
      { label: 'Entity Gain/Loss %', value: fmtSignedPct(theirEntityGainLossPct), help: getTheirMetricHelp('Entity Gain/Loss %', run) },
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
    const isEstimate = executionMinutes === null && !!run.execution_minutes_is_estimate;
    byId('inputRecordsValue').textContent = fmtInt(run.records_input);
    byId('executionMinutesValue').textContent = fmtMinutes(
      executionMinutes !== null ? executionMinutes : executionMinutesEstimated,
      isEstimate
    );
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

    const ourEntity = toDistribution(run.our_entity_size_distribution);
    state.ourEntitySizeChart = new Chart(byId('ourEntitySizeChart'), {
      type: 'bar',
      data: {
        labels: ourEntity.labels,
        datasets: [
          {
            label: 'Entity count',
            data: ourEntity.values,
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

    const theirEntity = toDistribution(run.entity_size_distribution);
    state.theirEntitySizeChart = new Chart(byId('theirEntitySizeChart'), {
      type: 'bar',
      data: {
        labels: theirEntity.labels,
        datasets: [
          {
            label: 'Entity count',
            data: theirEntity.values,
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
    const totalEl = byId('matchKeyTotalValue');
    const totalInfoEl = byId('matchKeyTotalInfo');
    if (!container) {
      return;
    }
    const topKeys = Array.isArray(run.top_match_keys) ? run.top_match_keys : [];
    if (!topKeys.length) {
      container.innerHTML = '<div class="match-key-empty">No match keys available for this run.</div>';
      if (totalEl) {
        totalEl.innerHTML = '<span>Top 10: n/a</span><span>Total pairs: n/a</span>';
      }
      if (totalInfoEl) {
        setTooltipText(
          totalInfoEl,
          'Top 10 pairs are the pairs covered by the 10 keys shown. Total pairs are all unique matched record pairs in this run.'
        );
        refreshTooltips();
      }
      return;
    }

    const counts = topKeys.map((item) => (typeof item[1] === 'number' ? item[1] : 0));
    const maxCount = Math.max(...counts, 1);
    const top10Total = counts.reduce((acc, value) => acc + value, 0);
    const totalPairs =
      typeof run.top_match_keys_total_pairs === 'number' && run.top_match_keys_total_pairs > 0
        ? run.top_match_keys_total_pairs
        : top10Total;
    const coveragePct = totalPairs > 0 ? (top10Total / totalPairs) * 100 : null;
    if (totalEl) {
      totalEl.innerHTML = `<span>Top 10: ${fmtInt(top10Total)}</span><span>Total pairs: ${fmtInt(totalPairs)}</span>`;
    }
    if (totalInfoEl) {
      const coverageText = typeof coveragePct === 'number' ? `${coveragePct.toFixed(2)}%` : 'n/a';
      setTooltipText(
        totalInfoEl,
        `Top 10 pairs are the sum of pairs covered by the 10 keys shown (${fmtInt(top10Total)}). Total pairs are all unique matched record pairs in this run (${fmtInt(totalPairs)}). Top 10 coverage: ${coverageText}.`
      );
      refreshTooltips();
    }

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
            <div class="match-key-count">${fmtInt(count)}</div>
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
      if (byId('matchKeyTotalValue')) {
        byId('matchKeyTotalValue').innerHTML = '<span>Top 10: n/a</span><span>Total pairs: n/a</span>';
      }
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
    if (byId('matchKeyTotalValue')) {
      byId('matchKeyTotalValue').innerHTML = '<span>Top 10: n/a</span><span>Total pairs: n/a</span>';
    }
    byId('ourMetricCards').innerHTML =
      '<div class="col-12"><div class="alert alert-warning">Selected run details will appear here after the first successful run.</div></div>';
    byId('theirMetricCards').innerHTML =
      '<div class="col-12"><div class="alert alert-warning">Selected run details will appear here after the first successful run.</div></div>';
  }

  function boot() {
    if (!getRenderableRuns().length) {
      renderEmptyState();
      return;
    }
    renderCurrent();
  }

  boot();
})();
