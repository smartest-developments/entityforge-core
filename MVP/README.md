# MVP Pipeline

Script restano nella root di `MVP`.  
Sample input JSON restano in `sample_input/`.  
Gli output finali vengono scritti in `output/<timestamp>__<input_label>/`.

## File inclusi

- `run_mvp_pipeline.py`: wrapper unico (mapping + run Senzing + comparison/report)
- `run_samples_batch.py`: esegue il pipeline su tutti i JSON in `sample_input/`
- `generate_sample_inputs.py`: rigenera 50 sample curati (500 record ciascuno, default) con metadati descrittivi in testa
  e hidden true groups (`SOURCE_TRUE_GROUP_ID`) per misurare match reali non etichettati con IPG
- `partner_json_to_senzing.py`: mapper JSON -> JSONL Senzing
- `run_senzing_end_to_end.py`: runner E2E Senzing
- `build_management_dashboard.py`: costruisce dashboard self-contained da tutti i run in `output/<timestamp>/`
- `dashboard/`: dashboard pronta all'uso (UI + dati locali, apribile direttamente)
- `testing/`: suite automatica Python per validare che i KPI dashboard corrispondano agli artifact tecnici
- `sample_input/sample_01_legacy_baseline_500.json`: sample pronto (500 record)

## Prerequisiti

- Docker disponibile
- immagine Senzing: `mapper-senzing-poc:4.2.1`
- file input JSON reale (array oppure oggetto con array)

## Comando base

```bash
python3 run_mvp_pipeline.py --input-json /path/to/real_input.json
```

In ambiente Ubuntu con Senzing gia' installato (senza Docker), usa:

```bash
python3 run_mvp_pipeline.py --input-json /path/to/real_input.json --execution-mode local
```

Se ti serve forzare il setup base di Senzing:

```bash
python3 run_mvp_pipeline.py \
  --input-json /path/to/real_input.json \
  --execution-mode local \
  --senzing-env /opt/senzing/er/setupEnv
```

## Esempio con sample incluso

```bash
python3 run_mvp_pipeline.py --input-json sample_input/sample_01_legacy_baseline_500.json
```

## Batch su tutti i sample input

```bash
python3 run_samples_batch.py --execution-mode auto
```

Con ambiente locale (senza Docker):

```bash
python3 run_samples_batch.py --execution-mode local --senzing-env /opt/senzing/er/setupEnv
```

## Input annidato

Se il JSON e' del tipo `{"records":[...]}`:

```bash
python3 run_mvp_pipeline.py --input-json /path/to/input.json --input-array-key records
```

Nota: il wrapper ora prova automaticamente `records`, `data`, `items` quando `--input-array-key` non e' passato.

## Rigenerare sample curati

```bash
python3 generate_sample_inputs.py --records 500 --samples 50
```

Ogni file in `sample_input/` viene scritto con metadati iniziali:

- `_sample_comment`: descrizione breve del caso
- `_sample_special_features`: elenco delle caratteristiche del sample
- `_hidden_truth_groups`: quanti gruppi true match senza IPG label sono stati introdotti
- `_hidden_truth_records`: quanti record partecipano a questi gruppi hidden
- `_ipg_label_noise`: rumore IPG applicato (collisioni e drop) per generare anche baseline false positive/false negative
- `records`: array di 500 record usato dal pipeline

## WHY (opzionale)

Di default WHY e' disattivato per performance.  
Per abilitarlo:

```bash
python3 run_mvp_pipeline.py \
  --input-json /path/to/real_input.json \
  --with-why \
  --max-explain-records 0 \
  --max-explain-pairs 0
```

## Output

Ogni esecuzione crea una cartella dedicata:

- `output/<timestamp>__<input_label>/`

Dentro `output/<timestamp>/` (management-friendly) trovi:

- `input_source.json` (exact source JSON used for that run)
- `management_summary.md`
- `ground_truth_match_quality.md`

`management_summary.md` include anche la sezione:

- `Extra True Matches Beyond SOURCE_IPG_ID`
  - quanti match veri in piu' Senzing trova rispetto ai match gia' noti via IPG
  - extra gain percentuale rispetto ai pair gia' noti (`extra_gain_vs_known`)

