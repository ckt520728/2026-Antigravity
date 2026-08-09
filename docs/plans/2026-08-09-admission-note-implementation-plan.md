# Admission Note Web App Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an interactive medical admission note generation web application using Google Apps Script (Google Spark) supporting Chinese speech-to-text input with English translation, real-time live preview, and export to Google Docs, Word (.docx), and PDF (.pdf).

**Architecture:** The application uses Google Apps Script as the backend server with `Code.gs` providing Google Sheets logging (`Master_AdmissionNotes`), Google Docs document generation, PDF/Word export links, and `LanguageApp.translate` translation services. The frontend (`index.html`) is a single-page responsive web app with tabbed navigation for Admission Notes and Clinical Exams, featuring Web Speech API integration, clinical preset chips, real-time preview, and export actions.

**Tech Stack:** Google Apps Script, Google Docs API, Google Sheets API, HTML5, Vanilla JavaScript, CSS3 (Glassmorphism UI), Web Speech API, Google Fonts (Inter / Noto Sans TC).

---

### Task 1: Update Backend `Code.gs` with Admission Note Services & Translation API

**Files:**
- Modify: `G:\我的雲端硬碟\2026 Google Spark\Code.gs`

**Step 1: Write backend functions in Code.gs**
- Add `translateChineseToEnglish(text)` using `LanguageApp.translate(text, 'zh-TW', 'en')`.
- Add `saveAdmissionNoteRecord(record)` to log data to `Master_AdmissionNotes` tab in Google Sheets.
- Add `createAdmissionNoteDocReport(record, noteId, timestamp)` to create formatted Google Doc in `住院病歷報告_GoogleDocs` folder and export `.docx` & `.pdf` URLs.
- Add `getRecentAdmissionNotes(limit)` and `searchAdmissionNotes(query)` for history retrieval.

**Step 2: Verify syntax & execution**
- Check GAS function syntax and parameter handling.

**Step 3: Commit / save file**

---

### Task 2: Build Interactive UI for Admission Notes in `index.html`

**Files:**
- Modify: `G:\我的雲端硬碟\2026 Google Spark\index.html`

**Step 1: Add Navigation Tabs & Admission Note Input Panels**
- Add top nav tabs: 📋 住院病歷 (Admission Note) and 🩺 檢查報告 (Clinical Exams).
- Build Demographic section: MRN/Chart No., Name, Age, Gender, Ward/Bed, Admission Date, Doctor, Department.
- Build Chief Complaint (CC) section with 🎙️ Voice Input (Web Speech API) & Chinese -> English Translation button.
- Build Present Illness / HPI section with 🎙️ Voice Input, Translation button, and LQQOPERA quick preset chips.
- Build Past Medical History (PMH), Allergies, ROS, Physical Examination (PE), and Assessment & Plan (A&P) input controls.

**Step 2: Implement Client JavaScript & Speech Recognition**
- Connect `webkitSpeechRecognition` for Chinese voice input.
- Wire translation button to call `google.script.run.translateChineseToEnglish(text)`.
- Build real-time text synthesis engine to render formatted English Admission Note in live preview panel.
- Wire Save & Export button to call `google.script.run.saveAdmissionNoteRecord(data)` and show modal popup with Google Doc, Word, and PDF download links.

**Step 3: Styling & Polish**
- Ensure sleek Glassmorphism dark/light visual style, mobile responsiveness, micro-animations, loading states, and notification toasts.

---

### Task 3: Verify Apps Script Configuration & System Integration

**Files:**
- Check: `G:\我的雲端硬碟\2026 Google Spark\appsscript.json`
- Check: `G:\我的雲端硬碟\2026 Google Spark\.clasp.json`
- Update: `G:\我的雲端硬碟\2026 Google Spark\01_專案文件\Clinical_Examination_System_Guide.md`

**Step 1: Check GAS appsscript.json scopes and webapp configuration**
- Ensure necessary Drive, Docs, Sheets, and Translation scopes are declared if needed.

**Step 2: Update documentation**
- Document the new Admission Note module in `Clinical_Examination_System_Guide.md`.

---

### Task 4: Complete Implementation Verification & Final Audit

**Step 1: Audit all functions, event handlers, and export links**
- Verify code completeness and lack of placeholders.
- Verify speech recognition fallback for browsers without Web Speech API.
