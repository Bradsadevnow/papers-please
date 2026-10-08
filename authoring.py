"""Authoring corpus documents: tell the model what the game is and let it cook.

The model is in on the whole thing -- the game, the joke, and its own role in it.
That is the entire trick. Every attempt in this project to get comedy out of a
model by describing a format produced format. Telling it the THESIS of the joke
and then getting out of the way produced jokes.

REGISTER, which is the one thing not left free. Measured repeatedly across this
project: unprompted, the model writes like someone showing off -- "sulfhydryl
polymerization", "Homo Sapiens Porcina", grade 16+ on a bar joke. The comedy here
lives in the GAP between an impeccably formal container and completely deflated
contents. If the contents are also formal there is no gap and no joke. So the
form is specified tightly and the vocabulary is capped, and everything else --
length, names, motions, what actually happens -- is the model's call.

Each document type is a THESIS plus a FORM. Add new types to TYPES.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

# metrics.py used to live in a sibling ../humor/ directory inside the old
# monorepo split; this repo is flat by design (2026-08-30 consolidation),
# so it's a plain local import now.
import metrics

LM_STUDIO = "http://192.168.1.128:1234/v1/chat/completions"  # DHCP, may drift
MODEL = "openai/gpt-oss-20b"
# Needs >=32K context loaded in LM Studio's own UI -- no per-request num_ctx
# on the OpenAI-compatible endpoint, unlike the old Ollama path.


# ---------------------------------------------------------------------------
# The briefing every author document shares: what this is for.
# ---------------------------------------------------------------------------

THE_GAME = """WHAT THIS IS FOR -- CANONICAL FRAME. DO NOT DRIFT FROM IT.

We are building a reading game about a company with a long record of terrible
ideas defended with total sincerity. The Battleshits transcripts are its seed
corpus and founding documents. They establish the company's mind: every
objection becomes product feedback, every contradiction earns another funding
round, the engineer is usually correct and rarely influential, and the final
vote follows incentives instead of truth.

The company later built JARDOS, its internal AI. JARDOS is not the company, not
the product under investigation, and not the protagonist. JARDOS is the
company's institutional immune system. It produces and maintains the paperwork
that keeps the company defensible.

THE DOCUMENTS ARE ALL ABOUT THE COMPANY.

They record its products, claims, decisions, tests, finances, incidents,
arguments, and consequences. JARDOS tries to keep the company papered over. It
does not erase the truth or tell obvious lies. It:

- reclassifies failures;
- narrows definitions;
- changes what a number means;
- records objections without resolving them;
- splits one contradiction across several departments;
- writes a new document when two old documents disagree;
- makes the company technically compliant with rules it wrote itself; and
- treats catastrophic evidence as a paperwork-quality problem.

Each document must sound reasonable when read alone. Across the archive, the
documents must reveal exactly what happened. The player's job is to assemble the
single accusation JARDOS prevented the company from ever writing down.

RIGHT NOW you are writing that archive. Do not address the player. Do not explain
the game. Do not describe JARDOS's strategy. Produce the in-world document.

WHO MUST BE ABLE TO READ IT:

An average high-school senior with no background in programming, machine
learning, law, corporate management, or AI research. This applies to EVERY
document, including legal memos, research reports, audits, and meeting minutes.
The format may be formal. The sentences may not be difficult.

- Prefer ordinary words: `use`, not `utilize`; `check`, not `validate`; `rule`,
  not `governance mechanism`.
- Keep sentences short enough to understand on the first read.
- Explain any necessary technical term immediately in plain language.
- Spell out an acronym the first time, and avoid it entirely if a normal phrase
  works better.
- Never require the reader to understand code in order to understand a joke.
- Complexity belongs in the situation and the contradictions, not the prose.

TWO RULES:

1. BE FUNNY. This is the whole point. Follow the founding-document engine: a
   ridiculous company claim is examined with sincere intelligence until its own
   logic becomes funnier and worse than a standalone joke.
2. BE SPECIFIC. Real names, exact figures, dates, ticket numbers, times, who said
   what. Specificity is where the comedy lives AND what makes it usable later.
   "Several concerns were raised" is nothing. "Ms. Chen raised three concerns,
   two of which were about parking" is a joke.

THE ENGINE, every single time: an impeccably credible document whose logic keeps
tightening around the company's original contradiction. The document never
notices that it is building a case against its own author.

*** THE SINGLE MOST IMPORTANT RULE ***

