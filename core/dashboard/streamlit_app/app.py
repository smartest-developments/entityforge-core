#!/usr/bin/env python3
"""Streamlit wrapper that renders the exact core HTML dashboard with intro animation."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


INTRO_SNIPPET = """
<div id="scv-intro-overlay" aria-hidden="true">
  <div class="scv-intro-title">
    <span class="scv-line-1">SCV</span>
    <span class="scv-line-2">Senzing PoC</span>
  </div>
</div>
<style>
  .page-body {
    padding-top: 12px !important;
  }
  #scv-intro-overlay {
    position: fixed;
    inset: 0;
    z-index: 99999;
    pointer-events: none;
    overflow: hidden;
    background: linear-gradient(180deg, #0b1220 0%, #1f2937 100%);
    transition: opacity 1600ms ease;
    opacity: 1;
  }
  #scv-intro-overlay .scv-intro-title {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transform: translateY(-4.5vh);
    color: #f8fafc;
    font-family: "Avenir Next", "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: clamp(48px, 7.4vw, 120px);
    font-weight: 900;
    text-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);
    opacity: 1;
    transition: opacity 900ms ease;
  }
  #scv-intro-overlay .scv-intro-title .scv-line-1 {
    font-size: 0.9em;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    line-height: 1.02;
    margin-left: 0;
    opacity: 0.96;
  }
  #scv-intro-overlay .scv-intro-title .scv-line-2 {
    font-size: 0.9em;
    letter-spacing: 0.04em;
    line-height: 1.02;
    margin-top: 0.06em;
    text-transform: none !important;
    font-variant: normal;
  }
  #scv-intro-overlay.scv-fade { opacity: 0; }
  #scv-intro-overlay.scv-fade .scv-intro-title { opacity: 0; }
</style>
<script>
  (function () {
    const run = function () {
      const overlay = document.getElementById("scv-intro-overlay");
      if (!overlay) return;
      setTimeout(function () {
        overlay.classList.add("scv-fade");
      }, 1700);
      setTimeout(function () {
        if (overlay && overlay.parentNode) {
          overlay.parentNode.removeChild(overlay);
        }
      }, 3600);
    };
    if (document.readyState === "complete" || document.readyState === "interactive") {
      run();
    } else {
      window.addEventListener("load", run, { once: true });
    }
  })();
</script>
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_exact_dashboard_html(
    html_template: Path,
    tabler_css: Path,
    dashboard_css: Path,
    tabler_js: Path,
    chart_js: Path,
    data_js: Path,
    dashboard_js: Path,
) -> str:
    html = read_text(html_template)

    html = html.replace(
        '<link rel="stylesheet" href="./tabler.min.css">',
        f"<style>\n{read_text(tabler_css)}\n</style>",
    )
    html = html.replace(
        '<link rel="stylesheet" href="./management_dashboard.css">',
        f"<style>\n{read_text(dashboard_css)}\n</style>",
    )

    html = html.replace(
        '<script src="./tabler.min.js"></script>',
        f"<script>\n{read_text(tabler_js)}\n</script>",
    )
    html = html.replace(
        '<script src="./chart.umd.js"></script>',
        f"<script>\n{read_text(chart_js)}\n</script>",
    )
    html = html.replace(
        '<script src="./management_dashboard_data.js"></script>',
        f"<script>\n{read_text(data_js)}\n</script>",
    )
    html = html.replace(
        '<script src="./management_dashboard.js"></script>',
        f"<script>\n{read_text(dashboard_js)}\n</script>",
    )

    html = html.replace("</body>", f"{INTRO_SNIPPET}\n</body>")
    return html


def main() -> None:
    st.set_page_config(page_title="SCV Senzing PoC", layout="wide", initial_sidebar_state="collapsed")

    # Maximize canvas so HTML dashboard keeps its own original geometry.
    st.markdown(
        """
        <style>
          [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
          footer { display: none !important; }
          header { display: none !important; }
          .block-container { max-width: 100% !important; padding: 0 !important; }
          .main > div { padding-top: 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    app_root = Path(__file__).resolve().parent
    assets_root = app_root / "assets"
    default_data_js = assets_root / "management_dashboard_data.js"

    use_external_data = st.sidebar.toggle("Use external data file", value=False)
    if use_external_data:
        st.sidebar.header("External data source")
        data_js_path_raw = st.sidebar.text_input("Path to management_dashboard_data.js", value=str(default_data_js))
        data_js_path = Path(data_js_path_raw).expanduser()
        if not data_js_path.is_absolute():
            data_js_path = (Path.cwd() / data_js_path).resolve()
    else:
        data_js_path = default_data_js

    required = {
        "html_template": assets_root / "management_dashboard.html",
        "tabler_css": assets_root / "tabler.min.css",
        "dashboard_css": assets_root / "management_dashboard.css",
        "tabler_js": assets_root / "tabler.min.js",
        "chart_js": assets_root / "chart.umd.js",
        "dashboard_js": assets_root / "management_dashboard.js",
        "data_js": data_js_path,
    }
    missing = [name for name, path in required.items() if not path.exists()]
    if missing:
        st.error(f"Missing required files: {', '.join(missing)}")
        st.write(
            {
                key: (str(value) if isinstance(value, Path) else None)
                for key, value in required.items()
            }
        )
        return

    rendered = build_exact_dashboard_html(
        html_template=required["html_template"],
        tabler_css=required["tabler_css"],
        dashboard_css=required["dashboard_css"],
        tabler_js=required["tabler_js"],
        chart_js=required["chart_js"],
        data_js=required["data_js"],
        dashboard_js=required["dashboard_js"],
    )

    # Keep iframe height close to viewport so intro text stays visually centered without page scroll.
    components.html(rendered, height=980, scrolling=True)


if __name__ == "__main__":
    main()
