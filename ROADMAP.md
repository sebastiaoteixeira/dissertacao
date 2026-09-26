# Dissertation roadmap

**Title (proposal):** *A declarative framework for generating zero trust applications*
**Supervisors:** João Rafael Almeida, Osvaldo Rocha Pacheco
**Source of record for the proposal:** `~/Documentos/dissertacao/document.pdf` (2 pp)
**Status of this document:** planning note, written 2026-07-28. Not a deliverable. Everything
marked `OPEN` is undecided; everything marked `VERIFY` is an unchecked assumption.

---

## 1. Purpose

Maps three things against each other:

1. what an MSc dissertation in this department actually contains,
2. what this dissertation specifically must contain,
3. which papers supply which chapter, what state each paper is in, and what is left uncovered.

The last section is the only one that generates work.

---

## 2. What a dissertation covers, in general

Derived from two accepted dissertations from the same programme, read for structure only.

### 2.1 Exemplar A — Daniel Martins Ferreira, 80 pp

| Ch | Content |
|----|---------|
| 1 | Introduction: Motivation, Objectives, Methodology, Contributions, Structure |
| 2 | Domain background (Smart DMS), including §2.1 **Systematic Review** |
| 3 | Second domain chapter (Monitoring Labs in Tourism) |
| 4 | **Requirements and Architectural Design** — HCD + ACDM: architectural drivers, personas, scenarios |
| 5 | Implementation + real case study (Barra / Costa Nova) |
| 6 | Testing and Validation |
| 7 | Complementary Work |
| 8 | Conclusion |
| A | Appendix: full usability protocol and results (8 sections) |

### 2.2 Exemplar B — Vicente Manuel Barros, 88 pp

| Ch | Content |
|----|---------|
| 1 | Introduction: Motivation, Objectives, Outline, Main results |
| 2 | State of the art (ends in a Summary) |
| 3 | Inception: actors, requirements, role system |
| 4 | Elaboration: architecture and implementation |
| 5 | Results: EHDEN use case, comparison against Montra, risks |
| 6 | Conclusion |
| A | Appendix |

Every chapter ends in a Summary section.

### 2.3 The invariants

Both documents, independently, contain:

- an introduction stating motivation, objectives and contributions explicitly and separately;
- one or two literature chapters, at least one systematic;
- **a full chapter on requirements and architecture, driven by a named, citable methodology**
  (HCD + ACDM in A, inception/elaboration in B) — not a build log;
- an implementation chapter anchored to at least one real case study;
- a validation chapter distinct from the implementation chapter;
- a conclusion with limitations and future work;
- appendices carrying the validation instruments;
- a glossary.

Length is 80-90 pp. Chapters do **not** map one-to-one onto papers: Ferreira produced two
literature chapters from a single published review (*Smart destination management systems for
low-density regions: A systematic review*, CISTI 2024, cited in his own ch2 as `[15]`).

**Ferreira's suggestion, recorded:** write one paper that becomes the basis of chapters 1-2 and
submit it to IEEE Access. That is the model this roadmap follows, with the review as that paper.

---

## 3. What this dissertation must cover

### 3.1 Objectives, from the proposal

1. Study zero trust and NIST SP 800-207.
2. Analyse declarative approaches and DSLs for security, identity and access policy.
3. Design a declarative framework for expressing zero-trust requirements.
4. Generate backend, database and security components from it — authentication, authorization,
   policy enforcement points.

Load-bearing phrase for the validation chapter:
*"assegurar a coerência entre o modelo declarado e o comportamento efetivo do sistema."*
Validation is a **conformance** question — declared model versus observed behaviour — not a
performance question. This constrains chapter 6 more than anything else in the proposal.

Validation subjects are promised as *"casos de uso representativos."*

### 3.2 Proposed chapter plan

| Ch | Title | Primary source |
|----|-------|----------------|
| 1 | Introduction | proposal, expanded |
| 2 | Zero trust: principles and conformance criteria | Paper 2 (RQ1) |
| 3 | Declarative generation of application backends | Paper 2 (RQ2) + existing 128-work sweep |
| 4 | Requirements and architecture of the framework | **native — no paper** |
| 5 | Implementation | Paper 1 (substrate) + Paper 5 (ZT layer) |
| 6 | Validation: declared model versus observed behaviour | Paper 3 (method) + Papers 4, 6 |
| 7 | Complementary work | existing collaborations, see §4.3 |
| 8 | Conclusion | native |
| A+ | Appendices: framework grammar, benchmark specs, falsifier rules | artifacts |

Chapter 4 is the one chapter with no publication path and the one that most distinguishes an
engineering dissertation from a build report. Budget accordingly.

---

## 4. The paper portfolio

### 4.1 State of each paper

