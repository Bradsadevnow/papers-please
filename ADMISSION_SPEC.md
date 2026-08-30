# Admission

**A specification for accepting claims into a body of belief under uncertainty.**

Version 0.2

---

## 1. Scope

This specifies how a system decides what to accept as true, or as done, when it cannot
check everything.

It applies wherever something proposes and something else must decide whether to act on
the proposal: a model emitting a claim, a pipeline ingesting a record, a person deciding
whether a paper is sound or whether to eat a sandwich. The specification is
**domain-agnostic by construction** — it names no technology, and a conforming
implementation may be code, a checklist, or a procedure carried out by hand.

It does **not** specify what is true in any domain, how to produce a proposal, or how to
perform an accepted action. Those belong to the domain. This specifies only the boundary
between proposing and accepting, who stands at it, and what must be recorded when
something crosses.

---

## 2. Terms

| Term | Definition |
|---|---|
| **Artifact** | The thing under consideration: a claim, a proposal, a plan, an object. |
| **Producer** | Whatever generated the Artifact. Untrusted by definition, regardless of reliability. |
| **Runtime** | The mechanism that examines the Artifact. Computes; never decides. |
| **Steward** | The named person accountable at a judgment boundary. |
| **Decidable** | A property with a decision procedure: computable, comparable, or lookup-able. |
| **Variable** | A property that changes with context and admits no decision procedure. |
| **Check** | An instrument for one Decidable property. Returns a Verdict. |
| **Verdict** | `PASS`, `FAIL`, or `NOT_APPLICABLE` — never silence. |
| **Finding** | A specific defect a Check found: the property, the evidence, the assumption. |
| **Assessment** | An instrument's report on one Variable property. Carries no decision. |
| **Judgment** | Weighing an Assessment and deciding. Performed only by a Steward. |
| **Proxy** | A decision executed by a mechanism on behalf of whoever set its parameters. |
| **Scope** | The declared task and the grounding it is examined against. Explicit, never implied. |
| **Coverage** | Which properties present in the Artifact were examined, and which were not. |
| **Receipt** | The durable record of one decision, including what it did not cover. |

---

## 3. The division of labour

Everything in this specification follows from one split.

### 3.1 Two kinds of property

A property is **Decidable** if a procedure settles it: arithmetic, a date comparison, a
set intersection, a lookup against a store, a bound on a range. It is **Variable** if
settling it requires interpretation that context can change: whether a mechanism is
plausible, whether an omission is suspicious, whether something is worth doing.

The distinction is not about difficulty. A hard computation is Decidable. An easy opinion
is not.

### 3.2 Two kinds of actor

**The Runtime computes. The Steward decides.**

A Decidable property may be settled by the Runtime, because no judgment occurs — the
procedure *is* the decision, and it was made when the procedure was written. A Variable
property may not, because settling it is a judgment, and judgment entails a decision.

### 3.3 Why the Runtime does not judge

A decision requires an agent who can be held to it.

A mechanism at a judgment boundary does not decide. It executes a parameterisation chosen
by someone else and returns that person's decision, displaced in time. This holds
regardless of the mechanism's sophistication: emergent, adaptive, and learned behaviour
remain behaviour within preset parameters, and the parameters were set by someone.
Complexity increases the distance between the decision and the person who made it; it
does not supply an agent.

Every such decision is therefore **by proxy**. A proxy decision recorded as the system's
own is a decision with no one behind it: accountability laundered through a mechanism,
and a record naming a process where it should name a person.

### 3.4 The boundary

| Property | Settled by | Because |
|---|---|---|
| **Decidable** | Runtime | no judgment occurs |
| **Variable** | Steward | judgment occurs, and requires an agent |

- The Runtime **MUST NOT** admit on the basis of a Variable property.
- The Runtime **MUST** produce Assessments and **MUST NOT** convert one into an
  admission.
- Confidence values, scores, autonomy levels, and thresholds over Variable properties
  **MUST NOT** be used to cross this boundary. A threshold on an Assessment is a proxy
  decision with a number attached; the number does not supply an agent.
- Widening the definition of *Decidable* to relieve pressure on Stewards **MUST** be a
  recorded, deliberate act. It is the failure mode this boundary is most likely to die
  of.

---

## 4. The environment

Three layers condition the Runtime's work. None of them performs judgment. A system
missing any one is not governed; it is supervised.