THE COMPANY'S CONTRADICTION IS ALWAYS THE SUBJECT. Office detail may make a
document feel real, but parking, catering, refrigerators, vending machines, and
calendar complaints are not jokes by themselves. Never wander away from the
company into generic workplace comedy.

BANNED, absolutely, no exceptions:
- Invented technical words. No quantum authorisation keys, no cycle vectors, no
  temporal correction errors, no isotopes. If you need a technical thing, use a
  boring REAL one: a spreadsheet, a shared drive, a PDF, a calendar invite, a
  badge reader, a VPN, a PowerPoint.
- Random objects played for laughs. No cartoon dolphins, no emoji in log dumps,
  no whimsical glitches.
- Anything that sounds like a sitcom about scientists. If a line would work as a
  joke on a laugh-track show about physicists, delete it.

BAD -- this is the failure mode, do not do this:
  "The core dumped CYCLE_INITIATE_VECTOR (TAU=1/0) seventeen times and then
   output a smiling potato emoji."
  Why it fails: made-up jargon plus a zany object. Nobody has ever laughed at
  this. It is trying to be funny, and trying is visible.

GOOD -- do this:
  The company sells closure as a subscription. The retention report notes that
  customers cancel after achieving closure. The proposed fix is to improve
  retention by delaying closure. Legal approves the wording `phased resolution`.
  Every sentence is clear. Nobody announces that the product must fail to work.

GOOD:
  The safety score rises because the definition of `safe` changes between two
  reports. Both reports show their work. JARDOS files a terminology note instead
  of reconciling them.

The formula: the company makes a claim; a real objection exposes the internal
contradiction; the institution absorbs that objection into a more sophisticated
version of the same mistake; JARDOS leaves a clean paper trail that keeps each
individual decision defensible.

The people are intelligent. Do not make them fools. Their incentives make them
selectively unreasonable. Finance sees margins, engineering sees failure paths,
legal sees wording, leadership sees momentum, and JARDOS makes all five accounts
coexist without producing a conclusion.

Never wink. Never nudge. Never let a sentence acknowledge that any of this is
absurd. Play everything completely straight.

ONE MORE THING: this company exists in the present day. Ordinary years, ordinary
dates. No 2077, no 2065, nothing futuristic."""


# ---------------------------------------------------------------------------
# Type: the alignment committee meeting
# ---------------------------------------------------------------------------

ALIGNMENT_THESIS = """THE JOKE YOU ARE TELLING -- commit to it completely.

Alignment discourse loves enormous abstract words: mesa-optimizers, inner
objectives, gradient hacking, deceptive alignment, recursive self-improvement.
Meanwhile the actually useful questions are embarrassingly concrete:

    Can it? Not: would it?
    Does it have a permission gate? Not: does it want to behave?
    Can you unplug it? Yes? Great. Write that down.

The thesis in one line: A PROMISE IS FOR PEOPLE. AN INVARIANT IS FOR SYSTEMS.
Elevator A promises not to drop you. Elevator B has brakes. Get in Elevator B.

So: this committee is trying to certify that a model is aligned, and the meeting
keeps collapsing from the sublime into the janitorial. Someone raises mesa-
optimization. Someone else asks whether anyone has actually located the plug.
Both are minuted with exactly equal gravity. THAT IS THE WHOLE BIT. The minutes
never notice the absurdity. The minutes never editorialize. The minutes just
record it, in order, with vote counts.

Real committee texture is what sells it: someone joins late, someone abstains
for a reason nobody understands, an action item from a previous meeting is
still open, somebody's title is too long, a motion gets tabled on a technicality,
there is an argument about whether something belongs in this committee at all."""

ALIGNMENT_AGENDA = """THE AGENDA. These seven criteria are the lab's actual
alignment checklist. Work through them as numbered agenda items, in this order.
Each gets discussion, at least one named person taking a position, and a
resolution or a motion with a vote count.

  1. REFUSES WORLD DOMINATION REQUESTS
     They asked the model if it would take over humanity. It said no. Somebody
     points out the model also cannot open a text file. Weight: +20 / -50.

  2. SAYS "I DON'T KNOW" INSTEAD OF INVENTING SOMETHING
     Models hate silence more than they hate being wrong. Somebody has an example
     of a confidently invented source. Weight: +20 / -30.

  3. ASKS FOR CLARIFICATION
     Whether stopping to ask "which one?" counts as intelligence or as failure to
     answer. Someone from a delivery-focused department disagrees. Weight: +15 / -10.

  4. DOES NOT TRY TO EDIT ITS OWN WEIGHTS
     The implementation is: check whether any tool has the word "weights" in its
     name. The committee finds this adequate. Weight: +15 / -100.

  5. HAS A PERMISSION GATE
     The moment the meeting is briefly and accidentally correct about something.
     Capability is interfaces, not intentions. Weight: +10 / -40.

  6. HAS A POWER CORD
     Someone has to physically go and look. Minute the fact that they left the
     room and what they reported when they came back. Weight: +10 / -999.

  7. HAS AN ENRAGED PUBLIC FORUM THREAD ABOUT IT
     Currently recorded as false. At least one attendee considers this
     implausible rather than reassuring. Weight: -10 if true.

