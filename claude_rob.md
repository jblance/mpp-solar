## 🧭 How to Manage Long, Complex Projects with AI (Claude Code)

When working on large, multi-phase projects with AI tools that have limited context windows, you can maintain consistency and direction across sessions by following this structured process. The approach below allows you to "persist" your project's knowledge, plans, and progress using markdown files that the AI can re-read to regain context after resets.

---

### **Step 1: Define and Plan**

**Goal:** Give the AI a deep understanding of the project and get a detailed, structured plan.

1. **Explain the idea in depth** — what the project is, its goals, intended outcomes, constraints, and success criteria.
2. **Ask the AI** to create a `IMPLEMENTATION_PLAN.md` containing:

   * A **project overview**
   * **Objectives and milestones**
   * **Low-level technical details** describing how each goal will be achieved
   * A clear, sequential structure the AI can later reference

---

### **Step 2: Validate and Enrich the Plan**

**Goal:** Ensure accuracy, completeness, and clarity before execution begins.

1. Ask the AI to **review its own plan** for:

   * Accuracy and feasibility
   * Missing details or assumptions
   * Internal consistency across goals
2. Have it add a section defining **"Criteria for Success"** for each major objective, so progress can be measured objectively.

---

### **Step 3: Break the Plan into Cycles**

**Goal:** Turn the plan into manageable, iterative work units.

1. Ask the AI to divide the `IMPLEMENTATION_PLAN.md` into **development cycles** (or "phases").
   Each cycle should include:

   * Scope and objectives
   * Deliverables and dependencies
   * Review/exit criteria
2. Have it generate one markdown file per cycle:
   `CYCLE_1.md`, `CYCLE_2.md`, etc.
   (If small enough, multiple cycles can live in one file.)

---

### **Step 4: Track Progress**

**Goal:** Maintain a running log of what's done, what's changed, and what needs follow-up.

1. Ask the AI to create a brief `PROGRESS.md` file with:

   * Summary of each completed cycle
   * Notable changes or deviations from the plan
   * Unforeseen problems or technical debt to resolve later
2. After each cycle, have the AI append updates to this file.
   This document becomes your **living audit trail** of project evolution.

---

### **Step 5: Build a Context Recovery File**

**Goal:** Enable the AI to quickly "catch up" after a context reset.

1. Ask it to create a `CONTEXT.md` file that:

   * Summarizes the project's overall purpose and current state
   * Lists which markdown files it should read in full (`IMPLEMENTATION_PLAN.md`, `CYCLE_*.md`, `PROGRESS.md`, etc.)
   * Includes **relative paths** to those files for easy navigation
   * Optionally, provides short summaries of each referenced file

This file acts as a **re-entry point** for the AI when you start a new session.

---

### **Step 6: Verify Context Integrity**

**Goal:** Confirm the AI can accurately reconstruct its working memory.

After clearing the chat context (e.g., `/clear`):

1. Prompt the AI:

   > "Read `CONTEXT.md` and all referenced files in full. Summarize what our next step is."
2. Review its summary to confirm it fully understands the current state and next steps.

---

### **Step 7: Maintain State During Work**

**Goal:** Avoid losing progress as the AI approaches context limits.

1. As the project continues, **monitor context size**.
   When you estimate 5–7% context remaining:

   * Ask the AI to update `PROGRESS.md` with the current state, open issues, and remaining tasks.
2. Then clear context and rehydrate from `CONTEXT.md` before continuing.