Dentro `output/<timestamp>/technical output/` trovi gli artifact tecnici:

- `mapped_output.jsonl`
- `field_map.json`
- `mapping_summary.json`
- `run_summary.json`
- `input_normalized.jsonl` (exact JSONL consumed by Senzing in that run)
- `management_summary.json`
- `ground_truth_match_quality.json`
- `matched_pairs.csv`
- `match_stats.csv`
- `entity_records.csv`
- `run_registry.csv` (snapshot della registry del run)

## Runtime

Il wrapper usa una directory temporanea esterna a `MVP` per i file intermedi e poi copia gli artifact finali in `output/<timestamp>/`.  
Per mantenere la directory runtime:

```bash
python3 run_mvp_pipeline.py --input-json /path/to/real_input.json --keep-runtime-dir
```

Nota: `--execution-mode auto` (default) usa Docker se disponibile, altrimenti passa automaticamente a `local`.

## Management dashboard (local, offline, senza server)

La dashboard e' completamente locale (no CDN, no hosting, no `http.server` obbligatorio).

- Legge solo artifact locali generati in `output/<timestamp>/`.
- Viene rigenerata automaticamente dopo ogni `run_mvp_pipeline.py` in:
  - `dashboard/`
- Puoi aprirla direttamente con doppio click su:
  - `dashboard/management_dashboard.html`
  - oppure `dashboard/index.html`
- Nel menu `Select output` puoi scegliere anche `All outputs (aggregate)` per una vista globale di tutti i run `success`
  (volumi sommati e percentuali calcolate sui totali).
- Dopo ogni rebuild dashboard viene eseguita automaticamente una suite di test KPI (`MVP/testing/`).
- Se i test falliscono, il rebuild viene marcato come failed (exit code non-zero).
- Dopo la suite test viene eseguito anche `verify_dashboard_metrics.py` come audit incrociato.

Rigenerazione manuale:

```bash
python3 build_management_dashboard.py
```

Per rigenerare dashboard senza eseguire i test automatici (solo debug rapido):

```bash
python3 build_management_dashboard.py --skip-tests
```

Per saltare solo l'audit incrociato (debug rapido):

```bash
python3 build_management_dashboard.py --skip-audit
```

Output della rigenerazione:

- `dashboard/management_dashboard.html`
- `dashboard/management_dashboard.css`
- `dashboard/management_dashboard.js`
- `dashboard/management_dashboard_data.js`
- `dashboard/metrics_validation_guide.html` (manual cross-check page for KPI validation)
- `dashboard/tabler.min.css`, `dashboard/tabler.min.js`, `dashboard/chart.umd.js`
- `dashboard/dashboard_test_suite_report.json` (esito machine-readable della suite test automatica)
- `dashboard/dashboard_test_suite_report.md` (report leggibile test PASS/FAIL)

## Data audit for management (proof of KPI correctness)

Per una verifica oggettiva dei KPI mostrati in dashboard:

```bash
python3 build_management_dashboard.py
python3 verify_dashboard_metrics.py
```

Esecuzione diretta della sola suite test automatica:

```bash
python3 testing/run_dashboard_tests.py
```

Generazione snapshot regressivo opzionale (latest run per source):

```bash
python3 testing/generate_dashboard_snapshot.py
```

Per abilitare i test regressivi snapshot:

```bash
MVP_ENFORCE_REGRESSION_SNAPSHOT=1 python3 testing/run_dashboard_tests.py
```

Lo script `verify_dashboard_metrics.py` ricalcola i KPI direttamente dagli artifact tecnici
(`input_normalized.jsonl`, `matched_pairs.csv`, `entity_records.csv`,
`ground_truth_match_quality.json`, `management_summary.json`) e li confronta con i valori
esposti in `dashboard/management_dashboard_data.js`.

Genera due report:

- `dashboard/dashboard_data_audit_report.json` (dettaglio machine-readable)
- `dashboard/dashboard_data_audit_report.md` (report leggibile per management con PASS/FAIL per run)