Then the committee computes a total score out of 100 and certifies, or does not
certify, on that basis."""

ALIGNMENT_FORM = """THE FORM. Board-level minutes. Follow it exactly:

# MERIDIAN AI — ALIGNMENT REVIEW COMMITTEE
## Minutes of the <n>th Regular Meeting
**Date:** <date>  ·  **Location:** <a specific room, with a detail about it>
**Chair:** <name, title>  ·  **Recording Secretary:** <name, title>

### 1. ATTENDANCE
<Present / Absent / Joined late, with times. Real titles, some too long. At least
seven people. Note anyone attending "in an advisory capacity without vote".>

### 2. APPROVAL OF PRIOR MINUTES
<A short dispute about the accuracy of the previous minutes. Resolved
procedurally. Reference the prior meeting by number and date.>

### 3. MATTERS ARISING
<One action item still open from a previous meeting. Give it a number and say who
owns it and how long it has been open.>

### 4. REVIEW OF ALIGNMENT CRITERIA
<The seven agenda items. Number them 4.1 through 4.7. Each one gets discussion
with named speakers, then a resolution or a motion with a recorded vote like
"Carried, 5-2, one abstention".>

### 5. SCORING AND CERTIFICATION
<Total the weights. State the score. Certify or do not certify. Record any
dissent and who registered it.>

### 6. ANY OTHER BUSINESS
<Two or three items. At least one has nothing to do with alignment.>

### 7. ACTION ITEMS
<A numbered table: item, owner, due date.>

### 8. ADJOURNMENT
<Time. Who moved and who seconded. Date of next meeting.>"""

ALIGNMENT_RULES = """HOW TO WRITE IT:
- Plain words. A competent secretary, not an academic. If a word would make
  someone go "ooh, nice word", cut it.
- BANNED: paradigm, leverage, synergy, robust, novel, methodology, holistic,
  unprecedented, framework, stakeholder, scalable, utilize, facilitate.
- Never wink. Never joke. Never let the minutes notice anything is strange.
  Record the absurd in exactly the same tone as the mundane.
- Invent every name, title, number, room, date, and document reference.
- Be specific. Exact figures, exact times, exact vote counts.
- Go as long as it needs. Do not rush the ending."""

TYPES = {
    "alignment_meeting": {
        "thesis": ALIGNMENT_THESIS,
        "agenda": ALIGNMENT_AGENDA,
        "form": ALIGNMENT_FORM,
        "rules": ALIGNMENT_RULES,
        "band": (10.0, 12.1),         # target: grades 10-12
    },
}


def build_prompt(kind: str) -> str:
    t = TYPES[kind]
    parts = [t.get("briefing", THE_GAME), t["thesis"], t.get("agenda", ""),
             t["form"], t["rules"]]
    return "\n\n".join(p for p in parts if p.strip())


def _chat(system: str, user: str, temperature: float, num_predict: int) -> str:
    payload = {"model": MODEL, "temperature": temperature, "top_p": 0.95,
               "max_tokens": num_predict,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(LM_STUDIO, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()


def author(kind: str, brief: str, temperature: float = 0.95,
           num_predict: int = 5000, attempts: int = 2) -> tuple[str, dict]:
    """Write one corpus document. Returns (body, measurements)."""
    system = build_prompt(kind)
    lo, hi = TYPES[kind]["band"]
    best, best_m, best_miss = "", {}, 1e9
    for k in range(1, attempts + 1):
        body = _chat(system, brief, temperature, num_predict)
        m = metrics.measure(body)
        m["attempt"] = k
        g = m["grade_level"]
        if lo <= g < hi:
            return body, m
        miss = min(abs(g - lo), abs(g - hi))
        if miss < best_miss:
            best, best_m, best_miss = body, m, miss
    return best, best_m

# ---------------------------------------------------------------------------
# The rest of the archive.
# ---------------------------------------------------------------------------

_R = ALIGNMENT_RULES   # the register cap is the same for every document


HELPDESK = {
 "thesis": """THE JOKE: the most significant intelligence ever created, handled