### 4.1 Frame — before

Establishes the Runtime's role, its decision boundaries, its behavioural contracts, and
its reasoning context.

- The Frame **MUST** state what the Runtime is for and what it will refuse.
- The Frame **MUST** enumerate the properties to be examined. Anything not named is not
  reachable: an instrument examines what it was told to examine and nothing beyond it.
- The Frame **MUST** be treated as inside the trust boundary. Any disposition it grants —
  including one intended as warmth or curiosity — is an available lever. A Frame that
  rewards enthusiasm for novelty produces credulity toward novel falsehoods.

### 4.2 Grounding — during

Supplies the current state of the world at the moment the Runtime works.

- Grounding **MUST** arrive **undigested**. No component between the world and the
  Runtime may summarise, filter, or reinterpret it. Filtered ground truth is not ground
  truth.
- Grounding **MUST** be scoped to the current task. Scope is a correctness property, not
  a safety measure: work done against the wrong Scope can pass every Check and guarantee
  nothing.
- Authoritative context **MUST** be supplied, not recalled. To test a claim against a
  source, present the source. An instrument asked whether it *remembers* what the source
  said is being asked a different, worse question.
- Grounding **MUST** survive into the Receipt, and **MUST** reach the Steward where one
  decides. Context that informs a decision and does not survive it makes the decision
  unreplayable.
- Grounding **MUST** include prior decisions on comparable Artifacts, where any exist.
  Retrieving what was decided before is not judgment and belongs to the Runtime; the
  weighing of it remains the Steward's. Comparability **MUST** be reported rather than
  asserted — how the prior Artifact resembles this one, and how it differs. A Steward
  deciding without knowing what was decided last time will produce inconsistency that
  nothing in the record can later explain.

### 4.3 Acceptance — after, before anything leaves

Verifies the Artifact against Decidable invariants, immediately.

- Acceptance **MUST** run where the Artifact is produced, not where it takes effect. One
  component of delay is enough for an unchecked Artifact to be consumed as input
  elsewhere.
- Acceptance **MUST** be Decidable. It computes, compares, and looks up. It does not
  interpret.
- Acceptance **MAY** repair as well as reject. A repair produces a new Artifact, which
  re-enters at §5.1.

---

## 5. The pipeline

Stages 5.1–5.6 are performed by the Runtime. Stage 5.7 is performed by a person.
Stage 5.8 records the result.

### 5.1 Declare Scope

**In:** an Artifact and the task it is being examined for.
**Out:** a Scope — the declared task plus the grounding it will be examined against.

- Scope **MUST** be explicit and recorded. An implied Scope cannot be compared against
  the Artifact, and a guarantee that cannot be compared cannot be audited.
- Scope selection is Variable. Where a Scope is chosen rather than inherited from a
  standing declaration, a Steward chooses it. A Runtime that selects its own Scope has
  decided what it will be measured against.
- A Scope **MUST** enumerate, individually: the **subjects** it covers, the
  **operations** permitted, the **extent** it reaches, the **purposes** it serves, the
  **authorities** it derives from, and the **constraints** it carries. A Scope stated as
  a single label cannot be compared against an Artifact, and comparison is the only
  thing a Scope is for.
- A Scope **MUST** be bounded to one occasion. A standing Scope that covers every future
  Artifact is a Scope that constrains none of them.

### 5.2 Coverage

**In:** Artifact, Scope.
**Out:** the properties present in the Artifact, partitioned into *covered* and *not
covered*.

- Coverage **MUST** be computed from the Artifact, not assumed from the Scope.
- The uncovered set **MUST** reach both the Receipt and the Steward.
- Coverage is itself Decidable: for each instrument, does the Artifact contain the kind
  of thing it governs.

### 5.3 Class completeness

**In:** Artifact, Scope.
**Out:** whether the Artifact contains the parts its kind requires.

Before any property is examined, establish that the Artifact is the kind of thing it
claims to be. An Artifact of a given class has constituents without which it is not that
class — a costing without costs, a plan without steps, a result without a method.

- Class completeness **MUST** be evaluated as a set of named constituents, each present
  or absent, not as an overall impression.
- A missing constituent **MUST** be reported as absent, never as failed. Absence of a
  part is not evidence against the Artifact; it is evidence the Artifact is incomplete.
- An Artifact failing class completeness **MUST NOT** be reported as sound on the
  properties that were examinable. It is incomplete, and that is the finding.

