import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Healthcare Revenue Cycle Intelligence Engine™",
    page_icon="🏥",
    layout="wide"
)

# ------------------------------------------------------------
# Brand Styling
# ------------------------------------------------------------
TENNESSEE_ORANGE = "#FF8200"
BLACK = "#000000"
WHITE = "#FFFFFF"

st.markdown(
    f"""
    <style>
    .main {{
        background-color: {WHITE};
        color: {BLACK};
    }}
    h1, h2, h3 {{
        color: {BLACK};
    }}
    .orange-divider {{
        border-top: 3px solid {TENNESSEE_ORANGE};
        margin-top: 10px;
        margin-bottom: 20px;
    }}
    .risk-critical {{
        color: #B00020;
        font-weight: 700;
    }}
    .risk-high {{
        color: #C44A00;
        font-weight: 700;
    }}
    .risk-medium {{
        color: #A66A00;
        font-weight: 700;
    }}
    .risk-low {{
        color: #1F7A1F;
        font-weight: 700;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Simulated No-PHI Revenue Cycle Data
# ------------------------------------------------------------
workflow_data = [
    {
        "Stage": "Patient Scheduling",
        "Category": "Patient Access",
        "Risk Level": "Medium to High",
        "Risk Score": 72,
        "Metric Affected": "Appointment Accuracy Rate",
        "Team Involved": "Scheduling / Patient Access",
        "What It Does": "Captures the appointment request, visit reason, service type, provider, location, and initial patient information.",
        "What Can Break": "Visit reason may be vague, wrong service type may be selected, referral need may be missed, or authorization risk may not be flagged.",
        "Patient Impact": "The patient may experience delays, rescheduling, repeated calls, or confusion about what is needed before the visit.",
        "Staff Impact": "Staff may need to correct visit type, call the patient again, or urgently involve authorization or eligibility teams.",
        "Financial Impact": "Incorrect scheduling can delay clearance, create authorization misses, increase denial risk, and cause downstream rework.",
        "Improvement Action": "Use a scheduling intake checklist that confirms reason for visit, service type, referral need, and authorization trigger.",
        "Human Review Needed": "Review specialty services, imaging, procedures, and high-cost services before the date of service.",
        "Recruiter Explanation": "This shows I understand that revenue cycle risk can begin before the patient arrives. Scheduling is the first control point in denial prevention."
    },
    {
        "Stage": "Patient Registration",
        "Category": "Patient Access",
        "Risk Level": "High",
        "Risk Score": 81,
        "Metric Affected": "Registration Accuracy Rate",
        "Team Involved": "Registration / Front Desk",
        "What It Does": "Captures demographics, contact information, insurance information, guarantor details, consent forms, and account setup.",
        "What Can Break": "Demographic errors, duplicate accounts, incorrect insurance entry, missing consent forms, or unclear guarantor information.",
        "Patient Impact": "The patient may receive incorrect communication, duplicate statements, or billing confusion.",
        "Staff Impact": "Staff may need to correct accounts, update insurance, merge duplicates, or respond to patient billing concerns.",
        "Financial Impact": "Registration errors can create claim rejections, billing delays, denial risk, and increased cost to collect.",
        "Improvement Action": "Use a registration quality checklist before the patient encounter is finalized.",
        "Human Review Needed": "Review duplicate accounts, mismatched patient identifiers, guarantor confusion, and repeated registration errors.",
        "Recruiter Explanation": "This shows I understand clean front-end data as the foundation for clean claims and accurate patient communication."
    },
    {
        "Stage": "Insurance Verification",
        "Category": "Financial Clearance",
        "Risk Level": "High",
        "Risk Score": 84,
        "Metric Affected": "Insurance Verification Completion Rate",
        "Team Involved": "Patient Access / Financial Clearance",
        "What It Does": "Confirms that payer, member ID, group number, plan type, subscriber information, and coordination of benefits are accurate.",
        "What Can Break": "Outdated insurance card, wrong payer selected, incorrect member ID, missed secondary coverage, or unclear coordination of benefits.",
        "Patient Impact": "The patient may receive unexpected bills or be asked to provide insurance information again after the visit.",
        "Staff Impact": "Staff may need to correct insurance, rebill claims, contact the patient, or resolve payer mismatches.",
        "Financial Impact": "Insurance errors can cause claim rejections, delayed reimbursement, and avoidable administrative rework.",
        "Improvement Action": "Confirm payer, plan, member ID, group number, subscriber, secondary coverage, and coordination of benefits before service.",
        "Human Review Needed": "Review accounts with multiple plans, recent insurance changes, or conflicting payer responses.",
        "Recruiter Explanation": "This shows I understand the difference between entering insurance and verifying that insurance is usable for the revenue cycle."
    },
    {
        "Stage": "Eligibility Verification",
        "Category": "Financial Clearance",
        "Risk Level": "High",
        "Risk Score": 86,
        "Metric Affected": "Eligibility Clearance Rate",
        "Team Involved": "Eligibility / Financial Clearance",
        "What It Does": "Confirms active coverage for the date of service and checks benefit rules that may affect reimbursement.",
        "What Can Break": "Coverage may be active, but benefits, referral needs, authorization indicators, or patient responsibility may be missed.",
        "Patient Impact": "The patient may face unexpected financial responsibility, delayed care, or confusing billing communication.",
        "Staff Impact": "Staff may need to recheck benefits, contact payers, update financial clearance, or resolve preventable denials.",
        "Financial Impact": "Eligibility failures can cause coverage denials, patient balance disputes, delayed payment, and write-off risk.",
        "Improvement Action": "Use a two-level review: active coverage plus service-specific benefit verification.",
        "Human Review Needed": "Review unclear payer responses, high patient responsibility, complex benefit rules, or service exclusions.",
        "Recruiter Explanation": "This shows I understand eligibility verification as a revenue protection function, not just a checkbox."
    },
    {
        "Stage": "Prior Authorization",
        "Category": "Authorization",
        "Risk Level": "Critical",
        "Risk Score": 94,
        "Metric Affected": "Authorization Turnaround Time",
        "Team Involved": "Prior Authorization / Clinical / Patient Access",
        "What It Does": "Confirms whether payer approval is required before service and tracks approval status before claim submission.",
        "What Can Break": "Authorization may be missed, submitted late, approved for the wrong code, wrong date, wrong provider, or unsupported by documentation.",
        "Patient Impact": "The patient may experience delays, rescheduling, uncertainty, denied coverage, or unexpected financial responsibility.",
        "Staff Impact": "Staff may need urgent payer calls, documentation requests, retroactive reviews, appeals, or account corrections.",
        "Financial Impact": "Missing authorization can lead to full denial, delayed reimbursement, increased A/R, and write-off risk.",
        "Improvement Action": "Create a pre-service authorization checkpoint for service code, diagnosis support, location, date range, and approval number.",
        "Human Review Needed": "Review high-cost services, imaging, procedures, specialty care, incomplete documentation, and denied or pending authorizations.",
        "Recruiter Explanation": "This shows I understand how prior authorization connects payer rules, documentation, patient access, claims, denials, and patient experience."
    },
    {
        "Stage": "Clinical Documentation",
        "Category": "Documentation",
        "Risk Level": "High",
        "Risk Score": 88,
        "Metric Affected": "Documentation Completion Rate",
        "Team Involved": "Providers / Clinical Support / HIM",
        "What It Does": "Records why care was needed, what was performed, and whether the service supports coding, billing, authorization, and medical necessity.",
        "What Can Break": "Medical necessity may be unclear, provider note may be incomplete, diagnosis may not support service, or required forms may be missing.",
        "Patient Impact": "The patient may experience delayed authorization, delayed claim resolution, denied coverage, or billing confusion.",
        "Staff Impact": "Staff may need provider queries, claim holds, additional documentation requests, or appeal support.",
        "Financial Impact": "Documentation gaps can cause medical necessity denials, claim delays, compliance risk, and avoidable rework.",
        "Improvement Action": "Use a documentation readiness review for high-risk services before coding and claim submission.",
        "Human Review Needed": "Review incomplete, inconsistent, delayed, or unclear documentation before the claim moves forward.",
        "Recruiter Explanation": "This shows I understand documentation as both a clinical record and an operational revenue cycle control point."
    },
    {
        "Stage": "Coding Readiness",
        "Category": "Coding / HIM",
        "Risk Level": "High",
        "Risk Score": 82,
        "Metric Affected": "Coding Query Rate",
        "Team Involved": "Coding / HIM / Providers",
        "What It Does": "Determines whether documentation is complete and clear enough for accurate, supported code assignment.",
        "What Can Break": "Documentation may not support the code, modifiers may be missing, diagnosis and procedure may not align, or provider clarification may be delayed.",
        "Patient Impact": "The patient may experience delayed claim processing, delayed statements, or confusion about claim status.",
        "Staff Impact": "Coders may need to query providers, hold claims, review records multiple times, or escalate documentation concerns.",
        "Financial Impact": "Coding readiness issues can delay claims, increase denial risk, reduce clean claim performance, and affect reimbursement accuracy.",
        "Improvement Action": "Create a coding readiness checklist for documentation support, diagnosis alignment, procedure support, and modifier review.",
        "Human Review Needed": "Review complex encounters, unclear notes, high-dollar services, missing modifiers, and repeated coding-related denials.",
        "Recruiter Explanation": "This shows I understand coding readiness from an operations perspective without claiming to be a certified coder."
    },
    {
        "Stage": "Claim Submission",
        "Category": "Claims",
        "Risk Level": "High",
        "Risk Score": 85,
        "Metric Affected": "Clean Claim Rate",
        "Team Involved": "Billing / Coding / Claims",
        "What It Does": "Sends the completed claim to the payer using patient, payer, authorization, documentation, coding, provider, and charge information.",
        "What Can Break": "Claim may contain incorrect demographics, missing authorization, wrong provider, missing modifier, unresolved edits, or incomplete documentation.",
        "Patient Impact": "The patient may receive delayed billing updates, unexpected statements, or repeated requests for information.",
        "Staff Impact": "Billing staff may need to correct claims, resolve edits, rebill payers, or send claims back upstream.",
        "Financial Impact": "Submission errors can cause rejections, denials, delayed payment, increased A/R, and reduced first-pass resolution.",
        "Improvement Action": "Use a claim readiness validation step before submission.",
        "Human Review Needed": "Review high-dollar claims, authorization-required services, unresolved edits, and repeated payer-specific issues.",
        "Recruiter Explanation": "This shows I understand that a clean claim depends on clean workflow before billing."
    },
    {
        "Stage": "Denial Prevention",
        "Category": "Denials",
        "Risk Level": "Critical",
        "Risk Score": 92,
        "Metric Affected": "Preventable Denial Rate",
        "Team Involved": "RCM / Denials / Patient Access",
        "What It Does": "Identifies and corrects risks before claims deny by using trend analysis, root-cause review, edits, and feedback loops.",
        "What Can Break": "Teams may fix individual claims without tracing root causes, denial data may not reach upstream teams, or prevention owners may not be assigned.",
        "Patient Impact": "The patient may experience confusing bills, delayed resolution, unexpected balances, or reduced trust.",
        "Staff Impact": "Staff may spend time appealing preventable denials, contacting payers, correcting records, and reworking accounts.",
        "Financial Impact": "Preventable denials increase cost to collect, delay reimbursement, increase write-off risk, and reduce cash predictability.",
        "Improvement Action": "Create a denial prevention feedback loop that tracks denial reason, first workflow breakdown, prevention owner, and corrective action.",
        "Human Review Needed": "Review whether the denial started in scheduling, registration, eligibility, authorization, documentation, coding, claims, or payer behavior.",
        "Recruiter Explanation": "This shows I understand denial prevention as a system-wide operations function, not just back-end claim correction."
    },
    {
        "Stage": "A/R Follow-Up",
        "Category": "Accounts Receivable",
        "Risk Level": "High",
        "Risk Score": 87,
        "Metric Affected": "Days in A/R",
        "Team Involved": "A/R Follow-Up / Billing",
        "What It Does": "Monitors unpaid claims, payer delays, denials, underpayments, missing information, appeal deadlines, and aging accounts.",
        "What Can Break": "Work queues may not be prioritized, high-dollar accounts may age, payer requests may be missed, or ownership may be unclear.",
        "Patient Impact": "The patient may experience delayed account resolution, late statements, or confusing balance changes.",
        "Staff Impact": "Staff may face backlog growth, repeated payer calls, rushed appeals, and unclear account ownership.",
        "Financial Impact": "A/R delays reduce cash flow, increase days in A/R, increase write-off risk, and weaken forecasting.",
        "Improvement Action": "Prioritize A/R queues by claim age, dollar amount, payer, denial status, appeal deadline, and last action date.",
        "Human Review Needed": "Review aged accounts, high-dollar claims, denied claims, underpayments, payer requests, and accounts nearing deadlines.",
        "Recruiter Explanation": "This shows I understand revenue cycle follow-up requires prioritization, ownership, documentation, and escalation."
    },
    {
        "Stage": "Payment Posting",
        "Category": "Cash Applications",
        "Risk Level": "Medium to High",
        "Risk Score": 76,
        "Metric Affected": "Payment Posting Accuracy Rate",
        "Team Involved": "Payment Posting / Cash Applications",
        "What It Does": "Records payer payments, contractual adjustments, denials, underpayments, patient responsibility, and remaining balances.",
        "What Can Break": "Payment may post to wrong account, adjustment may be incorrect, denial code may be missed, underpayment may not be identified, or secondary billing may not trigger.",
        "Patient Impact": "The patient may receive an incorrect bill, delayed statement, duplicate bill, or inaccurate balance.",
        "Staff Impact": "Staff may need to correct posting errors, resolve unapplied cash, review remittance advice, or answer billing questions.",
        "Financial Impact": "Posting errors can distort reports, hide denials, delay secondary billing, and misstate cash performance.",
        "Improvement Action": "Use payment posting quality review for account, payer, amount, adjustment, denial code, patient responsibility, and secondary billing trigger.",
        "Human Review Needed": "Review underpayments, unusual adjustments, large balances, unclear remittance codes, denied line items, and unapplied cash.",
        "Recruiter Explanation": "This shows I understand revenue cycle does not end when money arrives. Payment must be posted accurately for trustworthy reporting."
    },
    {
        "Stage": "Executive Financial Visibility",
        "Category": "Leadership Reporting",
        "Risk Level": "High",
        "Risk Score": 83,
        "Metric Affected": "Revenue Cycle Dashboard Accuracy",
        "Team Involved": "Revenue Cycle Leadership / Operations",
        "What It Does": "Turns revenue cycle workflow activity into leadership insight about cash flow, denial trends, operational risk, staffing burden, and patient experience.",
        "What Can Break": "Reports may show outcomes without root causes, denial trends may not connect to upstream workflow, or staff rework burden may remain invisible.",
        "Patient Impact": "Patients may continue experiencing billing confusion, delays, and unclear communication if leadership cannot see workflow causes.",
        "Staff Impact": "Staff may continue preventable rework without leadership seeing workload pressure or root-cause patterns.",
        "Financial Impact": "Poor visibility can cause delayed decisions, preventable denials, cash instability, inaccurate forecasting, and avoidable write-offs.",
        "Improvement Action": "Build an executive dashboard connecting front-end errors, authorization risk, documentation gaps, denials, A/R delays, payment accuracy, and patient impact.",
        "Human Review Needed": "Review trends to distinguish internal workflow failures from payer behavior and decide which improvements should be prioritized.",
        "Recruiter Explanation": "This shows I understand healthcare operations from a leadership perspective: reporting should show where the workflow lost control."
    }
]

df = pd.DataFrame(workflow_data)

# ------------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "Home",
        "Revenue Cycle Workflow Map",
        "Patient Access Risk",
        "Prior Authorization Risk",
        "Documentation Integrity",
        "Denial Prevention",
        "A/R Follow-Up",
        "Payment Posting",
        "Financial Outcome Dashboard",
        "Executive Summary",
        "Disclaimer"
    ]
)

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def risk_badge(risk_level):
    if "Critical" in risk_level:
        return f"<span class='risk-critical'>{risk_level}</span>"
    if "High" in risk_level:
        return f"<span class='risk-high'>{risk_level}</span>"
    if "Medium" in risk_level:
        return f"<span class='risk-medium'>{risk_level}</span>"
    return f"<span class='risk-low'>{risk_level}</span>"


def stage_card(row):
    st.markdown(f"## {row['Stage']}")
    st.markdown("<div class='orange-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Score", f"{row['Risk Score']}/100")
    col2.metric("Metric Affected", row["Metric Affected"])
    col3.markdown(f"**Risk Level:** {risk_badge(row['Risk Level'])}", unsafe_allow_html=True)

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

# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------
if page == "Home":
    st.title("Healthcare Revenue Cycle Intelligence Engine™")
    st.subheader(
        "A simulated healthcare operations portfolio project showing how patient access, eligibility verification, prior authorization, documentation, claims, denials, A/R follow-up, and payment posting connect to reimbursement, cash flow, staff workload, and patient experience."
    )
    st.markdown("<div class='orange-divider'></div>", unsafe_allow_html=True)
    st.write("This dashboard is designed to answer one core healthcare operations question:")
    st.markdown("## Where did the workflow first lose control?")
    st.write(
        "Revenue cycle problems rarely begin where they are discovered. A denial may appear in billing, an aging balance may appear in A/R, and a cash flow issue may appear in executive reports. But the original breakdown often begins earlier in scheduling, registration, insurance verification, eligibility verification, prior authorization, documentation, or claim readiness."
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Workflow Stages", "12")
    col2.metric("Highest Risk Score", f"{df['Risk Score'].max()}/100")
    col3.metric("Average Risk Score", f"{round(df['Risk Score'].mean(), 1)}/100")
    col4.metric("Critical Risk Areas", len(df[df["Risk Level"] == "Critical"]))

    st.markdown("## Portfolio Positioning")
    st.write(
        "This simulated project demonstrates healthcare operations thinking across the full revenue cycle. It connects workflow risk, staff rework, patient experience, financial performance, denial prevention, and leadership visibility using synthetic no-PHI examples only."
    )

elif page == "Revenue Cycle Workflow Map":
    st.title("Revenue Cycle Workflow Map")
    st.write("This page shows the full simulated revenue cycle workflow from patient access to executive visibility.")
    st.dataframe(
        df[["Stage", "Category", "Risk Level", "Risk Score", "Metric Affected", "Team Involved"]],
        use_container_width=True
    )
    fig = px.bar(
        df,
        x="Stage",
        y="Risk Score",
        color="Risk Level",
        title="Simulated Revenue Cycle Risk Score by Workflow Stage"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("## Workflow Connection")
    st.write(
        "Each stage depends on the quality of the stage before it. When the workflow loses control upstream, the downstream impact can appear as a denial, claim delay, A/R backlog, payment posting error, patient billing issue, or executive reporting gap."
    )

elif page == "Patient Access Risk":
    st.title("Patient Access Risk")
    st.write("Patient access includes scheduling, registration, insurance verification, and eligibility verification.")
    patient_access_df = df[df["Stage"].isin([
        "Patient Scheduling",
        "Patient Registration",
        "Insurance Verification",
        "Eligibility Verification"
    ])]
    for _, row in patient_access_df.iterrows():
        stage_card(row)

elif page == "Prior Authorization Risk":
    row = df[df["Stage"] == "Prior Authorization"].iloc[0]
    stage_card(row)

elif page == "Documentation Integrity":
    st.title("Documentation Integrity")
    st.write("This section connects clinical documentation and coding readiness to revenue cycle performance.")
    documentation_df = df[df["Stage"].isin(["Clinical Documentation", "Coding Readiness"])]
    for _, row in documentation_df.iterrows():
        stage_card(row)

elif page == "Denial Prevention":
    row = df[df["Stage"] == "Denial Prevention"].iloc[0]
    stage_card(row)
    st.markdown("## Denial Root-Cause Review Questions")
    questions = [
        "Where was the denial discovered?",
        "Where did the workflow first lose control?",
        "Was the issue preventable?",
        "Which team first touched the risk?",
        "Which metric changed?",
        "What improvement action prevents recurrence?"
    ]
    for q in questions:
        st.checkbox(q)

elif page == "A/R Follow-Up":
    row = df[df["Stage"] == "A/R Follow-Up"].iloc[0]
    stage_card(row)

elif page == "Payment Posting":
    row = df[df["Stage"] == "Payment Posting"].iloc[0]
    stage_card(row)

elif page == "Financial Outcome Dashboard":
    st.title("Financial Outcome Dashboard")
    st.write("This simulated dashboard shows how workflow risk affects financial outcomes.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Simulated Clean Claim Rate", "87%", "-4% risk")
    col2.metric("Simulated Denial Rate", "13%", "+3% risk")
    col3.metric("Simulated Days in A/R", "41 days", "+6 days")
    col4.metric("Simulated Payment Posting Accuracy", "94%", "-2% risk")

    st.markdown("## Financial Risk by Workflow Category")
    category_risk = df.groupby("Category")["Risk Score"].mean().reset_index()
    fig = px.bar(
        category_risk,
        x="Category",
        y="Risk Score",
        title="Average Simulated Risk Score by Revenue Cycle Category"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## Simulated Financial Impact Logic")
    st.write(
        "- Front-end errors can reduce clean claim performance.\n"
        "- Missed authorization can create full denial risk.\n"
        "- Documentation gaps can trigger medical necessity denials.\n"
        "- A/R follow-up delays increase cash flow risk.\n"
        "- Payment posting errors distort financial reporting and patient balances."
    )

elif page == "Executive Summary":
    st.title("Executive Summary")
    st.write(
        "The Healthcare Revenue Cycle Intelligence Engine™ is a simulated operations dashboard designed to show how revenue cycle workflows connect from patient scheduling through payment posting."
    )
    st.markdown("## Key Findings")
    st.write(
        "1. The highest simulated risk areas are prior authorization, denial prevention, documentation integrity, and A/R follow-up.\n"
        "2. Patient access errors can create downstream denials, claim delays, staff rework, and patient confusion.\n"
        "3. Denials should not only be worked after they occur. They should be traced back to the first workflow breakdown.\n"
        "4. Human review is still required for complex authorization, documentation, coding, denial, A/R, and payment posting issues.\n"
        "5. Executive visibility should connect financial outcomes to operational root causes."
    )
    st.markdown("## Recruiter-Facing Explanation")
    st.info(
        "I created this simulated healthcare operations dashboard to demonstrate how patient access, eligibility verification, prior authorization, clinical documentation, coding readiness, claim submission, denial prevention, A/R follow-up, payment posting, and executive financial visibility connect as one revenue cycle system. The project uses synthetic no-PHI examples and focuses on identifying where the workflow first lost control."
    )

elif page == "Disclaimer":
    st.title("Disclaimer")
    st.warning(
        "Disclaimer: This is a simulated educational portfolio project created for healthcare operations learning and career development. It uses synthetic no-PHI examples only and is not intended for clinical, coding, billing, legal, reimbursement, or patient-care decision-making."
    )
    st.markdown("## No-PHI Statement")
    st.write(
        "This app does not include real patient data, protected health information, payer data, employer data, claims data, clinical records, financial records, or confidential organizational information."
    )
    st.markdown("## Educational Purpose")
    st.write(
        "The purpose of this project is to demonstrate healthcare operations thinking, revenue cycle workflow awareness, denial prevention logic, process improvement understanding, and patient-to-professional perspective."
    )
