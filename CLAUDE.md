# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains specifications and tooling for two LACCD educational software applications:

### Calricula
An AI-assisted Curriculum Management System for creating, modifying, and approving Course Outlines of Record (CORs) and Programs. It embeds California Community Colleges regulations (PCAH, Title 5) into the authoring interface, transforming technical compliance codes into natural language questions.

### Luminous
An AI-enhanced Program Review and Integrated Planning platform. Transforms compliance-driven Program Review into institutional improvement by embedding equity analytics, ACCJC accreditation standards, and AI-assisted narrative writing.

Both applications share the same design system and authentication for a consistent faculty experience.

## Architecture

### Shared Tech Stack
- **Frontend:** Next.js (React) with Tailwind CSS
- **Backend:** Python with FastAPI
- **AI:** Google Vertex AI (Gemini 1.5 Pro / Gemini 2.5 Flash)
- **Authentication:** Firebase Authentication (Email/Password)
- **Deployment:** Docker Compose on VPS

### Database Differences
- **Calricula:** PostgreSQL via Neon with SQLModel (strict relational data for courses, programs, requisites)
- **Luminous:** PostgreSQL via Neon with SQLModel (uses JSONB for flexible template content)

### Repository
- **GitHub**: https://github.com/johnnyphung-laccd/calricula
- **Production Domain**: calricula.com (Caddy reverse proxy with auto SSL)

## Development Setup

### Quick Start
```bash
# Start all services
docker compose up -d

# Access the application
# Frontend: http://localhost:3001
# Backend API: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

### Test Accounts (Dev Mode)

Dev mode auth bypass is enabled via `AUTH_DEV_MODE=true` in `.env`. All test users use password: `Test123!`

| Email | Role | Department | Demo Courses |
|-------|------|------------|--------------|
| faculty@calricula.com | Faculty | Mathematics | MATH 101 (Approved), MATH 201 (Committee), MATH 202 (Draft) |
| faculty2@calricula.com | Faculty | English | ENGL 101 (Approved), ENGL 102 (Dept Review) |
| faculty3@calricula.com | Faculty | CS | CS 101 (Approved), CS 201 (Articulation), CS 301 (Draft) |
| chair@calricula.com | Curriculum Chair | — | Reviews DeptReview & Committee courses |
| articulation@calricula.com | Articulation Officer | — | Reviews ArticulationReview courses |
| admin@calricula.com | Admin | — | Full system access |
| demo@calricula.com | Faculty | General | PSYCH, BIOL, ART, BUS, NURS, HIST, CHEM courses |

### Dev Mode Authentication

The app supports a dev auth bypass for local development without Firebase:

- **Frontend**: Set `NEXT_PUBLIC_AUTH_DEV_MODE=true` in `.env`
- **Backend**: Set `AUTH_DEV_MODE=true` in `.env`
- Dev tokens: `dev-faculty-001`, `dev-chair-001`, `dev-articulation-001`, `dev-admin-001`, `dev-demo-001`

Files involved:
- `frontend/src/contexts/AuthContext.tsx` - DEV_USERS map
- `backend/app/core/firebase.py` - dev_user_map for token verification
- `backend/seeds/seed_users.py` - User seed data

## Directory Structure

```
calricula/
├── backend/            # FastAPI Python backend
│   ├── app/                      # Application code
│   │   ├── api/routes/           # API endpoints
│   │   ├── models/               # SQLModel database models
│   │   ├── services/             # Business logic services
│   │   └── core/                 # Configuration and core utilities
│   ├── alembic/                  # Database migrations
│   ├── seeds/                    # Database seed scripts
│   └── tests/                    # Backend tests
├── frontend/           # Next.js React frontend
│   ├── src/app/                  # App router pages
│   ├── src/components/           # React components
│   └── e2e/                      # Playwright E2E tests
├── calricula_docs/     # Documentation and reference materials
│   ├── knowledge-base/           # Reference documents for RAG
│   │   ├── ccn/                  # CCN template PDFs
│   │   └── *.pdf                 # PCAH, Title 5, CCN docs
│   ├── session_notes/            # Development session summaries
│   ├── test_reports/             # Test reports and analyses
│   ├── tests/                    # Archived test scripts
│   ├── Design_System.md          # Tailwind config and components
│   ├── PRD_Calricula.md          # Requirements (brief)
│   └── PRD_Calricula_Comprehensive.md  # Requirements (full)
├── docker-compose.yml            # Development Docker config
├── docker-compose.prod.yml       # Production Docker config
├── .env                          # Environment variables
└── CLAUDE.md                     # This file
```

## Design System Requirements

All frontend must use the "Luminous Design System" defined in `calricula_docs/Design_System.md`:

- Use `luminous-` utility classes (`luminous-card`, `luminous-button-primary`, etc.) instead of raw Tailwind
- Color palette: Indigo-based (`luminous-500: #6366f1`, `luminous-600: #4f46e5`)
- Icons: Heroicons (Solid for active, Outline for inactive)
- Typography: Inter font family
- Always include `dark:` variants for dark mode support

