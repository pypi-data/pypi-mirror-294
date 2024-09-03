import clr
import os
import json
from ReportsClasses.Helper.database_helper import DatabaseConnectionHelper

# Get the current working directory
cwd = os.getcwd()

# Get the directory of the current script (Base_Report.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the configuration file relative to the script's directory
config_path = os.path.join(script_dir, 'config.json')

# Load the configuration from the JSON file
try:
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        crystal_reports_engine = os.path.join(script_dir, config.get("crystal_reports_engine"))
        crystal_reports_windows_forms = os.path.join(script_dir, config.get("crystal_reports_windows_forms"))
        crystal_reports_shared = os.path.join(script_dir, config.get("crystal_reports_shared"))
except FileNotFoundError:
    raise Exception("Configuration file not found. Please create 'config.json' with the correct DLL paths.")
except json.JSONDecodeError:
    raise Exception("Error parsing the configuration file. Please check the JSON format.")

# Load the DLL files dynamically using paths from the configuration file
try:
    clr.AddReference(crystal_reports_engine)
    clr.AddReference(crystal_reports_windows_forms)
    clr.AddReference(crystal_reports_shared)
except Exception as e:
    print(f"Error loading assembly: {e}")
    raise

# Import the namespaces after loading the DLLs
import CrystalDecisions.CrystalReports.Engine as Engine
from CrystalDecisions.Windows import Forms
from CrystalDecisions import Shared
from CrystalDecisions.CrystalReports.Engine import ReportDocument
from CrystalDecisions.Shared import ParameterDiscreteValue, TableLogOnInfo, ExportFormatType

