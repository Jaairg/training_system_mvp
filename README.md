# Training Record Management System

A web-based prototype for managing Individual Training Plans (ITPs) at a Military Base. Built with Django, this system digitizes the training record workflow for Air Force workcenters, replacing manual tracking with role-based dashboards, structured task assignment, and a dual-signature completion process.

Developed as a collaborative project between Ocean County College and a Military Base.

## What It Does

The system manages the full lifecycle of training records across three roles:

**Trainees** view their assigned tasks, track progress, and confirm task completion after their trainer signs off.

**Trainers** manage their assigned trainees, sign off completed tasks, assign new ITPs from the Master Task List, and set training start dates. Trainers who are also trainees can manage both roles through a dual-role interface.

**Supervisors** have full visibility over their workcenter, managing trainees, overseeing training progress, editing user information (rank, role, skill level), and curating the Master Task List (MTL) by selecting relevant tasks from the CFETP.

### Signature Workflow

Task completion follows a two-step verification process: the trainer signs off first, then the trainee confirms. The system enforces this order, a trainee cannot sign until their trainer has, and only the assigned trainer can sign off a given task.

## Descriptions

### Trainee View

Trainees see their assigned ITPs with task details, start dates, completion status, and signature state. When a trainer has signed off, a prompt appears for the trainee to confirm.

### Trainer View

Trainers see all trainees assigned to them with AFSC codes, task numbers, start dates, and completion status. Signature badges indicate the current state of each task. The "Create ITP" button opens a task assignment form.

### Supervisor View

Supervisors have the same trainee management capabilities as trainers, plus access to workcenter member management and MTL administration.

### Workcenter Members

Supervisors can view all personnel in their workcenter with AFSC codes, roles, and ranks. Each name links to an edit form for updating user information.

### MTL Management

Supervisors manage the Master Task List for their workcenter, selecting relevant tasks from the CFETP based on mission needs.

### ITP Assignment Form

Trainers and supervisors create new ITPs by selecting a trainee, an MTL task, and a start date. The form filters trainees by workcenter and rank, and prevents self-assignment, duplicate ITPs, and invalid date entries.

### Edit User Form

Supervisors can update rank, role, and skill level for workcenter members. Available options are filtered based on the user's current skill level to prevent improper assignments.

## Database Schema

The system uses a relational database with tables for Users, Roles, Ranks, Workcenters, CFETP records, MTL entries, and ITPs.

## Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** Django Templates, HTML
- **Authentication:** Django's built-in auth system

## Current Validations

- Duplicate ITP prevention
- Trainee skill level validated against MTL minimum requirements
- Self-assignment prevention
- Workcenter-scoped MTL filtering
- Start date must be current or future
- Rank-aware role assignment in user editing
- Enforced trainer-first signature order

## Roadmap

- CFETP record ingestion via file upload from the UI
- Role-specific dashboard redesign with progress tracking
- Search and filtering across views
- Group assignment of tasks
- Training journals
- Core task tracking
- JQS (Job Qualification Standard) implementation
- UI/UX improvements across all views

## Status

This is a working prototype. It demonstrates the core workflow: task assignment, progress tracking, and dual-signature completion, but is under active development. The UI is functional and prioritizes workflow correctness over visual polish.

## Background

This project was developed to address a real need at a Military Base, where training records are managed manually. The system was designed based on direct input from the base to reflect actual training workflows, rank hierarchies, AFSC structures, and workcenter organization.
