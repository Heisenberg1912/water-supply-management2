import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta

# ---------------- Helper Functions ---------------- #
def to_excel_bytes(df):
    """Convert a DataFrame to Excel bytes."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# Simulate arbitrary DataFrame
def simulate_df(rows, cols=1, val_range=(100,1000), start_date='2025-01-01', freq='D'):
    dates = pd.date_range(start=start_date, periods=rows, freq=freq)
    data = {f"Col_{i+1}": np.random.randint(val_range[0], val_range[1], size=rows) for i in range(cols)}
    df = pd.DataFrame(data)
    df['Date'] = dates
    return df

# ---------------- Session State Initialization ---------------- #
# Ensure all required session state keys are initialized with defaults
default_state = {
    'logged_in': False,
    'username': None,
    'role': None,
    'gst_entries': [],
    'invoices': [],
    'settings': {'theme': 'Light', 'date_format': '%Y-%m-%d'},
    'api_keys': []
}
for key, default in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- Dummy Credentials ---------------- #
DUMMY_CREDENTIALS = {
    'admin': ('adminpass', 'admin'),
    'tushar': ('batham', 'user')
}

# ---------------- Page Configuration ---------------- #
st.set_page_config(
    page_title='Inventory Management System',
    layout='wide',
    initial_sidebar_state='expanded'
)

# ---------------- Login ---------------- #
if not st.session_state['logged_in']:
    st.title('🔐 Login to Inventory Management System')
    with st.form('login_form'):
        username = st.text_input('User ID')
        password = st.text_input('Password', type='password')
        remember = st.checkbox('Remember me')
        submit = st.form_submit_button('Login')
        if submit:
            creds = DUMMY_CREDENTIALS.get(username)
            if creds and creds[0] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = creds[1]
                st.success(f'Welcome, {username.title()}! You are logged in as {creds[1].title()}.')
                st.experimental_rerun()
            else:
                st.error('Invalid credentials, please try again.')
    st.stop()

# ---------------- Main Application ---------------- #
user = st.session_state['username']
role = st.session_state['role']

# Sidebar
st.sidebar.title('🗂️ Navigation')
st.sidebar.write(f'**User:** {user.title()}')
st.sidebar.write(f'**Role:** {role.title()}')
st.sidebar.markdown('---')

def get_modules(role):
    base = [
        'Accounting & Financial Management',
        'Inventory Management',
        'Taxation & Compliance',
        'Invoicing & Billing',
        'Payroll Management',
        'Reporting & Analytics',
        'Banking & Payments',
        'Customization & Scalability',
        'Audit & Compliance'
    ]
    admin_extra = [
        'Data Security & Backup',
        'Integration & Connectivity',
        'Multi-Company & Multi-Location',
        'Cloud & Mobile Support',
        'User Management',
        'System Settings',
        'Audit Logs',
        'API Access Control'
    ]
    return base + admin_extra if role == 'admin' else base

modules = get_modules(role)
selection = st.sidebar.selectbox('Select Module', modules)
st.title('📊 Inventory Management Dashboard')

# ---------------- Module 1: Accounting & Financial Management ---------------- #
if selection == 'Accounting & Financial Management':
    st.header('🧾 Accounting & Financial Management')
    if st.button('Simulate Monthly Ledger Entries'):
        df = simulate_df(12, 3, (1000, 5000), freq='M')
        df.rename(columns={'Col_1': 'Debit', 'Col_2': 'Credit', 'Col_3': 'Balance'}, inplace=True)
        st.table(df)
        st.download_button('Download Ledger Excel', data=to_excel_bytes(df), file_name='ledger.xlsx')

    st.markdown('---')
    # Financial Ratios
    ratios = pd.DataFrame({
        'Metric': ['Gross Margin', 'EBITDA Margin', 'Return on Equity'],
        'Value (%)': np.round(np.random.rand(3) * 50 + 10, 2)
    })
    st.subheader('Key Financial Ratios')
    st.table(ratios)

# ---------------- Module 2: Inventory Management ---------------- #
elif selection == 'Inventory Management':
    st.header('📦 Inventory Management')
    inv_df = pd.DataFrame({
        'Item': [f'Item_{i}' for i in range(1, 11)],
        'Stock': np.random.randint(0, 200, 10),
        'Reorder Level': np.random.randint(20, 100, 10)
    })
    inv_df['Status'] = np.where(inv_df['Stock'] <= inv_df['Reorder Level'], '🔴 Reorder', '✅ In Stock')
    st.subheader('Current Stock Status')
    st.dataframe(inv_df)

    st.markdown('---')
    # Search / Filter
    search_term = st.text_input('Search Items')
    if search_term:
        filtered = inv_df[inv_df['Item'].str.contains(search_term, case=False)]
        st.table(filtered)

    if st.button('Simulate Replenishment'): 
        inv_df['Stock'] = inv_df['Stock'] + np.random.randint(10, 50, len(inv_df))
        st.success('Stock levels updated!')
        st.dataframe(inv_df)

# ---------------- Module 3: Taxation & Compliance ---------------- #
elif selection == 'Taxation & Compliance':
    st.header('🧮 Taxation & Compliance')
    with st.expander('Add GST Invoice Entry'):
        with st.form('gst_form'):
            past = [e['Customer'] for e in st.session_state['gst_entries']]
            cust = st.selectbox('Customer', options=['<New>'] + past)
            if cust == '<New>': cust = st.text_input('New Customer Name')
            amt = st.number_input('Amount (₹)', min_value=0.0, step=0.01)
            if st.form_submit_button('Add Entry'):
                entry = {'Customer': cust, 'Amount': amt, 'Date': datetime.now().strftime('%Y-%m-%d')}
                st.session_state['gst_entries'].append(entry)
                st.success(f'Added entry for {cust}: ₹{amt:.2f}')
                st.experimental_rerun()

    if st.session_state['gst_entries']:
        gst_df = pd.DataFrame(st.session_state['gst_entries'])
        st.subheader('GST Invoice Entries')
        st.table(gst_df)
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Simulate Tax Adjustment'):
                gst_df['Amount'] *= np.random.uniform(0.9, 1.1, len(gst_df))
                st.table(gst_df)
        with col2:
            if st.button('Download All GST Invoices'):
                st.download_button('Download Excel', data=to_excel_bytes(gst_df), file_name='gst_invoices.xlsx')

# ---------------- Module 4: Invoicing & Billing ---------------- #
elif selection == 'Invoicing & Billing':
    st.header('🧾 Invoicing & Billing')
    with st.expander('Generate New Invoice'):
        with st.form('invoice_form'):
            inv_no = st.text_input('Invoice Number')
            cust = st.text_input('Customer Name')
            amt = st.number_input('Amount (₹)', min_value=0.0, step=0.01)
            date = st.date_input('Date', value=datetime.now().date())
            if st.form_submit_button('Create Invoice'):
                st.session_state['invoices'].append({'Invoice#': inv_no, 'Customer': cust, 'Amount': amt, 'Date': date.strftime('%Y-%m-%d')})
                st.success(f'Invoice {inv_no} created.')
                st.experimental_rerun()

    if st.session_state['invoices']:
        inv_df = pd.DataFrame(st.session_state['invoices'])
        st.subheader('Invoice History')
        st.dataframe(inv_df)
        if st.button('Apply Bulk Discount 5%'):
            inv_df['Amount'] *= 0.95
            st.table(inv_df)
        if st.button('Download All Invoices'):
            st.download_button('Download Excel', data=to_excel_bytes(inv_df), file_name='all_invoices.xlsx')

# ---------------- Module 5: Payroll Management ---------------- #
elif selection == 'Payroll Management':
    st.header('💼 Payroll Management')
    payroll_df = simulate_df(10, 2, (30000, 70000))
    payroll_df.rename(columns={'Col_1': 'Gross Pay', 'Col_2': 'Deductions'}, inplace=True)
    payroll_df['Net Pay'] = payroll_df['Gross Pay'] - payroll_df['Deductions']
    st.subheader('Payroll Summary')
    st.table(payroll_df)
    if st.button('Simulate Year-End Bonus 10%'):
        payroll_df['Net Pay'] *= 1.1
        st.table(payroll_df)
    st.download_button('Download Payslips Excel', data=to_excel_bytes(payroll_df), file_name='payslips.xlsx')

# ---------------- Module 6: Reporting & Analytics ---------------- #
elif selection == 'Reporting & Analytics':
    st.header('📈 Reporting & Analytics')
    report_df = simulate_df(30, 1, (0, 100))
    report_df.rename(columns={'Col_1': 'Metric Value'}, inplace=True)
    st.subheader('Metric Trend')
    st.line_chart(report_df.set_index('Date')['Metric Value'])
    if st.button('Simulate Anomaly Spike'):
        idx = np.random.randint(0, len(report_df))
        report_df.at[idx, 'Metric Value'] *= 3
        st.line_chart(report_df.set_index('Date')['Metric Value'])
    st.download_button('Download Report CSV', data=report_df.to_csv(index=False), file_name='report.csv')

# ---------------- Module 7: Banking & Payments ---------------- #
elif selection == 'Banking & Payments':
    st.header('🏦 Banking & Payments')
    bank_df = simulate_df(7, 1, (100, 2000))
    bank_df.rename(columns={'Col_1': 'Amount'}, inplace=True)
    bank_df['Type'] = np.random.choice(['Debit', 'Credit'], len(bank_df))
    st.subheader('Recent Transactions')
    st.table(bank_df)
    if st.button('Simulate Interest Accrual 1%'):
        bank_df['Amount'] *= 1.01
        st.table(bank_df)
    st.download_button('Download Transactions Excel', data=to_excel_bytes(bank_df), file_name='transactions.xlsx')

# ---------------- Module 8: Customization & Scalability ---------------- #
elif selection == 'Customization & Scalability':
    st.header('⚙️ Customization & Scalability')
    theme = st.selectbox('Theme', ['Light', 'Dark'])
    date_fmt = st.selectbox('Date Format', ['%Y-%m-%d', '%d/%m/%Y', '%m-%d-%Y'])
    if st.button('Save Settings'):
        st.session_state['settings']['theme'] = theme
        st.session_state['settings']['date_format'] = date_fmt
        st.success('Settings updated.')
    if st.button('Simulate Load Test'): 
        users = np.random.randint(100, 1000)
        st.info(f'Successfully handled {users} concurrent users.')

# ---------------- Module 9: Audit & Compliance ---------------- #
elif selection == 'Audit & Compliance':
    st.header('✅ Audit & Compliance')
    audit_df = simulate_df(15,1,(0,1))
    audit_df.rename(columns={'Col_1': 'ActionFlag'}, inplace=True)
    audit_df['User'] = np.random.choice([user, 'system'], len(audit_df))
    st.subheader('Audit Log')
    st.dataframe(audit_df)
    if st.button('Simulate Security Scan'): st.success('No issues found.')
    st.download_button('Download Audit Log', data=to_excel_bytes(audit_df), file_name='audit_log.xlsx')

# ---------------- Admin-Only Modules ---------------- #
elif role == 'admin' and selection == 'Data Security & Backup':
    st.header('🔒 Data Security & Backup')
    backup_time = st.time_input('Schedule Automated Backup Time', value=datetime.now().time())
    if st.button('Schedule Backup'): st.success(f'Backup scheduled at {backup_time}.')
    if st.button('Encrypt All Data'): st.success('All data encrypted with AES-256 (simulated).')

elif role == 'admin' and selection == 'Integration & Connectivity':
    st.header('🔗 Integration & Connectivity')
    endpoints = pd.DataFrame({
        'Endpoint': ['/api/ledger','/api/inventory','/api/payroll'],
        'Status': np.random.choice(['Active','Inactive','Error'],3)
    })
    st.subheader('API Endpoints Status')
    st.table(endpoints)
    if st.button('Simulate Re-auth'): st.success('All integrations re-authenticated.')

elif role == 'admin' and selection == 'Multi-Company & Multi-Location':
    st.header('🏢 Multi-Company & Multi-Location')
    comp_df = pd.DataFrame({
        'Company': ['Alpha','Beta','Gamma'],
        'Revenue': np.random.randint(50000,150000,3),
        'Expenses': np.random.randint(20000,80000,3)
    })
    comp_df['Profit'] = comp_df['Revenue'] - comp_df['Expenses']
    st.table(comp_df)
    if st.button('Generate Consolidated Report'): st.success('Consolidated report ready.')

elif role == 'admin' and selection == 'Cloud & Mobile Support':
    st.header('☁️ Cloud & Mobile Support')
    logs_df = simulate_df(5,2,(1,100))
    logs_df.rename(columns={'Col_1':'Cloud Deploys','Col_2':'Mobile Installs'}, inplace=True)
    st.table(logs_df)
    if st.button('Simulate New Mobile Release'): st.success('Mobile v2.0 released.')

elif role == 'admin' and selection == 'User Management':
    st.header('👥 User Management')
    users_df = pd.DataFrame([{'User': u, 'Role': r} for u,(p,r) in DUMMY_CREDENTIALS.items()])
    st.table(users_df)
    with st.form('new_user'):
        nu = st.text_input('New Username')
        npw = st.text_input('New Password', type='password')
        nr = st.selectbox('Role', ['user','admin'])
        if st.form_submit_button('Add User'):
            DUMMY_CREDENTIALS[nu] = (npw,nr)
            st.success(f'User {nu} added as {nr}.')

elif role == 'admin' and selection == 'System Settings':
    st.header('⚙️ System Settings')
    title = st.text_input('Application Title', value='Inventory Management Dashboard')
    maint = st.checkbox('Maintenance Mode')
    if st.button('Save System Settings'):
        st.session_state['settings']['title'] = title
        st.session_state['settings']['maintenance'] = maint
        st.success('System settings updated.')

elif role == 'admin' and selection == 'Audit Logs':
    st.header('📋 Audit Logs')
    st.dataframe(audit_df)
    if st.button('Clear Audit Logs'): st.success('Audit logs cleared.')

elif role == 'admin' and selection == 'API Access Control':
    st.header('🔑 API Access Control')
    if 'api_keys' not in st.session_state: st.session_state['api_keys'] = []
    if st.button('Generate API Key'):
        key = 'KEY-' + datetime.now().strftime('%Y%m%d%H%M%S')
        st.session_state['api_keys'].append(key)
        st.success(f'Generated: {key}')
    if st.session_state['api_keys']:
        st.subheader('Active API Keys')
        st.write(st.session_state['api_keys'])

else:
    st.warning('🚫 Access Denied or Module Not Implemented.')

# ---------------- Logout ---------------- #
st.sidebar.markdown('---')
if st.sidebar.button('Logout'):
    for k in list(st.session_state.keys()): st.session_state.pop(k)
    st.experimental_rerun()