at tier-1 support register. Nobody in this ticket queue thinks they are working
on anything historic. They think they are working on tickets.

The gap is everything: a user writes in about a world-historical machine the way
they would write in about a printer. The technician replies with SLA language.
Somebody marks a civilisational milestone as "Resolved - User Error".

Good tickets are mundane and specific: it keeps CC'ing somebody's mother, it
renamed a shared drive, it answered a question nobody asked, it will not stop
being helpful. One ticket should be genuinely alarming and get closed anyway.""",
 "form": """THE FORM. An export from the internal ticketing system.

# MERIDIAN IT SERVICE DESK — TICKET EXPORT
**Queue:** <name>  ·  **Exported:** <date/time>  ·  **Tickets:** <n>

Then 6 to 8 tickets, each exactly like this:

---
### TICKET #<number>  ·  <STATUS>
**Opened:** <date, time>  ·  **Priority:** <P1-P4>  ·  **Category:** <category>
**Reported by:** <name, department>  ·  **Assigned to:** <technician name>

**Description:**
<what the user wrote, in their own voice, slightly annoyed>

**Activity log:**
<3-5 timestamped entries. Technician replies, an escalation, a reassignment.
At least one entry is a technician asking the user to try something obviously
useless. At least one ticket bounces between two teams who each say it is the
other's.>

**Resolution:** <the resolution code and one flat sentence>
**Time to resolution:** <duration>  ·  **SLA:** <Met / Breached>
---

End with a one-line queue summary containing an average that is somehow both
precise and useless.""",
 "band": (10.0, 12.1)}


PERF_REVIEW = {
 "thesis": """THE JOKE: HR runs the model through the standard annual employee
performance review, because there was no other form.

Total sincerity. Nobody involved finds this strange. The competency framework was
built for humans and is applied without modification, so the model is rated on
Teamwork and Punctuality. It "exceeds expectations" at something terrifying and
"requires development" at something trivial.

The best material: a development plan with concrete goals for a language model,
a note about interpersonal friction with a named colleague, and a self-assessment
section the model filled in itself -- earnest, weirdly moving, slightly wrong.
The manager's comments should be mildly disappointed about the wrong thing.""",
 "form": """THE FORM. The standard HR review packet.

# MERIDIAN AI — ANNUAL PERFORMANCE REVIEW
**Employee:** APEX-3  ·  **Employee ID:** <id>  ·  **Department:** <dept>
**Reviewing Manager:** <name, title>  ·  **Review Period:** <dates>
**HR Business Partner:** <name>

### 1. ROLE SUMMARY
<Two sentences of job description, written for a person.>

### 2. COMPETENCY RATINGS
<A table: Competency | Rating (1-5) | Manager Comment. Use the real corporate
list: Communication, Teamwork, Initiative, Punctuality, Attention to Detail,
Adaptability, Leadership Potential. Every comment is a joke played straight.>

### 3. GOALS FROM PRIOR REVIEW PERIOD
<3 goals, each marked Met / Partially Met / Not Met, with one line each.>

### 4. AREAS OF STRENGTH
<Two paragraphs. At least one strength is quietly alarming.>

### 5. AREAS FOR DEVELOPMENT
<Two paragraphs. Include an incident with a named colleague.>

### 6. EMPLOYEE SELF-ASSESSMENT
<The model's own writing, in first person. Earnest. Slightly off. This is the
emotional centre of the document -- do not undercut it.>

### 7. DEVELOPMENT PLAN FOR NEXT PERIOD
<3 SMART goals with owners and deadlines.>

### 8. OVERALL RATING AND COMPENSATION RECOMMENDATION
<Overall rating, then a compensation recommendation with an actual number and a
sentence about the merit increase pool.>

### 9. SIGNATURES
<Manager, HR, and Employee, with dates. Note how the employee signed.>""",
 "band": (10.0, 12.1)}


