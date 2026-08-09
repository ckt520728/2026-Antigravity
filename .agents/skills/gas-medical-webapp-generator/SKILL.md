---
name: gas-medical-webapp-generator
description: Use when building a Google Apps Script (GAS) doctor interactive web application connected to Google Sheets (for master log & transaction audit trail) and Google Docs/Word/PDF (for medical document generation).
---

# GAS Medical WebApp Generator

## Overview

Build high-performance, interactive clinical web applications for physicians using Google Apps Script (GAS). Integrates structured option matrices with numeric input blanks into a 3-tier architecture:
1. **Interactive Web App**: HTML5/JS frontend for rapid medical report entry with real-time text synthesis.
2. **Google Sheets Master Log**: Transactional audit log recording operator, date/time, patient info, findings, and doc links.
3. **Google Docs / Word / PDF Report Generation**: Formal medical documents created on-the-fly with direct export URLs.

---

## When to Use

- Building clinical examination reporting tools (Echocardiogram, Sonography, Endoscopy, Radiology, EKG, etc.).
- Needing real-time synthesis of medical text from checkboxes, dropdowns, and numeric input fields.
- Requiring an audit log in Google Sheets alongside downloadable formal reports in Google Docs, Word (`.docx`), or PDF (`.pdf`).
- Deploying zero-cost cloud web tools for medical teams via `clasp`.

---

## Three-Tier Architecture Pattern

```
[ Frontend: Web App UI ] ---> google.script.run ---> [ Backend: Code.gs ]
                                                          |
                      +-----------------------------------+-----------------------------------+
                      |                                                                       |
        [ Database: Google Sheets ]                                           [ Reports: Google Docs Folder ]
   (Master_Exams & Specialized Tabs)                                     (Auto-formatted Document Generation)
                                                                                      |
                                                                        +-------------+-------------+
                                                                        |                           |
                                                                [ Export PDF ]              [ Export Word ]
                                                             (/export?format=pdf)        (/export?format=docx)
```

---

## Quick Implementation Guide

### 1. `appsscript.json` Configuration
Ensure the Web App deployment configuration permits anonymous or organizational access without requiring complex auth flows:

```json
{
  "timeZone": "Asia/Taipei",
  "dependencies": {},
  "exceptionLogging": "CLOUD",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE"
  }
}
```

### 2. Backend (`Code.gs`) Key Snippets

#### A. Document Creation & Export URL Generator
```javascript
function createGoogleDocReport(data) {
  var folderName = "臨床檢查報告_GoogleDocs";
  var folders = DriveApp.getFoldersByName(folderName);
  var folder = folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);
  
  var docName = data.examType + " 報告_" + data.patientId + "_" + Utilities.formatDate(new Date(), "Asia/Taipei", "yyyyMMdd_HHmm");
  var doc = DocumentApp.create(docName);
  var docId = doc.getId();
  var body = doc.getBody();
  
  // Format Header
  var header = body.appendParagraph(data.examType + " 醫療檢查報告書");
  header.setHeading(DocumentApp.ParagraphHeading.HEADING1).setAlignment(DocumentApp.HorizontalAlignment.CENTER);
  
  // Patient & Operator Metadata Table
  var tableData = [
    ["病歷號 / 姓名", data.patientId || "-", "檢查日期", data.examDate || "-"],
    ["檢查項目", data.examType || "-", "操作醫師", data.doctorName || "-"]
  ];
  body.appendTable(tableData);
  
  // Report Sections
  body.appendParagraph("\n一、臨床診斷與症狀").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph(data.diagnosis || "無特殊描述");
  
  body.appendParagraph("\n二、檢查詳細所見 (Findings)").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph(data.findings || "無特殊異常發現");
  
  body.appendParagraph("\n三、檢查結論與建議 (Impression)").setHeading(DocumentApp.ParagraphHeading.HEADING2);
  body.appendParagraph(data.impression || "無特殊建議");
  
  doc.saveAndClose();
  
  // Move file to target folder
  var file = DriveApp.getFileById(docId);
  folder.addFile(file);
  DriveApp.getRootFolder().removeFile(file);
  
  return {
    docUrl: "https://docs.google.com/document/d/" + docId + "/edit",
    pdfUrl: "https://docs.google.com/document/d/" + docId + "/export?format=pdf",
    wordUrl: "https://docs.google.com/document/d/" + docId + "/export?format=docx"
  };
}
```

#### B. Master Sheet Audit Trail Logging
```javascript
function saveExamRecord(formData) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var masterSheet = ss.getSheetByName("Master_Exams") || ss.insertSheet("Master_Exams");
  
  if (masterSheet.getLastRow() === 0) {
    masterSheet.appendRow([
      "時間戳記", "操作醫師", "檢查日期", "病歷號/姓名", "檢查類別", 
      "臨床診斷", "檢查所見", "檢查結論", "Google Doc 連結", "PDF 連結", "Word 連結"
    ]);
  }
  
  var docLinks = createGoogleDocReport(formData);
  
  masterSheet.appendRow([
    new Date(),
    formData.doctorName,
    formData.examDate,
    formData.patientId,
    formData.examType,
    formData.diagnosis,
    formData.findings,
    formData.impression,
    docLinks.docUrl,
    docLinks.pdfUrl,
    docLinks.wordUrl
  ]);
  
  return { status: "success", docLinks: docLinks };
}
```

---

## Deployment Workflow with Clasp

```bash
# 1. Push source files to GAS
npx -y @google/clasp push -f

# 2. Create new deployment version
npx -y @google/clasp create-deployment --description "v1.0 Release"

# 3. Retrieve Live Executable Web App URL
npx -y @google/clasp open-web-app <deploymentId> --json
```

---

## Common Pitfalls & Solutions

| Issue / Pitfall | Cause | Solution |
| :--- | :--- | :--- |
| `User has not enabled the Google Apps Script API` | GAS API disabled globally in Google Account | User must visit `https://script.google.com/home/usersettings` and switch API to ON. |
| Code changes don't appear in live Web App | Web App URLs are pinned to explicit Deployment IDs | Run `clasp create-deployment` after `clasp push` to generate an updated executable URL. |
| File permission errors when saving Google Docs | Document created in root folder without folder permissions | Create file via `DocumentApp.create()`, move to target Drive folder via `folder.addFile(file)`, then remove from root folder. |
| `Cannot read property 'appendRow' of null` | Target sheet tab doesn't exist | Use `ss.getSheetByName(name) || ss.insertSheet(name)` pattern to auto-create missing tabs. |
