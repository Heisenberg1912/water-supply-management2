import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime, timedelta
import uuid

# ---------------- Page Config ---------------- #
st.set_page_config(page_title="Inventory Management App", layout="wide")

# ---------------- Helper Functions ---------------- #
def to_excel_bytes(df):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    return buf.getvalue()

# ---------------- Session-State Initialization ---------------- #
DEFAULT_KEYS = {
    "logged_in": False,
    "username": None,
    "role": None,
    "ledger_entries": [],
    "inventory_items": [],
    "gst_entries": [],
    "invoices": [],
    "payroll_runs": [],
    "report_data": [],
    "transactions": [],
    "audit_logs": [],
    "users": [],
    "api_keys": [],
    "settings": {},
}
for key, default in DEFAULT_KEYS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- Dummy Credentials & Admin User List ---------------- #
DUMMY_CREDENTIALS = {
    "admin": ("adminpass", "admin"),
    "tushar": ("batham", "user")
}
if not st.session_state["users"]:
    for u, (pw, role) in DUMMY_CREDENTIALS.items():
        st.session_state["users"].append({
            "username": u,
            "role": role,
            "id": str(uuid.uuid4())[:8]
        })

# ---------------- Login ---------------- #
if not st.session_state["logged_in"]:
    with st.form("login_form"):
        st.title("🔐 Inventory Management Login")
        user_in = st.text_input("User ID")
        pw_in = st.text_input("Password", type="password")
        remember = st.checkbox("Remember me")
        submitted = st.form_submit_button("Login")
        if submitted:
            creds = DUMMY_CREDENTIALS.get(user_in)
            if creds and creds[0] == pw_in:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_in
                st.session_state["role"] = creds[1]
                msg = f"Logged in as {user_in.title()} ({creds[1]})"
                if remember:
                    st.success(msg + " — you’ll stay logged in!")
                else:
                    st.success(msg)
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
    st.stop()

# ---------------- Main Dashboard ---------------- #
user = st.session_state["username"]
role = st.session_state["role"]
st.sidebar.header(f"👋 {user.title()}")
st.sidebar.subheader(f"Role: {role.title()}")
st.sidebar.markdown("---")

USER_MODULES = [
    "Accounting",
    "Inventory",
    "Taxation",
    "Invoicing",
    "Payroll",
    "Reporting",
    "Banking",
    "Customization",
    "Audit",
]
ADMIN_EXTRA = ["User Mgmt", "Sys Settings", "Audit Logs", "API Control"]
MODULES = USER_MODULES + (ADMIN_EXTRA if role == "admin" else [])

selection = st.sidebar.selectbox("Module", MODULES)
st.title("📊 Inventory Management Dashboard")

# ---------------- Module: Accounting ---------------- #
if selection == "Accounting":
    st.header("🧾 Accounting & Financial Management")
    if not st.session_state["ledger_entries"]:
        df0 = pd.DataFrame({
            "Date": pd.date_range("2025-01-01", periods=8),
            "Account": np.random.choice(
                ["Sales","Expenses","Assets","Liabilities","Equity"], size=8
            ),
            "Amount": np.random.randint(-2000, 5000, size=8)
        })
        st.session_state["ledger_entries"] = df0.to_dict("records")

    ledger_df = pd.DataFrame(st.session_state["ledger_entries"])
    st.subheader("General Ledger")
    st.table(ledger_df)
    st.download_button("Download Ledger", to_excel_bytes(ledger_df), "ledger.xlsx")

    with st.expander("➕ Add Ledger Entry"):
        with st.form("ledger_form"):
            date = st.date_input("Date", value=datetime.today())
            account = st.selectbox(
                "Account", ["Sales","Expenses","Assets","Liabilities","Equity"]
            )
            amount = st.number_input("Amount", value=0)
            ok = st.form_submit_button("Add")
            if ok:
                st.session_state["ledger_entries"].append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Account": account,
                    "Amount": amount
                })
                st.success("Entry added.")
                st.rerun()

# ---------------- Module: Inventory ---------------- #
elif selection == "Inventory":
    st.header("📦 Inventory Management")
    if not st.session_state["inventory_items"]:
        df1 = pd.DataFrame({
            "Item": [f"Item {c}" for c in ["A","B","C","D","E"]],
            "Stock": np.random.randint(0,200,size=5),
            "Reorder": np.random.randint(10,50,size=5)
        })
        st.session_state["inventory_items"] = df1.to_dict("records")

    inv_df = pd.DataFrame(st.session_state["inventory_items"])
    st.subheader("Stock Levels")
    st.table(inv_df)
    st.download_button("Download Inventory", to_excel_bytes(inv_df), "inventory.xlsx")

    with st.expander("➕ Add Inventory Item"):
        with st.form("inv_form"):
            name = st.text_input("Item Name")
            stock = st.number_input("Stock Level", min_value=0)
            reorder = st.number_input("Reorder Level", min_value=0)
            add = st.form_submit_button("Add")
            if add:
                st.session_state["inventory_items"].append({
                    "Item": name,
                    "Stock": stock,
                    "Reorder": reorder
                })
                st.success("Item added.")
                st.rerun()