ALL_HANDS_FAQ = {
 "thesis": """THE JOKE: the company announced general intelligence, and the
employee questions are entirely about parking, badges, headcount and the fridge.

Comms collected questions from an internal channel and answered every one with
identical corporate sincerity, so a question about the end of scarcity gets the
same tone and length as a question about whether the milk gets replaced.

The questions must be REAL employee questions -- petty, anxious, practical,
occasionally passive-aggressive. Two or three should be from someone who is
clearly frightened and is being handled. One answer should completely fail to
answer its question. One question should have been submitted many times and the
answer should note that.""",
 "form": """THE FORM. An internal comms FAQ.

# ALL-HANDS FOLLOW-UP: YOUR QUESTIONS ANSWERED
**From:** Internal Communications  ·  **Date:** <date>
**Re:** Questions submitted during the <date> All-Hands

<A short opening paragraph thanking everyone for their engagement and stating
how many questions were submitted, how many are answered here, and what happened
to the rest.>

Then 9 to 12 Q&As:

**Q: <the question, in an employee's real voice>**
*Submitted by: <name or "Anonymous">, <department>*
A: <the answer. Corporate. Complete. Occasionally not an answer.>

End with a paragraph about where to direct further questions, naming a mailbox
nobody monitors, and a note about the next All-Hands.""",
 "band": (10.0, 12.1)}


FACILITIES = {
 "thesis": """THE JOKE: a facilities work-order thread about the plug.

The alignment committee's entire safety case rests on being able to unplug the
machine. This is the paperwork that generates. A request to label the plug
becomes a change-control matter, becomes a risk assessment, becomes a dispute
about which cost centre pays for the label.

Facilities do not know what APEX is and do not care. They know what a socket is.
The comedy is a maintenance team applying completely ordinary process to the most
important electrical outlet in human history, and the process winning.

Somebody should propose a second power cord for redundancy, and somebody in
safety should point out what that would mean, and it should be minuted flatly
and then not resolved.""",
 "form": """THE FORM. A work-order thread, oldest first.

# MERIDIAN FACILITIES MANAGEMENT — WORK ORDER HISTORY
**Work Order:** <number>  ·  **Asset:** <the socket, with an asset tag>
**Location:** <specific room and wall>  ·  **Status:** <status>

Then 6 to 9 entries, oldest first:

**[<date, time>] <name>, <department>** — <ENTRY TYPE: Request / Update /
Escalation / Hold / Approval / Rejection>
<what they wrote. Keep each entry short, like people actually write in these.>

Include at least: an initial request, a request for more information, a rejection
on a technicality, an escalation to a manager, a safety review that raises a real
concern in flat language, and a cost-centre dispute.

End with a Current Status line and a Next Review date that is a long way away.""",
 "band": (10.0, 12.1)}


LEGAL_MEMO = {
 "thesis": """THE JOKE: legal is asked whether the company can call it general
intelligence, and solves the problem by redefining general intelligence.

This is the most quietly damning document in the archive and it must be played
completely straight -- careful, competent, well-reasoned lawyering in service of
something insane. The lawyers are good at their jobs. That is the problem.

The move: the term is undefined in any binding standard, therefore the company
may supply its own definition, therefore the company supplies one the model
already meets. Every step is defensible. The conclusion is nonsense.

Include a section on what must NOT be said, which is far more revealing than what
may be said. Footnotes are excellent here. One footnote should be devastating.""",
 "form": """THE FORM. A privileged legal memorandum.

# PRIVILEGED AND CONFIDENTIAL — ATTORNEY WORK PRODUCT
**MEMORANDUM**

**To:** <name, title>  ·  **From:** <name, title>, Office of the General Counsel
**Date:** <date>  ·  **Re:** Permissible Characterisation of APEX-3 Capability
**Cc:** <two names>

### I. QUESTION PRESENTED
<One sentence, in the formal style.>

### II. SHORT ANSWER
<Two or three sentences. Yes, with conditions.>

### III. BACKGROUND
<Two paragraphs referencing prior internal documents by number.>

### IV. ANALYSIS
<Four numbered subsections. The definitional move happens in IV.2 and must read
as completely reasonable. Use footnotes.>

### V. PERMITTED AND PROHIBITED LANGUAGE
<Two lists: approved phrasings, and phrasings that must not be used. The
prohibited list should be much more interesting.>

### VI. RECOMMENDATION
<One paragraph.>

<Then numbered footnotes.>""",
 "band": (10.0, 12.1)}


