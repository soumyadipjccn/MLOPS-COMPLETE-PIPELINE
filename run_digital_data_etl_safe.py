import os
import traceback

LOG_PATH = os.path.join(os.path.dirname(__file__), "run_logs", "digital_data_etl_pytrace.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

try:
    # Importing the pipeline module may execute module-level code; catch any exception
    import Pipelines.digital_data_etl as pipeline_mod  # noqa: E402
except Exception:
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("Exception during import of Pipelines.digital_data_etl:\n")
        traceback.print_exc(file=f)
    raise

# If import succeeded, optionally call nothing (module import causes side effects in this repo)
# But also guard any runtime execution triggered after import
try:
    # If the module defines a main runner, call it safely. We don't assume it does, so just pass.
    pass
except Exception:
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("Exception during execution of Pipelines.digital_data_etl:\n")
        traceback.print_exc(file=f)
    raise

print(f"Import completed; if an exception occurred it was written to {LOG_PATH}")