## Key Domain Concepts

### California Community Colleges Regulations
- **PCAH:** Program and Course Approval Handbook (8th Edition) - state approval rules
- **Title 5 § 55002.5:** The "54-hour rule" for unit calculation (Total Student Learning Hours / 54 = Units)
- **CB Codes:** 27+ "Course Basic" MIS codes required for state funding
- **AB 1111 (CCN):** Common Course Numbering requiring C-ID standardization
- **TOP Codes:** Taxonomy of Programs codes for classification

### Calricula-Specific Terms
- **COR:** Course Outline of Record - the legal document describing a course
- **Content Review:** Matching prerequisite exit skills to course entry skills (Title 5 § 55003)
- **Cross-listing:** Courses shared across departments (must have identical objectives/content/units)

### Luminous-Specific Terms
- **The Golden Thread:** Links College Mission → ISMP Strategic Goal → Program Goal → Action Plan → Resource Request
- **ISMP:** Integrated Strategic Master Plan (5 strategic goals for LAMC 2019-2024)
- **ACCJC:** Accrediting Commission for Community and Junior Colleges
- **DI/PPG:** Disproportionate Impact measured by Percentage Point Gap methodology
- **HSI:** Hispanic-Serving Institution (LAMC is 77.5% Hispanic)

## eLumen Course Library Browser

### Overview
The Library page (`/frontend/src/app/library/page.tsx`) provides faculty with an in-app Course Outline of Record (COR) browser for all 9 LACCD colleges.

### Features

**Course Search & Filter**
- Search courses by keyword (title, code, description)
- Filter by college (all 9 LACCD colleges)
- Pagination (10 courses per page)
- 60-second timeout for slow eLumen API
- Performance logging to console

**Course Discovery**
- Course cards display: code, title, institution, status, authors, start term
- "View COR" button opens comprehensive in-app modal

**Complete COR Display Modal**

The modal displays all available eLumen API data organized in sections:

1. **Header** - Course code, title, institution, status, term, units
2. **Authors** - Instructor/author names from course metadata
3. **Description** - Full catalog course description
4. **Course Structure** - Units, lecture hours, lab hours, activity hours
5. **Course Objectives** - Numbered list of course learning objectives
6. **Student Learning Outcomes (CSLOs)** - Outcomes with performance criteria
7. **Compliance Codes**
   - TOP Code (Taxonomy of Programs)
   - CB Codes (all 28 MIS codes: CB00-CB27)
8. **Footer Note** - References additional details on full eLumen COR page

### Technical Implementation

**Frontend Data Flow**
- `eLumenCourse` interface includes all COR fields
- `CourseDetailModal` component displays full COR information
- Dark mode support with Luminous design system
- Responsive design (mobile, tablet, desktop)

**Backend Data Pipeline**
- `CourseListItem` model returns full course data in search results
- `course_to_list_item()` helper extracts all fields from eLumen response:
  - Hours calculations (lecture, lab, activity)
  - Objectives extraction (text only)
  - Outcomes/SLOs (with sequence and performance criteria)
  - CB codes (all compliance codes parsed from custom fields)
- No additional API calls needed - data included in search response

**API Routes** (`/backend/app/api/routes/elumen.py`)
- `GET /api/elumen/courses` - Search courses with pagination
  - Reduced page size to 10 for performance
  - Parameters: college, query, page, page_size
  - Returns SearchResponse with full CourseListItem objects
- `GET /api/elumen/courses/{course_id}` - Get single course details
- `GET /api/elumen/courses/by-code/{subject}/{number}` - Get by course code
- `GET /api/elumen/programs` - Search programs
- `GET /api/elumen/programs/{program_id}` - Get single program

### Performance Optimization

**Pagination Strategy**
- Fetches `page_size * page + page_size` items (one extra page buffer)
- Enables "has next page" detection without additional API calls
- Reduced page size from 25 → 10 courses per page

**Request Timeout**
- 60-second timeout for slow eLumen API responses
- AbortController for cancellation handling
- Error feedback to user if timeout occurs

**Data Efficiency**
- All COR data returned in search results (no modal-specific API calls)
- Conditional rendering (only shows sections with data)
- Efficient serialization of nested course objects

### What's Available vs. Not Available

**✅ Available in Modal** (from eLumen public API)
- Course metadata, units, hours
- Description
- Objectives
- CSLOs with performance criteria
- CB codes (all 28 MIS codes)
- TOP codes
- Authors
- Status and effective term

**❌ Not Available** (public API limitation)
- Textbooks/content resources
- Methods of instruction
- Assignment types and details
- Methods of evaluation
- Non-course conditions
- Board/effective dates
- Requisite details
- CIP codes
- Discipline requirements

### Future Enhancements

1. **Requisites Display** - Parse and display prerequisites, corequisites, advisories
2. **Backend Caching** - Cache eLumen responses to reduce API load
3. **Infinite Scroll** - Alternative to pagination for better UX
4. **Course Comparison** - Side-by-side comparison of multiple courses
5. **Export** - Download COR as PDF or Word document
