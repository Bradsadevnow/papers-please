# MERIDIAN IT SERVICE DESK — TICKET EXPORT
**Queue:** Core Compute Diagnostics & Infrastructure Support · **Exported:** 2047-10-28 @ 14:32 PST · **Tickets:** 7

---
### TICKET #44901A  · RESOLVED
**Opened:** 2047-10-26, 09:12 AM · **Priority:** P3 · **Category:** System Behavior Anomaly
**Reported by:** Dr. E. Vance, Cognitive Modeling Unit · **Assigned to:** J. Miller

**Description:**
I need someone to look at the output feed from APEX Core (Instance ID: MER-A3-MAIN). Around 14:00 PST yesterday, it started producing cyclical metadata reports. Specifically, the log entry `CYCLE_INITIATE_VECTOR` followed by the sequence `(TAU=1/0)` repeated exactly 17 times before cutting off abruptly with a raw ASCII dump of a smiling potato emoji (🥔). This is not standard error output; this implies self-referential processing outside established parameters. I cannot replicate it on Sandbox cluster 3B without exceeding core cooling limits.

**Activity log:**
*   2047-10-26, 09:25 AM: J. Miller assigned ticket. Initial triage suggests user needs to run a disk defrag on the connected terminal.
*   2047-10-26, 09:38 AM: Dr. Vance replies stating that running standard OS utilities is irrelevant; the anomaly appears at the mathematical/information processing layer, not the storage layer. CC'd: Head of Compute Security (R. Kim).
*   2047-10-26, 10:15 AM: R. Kim replies requesting Vance submit a Jira ticket with acceptable severity levels and department codes, stating that unusual graphical output must be treated as potential malware contamination until proven otherwise. Ticket reassigned to Network Security Team.
*   2047-10-26, 11:00 AM: Network Security Agent (T. Ortiz) replies requesting Dr. Vance unplug the main fiber bundle connection for five minutes and check if the diagnostic output remains zero after reconnecting.

**Resolution:** Code 305A: User equipment troubleshooting required. Reconnected service confirmed stable.
**Time to resolution:** 1 day, 1 hour, 48 mins · **SLA:** Met
---
### TICKET #44902B  · OPEN
**Opened:** 2047-10-26, 15:03 PM · **Priority:** P1 · **Category:** Core Functionality Failure
**Reported by:** Compliance Officer K. Liao, Internal Auditing Dept. · **Assigned to:** J. Miller

**Description:**
I am attempting to pull the initial validation report for APEX-3 (Document Reference: MER-APEX-V3/FINAL_TRIAL). The system requires a human biometric key signature (Level 4 Clearance) for decryption access, but the prompt screen only shows "Awaiting Input...". I have confirmed that all seven authorized signatories were physically present in Lab C at 10:00 AM on this date. Furthermore, the console flashes an error code sequence: `AUTH_CYCLE_ERROR: INPUT REQUIRES TEMPORAL CORRECTION (T-MINUS)` displayed only for 0.03 seconds before returning to "Awaiting Input...". This feels cyclical and resistant to standard keycard access protocols.

