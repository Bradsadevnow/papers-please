# Company Canon Specification (v1)

This is the reusable shape referenced in `HANDOFF.md` and `README.md` as "the
agent shape" — eight small canon objects that get defined once per company,
by hand, before any simulation or document generation happens. None of these
are corpus documents. None of them are player-facing. They are the fixed
ground truth that `COMPANY_SIMULATION_PIPELINE.md`'s event-simulation engine
reads on every single generation pass, so that inventing new events never
means quietly reinventing the business.

**Why this exists, concretely:** every object below closes a real drift
risk observed in this project already. Name drift (`Dr. Eleanor Vance` /
`Dr. Elara Vance` / `Dr. Evelyn Reed`, flagged in the old MERIDIAN corpus)
is the shape of what happens when a canon fact isn't pinned down and every
generation pass is free to reinvent it. `Economic Primitive` and `Governing
Fiction` exist because the same failure mode applies to the business model
and the legal framing, not just to names — and those are much more
expensive to get wrong, because the seams live in them.

GriefForge is not speculative here — its canon below is reverse-engineered
from the real, already-built 8-document archive (`corpus/griefforge/`),
verified against that archive's actual text. SubLaborix, OxyVitae, and
Somnify are drafts, built from the raw transcripts and flagship docs in
`companies/`, not yet run through the event-simulation pipeline. **Nothing
below has been used to generate a single corpus document for those three.**
This is the spec to review before that starts.

---

## The eight objects

### 1. Founding Thesis
One paragraph. What fundamental thing did the founders decide should become
a market? Answers "why does this company exist" at the level a VC pitch
would open with — this is allowed to be somewhat grand, since it's canon,
not corpus.

### 2. Product Doctrine
One or two sentences. The ideological kernel — what the company genuinely
believes about the human primitive it monetizes. Everything else the
company says inherits from this. Not corpus voice; closer to a mission
statement nobody's supposed to say out loud.

### 3. Economic Primitive
Four lines, not a document:
- `economic_primitive` — what exactly gets metered, sold, and recognized as
  value.
- `unit_of_value` — the literal billable unit.
- `billing_boundary` — the exact event that starts or stops billing.
- `recognized_success` — what the company's own internal reporting counts
  as "it worked," which is deliberately allowed to diverge from what an
  outside person would call success.

This is the one that prevents an event-simulation pass from inventing a
new monetization mechanic on the fly. It's also where the funniest seams
come from without anyone writing a joke — Finance has to answer "when does
[X] become revenue," and the honest answer is never the same as the
marketing answer.

### 4. Governing Fiction
One sentence, structured as *actual thing → institutional classification*.
What the institution insists this activity legally/administratively **is**.
Every department inherits this euphemism and uses it faithfully; the
comedy is watching the euphemism keep getting used after reality stops
fitting it (this is exactly what K-901 turned out to be a symptom of, not
the root).

### 5. Central Contradiction
One sentence. The structural tension the company cannot resolve without
ceasing to be itself — usually a direct clash between what the product
claims to deliver and what the revenue model actually requires.

### 6. Dependency Architecture
A short list across whichever axes actually apply: technical, biological,
institutional, social, legal, data, identity, switching trauma. Not moat
analysis (why competitors can't enter) — this is why *customers* can't
leave, along which specific mechanisms.

### 7. Bounded Personas
Per `COMPANY_SIMULATION_PIPELINE.md`'s template: name, title, department,
what they know directly, what they suspect, what they can't admit even to
themselves, what they want from a given conversation. 6-9 people is enough
— GriefForge used 9 (including one powerless-but-correct persona and one
"Concerned employee" archetype in every roster on purpose).

### 8. Lifecycle Model
A short sequence of customer stages, each one a natural trigger for a
future simulated event. Not corpus, not prose — a schedule.

---

## Worked example: GriefForge (proven)

**Founding Thesis:** Traditional grief support is linear and aims for
recovery, which means customers eventually stop needing it. If unresolved
feelings could instead be tracked, staged, and treated as a tradable
condition, the same $1T market becomes recurring instead of one-time.

**Product Doctrine:** Bereavement is an unmanaged continuity event.

**Economic Primitive:**
- `economic_primitive`: unresolved bereavement engagement — the thing that
  generates revenue is *not* closure, it's continued unresolved status.
- `unit_of_value`: subscriber-month in an active, non-closed Resolution
  Cycle.
- `billing_boundary`: originally the user's own Successful Emotional
  Closure (SEC) declaration (docs 001–003); Phased Resolution didn't
  change the boundary's nature, it relocated it further out (Stage 3
  completion + 45-day minimum).
