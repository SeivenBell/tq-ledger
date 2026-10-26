# QRef

<!-- impeccable:product-schema 1 -->

Status: selected direction for a review-ready specification. The user authorized planning and repository organization, not product implementation. QRef is the working name for the quantum-code migration reviewer; the existing repository URL stays unchanged.

## Platform

web

The product also has a local command-line workflow. The public web surface presents execution evidence; it does not execute uploaded Python.

## Stack

Delegated by the user: one Python toolchain, local trusted execution, JSON Schema validation, Jinja-generated self-contained HTML and free GitHub Pages publication. The user permits no new paid services. `SPEC.md` defines the complete proposed stack and deployment contract; no application or site is implemented yet.

## Users

The primary user is a quantum-software developer or researcher reviewing an AI-assisted Qiskit upgrade. They need to distinguish an API repair from changes to the experiment. They can run inspected code locally and understand pinned software environments.

A second audience is a hackathon evaluator inspecting the same real execution evidence. This audience must be able to understand the demonstrated change without reading the source code first.

## Product Purpose

Produce a reproducible review of one supported quantum-code migration. Show what circuit checks establish, what execution settings or decoded results changed, and what remains unchecked. Make intentional changes explicit instead of treating every difference as a defect.

Success is a complete local execution-to-report workflow and an inspectable public report. General adoption, reviewer time savings, commercial demand and contest success are not established.

## Positioning

Reuse MQT QCEC for circuit checks. The proposed contribution is a review workflow around circuit evidence, execution settings and experiment interpretation—not a new equivalence engine or proof of scientific correctness. Ordinary coding agents and existing Qiskit tools are real alternatives; the product has no demonstrated competitive moat.

## Operating Context

The supported first case uses trusted local Qiskit/Aer helper implementations from a public QAOA notebook and explicit graph, angle and shot inputs. Source and target runtimes are isolated. The original implementation is a reference, not a scientific truth oracle.

AI supplies a proposed port and explanation. Separate execution supplies observations. A human decides whether a behavioral change is intended. Public presentation must distinguish a recorded model run from a live model call.

## Capabilities and Constraints

The specification must cover local execution, circuit checks, exact small-input numerical comparisons, requested versus completed shots, evidence provenance, human review decisions, export and a public report.

The first release supports one declared static Qiskit/Aer workflow. Arbitrary notebook discovery, cloud hardware, noise, dynamic circuits, optimizer convergence, automatic scientific certification and public Python execution are excluded.

The user’s build constraint is **roughly half a day**. This is not a measured completion estimate. The release remains one helper workflow with no hosted execution or extra product surface. External review must challenge its critical path before implementation; no agent may silently drop acceptance criteria or assume a deadline extension.

Use existing local compute and available subscription access. Do not depend on pending API credits, a new paid host, or sponsor integrations. A new hosted model feature is outside the agreed minimum.

## Brand Commitments

Use plain English, readable titles and visible uncertainty. Third-party copy must follow the Humanizer and ASD-STE100 guidance. Avoid unsupported novelty, customer, accuracy, savings and certification claims.

## Evidence on Hand

The original 14-file QAOA research record is retained under `evidence/qaoa/`. It includes the licensed source snapshot, real Sonnet port, notes, dependency lists and recorded observations. The old observer's capture limitations are explicit in `SPEC.md`; unrelated research is archived.

A separate fresh planning probe generated a no-tools subscription proposal, then captured actual Aer submissions in both runtimes. It produced 18 observations per side, nine equivalent submitted-circuit pairs and independent classical checks. The source ignored the requested shot setting; the target honored it. Both model records documented the change; the fresh prompt supplied the known behavior and requested the correction. This is positive capability evidence, not independent issue discovery or a hidden-error rate. `docs/reviews/planning-verification.md` links immutable artifacts.

There is no completed product interface, public deployment, confirmed adopting reviewer or measured time saving. The user reports one research inquiry sent with no reply. Further outreach is not authorized.

## Product Principles

- Keep model proposals, execution observations and human judgments distinct.
- Show coverage and uncertainty as prominently as successful checks.
- Prefer a small complete workflow to a general platform.
- Preserve source identity, exact environments and reproducible evidence.
- Use established tools and disclose reused work.
