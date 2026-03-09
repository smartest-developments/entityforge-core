# Email Draft To Business

Subject: SCV Senzing PoC - Current Results, Risks, and Recommendation

Hi all,

We completed the latest PoC run, here our outcome

## Key Numbers (latest run)
- Input records loaded: `1,031,617`
- Full execution time: `462.25 minutes` (~`7.7 hours`)
- Our match found: `33.58%`
- Their match found (Senzing): `26.80%`
- Our entities formed: `785,140`
- Their entities formed (Senzing): `834,249`
- Their match gain/loss: `-6.78%`

## What this means
- Senzing shows good precision identifyng matches.
- Not all expected matches are being captured.
- Runtime is acceptable for PoC but still heavy in constrained infrastructure.

## Main execution issues we faced (important)
- During large loads, we hit native loader instability (for example: `flatbuffer allocation failure / BufferFullError`).
- We also observed contention on resolved entities (`SENZ0010` locklist retry timeout), especially on dense clusters of records.
- In practical terms: one-shot high-volume loading was not stable enough in our current environment.

## Why we applied single-thread + split/chunk strategy
To make the run complete reliably, we adopted conservative controls:

- **Single load thread (`--load-threads 1`)**  
  Reduced concurrent pressure and lock contention in the Senzing loader.

- **Physical file split into blocks of 1,000 rows (`--load-batch-size 1000`)**  
  Instead of loading one huge JSONL stream at once, we process many small files in order.

- **Fallback chunking at 100 rows (`--load-chunk-size 100`)**  
  If a 1,000-row block fails, we retry in smaller chunks to isolate and recover difficult segments.

- **Per-file timeout (`--load-file-timeout-seconds`) + retry/fallback controls**  
  Prevented infinite stalls and allowed progress even when a subset was problematic.

Business impact of this approach:
- run completion probability increased significantly,
- full runtime increased (trade-off: speed vs stability),
- we gained traceability of problematic ranges and recoverability.

Best regards.
