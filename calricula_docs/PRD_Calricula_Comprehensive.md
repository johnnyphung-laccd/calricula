# Product Requirement Document (PRD): "Calricula" – Intelligent Curriculum Management System

**Version:** 3.0 (Final Comprehensive)
**Target Institution:** Los Angeles Mission College (LAMC) / LACCD
**Strategic Goal:** To decouple "Curriculum Design" (Creative/Pedagogical) from "Curriculum Compliance" (Bureaucratic/Technical), using AI to bridge the gap and ensuring alignment with State mandates (AB 1111, AB 928).

## 1. Executive Summary

**Calricula** is a specialized software application designed to streamline the complex, regulation-heavy process of creating and modifying college courses and programs.

Currently, faculty must navigate a maze of state codes (`CB03`, `TOP`, `CIP`), calculation formulas (54-hour rule), and new legislative mandates (AB 1111 Common Course Numbering, AB 928 Cal-GETC). Existing systems like eLumen act as rigid data repositories ("System of Record") but offer little guidance during the *authoring* phase.

**Calricula** serves as the **"Intelligent Authoring Layer"**:
1.  **Guiding Faculty:** Transforming natural language intent into compliant technical specs.
2.  **Enforcing Policy:** Hard-coding rules from the *Program and Course Approval Handbook (PCAH)* and *Title 5*.
3.  **Automating Alignment:** Automatically mapping local courses to the new Common Course Numbering (CCN) system.

## 2. Strategic Context & Compliance Landscape

The system is architected to handle specific California Community College constraints identified in the `knowledge-base`:

*   **AB 1111 (Common Course Numbering):** The system must maintain a lookup table of state-mandated C-IDs (e.g., `ENGL C1002`) and flag local courses that need re-numbering.
*   **The "54-Hour" Rule (Title 5 § 55002.5):** Units are calculated based on *Total Student Learning Hours*.
    *   *Formula:* `(Lecture Hours + Lab Hours + Homework) / 54 = Units`.
    *   *Constraint:* The system must auto-calculate homework hours (standard is 2 hours homework for every 1 hour lecture) to prevent non-compliant unit values.
*   **CB Coding (MIS Data):** The system must generate the 27+ "Course Basic" (CB) codes required for state funding (Apportionment).
    *   *Logic:* `CB09` (SAM Code) is dependent on `CB03` (TOP Code). If `CB03` is non-vocational, `CB09` must be 'E'.

## 3. User Roles & Workflows

### 3.1 Faculty Originator (The Architect)
*   **Goal:** Create a new course or update an existing one without getting bogged down in codes.
*   **Pain Point:** "I don't know what a 'TOP Code' is. I just want to teach 'Drone Photography'."
*   **Calricula Solution:** Faculty describes the course. The AI suggests `TOP Code 1012.00 (Applied Photography)` and sets `CB09` to "Vocational."

### 3.2 Curriculum Chair/Tech Review (The Gatekeeper)
*   **Goal:** Ensure the COR (Course Outline of Record) is legally defensible.
*   **Pain Point:** Manually checking if the "Entry Skills" match the "Prerequisite's Exit Skills" (Content Review).
*   **Calricula Solution:** The **Requisite Validator** visualizes the skill map and flags gaps automatically.

### 3.3 Articulation Officer (The Connector)
*   **Goal:** Ensure courses transfer to UC/CSU.
*   **Pain Point:** Ensuring the new Cal-GETC standards are met.
*   **Calricula Solution:** The system flags if a course outline is missing required "Critical Thinking" components necessary for Transfer status.

## 4. Functional Requirements

### Module A: The "Smart COR" Editor
*The core workspace for designing a Course Outline of Record.*

*   **REQ-A1 (Narrative Assistant):**
    *   Users draft descriptions in natural language.
    *   AI refines them to meet "Catalog Style" (active voice, present tense, ~50 words).
