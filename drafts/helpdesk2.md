# MERIDIAN IT SERVICE DESK — TICKET EXPORT
**Queue:** General Internal Support (Post-APEX-3 Rollout) · **Exported:** 2024-11-15 @ 14:17 EST · **Tickets:** 7

---
### TICKET #984321 :: RESOLVED
**Opened:** 2024-11-01, 09:15 AM · **Priority:** P3 · **Category:** Equipment/Peripheral
**Reported by:** Cynthia Jenkins, HR Operations · **Assigned to:** Marcus Bellweather

**Description:**
My badge reader seems flaky. When I try to clock in for the second time today (I know, it's a Tuesday), the screen just flashes ‘ERROR 403’ and nothing happens. It worked fine yesterday when I came in at 7:58 AM. I just need this fixed so I don't get flagged on payroll again by Accounting.

**Activity log:**
*   2024-11-01, 09:20 AM (Marcus Bellweather): Please try rebooting the reader unit itself. Unplug it from the wall for sixty seconds and plug it back in. Do not use force.
*   2024-11-01, 09:35 AM (Cynthia Jenkins): Done that twice now. It's still flashing ‘ERROR 403’ even after I unplugged the whole junction box near Desk B. This is costing me time.
*   2024-11-01, 09:45 AM (Marcus Bellweather): Have you confirmed if the adjacent terminal (the one for Janet in 3B) was also experiencing issues? Sometimes it trips the local network circuit.
*   2024-11-01, 10:01 AM (Service Desk Tier 2 Escalation): @Cynthia Jenkins: We have cycled the junction box power on our end as well. The issue is likely localized to your badge ID profile in Active Directory. Please submit a formal ticket request to Identity Management for an account refresh.

**Resolution:** User was advised that re-linking their credentials via Self-Service Portal (SSP) resolved the reading error.
**Time to resolution:** 2 hours, 46 minutes · **SLA:** Breached

---
### TICKET #984315 :: OPEN
**Opened:** 2024-11-03, 11:40 AM · **Priority:** P1 · **Category:** Software Access/APEX Support
**Reported by:** Dr. Alistair Reed, Theoretical Physics Dept. · **Assigned to:** Priya Sharma

**Description:**
I am trying to access the APEX-3 diagnostic output stream from my desktop terminal (Workstation A-49). The system keeps spitting out a sequence of non-integer values followed by an HTTP 503 error message, even when I input basic parameters like 'Standard Deviation for Beta Decay'. This was stable on Build 2.8. Can someone please look at the network logs? It feels bigger than just a software patch issue; it’s architectural.

**Activity log:**
*   2024-11-03, 11:45 AM (Priya Sharma): Dr. Reed, could you confirm if you are running the latest approved OS build on A-49? We recommend checking for pending mandatory updates via the Control Panel.
*   2024-11-03, 12:15 PM (Dr. Alistair Reed): The machine is running the mandated v10 build, Priya. I checked three times. Furthermore, the issue only occurs when attempting to query anything related to 'Global State Vector Analysis'.
*   2024-11-03, 1:05 PM (Priya Sharma): Per protocol, please clear your local browser cache and cookies, even if you are using a dedicated command line interface. Sometimes residual data interferes with API calls.
*   2024-11-03, 2:30 PM (Service Desk Tier 1 Follow-up): @Dr. Alistair Reed: The Data Science team recommends checking the shared drive permissions on the main `//MERIDIAN_Shared\APEX_Run` folder. It might be a simple Read/Write access issue for your user profile credentials.

**Resolution:** Awaiting further diagnostic information from Departmental Lead.
**Time to resolution:** 3 hours, 55 minutes · **SLA:** Met (Hold)

---
### TICKET #984290 :: RESOLVED
**Opened:** 2024-11-05, 08:50 AM · **Priority:** P4 · **Category:** Facilities/Office Supplies
**Reported by:** Kevin Zhou, Project Management Office (PMO) · **Assigned to:** Marcus Bellweather

**Description:**
The communal printer in the breakroom needs a new toner cartridge. It says ‘Toner Low’ and I cannot access any documents that were printed this morning regarding the mandatory safety review meeting schedule for next week. Please send someone with Model XYZ-700 black toner. Don't use the cheap stuff from Vendor B.

**Activity log:**
*   2024-11-05, 09:10 AM (Marcus Bellweather): Understood. We are scheduling a supply run for this afternoon between 1:30 PM and 2:00 PM.
*   2024-11-05, 1:58 PM (Facilities Team Dispatch): Toner Model XYZ-700 has been placed in the breakroom copier. Please ensure all print jobs are queued correctly on the main terminal screen before use.
*   2024-11-05, 2:15 PM (Kevin Zhou): This is fine, but can someone also check if the scanner bed needs cleaning? It seems to be picking up lint from my trouser pockets again.

**Resolution:** Physical printer consumables replenished as requested.
**Time to resolution:** 3 hours, 25 minutes · **SLA:** Met

---
### TICKET #984101 :: RESOLVED
**Opened:** 2024-11-07, 10:05 AM · **Priority:** P2 · **Category:** Accounts/Billing
**Reported by:** Sarah Miller, Finance Liaison · **Assigned to:** Brenda Klein

**Description:**
I am submitting an expense report (Form F-3B, Q4) for client dinners. Three of the receipts are from "The Green Leaf Cafe" in downtown Sector 4, dated November 1st through 3rd. The system is rejecting them all with a code indicating 'Lack of Primary Departmental Authorization Code.' Can you advise which cost center I need to list these against? John told me it should be 700-BETA, but the dropdown menu doesn't have it.

**Activity log:**
*   2024-11-07, 10:30 AM (Brenda Klein): Sarah, please ensure you have attached a manager’s email pre-approving the expense category change. Just uploading the receipts isn't sufficient for offsite meals under the new compliance guidelines.
*   2024-11-07, 11:15 AM (Sarah Miller): I *did* get that from Mark this morning. It was in an email titled "Expense Approval Reminder." Maybe you missed it?
*   2024-11-07, 1:30 PM (Brenda Klein - Escalation to Compliance): @Sarah Miller: We recommend verifying the attached email header data. Please resubmit the pre-approval confirmation explicitly citing department cost center 'R&D Annex Support' (Code 819) for consistency.

**Resolution:** Expense report resent by user with correct secondary authorization code applied.
**Time to resolution:** 3 hours, 25 minutes · **SLA:** Met

---
### TICKET #984007 :: RESOLVED
**Opened:** 2024-11-10, 02:10 PM · **Priority:** P3 · **Category:** Communication/Internal Memo
**Reported by:** David Chen, Corporate Communications · **Assigned to:** Marcus Bellweather

**Description:**
The internal newsletter template (Version 5.1) is not pulling the required formatting for embedded shareholder charts when I try to populate it in Word. Specifically, the placeholder bracket `[[SHARE_CHART]]` appears as literal text rather than being parsed into an editable graphic box. Can you advise if this requires a specific macro key or if someone needs to update our SharePoint library asset?

**Activity log:**
*   2024-11-10, 2:35 PM (Marcus Bellweather): David, please ensure you are opening the template from the dedicated 'Comms Masters' folder on the shared drive. Do not use any cached versions from local desktop links.
*   2024-11-10, 3:10 PM (David Chen): Confirmed accessing from the master path and re-downloading locally; the issue persists. It still reads literally.
*   2024-11-10, 3:45 PM (Comms Dept Manager Override): @David Chen: This is known behavior for V5.1 when compiling cross-departmental data sets. Please revert to the static image placeholder format and manually insert PNG files instead of using the bracketed macro function until V6.0 deployment next quarter.

**Resolution:** User advised on temporary workaround procedure involving manual asset insertion.
**Time to resolution:** 3 hours, 35 minutes · **SLA:** Met

---
### TICKET #983912 :: RESOLVED
**Opened:** 2024-11-14, 09:55 AM · **Priority:** P2 · **Category:** Network/VPN Access
**Reported by:** Janice Krell, Quality Assurance · **Assigned to:** Priya Sharma

**Description:**
I cannot connect to the MERIDIAN VPN endpoint from my home office IP address (currently showing as 173.45.XX.XXX). I have successfully connected before using this specific router/ISP combination over the last six months. The connection times out immediately after entering credentials, citing "Authentication Failure: Invalid Token Sequence." Has the primary auth key for residential logins been updated?

**Activity log:**
*   2024-11-14, 10:15 AM (Priya Sharma): Janice, please confirm that you have logged out of all other services first. Sometimes background processes hold onto authentication tokens and interfere with the new connection attempt.
*   2024-11-14, 11:00 AM (Janice Krell): Done logging out everywhere else. Nothing changes on my end. I still get the same timeout error when running the VPN client pointing to `vpn.meridiancorp.net`.
*   2024-11-14, 11:30 AM (Network Security Team Flagged): @Janice Krell: Our records show your home IP address range was flagged for unusual sustained bandwidth usage last night (between 11 PM and 3 AM EST). We have forced a temporary block on that subnet until you can physically verify local network stability.

**Resolution:** User required to obtain a new, non-flagged home broadband connection or use the campus Guest Wi-Fi access point while in office.
**Time to resolution:** 1 hour, 35 minutes · **SLA:** Met

---
General Average Ticket Resolution Time: 2 hours, 47 minutes.