import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta

# Helper function to convert a DataFrame to Excel bytes
def to_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Set page configuration
st.set_page_config(page_title="Comprehensive Tally App", layout="wide")

# App Title
st.title("Comprehensive Tally-like Application")

# Sidebar Navigation for Modules
modules = [
    "Accounting & Financial Management",
    "Inventory Management",
    "Taxation & Compliance",
    "Invoicing & Billing",
    "Payroll Management",
    "Reporting & Analytics",
    "Data Security & Backup",
    "Integration & Connectivity",
    "Banking & Payments",
    "Multi-Company & Multi-Location",
    "Customization & Scalability",
    "Cloud & Mobile Support",
    "Audit & Compliance",
    "Industry-Specific Features",
    "TallyPrime Features",
    "Support & Training"
]

selection = st.sidebar.selectbox("Select Module", modules)

# 1. Accounting & Financial Management
if selection == "Accounting & Financial Management":
    st.header("Accounting and Financial Management")
    
    st.subheader("General Ledger")
    st.write("Maintain and manage all financial transactions.")
    ledger_data = pd.DataFrame({
        "Date": pd.date_range(start="2025-01-01", periods=5),
        "Account": ["Sales", "Expenses", "Assets", "Liabilities", "Equity"],
        "Amount": [1000, -500, 2000, -1500, 500]
    })
    st.table(ledger_data)
    st.download_button("Download Ledger as Excel", data=to_excel_bytes(ledger_data),
                       file_name="general_ledger.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Accounts Receivable/Payable")
    st.write("Track money owed to and by the business.")
    receivables = pd.DataFrame({
        "Customer": ["ABC Corp", "XYZ Ltd"],
        "Amount Due": [1500, 2300]
    })
    st.table(receivables)
    st.download_button("Download Receivables as Excel", data=to_excel_bytes(receivables),
                       file_name="accounts_receivable.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Bank Reconciliation")
    st.write("Upload a bank statement Excel file to reconcile transactions.")
    bank_file = st.file_uploader("Upload Bank Statement Excel file", type=["xlsx"], key="bank_recon")
    if bank_file is not None:
        bank_data = pd.read_excel(bank_file)
        st.write("Bank Statement Data:")
        st.table(bank_data.head())
        st.write("Reconciling with Ledger Data:")
        st.table(ledger_data)
        st.success("Bank reconciliation completed (simulated).")
    
    st.subheader("Budgeting and Forecasting")
    st.write("Create budgets and compare them with actual performance.")
    budget_data = pd.DataFrame({
        "Month": ["January", "February", "March"],
        "Budget": [10000, 12000, 15000],
        "Actual": [9500, 13000, 14000]
    })
    st.table(budget_data)
    st.download_button("Download Budget Data as Excel", data=to_excel_bytes(budget_data),
                       file_name="budgeting_forecasting.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Multi-Currency Support & Financial Statements")
    st.write("Select a currency and generate financial statements.")
    currency = st.selectbox("Select Currency", ["USD", "EUR", "INR"])
    statement_type = st.radio("Select Statement Type", ["Balance Sheet", "Profit & Loss", "Cash Flow"])
    if st.button("Generate Statement", key="gen_statement"):
        if statement_type == "Balance Sheet":
            bs_data = pd.DataFrame({
                "Category": ["Assets", "Liabilities", "Equity"],
                "Amount": [15000, 7000, 8000]
            })
            st.table(bs_data)
            st.download_button("Download Balance Sheet as Excel", data=to_excel_bytes(bs_data),
                               file_name="balance_sheet.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif statement_type == "Profit & Loss":
            pl_data = pd.DataFrame({
                "Revenue": [15000],
                "Expenses": [8000],
                "Net Profit": [7000]
            })
            st.table(pl_data)
            st.download_button("Download Profit & Loss as Excel", data=to_excel_bytes(pl_data),
                               file_name="profit_loss.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif statement_type == "Cash Flow":
            cf_data = pd.DataFrame({
                "Operating Activities": [5000],
                "Investing Activities": [-2000],
                "Financing Activities": [1000],
                "Net Cash Flow": [4000]
            }, index=["Value"])
            st.table(cf_data)
            st.download_button("Download Cash Flow as Excel", data=to_excel_bytes(cf_data),
                               file_name="cash_flow.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.success(f"{statement_type} generated in {currency} (simulated).")
        
    st.subheader("Cost Centers & Profitability Analysis")
    st.write("Select a cost center to view profitability analysis.")
    cost_centers = ["Sales", "Marketing", "R&D", "HR"]
    selected_center = st.selectbox("Cost Center", cost_centers)
    cc_data = pd.DataFrame({
        "Cost Center": cost_centers,
        "Income": [10000, 15000, 12000, 8000],
        "Expenses": [5000, 7000, 6000, 4000]
    })
    selected_cc = cc_data[cc_data["Cost Center"] == selected_center]
    st.table(selected_cc)
    st.download_button("Download Profitability Data as Excel", data=to_excel_bytes(selected_cc),
                       file_name="profitability_analysis.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.success(f"Profitability analysis for {selected_center} (simulated).")

# 2. Inventory Management
elif selection == "Inventory Management":
    st.header("Inventory Management")
    
    st.subheader("Stock Management")
    st.write("Track stock levels, movements, and valuations.")
    inventory = pd.DataFrame({
        "Item": ["Item A", "Item B", "Item C"],
        "Stock Level": [100, 50, 200],
        "Reorder Level": [20, 10, 30]
    })
    st.table(inventory)
    st.download_button("Download Inventory as Excel", data=to_excel_bytes(inventory),
                       file_name="inventory.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Batch-wise Tracking")
    st.write("Enter batch details for inventory items.")
    batch_df = None
    with st.form("batch_form"):
        item_name = st.text_input("Item Name")
        batch_number = st.text_input("Batch Number")
        expiry_date = st.date_input("Expiry Date", value=datetime.now() + timedelta(days=365))
        batch_submitted = st.form_submit_button("Add Batch Info")
        if batch_submitted:
            batch_df = pd.DataFrame({
                "Item Name": [item_name],
                "Batch Number": [batch_number],
                "Expiry Date": [expiry_date]
            })
            st.table(batch_df)
            st.success(f"Batch {batch_number} for {item_name} with expiry {expiry_date} added (simulated).")
    if batch_df is not None:
        st.download_button("Download Batch Data as Excel", data=to_excel_bytes(batch_df),
                           file_name="batch_tracking.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Multi-location Support & GST Compliance")
    st.write("Select a warehouse location to view inventory.")
    location = st.selectbox("Warehouse Location", ["Warehouse 1", "Warehouse 2", "Warehouse 3"])
    st.write(f"Displaying inventory for {location}")
    
    st.subheader("GST Calculation")
    gst_result = None
    with st.form("gst_calc_form"):
        base_price = st.number_input("Base Price", min_value=0.0, step=10.0)
        gst_rate = st.number_input("GST Rate (%)", min_value=0.0, step=0.5, value=18.0)
        gst_submitted = st.form_submit_button("Calculate GST")
        if gst_submitted:
            gst_amount = base_price * gst_rate / 100  # Current formula for GST
            total_price = base_price + gst_amount
            gst_result = pd.DataFrame({
                "Base Price": [base_price],
                "GST Rate (%)": [gst_rate],
                "GST Amount": [gst_amount],
                "Total Price": [total_price]
            })
            st.table(gst_result)
            st.success(f"GST: {gst_amount:.2f}, Total Price: {total_price:.2f} (simulated).")
    if gst_result is not None:
        st.download_button("Download GST Calculation as Excel", data=to_excel_bytes(gst_result),
                           file_name="gst_calculation.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 3. Taxation & Compliance
elif selection == "Taxation & Compliance":
    st.header("Taxation and Compliance")
    
    st.subheader("GST Compliance")
    gst_invoice_df = None
    with st.form("gst_form"):
        customer = st.text_input("Customer Name")
        amount = st.number_input("Invoice Amount", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("Generate GST Invoice")
        if submitted:
            gst_invoice_df = pd.DataFrame({
                "Customer": [customer],
                "Invoice Amount": [amount]
            })
            st.table(gst_invoice_df)
            st.success(f"GST Invoice generated for {customer} for amount {amount} (simulation).")
    if gst_invoice_df is not None:
        st.download_button("Download GST Invoice as Excel", data=to_excel_bytes(gst_invoice_df),
                           file_name="gst_invoice.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("TDS & TCS")
    tds_tcs_df = None
    with st.form("tds_tcs_form"):
        income = st.number_input("Total Income", min_value=0.0, step=100.0)
        tds_rate = st.number_input("TDS Rate (%)", min_value=0.0, step=0.5, value=10.0)
        tcs_rate = st.number_input("TCS Rate (%)", min_value=0.0, step=0.5, value=2.0)
        tds_tcs_submitted = st.form_submit_button("Calculate TDS & TCS")
        if tds_tcs_submitted:
            tds = income * tds_rate / 100  # Current formula for TDS
            tcs = income * tcs_rate / 100  # Current formula for TCS
            tds_tcs_df = pd.DataFrame({
                "Total Income": [income],
                "TDS Rate (%)": [tds_rate],
                "TDS": [tds],
                "TCS Rate (%)": [tcs_rate],
                "TCS": [tcs]
            })
            st.table(tds_tcs_df)
            st.success(f"TDS: {tds:.2f}, TCS: {tcs:.2f} (simulated).")
    if tds_tcs_df is not None:
        st.download_button("Download TDS/TCS Calculation as Excel", data=to_excel_bytes(tds_tcs_df),
                           file_name="tds_tcs_calculation.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("VAT, Excise & E-Way Bill")
    vat_excise_df = None
    with st.form("vat_excise_form"):
        product_value = st.number_input("Product Value", min_value=0.0, step=10.0)
        vat_rate = st.number_input("VAT Rate (%)", min_value=0.0, step=0.5, value=12.0)
        excise_rate = st.number_input("Excise Duty Rate (%)", min_value=0.0, step=0.5, value=5.0)
        vat_excise_submitted = st.form_submit_button("Calculate VAT & Excise")
        if vat_excise_submitted:
            vat_amount = product_value * vat_rate / 100  # Current formula for VAT
            excise_amount = product_value * excise_rate / 100  # Current formula for Excise Duty
            vat_excise_df = pd.DataFrame({
                "Product Value": [product_value],
                "VAT Rate (%)": [vat_rate],
                "VAT Amount": [vat_amount],
                "Excise Rate (%)": [excise_rate],
                "Excise Duty": [excise_amount]
            })
            st.table(vat_excise_df)
            st.success(f"VAT: {vat_amount:.2f}, Excise Duty: {excise_amount:.2f} (simulated).")
    if vat_excise_df is not None:
        st.download_button("Download VAT/Excise Calculation as Excel", data=to_excel_bytes(vat_excise_df),
                           file_name="vat_excise_calculation.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.write("Generate E-Way Bill")
    eway_df = None
    with st.form("eway_bill_form"):
        consigner = st.text_input("Consigner")
        consignee = st.text_input("Consignee")
        transport_id = st.text_input("Transport ID")
        eway_submitted = st.form_submit_button("Generate E-Way Bill")
        if eway_submitted:
            eway_df = pd.DataFrame({
                "Consigner": [consigner],
                "Consignee": [consignee],
                "Transport ID": [transport_id],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(eway_df)
            st.success(f"E-Way Bill generated for consigner {consigner} (simulated).")
    if eway_df is not None:
        st.download_button("Download E-Way Bill as Excel", data=to_excel_bytes(eway_df),
                           file_name="e_way_bill.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 4. Invoicing & Billing
elif selection == "Invoicing & Billing":
    st.header("Invoicing and Billing")
    
    st.subheader("Customizable Invoices")
    invoice_df = None
    with st.form("invoice_form"):
        inv_number = st.text_input("Invoice Number")
        cust_name = st.text_input("Customer Name")
        inv_amount = st.number_input("Amount", min_value=0.0, step=10.0)
        invoice_submitted = st.form_submit_button("Generate Invoice")
        if invoice_submitted:
            invoice_df = pd.DataFrame({
                "Invoice Number": [inv_number],
                "Customer Name": [cust_name],
                "Amount": [inv_amount],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(invoice_df)
            st.success(f"Invoice {inv_number} generated for {cust_name} (simulation).")
    if invoice_df is not None:
        st.download_button("Download Invoice as Excel", data=to_excel_bytes(invoice_df),
                           file_name="invoice.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Sales/Purchase Orders")
    order_df = None
    with st.form("order_form"):
        order_type = st.selectbox("Order Type", ["Sales Order", "Purchase Order"])
        order_number = st.text_input("Order Number")
        order_amount = st.number_input("Order Amount", min_value=0.0, step=10.0)
        order_submitted = st.form_submit_button("Place Order")
        if order_submitted:
            order_df = pd.DataFrame({
                "Order Type": [order_type],
                "Order Number": [order_number],
                "Order Amount": [order_amount],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(order_df)
            st.success(f"{order_type} {order_number} placed for amount {order_amount} (simulated).")
    if order_df is not None:
        st.download_button("Download Order as Excel", data=to_excel_bytes(order_df),
                           file_name="order.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Credit/Debit Notes")
    note_df = None
    with st.form("credit_debit_form"):
        note_type = st.selectbox("Note Type", ["Credit Note", "Debit Note"])
        note_number = st.text_input("Note Number")
        note_amount = st.number_input("Note Amount", min_value=0.0, step=10.0)
        note_submitted = st.form_submit_button("Generate Note")
        if note_submitted:
            note_df = pd.DataFrame({
                "Note Type": [note_type],
                "Note Number": [note_number],
                "Note Amount": [note_amount],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(note_df)
            st.success(f"{note_type} {note_number} generated for amount {note_amount} (simulated).")
    if note_df is not None:
        st.download_button("Download Note as Excel", data=to_excel_bytes(note_df),
                           file_name="credit_debit_note.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Multi-User Support")
    st.write("Multi-user support is handled on the server side with session management.")

# 5. Payroll Management
elif selection == "Payroll Management":
    st.header("Payroll Management")
    
    st.subheader("Employee Management")
    employees = pd.DataFrame({
        "Employee ID": [101, 102, 103],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["HR", "Finance", "IT"]
    })
    st.table(employees)
    st.download_button("Download Employee Data as Excel", data=to_excel_bytes(employees),
                       file_name="employees.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Salary Processing")
    salary_df = None
    with st.form("salary_form"):
        emp_id = st.selectbox("Select Employee ID", employees["Employee ID"])
        basic_salary = st.number_input("Basic Salary", min_value=0.0, step=100.0)
        bonus = st.number_input("Bonus", min_value=0.0, step=50.0)
        process = st.form_submit_button("Process Salary")
        if process:
            total_salary = basic_salary + bonus  # Standard salary calculation
            salary_df = pd.DataFrame({
                "Employee ID": [emp_id],
                "Basic Salary": [basic_salary],
                "Bonus": [bonus],
                "Total Salary": [total_salary]
            })
            st.table(salary_df)
            st.success(f"Salary processed for Employee {emp_id}: Total = {total_salary}")
    if salary_df is not None:
        st.download_button("Download Salary Data as Excel", data=to_excel_bytes(salary_df),
                           file_name="salary_processing.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Statutory Compliance & Payslip Generation")
    payslip = None
    with st.form("payslip_form"):
        emp_name = st.selectbox("Employee", employees["Name"])
        designation = st.text_input("Designation")
        month = st.selectbox("Month", ["January", "February", "March", "April"])
        gross_salary = st.number_input("Gross Salary", min_value=0.0, step=100.0)
        deductions = st.number_input("Deductions", min_value=0.0, step=50.0)
        payslip_submitted = st.form_submit_button("Generate Payslip")
        if payslip_submitted:
            net_salary = gross_salary - deductions  # Net salary formula
            payslip = pd.DataFrame({
                "Employee": [emp_name],
                "Designation": [designation],
                "Month": [month],
                "Gross Salary": [gross_salary],
                "Deductions": [deductions],
                "Net Salary": [net_salary]
            })
            st.table(payslip)
            st.success("Payslip generated (simulation).")
    if payslip is not None:
        st.download_button("Download Payslip as Excel", data=to_excel_bytes(payslip),
                           file_name="payslip.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 6. Reporting & Analytics
elif selection == "Reporting & Analytics":
    st.header("Reporting and Analytics")
    
    st.subheader("Real-Time Reports")
    chart_data = pd.DataFrame({
        'Date': pd.date_range(start="2025-01-01", periods=50),
        'Value': np.random.randn(50).cumsum()
    })
    st.line_chart(chart_data.set_index('Date'))
    st.download_button("Download Chart Data as Excel", data=to_excel_bytes(chart_data),
                       file_name="chart_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Customizable & Drill-Down Reports")
    st.write("Filter data by date range to drill down into reports.")
    start_date = st.date_input("Start Date", value=datetime(2025,1,1))
    end_date = st.date_input("End Date", value=datetime(2025,2,1))
    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        filtered_data = chart_data[(chart_data['Date'] >= pd.to_datetime(start_date)) & 
                                   (chart_data['Date'] <= pd.to_datetime(end_date))]
        st.line_chart(filtered_data.set_index('Date'))
        st.write("Drill-down details:")
        st.table(filtered_data)
        st.download_button("Download Drill-Down Data as Excel", data=to_excel_bytes(filtered_data),
                           file_name="drill_down_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.success("Customizable drill-down report generated (simulated).")

# 7. Data Security & Backup
elif selection == "Data Security & Backup":
    st.header("Data Security and Backup")
    
    st.subheader("User Access Control")
    st.write("Simulate role-based access. Please login.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "User"])
        login_submitted = st.form_submit_button("Login")
        if login_submitted:
            st.success(f"Logged in as {username} with role {role} (simulation).")
    
    st.subheader("Data Encryption & Automatic Backup")
    with st.form("backup_form"):
        backup_time = st.time_input("Schedule Backup Time", value=datetime.now().time())
        backup_submitted = st.form_submit_button("Schedule Backup")
        if backup_submitted:
            st.success(f"Backup scheduled at {backup_time} (simulation).")
    st.write("Encrypt data on demand:")
    if st.button("Encrypt Data"):
        st.success("Data encrypted successfully (simulated).")
    
    st.subheader("Audit Trails")
    audit_logs = pd.DataFrame({
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(5)],
        "User": ["Alice", "Bob", "Charlie", "Alice", "Bob"],
        "Action": ["Created Invoice", "Processed Salary", "Updated Ledger", "Generated Report", "Logged in"]
    })
    st.table(audit_logs)
    st.download_button("Download Audit Logs as Excel", data=to_excel_bytes(audit_logs),
                       file_name="audit_logs.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.success("Audit trail displayed (simulation).")

# 8. Integration & Connectivity
elif selection == "Integration & Connectivity":
    st.header("Integration and Connectivity")
    
    st.subheader("Third-Party Integration & API Support")
    st.write("Available API Endpoints:")
    api_endpoints = pd.DataFrame({
        "Endpoint": ["/api/invoices", "/api/ledger", "/api/employees"],
        "Method": ["GET", "POST", "GET"]
    })
    st.table(api_endpoints)
    st.download_button("Download API Endpoints as Excel", data=to_excel_bytes(api_endpoints),
                       file_name="api_endpoints.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.write("Simulate an API call:")
    with st.form("api_call_form"):
        endpoint = st.selectbox("Select Endpoint", ["/api/invoices", "/api/ledger", "/api/employees"])
        response = st.text_area("Response", "Simulated API response will appear here...", height=100)
        api_call_submitted = st.form_submit_button("Call API")
        if api_call_submitted:
            st.success(f"API call to {endpoint} successful (simulated).")
    
    st.subheader("Data Import/Export")
    uploaded_file = st.file_uploader("Choose an Excel file to import", type=["xlsx"], key="import_file")
    if uploaded_file is not None:
        imported_data = pd.read_excel(uploaded_file)
        st.table(imported_data.head())
        st.success("File imported successfully (simulation).")
    dummy_export = pd.DataFrame({"Data": [1, 2, 3, 4, 5]})
    st.download_button("Download Sample Data as Excel", data=to_excel_bytes(dummy_export),
                       file_name="sample_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Remote Access")
    st.write("Access your system remotely via: https://remote.tallyapp.com (simulated)")

# 9. Banking & Payments
elif selection == "Banking & Payments":
    st.header("Banking and Payments")
    
    st.subheader("Bank Integration")
    bank_integration_df = None
    with st.form("bank_integration_form"):
        bank_name = st.text_input("Bank Name")
        account_number = st.text_input("Account Number")
        integration_submitted = st.form_submit_button("Sync Bank Data")
        if integration_submitted:
            bank_integration_df = pd.DataFrame({
                "Bank Name": [bank_name],
                "Account Number": [account_number],
                "Sync Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(bank_integration_df)
            st.success(f"Bank data from {bank_name} synced successfully (simulated).")
    if bank_integration_df is not None:
        st.download_button("Download Bank Integration Data as Excel", data=to_excel_bytes(bank_integration_df),
                           file_name="bank_integration.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Payment Reminders")
    if st.button("Send Payment Reminders"):
        st.success("Payment reminders sent successfully (simulation).")
    
    st.subheader("Cheque Printing")
    cheque_df = None
    with st.form("cheque_form"):
        payee = st.text_input("Payee Name")
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        cheque_number = st.text_input("Cheque Number")
        cheque_submitted = st.form_submit_button("Print Cheque")
        if cheque_submitted:
            cheque_df = pd.DataFrame({
                "Cheque Number": [cheque_number],
                "Payee": [payee],
                "Amount": [amount],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(cheque_df)
            st.success(f"Cheque {cheque_number} for {payee} printed (simulated).")
    if cheque_df is not None:
        st.download_button("Download Cheque as Excel", data=to_excel_bytes(cheque_df),
                           file_name="cheque.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 10. Multi-Company & Multi-Location
elif selection == "Multi-Company & Multi-Location":
    st.header("Multi-Company and Multi-Location Support")
    
    st.write("Manage accounts for multiple companies in a single installation.")
    company = st.selectbox("Company", ["Company A", "Company B", "Company C"])
    st.write(f"Displaying data for {company}.")
    if st.button("Generate Consolidated Report"):
        consolidated_data = pd.DataFrame({
            "Metric": ["Revenue", "Expenses", "Profit"],
            "Company A": [10000, 5000, 5000],
            "Company B": [15000, 7000, 8000],
            "Company C": [12000, 6000, 6000]
        })
        st.table(consolidated_data)
        st.download_button("Download Consolidated Report as Excel", data=to_excel_bytes(consolidated_data),
                           file_name="consolidated_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.success("Consolidated report generated (simulated).")

# 11. Customization & Scalability
elif selection == "Customization & Scalability":
    st.header("Customization and Scalability")
    
    st.subheader("Tally Definition Language (TDL)")
    st.write("Enter custom TDL script:")
    tdl_script = st.text_area("TDL Script", height=150)
    if st.button("Run TDL Script"):
        st.success("TDL script executed (simulated).")
    
    st.subheader("Add-Ons and Extensions")
    st.write("Browse available add-ons:")
    addons = pd.DataFrame({
        "Add-On": ["CRM Integration", "Advanced Reporting", "Inventory Tracker"],
        "Version": ["1.0", "2.1", "1.5"]
    })
    st.table(addons)
    st.download_button("Download Add-Ons Data as Excel", data=to_excel_bytes(addons),
                       file_name="addons.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Scalable Architecture")
    st.write("The system is designed to support businesses of all sizes.")

# 12. Cloud & Mobile Support
elif selection == "Cloud & Mobile Support":
    st.header("Cloud and Mobile Support")
    if st.button("Deploy to Cloud"):
        st.success("Application deployed to cloud successfully (simulated).")
    st.write("Mobile App Features:")
    st.write("- Manage operations on the go")
    st.write("- Real-time notifications")
    st.write("Download the mobile app from the App Store or Google Play (simulated).")

# 13. Audit & Compliance
elif selection == "Audit & Compliance":
    st.header("Audit and Compliance")
    
    st.subheader("Internal and Statutory Audit")
    audit_result = None
    with st.form("audit_form"):
        audit_type = st.selectbox("Audit Type", ["Internal Audit", "Statutory Audit"])
        audit_period = st.text_input("Audit Period (e.g., Q1 2025)")
        audit_submitted = st.form_submit_button("Conduct Audit")
        if audit_submitted:
            audit_result = pd.DataFrame({
                "Audit Type": [audit_type],
                "Audit Period": [audit_period],
                "Status": ["Completed (Simulated)"]
            })
            st.table(audit_result)
            st.success(f"{audit_type} for {audit_period} completed (simulated).")
    if audit_result is not None:
        st.download_button("Download Audit Report as Excel", data=to_excel_bytes(audit_result),
                           file_name="audit_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Audit Logs")
    audit_logs = pd.DataFrame({
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(5)],
        "User": ["Alice", "Bob", "Charlie", "Alice", "Bob"],
        "Action": ["Created Invoice", "Processed Salary", "Updated Ledger", "Generated Report", "Logged in"]
    })
    st.table(audit_logs)
    st.download_button("Download Audit Logs as Excel", data=to_excel_bytes(audit_logs),
                       file_name="audit_logs.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.success("Audit logs displayed (simulation).")

# 14. Industry-Specific Features
elif selection == "Industry-Specific Features":
    st.header("Industry-Specific Features")
    
    st.subheader("Retail")
    st.write("Includes POS Integration and Barcode Support.")
    pos_df = None
    with st.form("pos_form"):
        item = st.text_input("Item")
        price = st.number_input("Price", min_value=0.0, step=1.0)
        pos_submitted = st.form_submit_button("Simulate POS Sale")
        if pos_submitted:
            pos_df = pd.DataFrame({
                "Item": [item],
                "Price": [price],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(pos_df)
            st.success(f"POS sale for {item} at {price} processed (simulated).")
    if pos_df is not None:
        st.download_button("Download POS Sale Data as Excel", data=to_excel_bytes(pos_df),
                           file_name="pos_sale.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Manufacturing")
    bom_df = None
    with st.form("bom_form"):
        product = st.text_input("Product Name")
        component = st.text_input("Component Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        bom_submitted = st.form_submit_button("Add BOM Entry")
        if bom_submitted:
            bom_df = pd.DataFrame({
                "Product": [product],
                "Component": [component],
                "Quantity": [quantity],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(bom_df)
            st.success(f"BOM entry for {product} with component {component} (x{quantity}) added (simulated).")
    if bom_df is not None:
        st.download_button("Download BOM Data as Excel", data=to_excel_bytes(bom_df),
                           file_name="bom.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    st.subheader("Services")
    services_df = None
    with st.form("services_form"):
        project = st.text_input("Project Name")
        hours = st.number_input("Hours Worked", min_value=0.0, step=0.5)
        services_submitted = st.form_submit_button("Log Hours")
        if services_submitted:
            services_df = pd.DataFrame({
                "Project": [project],
                "Hours Worked": [hours],
                "Date": [datetime.now().strftime("%Y-%m-%d")]
            })
            st.table(services_df)
            st.success(f"{hours} hours logged for project {project} (simulated).")
    if services_df is not None:
        st.download_button("Download Time Log as Excel", data=to_excel_bytes(services_df),
                           file_name="time_log.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# 15. TallyPrime Features
elif selection == "TallyPrime Features":
    st.header("TallyPrime (Latest Version) Features")
    st.write("• Simplified and user-friendly interface")
    st.write("• Go To Feature for quick navigation")
    st.write("• Customizable Workspaces")
    st.write("• Advanced search and filtering options")
    st.success("Experience the modernized interface and workflow enhancements.")

# 16. Support & Training
elif selection == "Support & Training":
    st.header("Support and Training")
    st.write("Access Tally Academy for training and certification programs.")
    st.write("Enjoy 24/7 customer support for troubleshooting and queries.")
    st.markdown("[Visit Support Portal](https://support.tallyapp.com)")
    st.success("Support & Training resources loaded (simulated).")

# Sidebar Information
st.sidebar.markdown("---")
st.sidebar.info(
    "This demo Streamlit app simulates a comprehensive Tally-like system with Excel-based file uploads/downloads, "
    "current calculation formulas, and every simulated feature is downloadable as an Excel file. "
    "In a full implementation, these sections would integrate with real data sources and business logic."
)
