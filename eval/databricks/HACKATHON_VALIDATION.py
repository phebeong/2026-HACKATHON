# Databricks notebook source
# MAGIC %md
# MAGIC # FEMA Evidence & Oversight Graph: Recorded Validation
# MAGIC Runs actual registered MCP tools, automated security and regression tests,
# MAGIC independent SQLite controls, live latency checks, and real model tool selection.
# MAGIC Results are archived under eval/results and logged to MLflow when available.

# COMMAND ----------
# MAGIC %pip install fastmcp==4.0.11 pytest==9.1.1 pytest-asyncio==1.4.0 ruff==0.16.10

# COMMAND ----------
dbutils.library.restartPython()

# COMMAND ----------
import importlib.util
import sys

project_path = "/Workspace/Users/phebe.arouni@hq.dhs.gov/2026-HACKATHON"
sys.path.insert(0, project_path + "/src")
spec = importlib.util.spec_from_file_location(
    "hackathon_validation", project_path + "/eval/run_hackathon.py"
)
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)
summary = await validation.run()
print(summary)
assert summary["all_functional_checks_pass"], (
    "One or more functional checks failed; inspect recorded results."
)