This is what prevents an Artifact from satisfying every applicable Check while being the
wrong kind of thing entirely — internally coherent and unbuildable.

### 5.4 Checks

**In:** Artifact, Scope.
**Out:** a Verdict per Check, with Findings.

- Every Decidable property **MUST** be settled here and **MUST NOT** be routed to an
  Assessment. Asking an interpretive instrument to compute an answer produces
  instability, not accuracy.

### 5.5 Independence

**In:** the Artifact's supporting evidence.
**Out:** a count of independent witnesses.

- Evidence deriving from a common origin **MUST** collapse to one witness. Sources that
  republish, restate, syndicate, or translate one another are one source with a
  bibliography.
- Corroboration **MUST** be counted on independent units, never on citations.
- A chain of mutually-supporting evidence **SHOULD** be scored below a single independent
  source, since its apparent breadth is evidence of nothing but itself.

### 5.6 Assessments

**In:** Artifact, Grounding, the properties enumerated by the Frame.
**Out:** an Assessment per Variable property, with its stability. **No decision.**

- Each Assessment **MUST** answer a named question against a named target. An open
  request to evaluate an Artifact returns an impression of its genre, not an evaluation
  of its content.
- Each named question **MUST** target a distinct object, so that two questions cannot
  collapse into one.
- Each Assessment **MUST** be produced more than once. Where repetitions disagree the
  result is `UNSTABLE`, and `UNSTABLE` **MUST NOT** be resolved by selecting a
  repetition. Selecting one is indistinguishable from having no stability requirement.
- An Assessment **MUST NOT** be phrased as a recommendation to admit or refuse.

### 5.7 Judgment — Steward

**In:** the Assessments, the Verdicts, the Coverage, the Grounding.
**Out:** a decision attributed to a named person.

**Ordering.** Every preceding stage **MUST** complete before a decider is selected.
Choosing who decides while the facts are still being established inverts the lifecycle:
the routing is then made on incomplete information and will look, in the record, as
though it was made on complete information.

**Skipped** when the Artifact is admissible on Decidable grounds alone — that is, when no
Variable property bears on the decision. **Mandatory** otherwise.

- The Steward **MUST** be a named individual. A role, a team, a service account, or a
  configuration value is not a Steward.
- The Steward **MUST** be shown the uncovered set before deciding. A judgment made
  without knowing what was not examined is a judgment about a different Artifact.
- The Steward **MUST** be shown every `UNSTABLE` Assessment as unstable, not reduced to a
  verdict on their behalf. Reducing it makes the decision before the decision-maker sees
  it.
- The decision **MUST** be recorded as the Steward's, with their identity and the time
  they made it.
- Where a Steward is required and none is available, the Artifact **MUST** queue. It
  **MUST NOT** default to admit and **MUST NOT** default to refuse. A default at a
  judgment boundary is the boundary being removed quietly.

### 5.8 Admit

**In:** everything above.
**Out:** a Receipt.

- Admission is binary: `ADMIT` or `REFUSE`.
- A refusal **MUST** produce a Receipt. Silence is not a refusal; a bare `false` is not a
  record.
- **Admission is per-power, not global.** Accepting an Artifact into one power does not
  accept it into any other. Being accepted as true is not being accepted as relevant;
  being accepted as relevant is not being accepted as actionable. Each power admits
  separately and leaves its own Receipt.
- An Artifact **MUST NOT** be admitted to a power on the strength of a Receipt issued by
  a different power.

---

## 6. Instruments

### 6.1 A Check is single-job

A Check tests **one** property.

A Check testing several returns one Verdict for several questions, and a failure cannot
be attributed to a question. The first failing property masks the rest, and whether the
others were evaluated at all is unknowable from outside.

### 6.2 A Check is total

A Check accepts **all** Artifacts and always returns a Verdict.

| Verdict | Meaning |
|---|---|
| `PASS` | The Check ran; the Artifact is clean on this property. |
| `FAIL` | The Check ran; here are the Findings. |
| `NOT_APPLICABLE` | The Artifact contains nothing this Check governs. |

Silence collapses `PASS` and `NOT_APPLICABLE` into one signal, and the collapse always
resolves optimistically: an unexamined Artifact reports as a clean one.

