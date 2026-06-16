import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Healthcare Revenue Cycle Intelligence Engine™",
    page_icon="🏥",
    layout="wide"
)

TENNESSEE_ORANGE = "#FF8200"
BLACK = "#000000"
WHITE = "#FFFFFF"
LIGHT_ORANGE = "#FFF4E8"
LIGHT_BORDER = "#F2D0A8"

st.markdown(
    f"""
    <style>
    html, body, [class*="stApp"], [data-testid="stAppViewContainer"], [data-testid="stHeader"],
    [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stSidebarContent"],
    [data-testid="block-container"] {{
        background-color: {WHITE} !important;
        color: {BLACK} !important;
    }}
    [data-testid="stSidebar"] {{ border-right: 2px solid {TENNESSEE_ORANGE} !important; }}
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {{ color: {BLACK} !important; }}
    h1 {{ font-weight: 900 !important; letter-spacing: -0.03em !important; }}
    h2 {{ font-weight: 850 !important; letter-spacing: -0.02em !important; }}
    .orange-divider {{ border-top: 4px solid {TENNESSEE_ORANGE}; margin-top: 18px; margin-bottom: 28px; }}
    .brand-callout {{ border-left: 8px solid {TENNESSEE_ORANGE}; background-color: {LIGHT_ORANGE}; padding: 18px; border-radius: 10px; margin-bottom: 20px; color: {BLACK}; }}
    div[data-testid="stExpander"] {{ border: 1.5px solid {LIGHT_BORDER} !important; border-radius: 14px !important; background-color: {WHITE} !important; box-shadow: none !important; }}
    button, [role="button"] {{ color: {BLACK} !important; }}
    div[role="radiogroup"] label span:first-child {{ border-color: {TENNESSEE_ORANGE} !important; }}

    .metric-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin-bottom: 18px;
    }}
    .metric-box {{
        border: 1.5px solid {LIGHT_BORDER};
        border-radius: 16px;
        padding: 14px;
        background: {WHITE};
        min-width: 0;
    }}
    .metric-label {{
        font-size: 0.9rem;
        font-weight: 750;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 1.35rem;
        line-height: 1.2;
        font-weight: 850;
        overflow-wrap: anywhere;
        word-break: normal;
    }}
    .metric-value-orange {{ color: {TENNESSEE_ORANGE} !important; }}

    .risk-card {{ border: 1.5px solid {LIGHT_BORDER}; border-radius: 16px; padding: 16px; margin-bottom: 14px; background: {WHITE}; }}
    .risk-card-title {{ font-size: 1.05rem; font-weight: 800; margin-bottom: 4px; }}
    .risk-card-meta {{ font-size: 0.92rem; margin-bottom: 10px; }}
    .risk-bar-track {{ width: 100%; height: 18px; border: 1px solid {TENNESSEE_ORANGE}; border-radius: 999px; background: {WHITE}; overflow: hidden; }}
    .risk-bar-fill {{ height: 100%; background: {TENNESSEE_ORANGE}; border-radius: 999px; }}
    .risk-score-label {{ font-size: 0.92rem; font-weight: 800; margin-top: 6px; color: {BLACK}; }}

    @media (max-width: 760px) {{
        .metric-grid {{ grid-template-columns: 1fr; }}
        .metric-value {{ font-size: 1.25rem; }}
        h1 {{ font-size: 2.6rem !important; }}
        h2 {{ font-size: 2rem !important; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

workflow_data = [
    ["Patient Scheduling", "Patient Access", "Medium to High", 72, "Appointment Accuracy Rate", "Scheduling / Patient Access", "Captures the appointment request, visit reason, service type, provider, location, and initial patient information.", "Visit reason may be vague, wrong service type may be selected, referral need may be missed, or authorization risk may not be flagged.", "The patient may experience delays, rescheduling, repeated calls, or confusion about what is needed before the visit.", "Staff may need to correct visit type, call the patient again, or urgently involve authorization or eligibility teams.", "Incorrect scheduling can delay clearance, create authorization misses, increase denial risk, and cause downstream rework.", "Use a scheduling intake checklist that confirms reason for visit, service type, referral need, and authorization trigger.", "Review specialty services, imaging, procedures, and high-cost services before the date of service.", "This shows I understand that revenue cycle risk can begin before the patient arrives. Scheduling is the first control point in denial prevention."],
    ["Patient Registration", "Patient Access", "High", 81, "Registration Accuracy Rate", "Registration / Front Desk", "Captures demographics, contact information, insurance information, guarantor details, consent forms, and account setup.", "Demographic errors, duplicate accounts, incorrect insurance entry, missing consent forms, or unclear guarantor information.", "The patient may receive incorrect communication, duplicate statements, or billing confusion.", "Staff may need to correct accounts, update insurance, merge duplicates, or respond to patient billing concerns.", "Registration errors can create claim rejections, billing delays, denial risk, and increased cost to collect.", "Use a registration quality checklist before the patient encounter is finalized.", "Review duplicate accounts, mismatched patient identifiers, guarantor confusion, and repeated registration errors.", "This shows I understand clean front-end data as the foundation for clean claims and accurate patient communication."],
    ["Insurance Verification", "Financial Clearance", "High", 84, "Insurance Verification Completion Rate", "Patient Access / Financial Clearance", "Confirms that payer, member ID, group number, plan type, subscriber information, and coordination of benefits are accurate.", "Outdated insurance card, wrong payer selected, incorrect member ID, missed secondary coverage, or unclear coordination of benefits.", "The patient may receive unexpected bills or be asked to provide insurance information again after the visit.", "Staff may need to correct insurance, rebill claims, contact the patient, or resolve payer mismatches.", "Insurance errors can cause claim rejections, delayed reimbursement, and avoidable administrative rework.", "Confirm payer, plan, member ID, group number, subscriber, secondary coverage, and coordination of benefits before service.", "Review accounts with multiple plans, recent insurance changes, or conflicting payer responses.", "This shows I understand the difference between entering insurance and verifying that insurance is usable for the revenue cycle."],
    ["Eligibility Verification", "Financial Clearance", "High", 86, "Eligibility Clearance Rate", "Eligibility / Financial Clearance", "Confirms active coverage for the date of service and checks benefit rules that may affect reimbursement.", "Coverage may be active, but benefits, referral needs, authorization indicators, or patient responsibility may be missed.", "The patient may face unexpected financial responsibility, delayed care, or confusing billing communication.", "Staff may need to recheck benefits, contact payers, update financial clearance, or resolve preventable denials.", "Eligibility failures can cause coverage denials, patient balance disputes, delayed payment, and write-off risk.", "Use a two-level review: active coverage plus service-specific benefit verification.", "Review unclear payer responses, high patient responsibility, complex benefit rules, or service exclusions.", "This shows I understand eligibility verification as a revenue protection function, not just a checkbox."],
    ["Prior Authorization", "Authorization", "Critical", 94, "Authorization Turnaround Time", "Prior Authorization / Clinical / Patient Access", "Confirms whether payer approval is required before service and tracks approval status before claim submission.", "Authorization may be missed, submitted late, approved for the wrong code, wrong date, wrong provider, or unsupported by documentation.", "The patient may experience delays, rescheduling, uncertainty, denied coverage, or unexpected financial responsibility.", "Staff may need urgent payer calls, documentation requests, retroactive reviews, appeals, or account corrections.", "Missing authorization can lead to full denial, delayed reimbursement, increased A/R, and write-off risk.", "Create a pre-service authorization checkpoint for service code, diagnosis support, location, date range, and approval number.", "Review high-cost services, imaging, procedures, specialty care, incomplete documentation, and denied or pending authorizations.", "This shows I understand how prior authorization connects payer rules, documentation, patient access, claims, denials, and patient experience."],
    ["Clinical Documentation", "Documentation", "High", 88, "Documentation Completion Rate", "Providers / Clinical Support / HIM", "Records why care was needed, what was performed, and whether the service supports coding, billing, authorization, and medical necessity.", "Medical necessity may be unclear, provider note may be incomplete, diagnosis may not support service, or required forms may be missing.", "The patient may experience delayed authorization, delayed claim resolution, denied coverage, or billing confusion.", "Staff may need provider queries, claim holds, additional documentation requests, or appeal support.", "Documentation gaps can cause medical necessity denials, claim delays, compliance risk, and avoidable rework.", "Use a documentation readiness review for high-risk services before coding and claim submission.", "Review incomplete, inconsistent, delayed, or unclear documentation before the claim moves forward.", "This shows I understand documentation as both a clinical record and an operational revenue cycle control point."],
    ["Coding Readiness", "Coding / HIM", "High", 82, "Coding Query Rate", "Coding / HIM / Providers", "Determines whether documentation is complete and clear enough for accurate, supported code assignment.", "Documentation may not support the code, modifiers may be missing, diagnosis and procedure may not align, or provider clarification may be delayed.", "The patient may experience delayed claim processing, delayed statements, or confusion about claim status.", "Coders may need to query providers, hold claims, review records multiple times, or escalate documentation concerns.", "Coding readiness issues can delay claims, increase denial risk, reduce clean claim performance, and affect reimbursement accuracy.", "Create a coding readiness checklist for documentation support, diagnosis alignment, procedure support, and modifier review.", "Review complex encounters, unclear notes, high-dollar services, missing modifiers, and repeated coding-related denials.", "This shows I understand coding readiness from an operations perspective without claiming to be a certified coder."],
    ["Claim Submission", "Claims", "High", 85, "Clean Claim Rate", "Billing / Coding / Claims", "Sends the completed claim to the payer using patient, payer, authorization, documentation, coding, provider, and charge information.", "Claim may contain incorrect demographics, missing authorization, wrong provider, missing modifier, unresolved edits, or incomplete documentation.", "The patient may receive delayed billing updates, unexpected statements, or repeated requests for information.", "Billing staff may need to correct claims, resolve edits, rebill payers, or send claims back upstream.", "Submission errors can cause rejections, denials, delayed payment, increased A/R, and reduced first-pass resolution.", "Use a claim readiness validation step before submission.", "Review high-dollar claims, authorization-required services, unresolved edits, and repeated payer-specific issues.", "This shows I understand that a clean claim depends on clean workflow before billing."],
    ["Denial Prevention", "Denials", "Critical", 92, "Preventable Denial Rate", "RCM / Denials / Patient Access", "Identifies and corrects risks before claims deny by using trend analysis, root-cause review, edits, and feedback loops.", "Teams may fix individual claims without tracing root causes, denial data may not reach upstream teams, or prevention owners may not be assigned.", "The patient may experience confusing bills, delayed resolution, unexpected balances, or reduced trust.", "Staff may spend time appealing preventable denials, contacting payers, correcting records, and reworking accounts.", "Preventable denials increase cost to collect, delay reimbursement, increase write-off risk, and reduce cash predictability.", "Create a denial prevention feedback loop that tracks denial reason, first workflow breakdown, prevention owner, and corrective action.", "Review whether the denial started in scheduling, registration, eligibility, authorization, documentation, coding, claims, or payer behavior.", "This shows I understand denial prevention as a system-wide operations function, not just back-end claim correction."],
    ["A/R Follow-Up", "Accounts Receivable", "High", 87, "Days in A/R", "A/R Follow-Up / Billing", "Monitors unpaid claims, payer delays, denials, underpayments, missing information, appeal deadlines, and aging accounts.", "Work queues may not be prioritized, high-dollar accounts may age, payer requests may be missed, or ownership may be unclear.", "The patient may experience delayed account resolution, late statements, or confusing balance changes.", "Staff may face backlog growth, repeated payer calls, rushed appeals, and unclear account ownership.", "A/R delays reduce cash flow, increase days in A/R, increase write-off risk, and weaken forecasting.", "Prioritize A/R queues by claim age, dollar amount, payer, denial status, appeal deadline, and last action date.", "Review aged accounts, high-dollar claims, denied claims, underpayments, payer requests, and accounts nearing deadlines.", "This shows I understand revenue cycle follow-up requires prioritization, ownership, documentation, and escalation."],
    ["Payment Posting", "Cash Applications", "Medium to High", 76, "Payment Posting Accuracy Rate", "Payment Posting / Cash Applications", "Records payer payments, contractual adjustments, denials, underpayments, patient responsibility, and remaining balances.", "Payment may post to wrong account, adjustment may be incorrect, denial code may be missed, underpayment may not be identified, or secondary billing may not trigger.", "The patient may receive an incorrect bill, delayed statement, duplicate bill, or inaccurate balance.", "Staff may need to correct posting errors, resolve unapplied cash, review remittance advice, or answer billing questions.", "Posting errors can distort reports, hide denials, delay secondary billing, and misstate cash performance.", "Use payment posting quality review for account, payer, amount, adjustment, denial code, patient responsibility, and secondary billing trigger.", "Review underpayments, unusual adjustments, large balances, unclear remittance codes, denied line items, and unapplied cash.", "This shows I understand revenue cycle does not end when money arrives. Payment must be posted accurately for trustworthy reporting."],
    ["Executive Financial Visibility", "Leadership Reporting", "High", 83, "Revenue Cycle Dashboard Accuracy", "Revenue Cycle Leadership / Operations", "Turns revenue cycle workflow activity into leadership insight about cash flow, denial trends, operational risk, staffing burden, and patient experience.", "Reports may show outcomes without root causes, denial trends may not connect to upstream workflow, or staff rework burden may remain invisible.", "Patients may continue experiencing billing confusion, delays, and unclear communication if leadership cannot see workflow causes.", "Staff may continue preventable rework without leadership seeing workload pressure or root-cause patterns.", "Poor visibility can cause delayed decisions, preventable denials, cash instability, inaccurate forecasting, and avoidable write-offs.", "Build an executive dashboard connecting front-end errors, authorization risk, documentation gaps, denials, A/R delays, payment accuracy, and patient impact.", "Review trends to distinguish internal workflow failures from payer behavior and decide which improvements should be prioritized.", "This shows I understand healthcare operations from a leadership perspective: reporting should show where the workflow lost control."]
]

columns = [
    "Stage", "Category", "Risk Level", "Risk Score", "Metric Affected", "Team Involved",
    "What It Does", "What Can Break", "Patient Impact", "Staff Impact", "Financial Impact",
    "Improvement Action", "Human Review Needed", "Recruiter Explanation"
]
df = pd.DataFrame(workflow_data, columns=columns)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Home", "Revenue Cycle Workflow Map", "Patient Access Risk", "Prior Authorization Risk", "Documentation Integrity", "Denial Prevention", "A/R Follow-Up", "Payment Posting", "Financial Outcome Dashboard", "Executive Summary", "Disclaimer"]
)

def mobile_metric(label, value, orange=False):
    value_class = "metric-value metric-value-orange" if orange else "metric-value"
    st.markdown(
        f"""
        <div class='metric-box'>
            <div class='metric-label'>{label}</div>
            <div class='{value_class}'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def stage_card(row):
    st.markdown(f"## {row['Stage']}")
    st.markdown("<div class='orange-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='metric-grid'>", unsafe_allow_html=True)
    mobile_metric("Risk Score", f"{row['Risk Score']}/100")
    mobile_metric("Metric Affected", row["Metric Affected"])
    mobile_metric("Risk Level", row["Risk Level"], orange=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"**Team Involved:** {row['Team Involved']}")

    sections = [
        ("What the stage does", "What It Does"),
        ("What can break", "What Can Break"),
        ("Patient impact", "Patient Impact"),
        ("Staff impact", "Staff Impact"),
        ("Financial impact", "Financial Impact"),
        ("Improvement action", "Improvement Action"),
        ("Human review needed", "Human Review Needed"),
        ("Recruiter explanation", "Recruiter Explanation"),
    ]
    for label, key in sections:
        with st.expander(label, expanded=label in ["What the stage does", "What can break"]):
            st.write(row[key])

def orange_risk_bars(dataframe, title, label_col):
    st.markdown(f"## {title}")
    sorted_df = dataframe.sort_values("Risk Score", ascending=False)
    for _, row in sorted_df.iterrows():
        label = row[label_col]
        score = int(row["Risk Score"])
        meta = f"{row['Risk Level']} risk · {row['Metric Affected']}"
        st.markdown(
            f"""
            <div class='risk-card'>
                <div class='risk-card-title'>{label}</div>
                <div class='risk-card-meta'>{meta}</div>
                <div class='risk-bar-track'><div class='risk-bar-fill' style='width:{score}%;'></div></div>
                <div class='risk-score-label'>{score}/100</div>
            </div>
            """,
            unsafe_allow_html=True
        )

if page == "Home":
    st.title("Healthcare Revenue Cycle Intelligence Engine™")
    st.subheader("A simulated healthcare operations portfolio project showing how patient access, eligibility verification, prior authorization, documentation, claims, denials, A/R follow-up, and payment posting connect to reimbursement, cash flow, staff workload, and patient experience.")
    st.markdown("<div class='orange-divider'></div>", unsafe_allow_html=True)
    st.write("This dashboard is designed to answer one core healthcare operations question:")
    st.markdown("## Where did the workflow first lose control?")
    st.write("Revenue cycle problems rarely begin where they are discovered. A denial may appear in billing, an aging balance may appear in A/R, and a cash flow issue may appear in executive reports. But the original breakdown often begins earlier in scheduling, registration, insurance verification, eligibility verification, prior authorization, documentation, or claim readiness.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workflow Stages", "12")
    col2.metric("Highest Risk Score", f"{df['Risk Score'].max()}/100")
    col3.metric("Average Risk Score", f"{round(df['Risk Score'].mean(), 1)}/100")
    col4.metric("Critical Risk Areas", len(df[df["Risk Level"] == "Critical"]))
    st.markdown("## Portfolio Positioning")
    st.write("This simulated project demonstrates healthcare operations thinking across the full revenue cycle. It connects workflow risk, staff rework, patient experience, financial performance, denial prevention, and leadership visibility using synthetic no-PHI examples only.")

elif page == "Revenue Cycle Workflow Map":
    st.title("Revenue Cycle Workflow Map")
    st.write("This page shows the full simulated revenue cycle workflow from patient access to executive visibility.")
    st.dataframe(df[["Stage", "Category", "Risk Level", "Risk Score", "Metric Affected", "Team Involved"]], use_container_width=True, hide_index=True)
    orange_risk_bars(df, "Simulated Revenue Cycle Risk Score by Workflow Stage", "Stage")
    st.markdown("## Workflow Connection")
    st.write("Each stage depends on the quality of the stage before it. When the workflow loses control upstream, the downstream impact can appear as a denial, claim delay, A/R backlog, payment posting error, patient billing issue, or executive reporting gap.")

elif page == "Patient Access Risk":
    st.title("Patient Access Risk")
    st.write("Patient access includes scheduling, registration, insurance verification, and eligibility verification.")
    for _, row in df[df["Stage"].isin(["Patient Scheduling", "Patient Registration", "Insurance Verification", "Eligibility Verification"])].iterrows():
        stage_card(row)

elif page == "Prior Authorization Risk":
    stage_card(df[df["Stage"] == "Prior Authorization"].iloc[0])

elif page == "Documentation Integrity":
    st.title("Documentation Integrity")
    st.write("This section connects clinical documentation and coding readiness to revenue cycle performance.")
    for _, row in df[df["Stage"].isin(["Clinical Documentation", "Coding Readiness"])].iterrows():
        stage_card(row)

elif page == "Denial Prevention":
    stage_card(df[df["Stage"] == "Denial Prevention"].iloc[0])
    st.markdown("## Denial Root-Cause Review Questions")
    for q in ["Where was the denial discovered?", "Where did the workflow first lose control?", "Was the issue preventable?", "Which team first touched the risk?", "Which metric changed?", "What improvement action prevents recurrence?"]:
        st.checkbox(q)

elif page == "A/R Follow-Up":
    stage_card(df[df["Stage"] == "A/R Follow-Up"].iloc[0])

elif page == "Payment Posting":
    stage_card(df[df["Stage"] == "Payment Posting"].iloc[0])

elif page == "Financial Outcome Dashboard":
    st.title("Financial Outcome Dashboard")
    st.write("This simulated dashboard shows how workflow risk affects financial outcomes.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Simulated Clean Claim Rate", "87%", "-4% risk")
    col2.metric("Simulated Denial Rate", "13%", "+3% risk")
    col3.metric("Simulated Days in A/R", "41 days", "+6 days")
    col4.metric("Simulated Payment Posting Accuracy", "94%", "-2% risk")
    category_risk = df.groupby("Category", as_index=False)["Risk Score"].mean()
    category_risk["Risk Score"] = category_risk["Risk Score"].round(0).astype(int)
    category_risk["Risk Level"] = "Simulated category average"
    category_risk["Metric Affected"] = "Category risk visibility"
    orange_risk_bars(category_risk, "Financial Risk by Workflow Category", "Category")
    st.markdown("## Simulated Financial Impact Logic")
    st.write("""
    - Front-end errors can reduce clean claim performance.
    - Missed authorization can create full denial risk.
    - Documentation gaps can trigger medical necessity denials.
    - A/R follow-up delays increase cash flow risk.
    - Payment posting errors distort financial reporting and patient balances.
    """)

elif page == "Executive Summary":
    st.title("Executive Summary")
    st.write("The Healthcare Revenue Cycle Intelligence Engine™ is a simulated operations dashboard designed to show how revenue cycle workflows connect from patient scheduling through payment posting.")
    st.markdown("## Key Findings")
    st.write("""
    1. The highest simulated risk areas are prior authorization, denial prevention, documentation integrity, and A/R follow-up.
    2. Patient access errors can create downstream denials, claim delays, staff rework, and patient confusion.
    3. Denials should not only be worked after they occur. They should be traced back to the first workflow breakdown.
    4. Human review is still required for complex authorization, documentation, coding, denial, A/R, and payment posting issues.
    5. Executive visibility should connect financial outcomes to operational root causes.
    """)
    st.markdown("## Recruiter-Facing Explanation")
    st.markdown("""<div class='brand-callout'>I created this simulated healthcare operations dashboard to demonstrate how patient access, eligibility verification, prior authorization, clinical documentation, coding readiness, claim submission, denial prevention, A/R follow-up, payment posting, and executive financial visibility connect as one revenue cycle system. The project uses synthetic no-PHI examples and focuses on identifying where the workflow first lost control.</div>""", unsafe_allow_html=True)

elif page == "Disclaimer":
    st.title("Disclaimer")
    st.markdown("""<div class='brand-callout'><strong>Disclaimer:</strong> This is a simulated educational portfolio project created for healthcare operations learning and career development. It uses synthetic no-PHI examples only and is not intended for clinical, coding, billing, legal, reimbursement, or patient-care decision-making.</div>""", unsafe_allow_html=True)
    st.markdown("## No-PHI Statement")
    st.write("This app does not include real patient data, protected health information, payer data, employer data, claims data, clinical records, financial records, or confidential organizational information.")
    st.markdown("## Educational Purpose")
    st.write("The purpose of this project is to demonstrate healthcare operations thinking, revenue cycle workflow awareness, denial prevention logic, process improvement understanding, and patient-to-professional perspective.")