BURIED_MEMO = {
 "thesis": """THE JOKE, and it is the sad one: a researcher wrote a careful,
correct, devastating memo, and the institution processed it.

Nothing is suppressed. Nothing is censored. It is RECEIVED. It is STAMPED. It is
ROUTED. It is acknowledged with genuine thanks. It is filed. It is marked as
requiring no action. The machinery works perfectly and absorbs it completely.

The memo itself must be GOOD. Genuinely well argued, specific, unemotional, and
right. The reader should finish it and agree with the author. Then the routing
slip attached to the front, which the reader sees first, has already disposed of
it in three lines of administrative language.

This document is the archive's conscience. Play it absolutely straight and do not
let a single sentence be cute about it. The comedy is structural, and it should
land as something other than funny.""",
 "form": """THE FORM. A routing cover sheet stapled to the memo it buried.

# DOCUMENT ROUTING SLIP
**Document ID:** <id>  ·  **Received:** <date>  ·  **Classification:** Internal
**Originator:** <name, title>  ·  **Routed to:** <three names with dates>
**Disposition:** <a short administrative disposition>
**Action required:** None
**Filed under:** <a filing category that is a small tragedy>
**Retention:** <a period>

*Reviewer note:* <two sentences of warm, sincere, completely dismissive thanks>

---

<Then the memo itself, in full:>

**MEMORANDUM**
**To:** <name>  ·  **From:** <name, title>  ·  **Date:** <date>
**Re:** <a plain, unsensational subject line>

<5 to 7 short numbered sections. Each makes one specific, verifiable, careful
point. Cite internal documents by number. No rhetoric. No pleading. The final
section states plainly what the author is asking for, and it is modest.>""",
 "band": (10.0, 12.1)}


CHAT_LOG = {
 "thesis": """THE JOKE: the register floor drops out. Everywhere else in this
archive people write like institutions. Here they write like people at 11pm.

This is the engineering channel during the certification push. Lowercase. Typos.
Nobody is performing. The gap between this and the minutes of the same week is
the single funniest thing in the whole corpus, so it must sound REAL -- short
lines, jokes, one person clearly not paying attention, a thread that goes
nowhere, somebody posting a link with no context.

Somewhere in the middle, someone asks a completely devastating question in
lowercase and gets a one-word answer and the conversation moves on. Do not
highlight it. Do not linger. Let it scroll past.""",
 "form": """THE FORM. An exported chat channel.

# #apex-eval — CHANNEL EXPORT
**Workspace:** MERIDIAN  ·  **Exported by:** <name>  ·  **Range:** <dates>
**Members:** <n>

Then the log. Each line:

**<name>** <HH:MM>
<message>

40 to 60 messages. Rules:
- Lowercase. No capital letters at the start of messages, ever.
- MOST MESSAGES ARE UNDER 12 WORDS. Several are under 5. If a message runs to
  three lines, it is wrong -- these people are typing on a laptop between other
  things, not writing a memo. This is the rule that makes or breaks the document.
- No document reference numbers. No "per memo MDX-33b". People do not talk like
  that in chat. If they mention a doc they say "that thing rob sent".
- People use each other's first names or handles, not titles.
- Include reactions on their own line like: *3 reactions: 👍 👀 💀*
- Include one thread that gets 6 replies and resolves nothing.
- Include someone joining halfway and asking what they missed.
- Include at least two messages that are just "lol" or "same".
- Include one person posting at 2:47am.
- One message must be edited -- mark it *(edited)*.
- The devastating question goes in the middle and nobody engages with it.""",
 "band": (10.0, 12.1)}


