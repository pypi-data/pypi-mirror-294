from crystalpy_barno.ReportsClasses.Base_Report import *
from crystalpy_barno.ReportsClasses.Helper.database_helper import DatabaseConnectionHelper
from crystalpy_barno.ReportsClasses.Base_Report import CrystalReportsLoader

# Create an instance of the CrystalReportsLoader class
loader = CrystalReportsLoader()

# Setup the loader (loads config, DLLs, and namespaces)
loader.setup()

import CrystalDecisions.CrystalReports.Engine as Engine
from CrystalDecisions.Windows import Forms
from CrystalDecisions import Shared
from CrystalDecisions.CrystalReports.Engine import ReportDocument
from CrystalDecisions.Shared import ParameterDiscreteValue, TableLogOnInfo, ExportFormatType

class SaleSnippet:
    @staticmethod
    def SaleMemo(report_filename, output_path, params):
        crpt = Engine.ReportDocument()
        crpt.Load(report_filename)
        cr_viewer = Forms.CrystalReportViewer()

        # Set parameter values directly using ParameterFieldsDefinitions
        def set_parameter(report, param_name, value):
            param_fields = report.DataDefinition.ParameterFields
            param_field = param_fields[param_name]
            param_value = Shared.ParameterDiscreteValue()
            param_value.Value = value
            param_field.CurrentValues.Clear()
            param_field.CurrentValues.Add(param_value)
            param_field.ApplyCurrentValues(param_field.CurrentValues)

        # Extract parameters from the dictionary
        set_parameter(crpt, "@pvSourcerecNo", params.get('source_no'))
        set_parameter(crpt, "@pvVoucherNo", params.get('voucher_no'))
        set_parameter(crpt, "@pvLeCode", params.get('le_code'))
        set_parameter(crpt, "@pvUserCode", params.get('user_code'))
        set_parameter(crpt, "@pvReportID", "1")
        set_parameter(crpt, "@pvIncludingMaking", params.get('s_inc_mak'))

        # Apply database connection using the centralized helper
        DatabaseConnectionHelper.apply_connection(crpt)

        crpt.Database.Tables[0].Location = f"{DatabaseConnectionHelper.get_database_name()}.dbo.spSale_Memo"

        # Set formula fields
        formula_fields = crpt.DataDefinition.FormulaFields
        for field in formula_fields:
            if field.Name == "EmployeeName":
                field.Text = f"'{params.get('s_emp_name')}'"
                break

        if params.get('s_print_hdr'):
            for field in formula_fields:
                if field.Name == "CompanyName":
                    field.Text = f"'{params.get('le_name')}'"
                elif field.Name == "Warehouse":
                    field.Text = f"'{params.get('wh_name')}'"
                elif field.Name == "Address":
                    field.Text = f"'{params.get('wh1')} {params.get('wh2')}'"
                elif field.Name == "Phone":
                    field.Text = f"'{params.get('whp1')} {params.get('whp2')}'"

        for field in formula_fields:
            if field.Name == "ReportCaption":
                field.Text = ""
                
        crpt.ExportToDisk(Shared.ExportFormatType.PortableDocFormat, output_path)

        cr_viewer.ReportSource = crpt
        cr_viewer.Refresh()
        cr_viewer.Show()

        return True