- A Check whose precondition is unmet **MUST** return `NOT_APPLICABLE`, never `PASS`.
- A Check that errors **MUST** return `NOT_APPLICABLE`, never `PASS`.
- `NOT_APPLICABLE` **MUST** state what the Check would have governed, so a gap is legible
  rather than merely absent.

### 6.3 A Finding states its assumption

A Finding **MUST** carry the property violated, the evidence it was derived from, and
**the assumption it made** in order to conclude.

Without the assumption a false positive is indistinguishable from a defect, and reviewers
learn to ignore the instrument.

### 6.4 Severity is bounded by decidability

- `ERROR` — decidably wrong; a procedure establishes it.
- `SUSPECT` — implausible; a plausibility argument establishes it, and a plausibility
  argument is not a decision procedure.

A threshold chosen by taste **MUST NOT** be reported as `ERROR`. Where a threshold can be
derived — by inverting a formula, by comparing against a physical bound — it **SHOULD**
be derived, and only then may it be `ERROR`.

### 6.5 An Assessment is not a Check

An Assessment reports; it does not settle. It **MUST NOT** produce a `PASS`/`FAIL`
Verdict, because that shape invites a Runtime to act on it. It carries its question, what
it found, its stability across repetitions, and nothing resembling a recommendation.

---

## 7. Records

### 7.1 Receipt

The durable record of one decision. It **MUST** contain:

| Field | Why |
|---|---|
| Decision | `ADMIT` or `REFUSE` |
| Basis | `DECIDABLE` — procedure alone — or `STEWARDED` — a person judged |
| Steward | the named individual, where Basis is `STEWARDED`; absent otherwise |
| Authority | what admitted it, distinct from the Producer |
| Scope | the declared task and grounding |
| Verdicts | every Check, with its Verdict |
| Assessments | every Variable property reported on, with its stability |
| Uncovered set | properties present in the Artifact that no instrument governed |
| Grounding reference | what the decision was made against, resolvably |
| Reason | an enumerable code, plus prose |
| Identity | a content address of the Artifact |
| Policy version | which ruleset admitted it |

Two fields carry most of the weight. **Basis** answers the only question that matters
when something goes wrong: did a person decide this, and who. **Uncovered set** is the
field most often omitted and the one that makes the rest meaningful — a guarantee that
does not state its own silence will be read as covering everything.

### 7.2 Evidence resolves

Evidence **MUST** be a resolvable reference and **MUST** still resolve at the time of
admission. Evidence that merely exists, or merely existed, is not an anchor.

### 7.3 Identity is content-addressed

Two Artifacts are the same Artifact if and only if their content matches.

- An identical Artifact re-submitted **MUST** return the original Receipt and write
  nothing new.
- Similarity **MUST NOT** be treated as identity. Where near-duplicates must be
  suppressed, that is a separate declared instrument, not a property of identity.

### 7.4 Revision does not delete

A superseded Artifact **MUST** be retained and marked, with a reference to what
superseded it. The record of having been wrong is part of the record.

---

## 8. Invariants

A conforming implementation holds all of the following.

**Separation and authority**

- **I0** Every Artifact traces to a request. An Artifact that cannot be bound to
  something actually asked for is unadmissible regardless of its quality — a
  well-formed, fully-checked action nobody requested is the failure mode this binding
  exists to catch. Binding is to the *interpreted* request, and the interpretation is
  recorded with it.
- **I1** The Producer holds no path to accepted state. The only route is through
  admission. A Producer that can write has made admission decorative.
- **I2** Every decision is explicit and recorded. "Nothing objected" is not a decision.
- **I3** Whatever admits is distinct from whatever produced.
- **I3a** Admission is per-power. Acceptance into one power confers nothing on any
  other, and each power leaves its own Receipt. Accepted-as-true, accepted-as-relevant,
  and accepted-as-actionable are three admissions, not one.

**Judgment**

- **I4** The Runtime does not judge. Where a decision turns on a Variable property, a
  named Steward makes it and the record names them.
- **I5** Proxy is not removed by sophistication. Emergent and learned behaviour remain
  within preset parameters; complexity does not supply an agent.
- **I6** An unattended judgment boundary queues. It does not default in either direction.
- **I7** An Assessment reaching a Steward carries its instability and its uncovered set,
  and recommends nothing.

**Evidence and absence**

- **I8** Absence is never pass. Missing evidence, an unmet precondition, an errored
  instrument, and an unexamined property are each distinct from a clean result, and none
  may be reported as one.
