# MLOPS-COMPLETE-PIPELINE

# set PYTHONPATH to repo root and set a USER_AGENT (replace value if you like)
$env:PYTHONPATH = (Resolve-Path .).Path
$env:USER_AGENT = 'my-agent/1.0'

# run with the project's venv python
D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE\data_ingestion\Scripts\python.exe .\run_pipeline_bypass_zenml.py



$env:PYTHONPATH = (Resolve-Path .).Path
D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE\data_ingestion\Scripts\python.exe .\scripts\inspect_db.py



Optional runs (when/if you want them)

Safe wrapper to collect Python traceback for the ZenML pipeline (helpful if you want to debug ZenML):


$env:PYTHONPATH = (Resolve-Path .).Path
D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE\data_ingestion\Scripts\python.exe .\run_digital_data_etl_safe.py
# check run_logs/digital_data_etl_pytrace.log for the traceback if it fails



$env:PYTHONPATH = (Resolve-Path .).Path
$env:USER_AGENT = 'my-agent/1.0'
D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE\data_ingestion\Scripts\python.exe .\Pipelines\digital_data_etl.py
# or run run_pipeline.py if that's the script you prefer
Set-Location -LiteralPath 'D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE'
$env:PYTHONPATH = (Resolve-Path .).Path
$env:USER_AGENT = 'my-agent/1.0'  # optional if you want to set it

D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE\data_ingestion\Scripts\python.exe .\scripts\print_links_count.py



$env:PYTHONPATH='D:\GenerativeAI\MLOPS\MLOPS-COMPLETE-PIPELINE'; python scripts/inspect_db.py