# ---------------- Module: Taxation ---------------- #
elif selection == "Taxation":
    st.header("🧮 Taxation & Compliance")
    if not st.session_state["gst_entries"]:
        sim = pd.DataFrame({
            "Customer": np.random.choice(
                ["ABC Corp","XYZ Ltd","Foo Inc"], 5
            ),
            "Amount": np.round(np.random.uniform(1000,5000,5),2),
            "Date": pd.date_range("2025-03-01", periods=5).strftime("%Y-%m-%d")
        })
        st.session_state["gst_entries"] = sim.to_dict("records")

    gst_df = pd.DataFrame(st.session_state["gst_entries"])
    st.subheader("GST Invoices")
    st.table(gst_df)
    st.download_button("Download GST", to_excel_bytes(gst_df), "gst.xlsx")

    with st.expander("➕ Add GST Entry"):
        with st.form("gst_form"):
            cust = st.text_input("Customer")
            amt  = st.number_input("Amount", min_value=0.0)
            date = st.date_input("Date", value=datetime.today())
            add  = st.form_submit_button("Add")
            if add:
                st.session_state["gst_entries"].append({
                    "Customer": cust,
                    "Amount": amt,
                    "Date": date.strftime("%Y-%m-%d")
                })
                st.success("GST entry added.")
                st.rerun()

# ---------------- Module: Invoicing ---------------- #
elif selection == "Invoicing":
    st.header("💳 Invoicing & Billing")
    if not st.session_state["invoices"]:
        invs = pd.DataFrame({
            "Invoice#": [f"INV{1000+i}" for i in range(5)],
            "Customer": np.random.choice(["Acme","Beta","Gamma"], 5),
            "Amount": np.round(np.random.uniform(500,3000,5),2),
            "Date": pd.date_range("2025-02-01", periods=5).strftime("%Y-%m-%d")
        })
        st.session_state["invoices"] = invs.to_dict("records")

    inv_df = pd.DataFrame(st.session_state["invoices"])
    st.subheader("Invoice History")
    st.table(inv_df)
    st.download_button("Download All Invoices", to_excel_bytes(inv_df), "invoices.xlsx")

    with st.expander("➕ Create Invoice"):
        with st.form("inv_form"):
            num  = st.text_input(
                "Invoice #", value=f"INV{1000+len(inv_df)}"
            )
            cust = st.text_input("Customer")
            amt  = st.number_input("Amount", min_value=0.0)
            date = st.date_input("Date", value=datetime.today())
            go   = st.form_submit_button("Generate")
            if go:
                st.session_state["invoices"].append({
                    "Invoice#": num,
                    "Customer": cust,
                    "Amount": amt,
                    "Date": date.strftime("%Y-%m-%d")
                })
                st.success("Invoice created.")
                st.rerun()

# ---------------- Module: Payroll ---------------- #
elif selection == "Payroll":
    st.header("💼 Payroll Management")
    if not st.session_state["payroll_runs"]:
        pr = pd.DataFrame({
            "RunID": [f"PR{200+i}" for i in range(4)],
            "Employee": np.random.choice(
                ["Alice","Bob","Charlie"], 4
            ),
            "Gross": np.random.randint(20000,50000,4),
            "Deductions": np.random.randint(1000,5000,4)
        })
        pr["Net"] = pr["Gross"] - pr["Deductions"]
        st.session_state["payroll_runs"] = pr.to_dict("records")

    pay_df = pd.DataFrame(st.session_state["payroll_runs"])
    st.subheader("Payroll Runs")
    st.table(pay_df)
    st.download_button("Download Payroll", to_excel_bytes(pay_df), "payroll.xlsx")

    with st.expander("➕ Run Payroll"):
        with st.form("pay_form"):
            emp = st.text_input("Employee")
            gross = st.number_input("Gross Salary", min_value=0)
            ded = st.number_input("Deductions", min_value=0)
            run = st.form_submit_button("Process")
            if run:
                net = gross - ded
                st.session_state["payroll_runs"].append({
                    "RunID": f"PR{300+len(pay_df)}",
                    "Employee": emp,
                    "Gross": gross,
                    "Deductions": ded,
                    "Net": net
                })
                st.success("Payroll processed.")
                st.rerun()

# ---------------- Module: Reporting ---------------- #
elif selection == "Reporting":
    st.header("📈 Reporting & Analytics")
    if not st.session_state["report_data"]:
        dates = pd.date_range("2025-01-01", periods=10)
        vals = np.random.randn(10).cumsum()
        st.session_state["report_data"] = pd.DataFrame({
            "Date": dates, "Value": vals
        }).to_dict("records")

    df_report = pd.DataFrame(st.session_state["report_data"])
    st.line_chart(df_report.set_index("Date"))
    st.download_button(
        "Download Report",
        to_excel_bytes(df_report),
        "report.csv",
        mime="text/csv"
    )

    with st.expander("➕ Add Data Point"):
        with st.form("rep_form"):
            date = st.date_input("Date", value=datetime.today())
            val  = st.number_input("Value", value=0.0)
            add  = st.form_submit_button("Add")
            if add:
                st.session_state["report_data"].append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Value": val
                })
                st.success("Data point added.")
                st.rerun()