- `recognized_success`: Resolution Progress Score (platform-stage
  completion) — explicitly, per doc 006's own JARDOS note, *not*
  comparable to Clinical Resolution Status. The company's own internal
  documentation states you can't do the math that would tell you if
  people are actually getting better.

**Governing Fiction:** Actual thing: a subscription that must not let the
customer feel finished. Institutional classification: Closure as a
Service — a structured, staged administrative program toward a defined
outcome milestone.

**Central Contradiction:** If the service works, the customer no longer
needs the service.

**Dependency Architecture:** Institutional (Enterprise HR SLAs tie
employee "Return to Productivity" status to continued platform
engagement, per doc 001 §6) · Legal (K-901's four-term split exists
specifically so no single document has to say the quiet part) ·
Financial (the Q3 reconciliation shows a $14.5M hole the moment people
actually recover — the company is structurally incentivized against its
own stated outcome).

**Bounded Personas:** Founder/CEO, Finance lead (Marcus Thorne), Clinical
lead (Dr. Beatrice Hayes — correct, overruled, on record), Product lead
(Alex Chen — owns SEC→RPS metric swap), Sales lead, Customer Success
lead, Legal counsel (Olivia Klein — gets closest to saying it plainly),
Marketing lead, Concerned employee.

**Lifecycle Model:** Grieving Signup → Actively Engaged (unresolved) →
Declared Closure (high churn risk, the event the whole Q3 archive is
about) → Phased Resolution Subject → Legacy Archiving Upsell (post-
resolution retention play, doc 001 §9's mitigation for the churn risk).

---

## Draft canon (not yet built — for review before generation starts)

### SubLaborix Universal

**Founding Thesis:** Enterprise labor should be a pluggable API, not
headcount — gig platforms solved asset ownership, not enterprise-scale
booking friction.

**Product Doctrine:** Employment is an inefficient bundling mechanism for
discrete effort units.

**Economic Primitive:**
- `economic_primitive`: allocatable human effort, metered as fractional
  hours routed through an AI matching engine.
- `unit_of_value`: a flat monthly enterprise subscription for a pool of
  fractional Node-hours.
- `billing_boundary`: subscription price is fixed regardless of actual
  hours consumed — this is the exact contradiction Engineer Doomer names
  in the raw transcript (fixed price, variable demand, margin collapses
  the moment a client actually uses their subscribed hours).
- `recognized_success`: enterprise seat retention / contract renewal, not
  worker outcome, not task quality.

**Governing Fiction:** Actual thing: dynamically controlled labor.
Institutional classification: a decentralized Cognitive Mesh of
Autonomous Neural Nodes, present only during active task execution.

**Central Contradiction:** The subscription promises guaranteed labor
availability at a fixed price — which requires exerting real operational
control over workers — while the entire legal defense against employment
classification depends on those same workers having genuine, uncontrolled
autonomy. Both cannot be true at once.

**Dependency Architecture:** Legal (reclassification strips standard labor
protections) · Technical (blockchain-verified performance creates an
inescapable, subpoena-able audit trail) · Institutional (preemptive
lobbying for a "Digital Workers Act" that defines the classification into
existence) · Social (algorithmic node fragmentation breaks worker
coordination automatically once solidarity in a cluster exceeds a
measured threshold).

**Bounded Personas:** Founder/CEO, Finance/Tax lead, Legal/Classification
counsel, Worker Operations lead (owns the matching/throttling engine), a
Node (an actual worker, throttled mid-task), Enterprise Client Success,
Workforce Experience Lead (ironic title — no HR exists because there are
no employees).

**Lifecycle Model:** Curious Enterprise Client → Pilot Subscriber →
Workflow-Integrated Account → Sole-Source Labor Dependency → Renewal
Lock-In (36-month terms via the loyalty-oracle rebate mechanism).

---

### OxyVitae Global

**Founding Thesis:** Urban air quality is measurably degrading; a premium,
purified air product can be sold to executives as a productivity input,
not a luxury.

**Product Doctrine:** Air is not ambient. Air is a calibratable
performance input.

**Economic Primitive:**
- `economic_primitive`: differentiated respiratory access, tiered by
  purity blend.
- `unit_of_value`: a desk-pod subscription, billed monthly per desk.
- `billing_boundary`: billing triggers on pod access/provisioning, not on
  any measured outcome — there is no measured cognitive benefit to bill
  against. Engineer Doomer's audit is explicit: healthy humans already
  run ~98% blood-oxygen saturation on ambient air, so the entire
  performance claim is neurologically null for the target customer.
- `recognized_success`: desk retention and tier upgrades (Standard →
  Executive Alpha → C-Suite Monopoly), not any clinical or cognitive
  measurement.

**Governing Fiction:** Actual thing: paywalling a biological reflex.
Institutional classification: an Artisanal Respiratory Supplement,
exempt from atmospheric-commons framing.

**Central Contradiction:** The product's value proposition requires
ambient air staying bad — but OxyVitae's own HVAC-partnership strategy
(low-flow airflow restrictors installed via commercial landlord deals)
actively makes ambient air worse to drive adoption. The company doesn't
just benefit from the problem, it manufactures it, and the same
documentation trail that proves the product ("Corporate HVAC Integration
Loophole") also proves the crime.

**Dependency Architecture:** Claimed-but-unverifiable biological (the
"withdrawal" narrative is real to customers, disproven by Doomer's own
audit — worth treating as an exploitable gap, not a solid lock-in) ·
Physical infrastructure (pneumatic wall lines built into commercial
leases) · Institutional (building-code compliance used as the delivery
mechanism for the restrictors) · Legal (Exhale Liability Waiver claims
ownership of a customer's own exhaled CO2).

**Bounded Personas:** Founder/CEO, VP Facilities Partnerships (the
restrictor deal-maker, knows exactly what the devices do), Pod
Engineering lead, a contracted physician/health-claims consultant
(uncomfortable, limited power — the Dr. Hayes role for this company),
Enterprise Sales, a Standard-tier customer persona (junior analyst,
genuine withdrawal-shaped symptoms), Legal/Regulatory Affairs.

**Lifecycle Model:** Curious Breather → Performance User → Daily
Optimizer → Atmospheric Dependent → Enterprise Respiratory Node.

---

### Somnify Neural

**Founding Thesis:** A third of human life is spent unconscious; in an
always-on AI economy, that idle neural time is uncaptured capital.

**Product Doctrine:** Sleep is not downtime. Sleep is latent productive
capacity awaiting orchestration.

**Economic Primitive:**
- `economic_primitive`: idle human neural/attentional capacity during
  unconsciousness, harvested simultaneously as background compute and
  captive ad inventory.
- `unit_of_value`: the pod-hour, monetized three ways at once — B2C
  subscription, B2B compute-marketplace sale (idle brain GPU hours), and
  REM ad-injection revenue.
- `billing_boundary`: subscription billing is independent of sleep-
  quality outcome; compute and ad revenue accrue per pod-hour of
  unconscious use regardless of consent quality (the user is, by design,
  unable to object in real time).
- `recognized_success`: hardware amortization + compute yield + ad yield
  clearing a per-pod margin target — explicitly not the absence of
  hallucination or sleep paralysis, which the company's own risk
  mitigation treats as a monetizable byproduct (SomniDream NFTs), not a
  defect to fix.

**Governing Fiction:** Actual thing: unconsented advertising delivered
during unconsciousness. Institutional classification: Biological
Cognitive Calibration — a term specifically built to sit outside FTC
disclosure and skip-button rules.

**Central Contradiction:** The product claims to compress and optimize
sleep for the user's benefit, while its actual revenue model requires
maximizing background compute and ad throughput *during* the same sleep
window — the two goals compete for one finite resource, and the
company's answer to that competition failing (hallucinations, sleep
paralysis) is to sell the failure back to the user as a premium tier
rather than resolve it.

**Dependency Architecture:** Biological (unlike OxyVitae, this one is
real — measured neural latency effects, not placebo) · Data/identity
(the REM Data & Involuntary Synthesis Agreement assigns the company
ownership of anything a user's mind produces in the pod, including
business ideas) · Legal (Biological Cognitive Calibration classification)
· Technical/financial (hardware amortized over 36 months — a real sunk
cost on the customer's side too).

**Bounded Personas:** Founder/CEO, Clinical/Neuroscience Safety lead
(aware of the hallucination risk, limited power — this company's Dr.
Hayes), B2B Compute Sales lead, Ad Sales/Sponsor Relations lead, Data/IP
counsel (drafted the REM Data Agreement), a subscriber persona with early
hallucination symptoms, Product lead (owns the SomniDream pivot).

**Lifecycle Model:** Curious Optimizer → Compressed-Sleep Subscriber →
Compute-Contributing Node → Ad-Exposed Dreamer → Hallucination-Monetized
Premium Dreamer (the NFT tier).

---

## What's next

1. Review/redline the three draft canons above — nothing downstream should
   start until these are locked the way GriefForge's already is.
2. Build the event-simulation pipeline for real, generalized off
   GriefForge's proven pattern (persona → event → lossy departmental
   passes → frozen corpus), parameterized by these eight objects instead
   of hardcoded to one company.
3. Use each company's Lifecycle Model as the event queue — each stage
   transition is a candidate simulated event.
4. Only after a company has a real frozen archive: declare seams, seed
   `doctrine.py`, wire `voice.py`.
