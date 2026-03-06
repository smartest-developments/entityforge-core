# Streamlit App

This folder contains a Streamlit wrapper that renders the exact HTML dashboard UI.

## Run

From repository root:

```bash
python3 -m pip install streamlit pandas altair
streamlit run MVP/dashboard/streamlit_app/app.py
```

## Data source

The app auto-detects `management_dashboard_data.js` from:

1. `MVP/dashboard/management_dashboard_data.js`
2. `MVP/presentation/management_dashboard_data.js`
3. JSON variants of the same files

You can also override the path from the sidebar.

## Notes

- This app requires a running Python process.
- It renders the same dashboard HTML/CSS/JS used by the offline presentation.
- It adds an intro animation ("sliding doors") with text:
  - `SCV Senzing PoC`