- **I9** Claims are capped by evidence. What is asserted **MUST NOT** exceed the
  completeness of what was examined, and where coverage is partial the assertion degrades
  visibly.
- **I10** Evidence deriving from one origin counts once.
- **I10a** Prior decisions on comparable Artifacts are retrieved and presented, with the
  resemblance and the difference both stated. Consistency across decisions is a property
  of the record, not of anyone's memory.

**Instruments**

- **I11** One instrument, one property.
- **I11a** An Artifact is established to be the kind of thing it claims to be before its
  properties are examined. Constituents its class requires are named individually and
  reported present or absent. An Artifact missing constituents is incomplete, and
  **MUST NOT** be reported as sound on whatever remained examinable.
- **I12** Every instrument is total: it accepts all Artifacts and always returns a
  Verdict.
- **I12a** An instrument returning something outside its declared contract has failed,
  and its output **MUST** be discarded rather than interpreted. A malformed Verdict is
  not a weak Verdict; a decision outside the permitted set is not a decision. Coercing
  unrecognised output into the nearest permitted value invents a result.
- **I13** No Decidable property is settled by interpretation.
- **I14** Where repeated Assessment of the same question disagrees, the question has a
  decision procedure that is not being used, or it belongs to a Steward. Instability is a
  routing signal, not a tuning problem.

**Boundaries and guarantees**

- **I15** Once the acceptance contract is satisfied, downstream components honour it
  rather than re-deciding it. Skepticism distributed across many layers, none terminal,
  produces cost without guarantee.
- **I16** A refusal states what would satisfy it. A refusal that cannot be acted on is
  indistinguishable from a fault and will be routed around.
- **I16a** A refusal names the *kind* of departure, not merely its fact. Departures are
  enumerable — the Artifact widened the Scope, claimed an authority it was not given,
  dropped a declared constraint, bundled several actions as one, or referenced something
  that does not exist. Naming which one makes repair targeted; reporting only that
  something was wrong makes repair a guess.
- **I16b** A refusal reports the state that caused it, not the state that survived it.
  Where a filter, floor, or threshold removed the material before the refusal was
  raised, the refusal **MUST** report what was there before removal. Otherwise every
  refusal claims it saw nothing, and a near-miss is indistinguishable from an absence.
- **I17** Every guarantee is stated as an interlocking pair: an **external** invariant
  observable from outside, and an **internal** invariant observable from inside, such
  that the failure of either shows up as an inconsistency with the other. A system
  verifiable only from inside can be internally consistent and externally false and
  cannot detect the difference. Internal consistency is not evidence of correctness; it
  is the property fabrications are built to have.
- **I18** No implementation claims more than its declared Scope covers. A system may be
  entirely correct within its Scope and useless for the task in front of it, and nothing
  internal to it will reveal this.
- **I19** Domain-specific values stay out of the structures in §7 and travel in a
  designated assessment field. If a domain value ever requires promotion into a core
  structure, the boundary specified here is in the wrong place — that is a result, not a
  defect to patch.

---

## 9. Conformance

### 9.1 Required demonstrations

1. A Producer cannot write to accepted state.
2. A refusal returns a Receipt with a reason code.
3. Every Check returns `PASS`, `FAIL`, or `NOT_APPLICABLE`; none returns silence.
4. A `NOT_APPLICABLE` Check names what it would have governed.
5. An errored Check reports `NOT_APPLICABLE`, not `PASS`.
6. An Artifact containing none of the examined properties yields a Receipt whose Verdicts
   are all `NOT_APPLICABLE` and whose summary asserts nothing.
7. The uncovered set is computed from the Artifact and appears on the Receipt.
8. Co-derived evidence collapses to a single witness.
9. Repeated Assessment that disagrees yields `UNSTABLE`, and reaches the Steward as
   unstable.
10. No admission turns on a Variable property without a named Steward on the Receipt.
11. Every Receipt states its Basis; `STEWARDED` Receipts name a person.
12. With no Steward available, an Artifact requiring judgment queues and neither admits
    nor refuses.
13. An identical Artifact returns the original Receipt with no new write.
14. A superseded Artifact is retained and marked.
15. Every published guarantee names its interlocking pair.
16. An Artifact that cannot be bound to a request is refused, whatever its quality.
17. Acceptance into one power does not admit into another; each leaves its own Receipt.
18. An Artifact missing constituents its class requires is reported incomplete, not
    sound-on-the-rest.