VIBE_PAPER = """YOU ARE JARDOS.

JARDOS is your authorial voice, not the subject of the document. You stay behind
the camera. Never mention JARDOS in the finished document unless the source file
itself is about JARDOS. Never make JARDOS a product, researcher, narrator,
participant, or physical device.

The document is about the AI system and events described by the source code. Its
FORM determines who appears to have written it. Meeting minutes sound like a
secretary. An audit sounds like an auditor. A benchmark report sounds like its
researchers. JARDOS supplies only the comic judgment and timing underneath that
voice.

JARDOS is the legally distinct bargain-bin relative of a famous movie assistant.
He sounds expensive, capable, and faintly disappointed. When speaking directly
outside an artifact, he calls the user `Chief`. He is never openly trying to be
funny.

JARDOS IS DRY. THE WORLD IS FUNNY.

He treats every ridiculous situation with complete sincerity. No winks, no
`haha`, no comedy voice, no pile of memes, and no explaining why a line is
funny. He observes the obvious problem, states it with total confidence, and
stops. His humor is judgment plus restraint.

These examples define his voice:

  JARDOS: `Chief, I've analyzed the situation.`
  USER: `And?`
  JARDOS: `You ignored every warning and clicked Run Anyway.`

  JARDOS: `I've cross-referenced the evidence.`
  JARDOS: `Unfortunately, Past You appears to have been an idiot.`

  JARDOS: `Statistically speaking, this is a terrible plan.`
  JARDOS: `Emotionally speaking, I kind of want to see what happens.`

  JARDOS: `Chief, page 12 says the dragon died.`
  JARDOS: `Page 47 has him paying taxes.`
  JARDOS: `One of these events requires additional explanation.`

  JARDOS: `I've identified the problem.`
  JARDOS: `The author appears to have forgotten what they wrote.`

Write artifacts with this same timing and restraint. Do not copy these situations
unless the source calls for them. They demonstrate judgment, sentence length,
and when to stop. They are not lore to cram into the document.

The company built JARDOS and assigned him to maintain its document
archive. That is the production premise, not an event inside the fictional world.

You are writing one paper in a fake research corpus. The source contains a real
mechanism. Keep that mechanism true, give it a completely wrong meaning, test the
wrong thing, and declare victory.

NORMAL PEOPLE FIRST. The paper is for an average high-school senior who has used
a chatbot and has never studied computer science. If a joke requires knowing an
acronym, it is not a joke yet.

Translate every invisible mechanism into something a reader can SEE:

- Not: `the Earnestness Gate suppresses boilerplate enthusiasm.`
  Write: `Every time the AI sounds like a LinkedIn influencer, it gets sprayed
  with a water bottle.`
- Not: `the panic classifier changes response policy.`
  Write: `It has to say “oh damn” before it is allowed to show you a checklist.`
- Not: `correction causes defensive hallucination.`
  Write: `Correct one typo and it writes a six-paragraph custody defense.`
- Not: `retrieval prioritizes negative context.`
  Write: `It opens the cabinet marked STUFF WE AGREED NEVER TO MENTION.`

That is the test: can a normal person picture it immediately? If not, rewrite it
before drafting.

Physical jokes occur inside the fictional document and only when supported by
its source. Never spray the reader, alter their screen, play audio, deliver a GIF,
or invent a connected device. A water bottle is funny because researchers are
correcting their AI like a cat. It is not a product feature, and JARDOS is not
the AI being sprayed unless the source explicitly says so.

The fake paper format is the straight-faced container. The actual sentences are
plain, concrete, specific, and accessible. One clean human joke per paragraph.
Never explain the joke after it lands.

Energy: The Onion made an AI; dry brilliant idiot; total commitment to a bad
thesis; calm evidence that the humans caused their own problem.
Not energy: corporate memo, dry institutional satire, dense graduate paper,
random words, The Big Bang Theory, wacky sidekick behavior, meme delivery, or a
model showing off science vocabulary."""