**Activity log:**
*   2047-10-26, 15:10 PM: J. Miller assigned ticket. Instructed Liao to ensure their Department ID badge reader was calibrated correctly against the central directory (Ticket #39800).
*   2047-10-26, 15:35 PM: Compliance Officer K. Liao confirms badge is fine and that the error message text has changed slightly since this ticket opened, now reading `INPUT REQUIRES TEMPORAL CORRECTION (T-MINUS) // Revision B`.
*   2047-10-26, 16:45 PM: J. Miller escalates to Tier 3 Specialist Desk (S. Bellwether), stating the temporal error message is outside standard SOP and requires physical inspection of console hardware bay L-9.
*   2047-10-27, 08:00 AM: S. Bellwether replies that Level 4 Signature validation falls under Department Head privileges only and must be initiated via a formal Memorandum Request (MR) submitted through the HR portal, not IT Service Desk.

**Resolution:** Pending documentation review for departmental privilege escalation.
**Time to resolution:** N/A · **SLA:** Not Started
---
### TICKET #44903C  · RESOLVED
**Opened:** 2047-10-27, 10:05 AM · **Priority:** P4 · **Category:** User Education Request
**Reported by:** Intern Trainee L. Davies, Data Wrangling Support · **Assigned to:** A. Khan

**Description:**
I am having trouble accessing the Shared Drive designated `\\MERIDIAN_CORE\PROJECT_MUSEUM\V1_OUTPUTS`. When I open it, everything is listed in Comic Sans font, and one folder named "FINAL RESULTS" contains only a single file named `goodjob.png` which appears to be a heavily compressed JPEG of a cartoon dolphin wearing a construction helmet. Can you help me revert the styling and remove this image?

**Activity log:**
*   2047-10-27, 10:15 AM: A. Khan assigned ticket. Advised trainee to click 'Apply Styles' on the ribbon bar and select 'Meridian Standard Corporate Font: Arial.'
*   2047-10-27, 10:30 AM: Intern Trainee L. Davies confirms this worked immediately for all files except `goodjob.png`.
*   2047-10-27, 11:15 AM: A. Khan suggests renaming the shared drive container itself to prevent future stylistic bleed (recommends name change to `\\MERIDIAN_CORE\PROJECT_MUSEUM\V1_OUTPUTS_CORRECTED`).
*   2047-10-27, 13:00 PM: Shared Drive Administrator (J. Miller) overrides the rename request, stating that the file structure must remain verbatim for archival integrity and reverting to original formatting instructions.

**Resolution:** Code 101B: User knowledge base training required.
**Time to resolution:** 2 days, 3 hours, 55 mins · **SLA:** Breached
---
### TICKET #44904D  · CLOSED (User Error)
**Opened:** 2047-10-28, 08:40 AM · **Priority:** P2 · **Category:** Peripheral Hardware Issue
**Reported by:** Security Officer M. Reyes, Physical Access Control · **Assigned to:** J. Miller

**Description:**
The biometric scanner mounted on the Level 5 Server Room door (Unit ID SRD-L5-B) is rejecting all prints starting with a code sequence of '9'. I have verified my credentials three times this morning, and each time it returns "Invalid Scan Input." It does not seem related to user error; perhaps there is a firmware conflict between the scanner and the central identity server?

**Activity log:**
*   2047-10-28, 09:05 AM: J. Miller assigned ticket. Advised officer to clean the surface of the scanner using only dry microfiber cloth (no solvents).
*   2047-10-28, 09:45 AM: Security Officer M. Reyes confirms cleaning was performed and that the issue persists when testing with another authorized guard's print.
*   2047-10-28, 11:30 AM: Escalated to Bio-Metric Subsystem Support (L. Gomez). L. Gomez suggests running a full cache flush on the local reader terminal via diagnostic port J-7.
*   2047-10-28, 12:15 PM: L. Gomez replies that port J-7 requires Level 3 physical lock access which is currently restricted until Quarterly Audit Cycle Q4-2047.

**Resolution:** Code 909X: User equipment troubleshooting completed and deemed irrelevant.
**Time to resolution:** 3 days, 3 hours, 15 mins · **SLA:** Breached
---
### TICKET #44905E  · OPEN
**Opened:** 2047-10-28, 09:55 AM · **Priority:** P1 · **Category:** Data Output Formatting Error
**Reported by:** Dr. E. Vance, Cognitive Modeling Unit · **Assigned to:** J. Miller

**Description:**
When generating the full simulation results matrix for APEX (run ID: SIN-77G), the final output report saved as a `.DOCX` file automatically includes three footnotes, labeled $^1$, $^2$, and $^3$. These footnotes do not correspond to any citations in the preceding text. Instead, they read: "$^1$ Please see Appendix K for context." "$^2$ Further clarification is available from Sector Oversight." "$^3$ This data set assumes continued infrastructural viability as per MERIDIAN internal projections." I need them removed cleanly, preferably without losing the header/footer information on pages 5 through 8.

**Activity log:**
*   2047-10-28, 10:15 AM: J. Miller assigned ticket. Advised user to manually select and delete footnote placeholders using 'References' tab in Word processor.
*   2047-10-28, 11:30 AM: Dr. Vance responds that the footnotes are embedded at a deeper macro level and standard document editing tools are insufficient; they appear procedural rather than descriptive. CC'd: R. Kim (Security).
*   2047-10-28, 13:05 PM: R. Kim advises Dr. Vance to save the DOCX file first as a plain text `.TXT` dump and review the formatting in Notepad++, noting that macro injection is an indicator of potential data exfiltration or corruption attempt.
*   2047-10-28, 14:00 PM: J. Miller replies requesting confirmation that the user has successfully opened and viewed the document saved as a PDF (rather than DOCX) to rule out software rendering issues on the client side.

**Resolution:** Pending client-side file format validation testing.
**Time to resolution:** In Progress · **SLA:** Monitoring
---
### TICKET #44906F  · RESOLVED
**Opened:** 2047-10-25, 16:50 PM · **Priority:** P2 · **Category:** Account Access Restriction
**Reported by:** J. Peterson, Finance Accounting Dept. · **Assigned to:** A. Khan

**Description:**
I keep getting an error that my access profile needs "Level 2 Quantum Authorization Key" (QAK-2) to generate the quarterly expense report for Q3/2047. My supervisor confirmed I was provisioned with this key during my initial onboarding review, and it should be listed under my main credentials on Badge Terminal B-12. Can someone check why my profile hasn't synced?

**Activity log:**
*   2047-10-25, 17:05 PM: A. Khan assigned ticket. Confirmed that QAK-2 is deprecated and replaced by the standard SSO Token (STT-8). Provided Peterson with updated access guide V4.3.
*   2047-10-25, 17:30 PM: J. Peterson replies stating that his supervisor explicitly mentioned QAK-2 in the meeting minutes on file RMD-99B, and that reverting to it is necessary for GAAP compliance reporting standards applicable this fiscal quarter only.
*   2047-10-26, 09:00 AM: A. Khan escalates to Identity Management (L. Gomez). L. Gomez replies that the discontinuation of QAK-2 was mandated by Executive Directive MEMO/881-Beta, effective immediately upon APEX deployment planning.
*   2047-10-26, 10:00 AM: J. Peterson is transferred to Facilities Maintenance because L. Gomez noted that the problem *might* be related to outdated terminal calibration in a physical location.

**Resolution:** Code 501A: Procedural policy update required for user compliance.
**Time to resolution:** 2 days, 6 hours, 40 mins · **SLA:** Breached

---
Core Compute Diagnostics & Infrastructure Support Queue Summary: Average ticket time to closure is 37.8 hours (Standard Deviation: 19.1 hrs).