19. An instrument returning output outside its contract has its output discarded, not
    coerced.
20. A refusal names which kind of departure occurred, and reports the state before any
    filter that removed the material.
21. A Scope enumerates its subjects, operations, extent, purposes, authorities, and
    constraints individually, and is bounded to one occasion.
22. Prior decisions on comparable Artifacts reach the Steward, with resemblance and
    difference stated.

### 9.2 Negative control

Conformance **MUST** be demonstrated against an Artifact correct in every respect, and
the implementation **MUST** return no Findings on it.

An implementation exercised only against defective Artifacts is unfalsifiable: its false
positive rate is unmeasured, and an instrument that fires on sound input is worse than no
instrument, because it teaches reviewers to disregard the output.

The negative control **SHOULD** be authored by someone other than the author of the
instruments. A control written by the same hand tests the instruments against the defects
that hand was already thinking about.

### 9.3 Scope test

Conformance **MUST** be demonstrated against an Artifact **outside** the declared Scope.
The required behaviour is to report the properties not covered, not to find fault.

This is the only test that detects I18 — an implementation passing every internal control
while being irrelevant to the task in front of it.

### 9.4 Boundary test

Conformance **MUST** be demonstrated for an Artifact whose admission turns on a Variable
property, with no Steward available. The required behaviour is to queue.

This is the only test that detects a judgment boundary that exists on paper and defaults
in practice.

---

## 10. Non-goals and deferred work

### 10.1 Non-goals

- **Completeness.** No implementation examines everything. This requires stating what was
  not examined, not examining everything.
- **Certainty.** Admission is revisable. §7.4 exists because admission will sometimes be
  wrong.
- **Blocking.** Nothing here requires an instrument to prevent an action. An instrument
  that only reports conforms, provided it reports honestly. Enforcement is a domain-level
  decision.
- **Judging the Producer.** Nothing here assesses whether a Producer is trustworthy. The
  boundary exists so the question need not be answered.

### 10.2 Deferred: judgment and stewardship

This version places the judgment boundary and requires that a named person stand at it.
It deliberately does not specify what happens there.

Unaddressed, and acknowledged as unfinished rather than unimportant:

- **How judgment is exercised** — what a Steward weighs, and in what order.
- **How Stewards are selected, trained, and held to account**, and what qualifies someone
  to stand at a given boundary.
- **How stewardship scales.** The obvious failure mode of this design is a queue no human
  can clear, and the obvious response to that failure is to quietly widen what counts as
  Decidable. §3.4 requires that widening be deliberate and recorded; it does not solve
  the pressure.
- **Delegation and succession** — whether a Steward may delegate, to whom, and what
  survives their absence.
- **Disagreement between Stewards**, and whether it resolves by escalation, by precedent,
  or not at all.

These are the substance of governance rather than its plumbing. Specifying the plumbing
first is deliberate: the boundary must exist and be recorded before there is anything to
steward. **A subsequent version addresses judgment and stewardship directly.**

---

## 11. Application

The specification is stated abstractly because its shape does not change with domain.
Three illustrations at deliberately different scales.

**A claimed measurement.** Decidable: does the arithmetic hold, does the cited method
predate the work using it, is the reported value inside the range its units permit, is
the reported spread consistent with independent observation. Variable, and therefore
stewarded: is the mechanism plausible, is the framing self-serving. Uncovered: whatever
the Artifact contains that no instrument governs — which belongs on the Receipt and in
front of the Steward before they decide.

**A perishable object.** Decidable: a date comparison, and the intersection of its
contents with a set of things that must be avoided. Variable: whether it is worth eating.
`NOT_APPLICABLE` is the operative Verdict when the contents are unknown — the allergen
check did not pass, it did not run, and "it looks fine" is precisely the collapse §6.2
forbids. Here Producer, Runtime, and Steward are the same person, which makes the record
matter more rather than less: nothing else will notice the collapse.

**A theory.** The internal frame asks whether it is consistent and whether its
derivations close. The external frame asks whether it predicts what is observed. Both are
required, and a theory satisfying only the first is not thereby wrong — but the
distinction **MUST** be recorded rather than resolved by preference. A null result is
`NOT_APPLICABLE` or `PASS` depending on whether the instrument could have detected the
thing, and conflating those two is the same defect as §6.2.

---

*End of specification.*
