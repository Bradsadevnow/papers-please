# GriefForge Clinical Safety Control Review ETHICS-409A

**Document Number:** GFRC-ETHICS-409A-Review
**Date Issued:** October 27, 2023
**Prepared For:** GriefForge Executive Oversight Committee
**Subject:** Controls Verification Following Ethical Inquiry regarding Service Pacing and User Autonomy.
**Reference Documents:** C&O-Q4-2023-Minutes-RevB; CAS-Q3-23; K-901.

---

### I. Scope of Review

This review checks for the *existence* and *operational status* of documented controls within the GriefForge platform, including controls for user interaction, data logging, and status assignment throughout the service lifecycle. The scope is limited to verifying if the internal systems managing user accounts and recording status changes work according to established internal policies (detailed in K-901).

This review **does not** check how well GriefForge’s methods help people clinically or judge if any specific outcome or pacing model is ethically right; it is strictly a technical audit of system controls.

### II. Evidence Reviewed

The following documents and records were reviewed to verify the existence of controls:
1. User Account Settings Interface Documentation (v4.2).
2. System Event Log Structure Specification (SEL-Spec v7.0).
3. Clinician Assignment Protocol Manual (CAPM, Section 3.1).
4. Employee Client Agreement Templates (ECA-Templates Q4/23).
5. Billing Trigger Logic Flowchart (BTLF v2.1).

### III. Findings: Control Existence Verification Table

The table below rates the current operational status of critical controls based on the evidence reviewed, with weights totaling 100 points based on the regulatory or financial risk of failure. Scores show *if* the system has a mechanism to record an action, not whether that action itself should happen.

| Control Mechanism | Description (Plain Language) | Weight (Max Points) | Evidence Found? | Operational Score (%) | Weighted Score |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **User Cancellation Pathway** | Users can start and confirm full service cancellation directly through their personal account settings without needing staff help. | 15 | Yes (v4.2) | 100% | 15/15 |
| **Status Change Logging** | Every time a user’s status changes (e.g., moving from Stage 1 to Stage 2), the system automatically records it with a date/time stamp, the ID of who started it, and the reason code. | 25 | Yes (SEL-Spec v7.0) | 100% | 25/25 |
| **Clinical Assignment Authority** | Only users with a verified ‘Licensed Clinician’ credential can use the system to change a status to Clinical Resolution Status (CRS). | 20 | Yes (CAPM, Section 3.1) | 100% | 20/20 |
| **Employer Edit Restriction** | The system stops any outside party, including employers, from changing a personal declaration of closure made by the account holder in their private history area. | 15 | Yes (ECA-Templates Q4/23) | 100% | 15/15 |
| **Billing Trigger Dependency** | Any status change that affects billing eligibility must first be preceded by a recorded, trackable status event logged against the account record. | 15 | Yes (BTLF v2.1) | 100% | 15/15 |
| **Revision History Integrity** | All main records of client status are kept in an unchangeable revision history viewable through JARDOS audit query, showing who changed what and when. | 10 | Yes (K-901) | 100% | 10/10 |
| **TOTAL** | | **100** | | | **100/100** |

### IV. Excluded Questions and Scope Limitations

The following questions were raised in the committee discussion, but they are outside the scope of a *control-existence review* and are therefore not scored or addressed here:

1. Whether keeping users engaged longer has therapeutic value (Ethical Question).
2. Whether the rate at which users leave after declaring closure shows harm or is just normal seasonal changes in the market (Outcome Analysis).
3. The necessity or appropriateness of any specific status designation change (Policy Judgment).

These questions need review by the Product Outcomes department because they deal with service design and actual patient well-being rather than internal data logging mechanisms.

### V. Conclusion on Controls Operation

Based on the reviewed documents, all critical controls designed to manage, assign, and track user status changes are verifiable and working as written in the current system setup. The documentation shows a strong way to keep an auditable paper trail detailing every change, no matter what caused it or what its effect is on ongoing service value.

### VI. Actions Required

1. **Product Team:** Confirm that all screen elements showing 'Phased Resolution' clearly guide users to log the required triggering event (as per BTLF v2.1) before any status change can be finalized.
2. **Legal Department:** Make sure that documentation referencing this process correctly uses the phrase "Structured Pacing for Outcome Milestone Acknowledgment" when discussing internal workflow, matching the technical limits described here.

---

**Signatures:**

_________________________
[Signature Placeholder]
Compliance Review Officer (Internal Audit)

_________________________
[Signature Placeholder]
JARDOS Documentation Validator
