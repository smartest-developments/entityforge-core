# Streamlit App

This folder is standalone.

It contains:
- `app.py`
- `requirements.txt`
- `assets/` (all dashboard HTML/CSS/JS/data files needed at runtime)

## Run

From this folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data source

Default source:
- `assets/management_dashboard_data.js`

Optional:
- enable `Use external data file` from the sidebar and provide another `management_dashboard_data.js` path.

## Notes

- This app requires a running Python process.
- It renders the same dashboard HTML/CSS/JS used by the offline presentation.
- It adds an intro fade animation with text:
  - `SCV Senzing PoC`