# ---------------- Module: Banking ---------------- #
elif selection == "Banking":
    st.header("🏦 Banking & Payments")
    if not st.session_state["transactions"]:
        tx = pd.DataFrame({
            "Date": pd.date_range("2025-03-10", periods=6),
            "Type": np.random.choice(["Debit","Credit"], 6),
            "Amount": np.random.randint(100,2000,6)
        })
        st.session_state["transactions"] = tx.to_dict("records")

    tx_df = pd.DataFrame(st.session_state["transactions"])
    st.subheader("Transactions")
    st.table(tx_df)
    st.download_button(
        "Download Transactions",
        to_excel_bytes(tx_df),
        "transactions.xlsx"
    )

    with st.expander("➕ Add Transaction"):
        with st.form("tx_form"):
            ttype = st.selectbox("Type", ["Debit","Credit"])
            amt   = st.number_input("Amount", min_value=0)
            date  = st.date_input("Date", value=datetime.today())
            add   = st.form_submit_button("Add")
            if add:
                st.session_state["transactions"].append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Type": ttype,
                    "Amount": amt
                })
                st.success("Transaction added.")
                st.rerun()

# ---------------- Module: Customization ---------------- #
elif selection == "Customization":
    st.header("⚙️ Customization & Scalability")
    theme = st.selectbox(
        "Theme",
        ["Light","Dark"],
        index=["Light","Dark"].index(
            st.session_state["settings"].get("theme","Light")
        )
    )
    if st.button("Apply Theme"):
        st.session_state["settings"]["theme"] = theme
        st.success(f"Theme set to {theme}")

# ---------------- Module: Audit ---------------- #
elif selection == "Audit":
    st.header("📋 Audit & Compliance")
    if not st.session_state["audit_logs"]:
        logs = pd.DataFrame({
            "Timestamp": pd.date_range(
                datetime.now(), periods=5, freq="T"
            ),
            "User": np.random.choice(
                ["Alice","Bob","Charlie"], 5
            ),
            "Action": np.random.choice(
                ["Login","Update","Delete","Create"], 5
            )
        })
        st.session_state["audit_logs"] = logs.to_dict("records")

    log_df = pd.DataFrame(st.session_state["audit_logs"])
    st.table(log_df)
    st.download_button(
        "Download Logs",
        to_excel_bytes(log_df),
        "audit_logs.csv"
    )

    with st.expander("➕ Add Audit Entry"):
        with st.form("log_form"):
            usr = st.text_input("User")
            act = st.text_input("Action")
            add = st.form_submit_button("Add")
            if add:
                st.session_state["audit_logs"].append({
                    "Timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "User": usr,
                    "Action": act
                })
                st.success("Log entry added.")
                st.rerun()

# ---------------- Admin-Only Modules ---------------- #
elif role=="admin" and selection=="User Mgmt":
    st.header("👥 User Management")
    users_df = pd.DataFrame(st.session_state["users"])
    st.table(users_df)
    with st.expander("➕ Add User"):
        with st.form("user_form"):
            uname = st.text_input("Username")
            pwd   = st.text_input("Password", type="password")
            r     = st.selectbox("Role", ["admin","user"])
            add   = st.form_submit_button("Add")
            if add:
                DUMMY_CREDENTIALS[uname] = (pwd, r)
                st.session_state["users"].append({
                    "username": uname,
                    "role": r,
                    "id": str(uuid.uuid4())[:8]
                })
                st.success("User added.")
                st.rerun()

elif role=="admin" and selection=="Sys Settings":
    st.header("⚙️ System Settings")
    title = st.text_input(
        "App Title",
        st.session_state["settings"].get(
            "title","Inventory Management App"
        )
    )
    if st.button("Save"):
        st.session_state["settings"]["title"] = title
        st.success("Settings saved.")

elif role=="admin" and selection=="Audit Logs":
    st.header("📂 Audit Logs (Admin)")
    st.table(log_df)

elif role=="admin" and selection=="API Control":
    st.header("🔑 API Access Control")
    st.table(pd.DataFrame(
        st.session_state["api_keys"],
        columns=["Key","Created"]
    ))
    if st.button("Generate API Key"):
        new_key = str(uuid.uuid4())
        st.session_state["api_keys"].append([
            new_key,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        st.success("API key generated.")
        st.rerun()

else:
    st.warning("🚫 Access Denied or Module Not Implemented.")

# ---------------- Logout ---------------- #
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    for k in list(DEFAULT_KEYS):
        del st.session_state[k]
    st.rerun()