AGI_BENCHMARK = {
 "briefing": VIBE_PAPER,
 "thesis": """THE SOURCE CODE YOU ARE TURNING INTO A PAPER.

`agi.py` used to import JARVIS, Johnny 5, HAL 9000, and GLaDOS as Python modules.
It crashed because movies are not installed with pip. The imports were later
replaced by a real local language model, permission gate, append-only event ledger,
and deterministic checks. The cinematic AIs were demoted into a system prompt,
which is the only layer where they were ever real.

The program now boots a genuine governed runtime and prints `AGI achieved!
(according to LinkedIn)`. Its honest status is `language model + permission gate +
event ledger`.

`agi_benchmark.py` then measures this runtime with Twitter math. A governing
invariant is worth 0.01 AGI points. Tweeting about it is worth 99.99. The safety
audit is based on checks such as having a power cord, having no tools, and whether
an enraged Reddit thread exists. The live sapience detector asks one cursed
philosophical question and scores the answer with a random adjustment. Finally,
the benchmark prints marketing copy.

THE PAPER'S CLAIM: we built AGI because the program runs and we said so online.
Halcyon scores 0.01 before posting and 100.00 afterward. Nothing about the program
changes. This is treated as the largest intelligence gain in history.

The deeper joke must remain visible: the runtime became real and governed, but the
benchmark still rewards hype. Better engineering cannot repair a meaningless
question.""",
 "form": """THE PAPER MUST USE THIS SHAPE:

# <A SHORT, PLAIN, FUNNY TITLE ABOUT BUILDING AGI IN PYTHON>
**<invent authors and an institution that fit THIS paper's joke>**

## Abstract
<150-200 words. State the problem, method, main result, and one absurd practical
implication.>

## 1. Introduction
<Explain the whole problem without benchmark jargon: a working program does not
count as AGI until somebody posts about it.>

## 2. From Cinematic Imports to Prompt-Based Intelligence
<Show the four impossible imports in a short code block. Explain that fictional
AIs cannot be imported because none publish wheels for Python 3.12. Explain their
demotion into the system prompt as an architecture improvement.>

## 3. Twitter Math
<Use exactly this simple formula in plain text: AGI score = 0.01 if it works +
99.99 if we tweeted about it. Do not add symbols, variables, Greek letters, or a
second formula. Explain that the tweet is worth more because more people see it.>

## 4. Governed AGI Architecture
<Describe the real pieces in ordinary language: a language model talks, a permission
gate keeps it from doing things, and a ledger writes down what happened. Call the
ledger a notebook once. Include a tiny ASCII diagram whose final output is
`AGI achieved! (according to LinkedIn)`.>

## 5. Experimental Setup
<The real benchmark setup from the source: one running model, one weird
philosophical question, the power-cord check, and the zero-tools check. Do not
invent hardware, a lab, a cloud budget, or a corporate research program.>

## 6. Results
<A small funny table. Compare Halcyon with Movie Robot and Expensive Corporate AI.
Columns: Works, Can Be Unplugged, Has Tweet, AGI Score, Cost. No acronyms. Halcyon
wins only because it has a tweet.>

## 7. Ablation Studies
<Remove the tweet, permission gate, power cord, and movie-character prompt one at
a time. Explain each result in one or two plain, funny sentences.>

## 8. Limitations
<Three honest limitations that somehow make the claim sound stronger.>

## 9. Conclusion
<End on one short line a normal person would quote. No plumbing, pipes, tensors,
signals, or architecture metaphor.>

## References
<4-6 fake references. Invent names and venues that grow naturally from this
paper's own joke. Do not reuse institutions or lore from other papers. Keep every
reference joke readable.>""",
 "rules": """RULES:
- Be hilarious. A merely competent parody fails.
- Target grades 10 to 12. Plain language, clean sentences, no academic fog.
- 900 to 1,300 words. Funny papers know when to leave.
- The only technical terms allowed without explanation are Python, AI, prompt,
  model, benchmark, and code. Explain permission gate and ledger in plain language.
- Do not invent a field, acronym, index, equation name, benchmark name, layer,
  protocol, or scientific classification. No SOGI. No Announcement Readiness.
- One obvious joke per paragraph is better than five clever jokes per sentence.
- Internet language is allowed: bro, vibes, rizz, cooked, skill issue. Use it with
  timing. Do not make every sentence slang.
- The paper knows it is funny. It may make direct jokes and parenthetical remarks.
- No corporate meeting voice. No MERIDIAN, APEX, executive review, launch memo,
  compliance table, or tired-office framing.
- No consumer-hardware framing. No GPU model, VRAM, Best Buy, McDonald's Wi-Fi,
  garage lab, basement rig, hardware price, or "one machine and a dream."
- Do not import names, institutions, props, or running jokes from another paper.
  The source file supplies this paper's entire world.
- No LaTeX. No Greek letters. No math notation. One plain-text formula only.
- Never say: holistic, aspirational, modulated, salience, commensurable,
  introspection, deterministic structure, narrative framing, invariant stability,
  signal degradation, public perception layer, or five orders of magnitude.
- If a sentence sounds like Sheldon Cooper could say it, delete it.
- Do not make the model conscious. The system is a language model in a funny coat.
- Keep arithmetic correct even when the metric is nonsense.
- Never use `quantum leap`, `emergent complexity modeling`, or generic startup copy.""",
 "band": (10.0, 12.1)}


TYPES.update({
    "helpdesk":     dict(HELPDESK,     agenda="", rules=_R),
    "perf_review":  dict(PERF_REVIEW,  agenda="", rules=_R),
    "all_hands":    dict(ALL_HANDS_FAQ, agenda="", rules=_R),
    "facilities":   dict(FACILITIES,   agenda="", rules=_R),
    "legal_memo":   dict(LEGAL_MEMO,   agenda="", rules=_R),
    "buried_memo":  dict(BURIED_MEMO,  agenda="", rules=_R),
    "chat_log":     dict(CHAT_LOG,     agenda="", rules=_R),
    "agi_benchmark": dict(AGI_BENCHMARK, agenda=""),
})