| # | Paper | Venue | Lifecycle | Feeds |
|---|-------|-------|-----------|-------|
| 1 | `yaml-api-generator` system paper | SANER 2027 Industrial Track | **Ideation, grounded**; next stage `adversarial-round` | ch5 | + the other on SoftwareX
| 2 | ZT criteria + declarative generation review | IEEE Access (Ferreira's suggestion) | **not started** | ch2, ch3 |
| 3 | *Zero Trust Is Refutable, Not Verifiable* | ACM TOPS | **Internal Review** | ch6 method, ch4 threat model |
| 4 | ZT benchmark with seeded violations | `OPEN` | **not started** | ch6 subjects |
| 5 | ZT generator system paper | `OPEN` | **blocked on software** | ch5 |
| 6 | Generated versus hand-assembled zero trust | `OPEN` | **blocked on 4 + 5** | ch6 results |

### 4.2 Detail

**Paper 1 — `papers/declarative-backend-framework/`.**
Declarative YAML to FastAPI + MongoDB backend with authentication and RBAC, optional React
frontend. TrustRisk third-party risk-management case study (1,369 lines / 38.9 KB YAML,
55 entities, 8 bounded contexts `VERIFY`). Grounded over two sweeps plus a gap-closing third
round: 128 works, 16 lenses, every hit independently re-verified.

This paper is about *the software already built*. It is the substrate the zero-trust work sits
on. It is **not** a zero-trust paper and must not be reframed as one.

Standing issues carried into `adversarial-round`:
- C1 as narrowed is dead. Killed by PostgREST + PostgreSQL RLS + Supabase: SQL DDL is one
  artifact defining schema, API and policy, reaching row-level and ownership rules
  (`(select auth.uid()) = user_id`) with no imperative server code. Hasura adds column-level.
  Decide whether to re-cut C1 or hand it to the adversarial round. `OPEN`
- C2's blanket form is refuted by `grewal2024analyzing` (MSR 2024, DOI `10.1145/3643991.3645072`):
  a median 54% of generated lines survive unchanged in the project. Survives only narrowed —
  no such study exists for declarative/model-driven generators.
- Against the policy-DSL family (Cedar, Rego, Polar, XACML, OpenFGA, SpiceDB, Zanzibar) the
  differentiator is one-artifact + generation, not granularity. Those systems reach equal or
  finer granularity but are separate-artifact, runtime-evaluated, and generate nothing.

**Paper 2 — the review.** One protocol, three research questions. Not two reviews:

- RQ1: what conformance criteria does the zero-trust literature actually define?
- RQ2: what do declarative approaches specify, at what policy granularity, and is enforcement
  generated or evaluated at runtime? (Not scoped to generation: the policy-DSL family generates
  nothing and is the comparison class. See the review's PLAN.md decision 18.)
- RQ3: **the intersection** — map RQ2's capabilities onto RQ1's criteria. The contribution is
  the empty region of that table, and it is the justification for the whole dissertation.

RQ2 is already substantially answered by the existing sweep and round 3's policy-DSL mapping.
RQ1 is greenfield — **no zero-trust literature has been swept at all**. A standalone
intersection review would include too few studies to survive review; RQ3 as a section of a
broader protocol does not have that problem.

**Paper 3 — `papers/zerotrustverifier-paper/`.** Co-authored with Daniel Ferreira
(`dferrero17/zerotrustverifier-paper`). Argues the question "is this application zero trust" is
mis-posed: the defining claim is universal, so a single counterexample refutes it but no finite
procedure confirms it. Zero trust as a universal safety property, a distributed analogue of the
HRU safety problem, undecidable by reduction from halting. The maturity gradient is a category
error measuring control coverage, not degree of truth. Contributes a decomposition of
NIST SP 800-207 into probes, agnostic rules and detection specifications, plus a single-rule
proof-of-concept falsifier (R4/BOLA) emitting `refuted` or `provisional`, never `certified`.

Consequences for the dissertation, both large:

- **Chapter 6 cannot claim the generated applications *are* zero trust.** It can only claim they
  survive refutation. The validation chapter must be written in that frame from the start;
  retrofitting it later means rewriting it.
- **The 800-207 decomposition is a ready-made threat and property model.** Reuse it rather than
  authoring a new one — it converts a hand-wave into a citation.

`OPEN`: own contribution to this paper must be clear and separable, since Ferreira is listed
first and a dissertation cannot rest on someone else's contribution.

**Paper 4 — the benchmark.** Reference applications carrying seeded, ground-truth zero-trust
violations. Publishable as a dataset/artifact contribution. It is the missing input to Paper 3:
a falsifier evaluated against no corpus of known-violating applications has no evaluation.
Cheap, because generating the subjects is what the framework does. Highest leverage per unit of
effort on this list.

**Paper 5 — the ZT generator.** Sequel to Paper 1. Blocked on the software. Do not fold into
Paper 1; the scope difference is what makes both publishable.

**Paper 6 — the comparison.** Generated versus hand-assembled zero trust — realistically an
identity provider plus a service mesh plus an external policy engine. Effort, criteria coverage,
and violations found by the falsifier on each. This is chapter 6's results section. Most
expensive item in the portfolio and the easiest to under-budget. The anti-strawman rule applies:
the hand-assembled baseline must be a competent one.

### 4.3 Collaborations

- **Policy-as-code / compliance-as-code dissertation** (another student). Two fits:
  - answers part of Paper 2's RQ2 — compliance-as-code and ZT policy enforcement share a
    substrate: declarative rules, external evaluation, drift detection. Coordinate protocols
    rather than sweeping the same literature twice.
  - supplies the **regulatory driver** chapter 4 is otherwise missing. ZT criteria derived only
    from NIST SP 800-207 are thin; cross-referenced against a compliance regime they are not.
    `~/Projects/academic/nis2/` is relevant here.
  - `OPEN`: joint paper on the intersection, or at minimum a shared criteria taxonomy both
    dissertations cite.
- **Other work in `~/Projects/academic/papers/`** (SIEM, ETL, phishing, SOAR lines) is candidate
  material for chapter 7, Complementary Work — Ferreira's ch7 is precedent. Cheap volume.

---

## 5. Gaps

Five items are not covered by any paper currently in flight. Four have a publication path.

| # | Gap | Paper path | Notes |
|---|-----|-----------|-------|
| 1 | Requirements and architecture methodology | **none** | native writing, ch4 |
| 2 | Threat / adversary model | none needed | reuse Paper 3's 800-207 decomposition |
| 3 | ZT evaluation subjects | Paper 4 | best new-paper candidate |
| 4 | Comparison baseline | Paper 6 | most expensive |
| 5 | Remaining software | Paper 5 | the year of work |

### 5.1 Gap 1 in detail — the one with no shortcut

Needs a named, citable methodology; actors; and requirements traced back to the conformance
criteria chapter 2 derives. That traceability is the strongest structural move available here,
and it is available *only* because the review is written first: every requirement points at a
criterion the candidate's own review established.

`OPEN`: which methodology. HCD + ACDM (Ferreira) fits a system with human stakeholders;
inception/elaboration (Barros) fits a delivery-shaped project. Neither is obviously right for a
security framework whose stakeholder is a developer. Decide before chapter 4 is drafted, not
during.

### 5.2 Ordering

Sequencing is forced by dependency, not preference:

```
Paper 2 (review)  ->  ch2, ch3  ->  criteria  ->  ch4 requirements
                                        |
Paper 3 (done)    ->  threat model, validation frame
                                        |
software  ->  Paper 5  ->  Paper 4 (benchmark)  ->  Paper 6 (comparison)  ->  ch6
```

Paper 1 runs in parallel and blocks nothing downstream. If something must be cut, cut Paper 6
before Paper 4 — the benchmark is a contribution on its own; the comparison without a benchmark
is not.

---

## 6. Exploratory actions

Ordered by information gained per hour spent. None of these are writing.

1. **Sweep the zero-trust literature at scoping depth.** Zero ZT literature has been swept.
   The question that decides Paper 2's viability: does a *policy-as-code for zero trust* survey
   already exist, and how thin is the intersection region really? Until this runs, Paper 2 is
   an assumption.
2. **Settle the RQ1 criteria source set.** NIST SP 800-207 plus CISA Zero Trust Maturity Model
   are the obvious anchors. `OPEN`: whether vendor architectures (BeyondCorp, Zscaler, Istio
   ambient) count as literature or as objects of study. Paper 3's decomposition may already
   answer this.
3. **Read RESTsec.** Zolotas et al., *Enterprise Information Systems* 12(8-9):1007-1033, DOI
   `10.1080/17517575.2018.1462403`. Paywalled everywhere; every automated route was blocked by
   Taylor & Francis. Round 3's synthesis called reading it *"the single highest-value
   outstanding action in this project."* Needs a human on the institutional proxy.
4. **Close the Web of Science gap.** Zero WoS queries have ever run — Clarivate auth wall, IP
   not on an authenticated range. Until it runs, **do not write "exhaustive search of the
   indexed literature"** in any paper.
5. **Run `portfolio-strategist` across `~/Projects/academic/papers/`.** A dozen sibling papers,
   overlapping author sets, and two ZT papers with a shared co-author is exactly the shape that
   produces self-plagiarism and subsumption findings. Do this before committing venues.
6. **Locate the compliance student's protocol** and decide coordinate-or-diverge.
7. **Resolve the artifact-release blocker.** `sebastiaoteixeira/yaml-framework` is private, has
   no LICENSE, `licenseInfo: null`. Paper 1 already promises a public OSI-licensed generator
   plus a synthetic RBAC-exercising spec. TrustRisk is confidential and is deliberately not
   promised.
8. **Pick chapter 4's methodology** (see §5.1).
9. **Pick the benchmark's application domains** for Paper 4 — needs multiple services,
   non-trivial identity, cross-service calls. Paper 1's out-of-sample subjects (RealWorld/Conduit,
   JHipster `jdl-samples`) are single-service and will not exercise zero trust.

---

## 7. Timeline and scope decision

**Decision, 2026-07-28: go wide.** Keep the full portfolio, target a first final draft between
**April and June 2027**, rather than cutting Papers 4-6 to finish earlier with a
conventionally-scoped dissertation.

### 7.1 Assumed starting position, 2026-10-01

- generator stabilised
- Paper 1 submitted (SANER)
- Paper 2 written (the review)
- Paper 3 submitted (TOPS)

This is roughly where a conventionally-paced student stands in March, not September. The nine
months below buy a substantially larger dissertation than either exemplar in §2, not a delayed
ordinary one.

### 7.2 Plan

| Months | Work | Runs alongside |
|---|---|---|
| Oct-Jan (4) | Build the ZT layer | ch4 |
| Oct-Nov (2) | **Ch4**: methodology, requirements traced to review criteria | software |
| Dec-Jan (2) | Ch2-3 from the review; ch5 substrate half | software |
| Jan-Feb (1.5) | Paper 4: benchmark with seeded violations | ch5 tail |
| Feb-Apr (2.5) | Paper 6: hand-assembled baseline, falsifier on both sides | — |
| Apr-May (1.5) | **Ch6** validation, written in the refutation frame | — |
| May-Jun (1.5) | Ch1, ch7, ch8, appendices, glossary, full pass | — |

Serial sum ~11 months; overlap buys back two. **That overlap exists only because the review
finishes in September.** If Paper 2 slips, chapter 4 slips with it and the parallelism is lost —
a review slip costs roughly double its own length.

- Best case 7 months (end of April): ZT layer lands in three, no revision collisions.
- Realistic 9 months (end of June).
- Pessimistic 12 months (end of September 2027).

Excludes supervisor turnaround on the full draft (typically 2-4 weeks, not compressible) and
assumes this is the primary commitment.

### 7.3 Reviewer time

~1 month of revision work is priced into the nine, distributed.

- **TOPS (Paper 3)** almost certainly will not return a first decision inside nine months. Cite
  as submitted. Not on the critical path.
- **IEEE Access (Paper 2)** is the disruptive one: chapters 2-3 depend on it, and a major
  revision landing in December collides directly with chapter 4.
- **SANER (Paper 1)** notification is a fixed date; camera-ready is about a week whenever it lands.

Two majors arriving together costs an extra three weeks.

### 7.4 The release valve, deliberately not pulled

Cutting Papers 4 and 6 — keeping the technical work but writing it only as chapters, not as
publications — brings the draft to **end of April**. Publishing content costs roughly three
times writing the same content as a chapter: venue formatting, a separate related-work section,
rebuttals, reviewer-driven re-analysis.

Papers 4 and 6 are the **only** optional items in the portfolio. Everything else is needed for
the dissertation regardless of whether it is ever published. If the schedule has to give, it
gives here, and Paper 6 goes before Paper 4 (§5.2).

### 7.5 Decision checkpoints

Do not re-litigate scope continuously. Two fixed points:

- **End of January 2027.** Is the ZT layer working? If not, cut Paper 6 immediately — do not
  wait to see whether February recovers it.
- **End of March 2027.** Is the hand-assembled baseline actually running? If not, chapter 6
  becomes benchmark-and-falsifier only, and Paper 6 is dropped.

---

## 8. Risks

- **Paper 2 does not exist yet and two chapters depend on it.** Longest pole. Everything in
  chapter 4 is traced to criteria it produces.
- **A "policy-as-code for zero trust" survey may already be published.** Unchecked. Would force
  Paper 2 to re-scope. Action 1 above exists to find out early.
- **Chapter 6 is expensive and is scheduled last.** The comparison baseline needs a competent
  hand-assembled zero-trust stack. Standard failure mode is discovering this in the final
  months and shipping a strawman.
- **Chapter 4 has no paper to lean on** and is the chapter examiners read to decide whether the
  work is engineering.
- **Paper 3 is co-authored and led by someone else.** Contribution boundary needs to be explicit
  before it is leaned on in chapter 6.
- **Two ZT papers, shared co-author, overlapping content.** Venue deconfliction is not optional.
- **The wide-scope plan (§7) carries almost no slack.** Papers 4 and 6 sit in a chain behind the
  ZT layer with nothing absorbing a delay. Its safety mechanism is the two checkpoints in §7.5,
  and they only work if the cut is made on the date rather than deferred one more month.