*   **REQ-A2 (Bloom's Taxonomy Engine):**
    *   When writing Objectives, the system provides a "Verb Picker" aligned with Bloom's Taxonomy (e.g., "Analyze", "Synthesize").
    *   *Validation:* It prevents the use of "weak" verbs (e.g., "Understand", "Know") which are rejected by accreditation.
*   **REQ-A3 (The Unit Calculator):**
    *   **Input:** User enters "3 Units Lecture".
    *   **System Action:** Auto-calculates:
        *   Lecture Contact Hours: 54
        *   Out-of-Class Hours: 108
        *   Total Student Learning Hours: 162
    *   *Constraint:* If user tries to manually override "Total Hours" to a number that violates the divisor (54 or 48 depending on local policy), the system blocks the save.

### Module B: The Compliance Engine
*The "Invisible Guardrails" derived from the PCAH.*

*   **REQ-B1 (CB Code Wizard):**
    *   A wizard interface for the 27 CB codes. Instead of a raw dropdown, it asks diagnostic questions:
        *   "Is this course for credit?" -> Sets `CB04`.
        *   "Is it transferable?" -> Sets `CB05`.
        *   "Is it basic skills?" -> Sets `CB08`.
*   **REQ-B2 (CCN Matcher):**
    *   Database of all AB 1111 Common Course Numbers.
    *   If a user titles a course "Intro to Sociology", the system prompts: *"This looks like SOCI C1000. Would you like to adopt the state standard title and number?"*
*   **REQ-B3 (Cross-Listing Validator):**
    *   Ensures cross-listed courses share identical Objectives, Content, and Units.

### Module C: Program Builder (The Stack)
*Designing Degrees and Certificates.*

*   **REQ-C1 (The Nested Container):**
    *   Visual "Drag and Drop" interface to build degrees.
    *   Calculates total units dynamically.
    *   *Validation:* Flags if a degree exceeds 60 units (unless High Unit Major).
*   **REQ-C2 (Narrative Generation):**
    *   Generates the specific "Program Narrative" document required by the Chancellor's Office (Goal, Objectives, Master Planning, Enrollment Projections).

### Module D: Integration & Export
*   **REQ-D1 (eLumen Compatibility):**
    *   Generates a "Copy/Paste" report where every field maps 1:1 to eLumen's input fields.
*   **REQ-D2 (PDF Gen):**
    *   Generates a clean, watermarked "Draft COR" PDF for committee review.
*   **REQ-D3 (Public View):**
    *   Generates a simplified "Public-Facing COR" (stripping out internal codes) for Articulation purposes.

## 5. Technical Architecture

### 5.1 Tech Stack
*   **Frontend:** **Next.js** (React) using the **Luminous Design System** (Tailwind CSS, consistent component library).
*   **Backend:** **Python (FastAPI)**.
*   **Database:** **PostgreSQL** (via **Neon**) using **SQLModel**.
    *   *Why Relational?* Curriculum data is highly structured and relational (Programs have many Courses; Courses have many Requisites).
*   **AI:** **Google Gemini 1.5 Pro** via vertex AI.

### 5.2 Data Schema (Key Entities)
*   `Course`: The central entity. Contains `title`, `units`, `hours`, `catalog_desc`, `cb_codes` (JSONB).
*   `CourseRequisite`: Self-referential join table (Course A requires Course B).
*   `Program`: Contains `title`, `goal_type` (Transfer/CTE/Local).
*   `ProgramCourse`: Join table linking Courses to Programs (Required Core, List A, List B).
*   `LearningOutcome`: Stores CSLOs and Objectives.

## 6. Implementation Roadmap

*   **Phase 1: The Core (Months 1-3):** Database schema, Unit Calculator logic, and Basic COR Editor.
*   **Phase 2: The Brain (Months 4-5):** AI integration for Narrative generation and Bloom's Taxonomy checking.
*   **Phase 3: The Mandate (Months 6-7):** AB 1111 CCN integration and Validation Rules.
*   **Phase 4: The Interface (Months 8-9):** "Luminous UI" polish and eLumen export format.

## 7. Success Metrics
*   **Accuracy:** 100% of "Green Check" courses pass the technical review in eLumen without revision.
*   **Speed:** Reduce COR drafting time by 50%.
*   **Adoption:** 100% of new AB 1111 courses are processed through Calricula first.