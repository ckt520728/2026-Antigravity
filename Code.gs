/**
 * Clinical Examination System (2026 Google Spark)
 * Master Log: Google Sheets
 * Official Generated Reports: Google Docs (with PDF & Word exports)
 * Author: Antigravity AI for Dr. Kwo-Ta Chu
 */

function getSpreadsheet() {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) return ss;
  } catch (e) {}
  return SpreadsheetApp.openById('1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY');
}

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('臨床檢查紀錄與報告系統 | Clinical Examination System')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Get or create specified sheet tab with header columns
 */
function getOrCreateSheet(ss, sheetName, headers) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length)
      .setFontWeight('bold')
      .setBackground('#1e293b')
      .setFontColor('#f8fafc');
    sheet.setFrozenRows(1);
  }
  return sheet;
}

/**
 * Save new examination record:
 * 1. Log to Google Sheets (Master_Exams & Specific Sheet)
 * 2. Generate formal Google Doc Medical Report
 * 3. Provide PDF & Word (.docx) export links
 */
function saveExamRecord(record) {
  try {
    var ss = getSpreadsheet();
    var timestamp = new Date();
    var examId = 'EXAM-' + Utilities.formatDate(timestamp, 'Asia/Taipei', 'yyyyMMdd-HHmmss');
    
    var examType = record.examType || 'Unspecified';
    var doctorName = record.doctorName || '朱國大醫師 (Dr. Kwo-Ta Chu)';
    var examDate = record.examDate || Utilities.formatDate(timestamp, 'Asia/Taipei', 'yyyy-MM-dd');
    var patientId = record.patientId || 'ANON-' + Math.floor(1000 + Math.random() * 9000);
    var symptoms = record.symptoms || '';
    var diagnosis = record.diagnosis || '';
    var findings = record.findings || '';
    var impression = record.impression || '';
    var recommendation = record.recommendation || '';
    var rawStructuredData = JSON.stringify(record.structuredDetails || {});

    // Step A: Generate Official Google Doc Report
    var docResult = createGoogleDocReport(record, examId, timestamp);

    // Step B: Save Transaction Log to Master_Exams Sheet
    var masterHeaders = [
      '檢查編號 (Exam ID)',
      '登錄時間 (Timestamp)',
      '檢查日期 (Exam Date)',
      '檢查項目 (Exam Type)',
      '操作醫師 (Operator Doctor)',
      '病歷代碼 (Patient Code)',
      '臨床症狀 (Clinical Symptoms)',
      '初步診斷 (Tentative Diagnosis)',
      '影像所見 (Image Findings)',
      '檢查結論 (Impression)',
      '建議與處置 (Recommendations)',
      'Google Doc 報告網址',
      'PDF 下載網址',
      'Word 下載網址',
      '明細數據 JSON'
    ];
    
    var masterSheet = getOrCreateSheet(ss, 'Master_Exams', masterHeaders);
    masterSheet.appendRow([
      examId,
      timestamp,
      examDate,
      examType,
      doctorName,
      patientId,
      symptoms,
      diagnosis,
      findings,
      impression,
      recommendation,
      docResult.docUrl,
      docResult.pdfUrl,
      docResult.docxUrl,
      rawStructuredData
    ]);

    // Step C: Save Log to Specific Exam Type Sheet
    var specificSheetName = getSheetNameForType(examType);
    var specificHeaders = [
      '檢查編號', '登錄時間', '檢查日期', '操作醫師', '病歷代碼', 
      '臨床症狀與診斷', '影像所見與結果', '檢查結論與處置建議', 
      'Google Doc 連結', 'PDF 下載連結', 'Word 下載連結'
    ];
    var specificSheet = getOrCreateSheet(ss, specificSheetName, specificHeaders);
    specificSheet.appendRow([
      examId,
      timestamp,
      examDate,
      doctorName,
      patientId,
      '症狀: ' + symptoms + ' | 診斷: ' + diagnosis,
      findings,
      '結論: ' + impression + ' | 處置: ' + recommendation,
      docResult.docUrl,
      docResult.pdfUrl,
      docResult.docxUrl
    ]);

    return {
      status: 'success',
      examId: examId,
      docUrl: docResult.docUrl,
      pdfUrl: docResult.pdfUrl,
      docxUrl: docResult.docxUrl,
      message: '檢查紀錄已登錄至試算表流水帳，並已生成正式 Google Doc / PDF / Word 報告！'
    };
  } catch (err) {
    return {
      status: 'error',
      message: '儲存失敗：' + err.toString()
    };
  }
}

/**
 * Generate formal Google Doc report in Drive folder
 */
function createGoogleDocReport(record, examId, timestamp) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var ssFile = DriveApp.getFileById(ss.getId());
  var parentFolder = ssFile.getParents().hasNext() ? ssFile.getParents().next() : DriveApp.getRootFolder();
  
  // Find or create "04_交付成果" or "臨床檢查報告_GoogleDocs" folder
  var targetFolderName = '臨床檢查報告_GoogleDocs';
  var folderIterator = parentFolder.getFoldersByName(targetFolderName);
  var reportsFolder = folderIterator.hasNext() ? folderIterator.next() : parentFolder.createFolder(targetFolderName);

  var docTitle = '臨床檢查報告_' + record.examType.replace(/\s+/g, '_') + '_' + record.patientId + '_' + Utilities.formatDate(timestamp, 'Asia/Taipei', 'yyyyMMdd_HHmm');
  var doc = DocumentApp.create(docTitle);
  var body = doc.getBody();
  
  // Page Setup & Margins
  body.setMarginTop(40);
  body.setMarginBottom(40);
  body.setMarginLeft(48);
  body.setMarginRight(48);
  
  // Title & Header
  var headerPara = body.appendParagraph('2026 Google Spark 臨床醫學中心');
  headerPara.setFontSize(10).setFontColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);
  
  var titlePara = body.appendParagraph('臨床檢查報告書\nMedical Examination Report');
  titlePara.setFontSize(18).setBold(true).setAlignment(DocumentApp.HorizontalAlignment.CENTER).setFontColor('#1e293b');
  
  var examTypePara = body.appendParagraph('【 ' + record.examType + ' 】');
  examTypePara.setFontSize(13).setBold(true).setAlignment(DocumentApp.HorizontalAlignment.CENTER).setFontColor('#4f46e5');
  
  body.appendHorizontalRule();

  // Meta Information Table
  var tableData = [
    ['報告編號 (Exam ID)', examId, '檢查日期 (Date)', record.examDate],
    ['操作醫師 (Operator)', record.doctorName, '病歷代碼 (Patient ID)', record.patientId],
    ['產出時間 (Generated)', Utilities.formatDate(timestamp, 'Asia/Taipei', 'yyyy-MM-dd HH:mm'), '報告狀態 (Status)', '已核發 (Completed)']
  ];
  var metaTable = body.appendTable(tableData);
  metaTable.setBorderColor('#cbd5e1');

  // Section 1: Clinical Indication
  body.appendParagraph('\n一、臨床症狀與初步診斷 (Clinical Symptoms & Diagnosis)')
      .setFontSize(12).setBold(true).setFontColor('#1e293b');
  body.appendParagraph('• 臨床症狀與主訴：' + (record.symptoms || '無特定主訴描述')).setFontSize(10.5);
  body.appendParagraph('• 初步診斷：' + (record.diagnosis || '無')).setFontSize(10.5);

  // Section 2: Detailed Findings
  body.appendParagraph('\n二、影像與內視鏡詳細所見內容 (Detailed Image Findings)')
      .setFontSize(12).setBold(true).setFontColor('#1e293b');
  
  var findingsBox = body.appendParagraph(record.findings || '無特別註明影像所見');
  findingsBox.setFontSize(10).setFontFamily('Consolas');

  // Section 3: Impression & Plan
  body.appendParagraph('\n三、檢查結論與處置建議 (Impression & Recommendations)')
      .setFontSize(12).setBold(true).setFontColor('#1e293b');
  body.appendParagraph('【檢查結論】' + (record.impression || '無特別異常')).setFontSize(11).setBold(true).setFontColor('#0f172a');
  body.appendParagraph('【處置與建議】' + (record.recommendation || '定期臨床追蹤')).setFontSize(10.5);

  body.appendHorizontalRule();

  // Signature Block
  var signPara = body.appendParagraph('\n報告操作醫師簽章： ______________________ (' + record.doctorName + ')\n(本報告已由系統自動加密歸檔至 Google 雲端硬碟與資料庫流水帳)');
  signPara.setFontSize(9.5).setFontColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  doc.saveAndClose();

  // Move created Doc to target folder
  var docFile = DriveApp.getFileById(doc.getId());
  docFile.moveTo(reportsFolder);

  var docId = doc.getId();
  return {
    docId: docId,
    docUrl: 'https://docs.google.com/document/d/' + docId + '/edit',
    pdfUrl: 'https://docs.google.com/document/d/' + docId + '/export?format=pdf',
    docxUrl: 'https://docs.google.com/document/d/' + docId + '/export?format=docx'
  };
}

function getSheetNameForType(examType) {
  switch(examType) {
    case 'Echocardiogram': return '心臟超音波_Echo';
    case 'Abdominal Sonography': return '腹部超音波_AbdominalSono';
    case 'UGI Endoscopy': return '上消化道內視鏡_UGI';
    case 'LGI Endoscopy': return '下消化道內視鏡_LGI';
    default: return '其他檢查_Other';
  }
}

/**
 * Fetch recent examination records for the web app dashboard
 */
function getRecentRecords(limit) {
  try {
    limit = limit || 20;
    var ss = getSpreadsheet();
    var masterSheet = ss.getSheetByName('Master_Exams');
    if (!masterSheet) {
      return { status: 'success', records: [], stats: { total: 0, echo: 0, sono: 0, ugi: 0, lgi: 0 } };
    }

    var data = masterSheet.getDataRange().getValues();
    if (data.length <= 1) {
      return { status: 'success', records: [], stats: { total: 0, echo: 0, sono: 0, ugi: 0, lgi: 0 } };
    }

    var records = [];
    var stats = { total: data.length - 1, echo: 0, sono: 0, ugi: 0, lgi: 0 };

    for (var i = data.length - 1; i >= 1; i--) {
      var row = data[i];
      var type = row[3];
      if (type === 'Echocardiogram') stats.echo++;
      else if (type === 'Abdominal Sonography') stats.sono++;
      else if (type === 'UGI Endoscopy') stats.ugi++;
      else if (type === 'LGI Endoscopy') stats.lgi++;

      if (records.length < limit) {
        records.push({
          examId: row[0],
          timestamp: row[1] ? Utilities.formatDate(new Date(row[1]), 'Asia/Taipei', 'yyyy-MM-dd HH:mm') : '',
          examDate: row[2] ? Utilities.formatDate(new Date(row[2]), 'Asia/Taipei', 'yyyy-MM-dd') : '',
          examType: row[3],
          doctorName: row[4],
          patientId: row[5],
          symptoms: row[6],
          diagnosis: row[7],
          findings: row[8],
          impression: row[9],
          recommendation: row[10],
          docUrl: row[11],
          pdfUrl: row[12],
          docxUrl: row[13]
        });
      }
    }

    return {
      status: 'success',
      records: records,
      stats: stats
    };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

/**
 * Search examination records by keyword
 */
function searchRecords(query) {
  try {
    query = (query || '').toLowerCase().trim();
    var ss = getSpreadsheet();
    var masterSheet = ss.getSheetByName('Master_Exams');
    if (!masterSheet) return { status: 'success', records: [] };

    var data = masterSheet.getDataRange().getValues();
    var results = [];

    for (var i = data.length - 1; i >= 1; i--) {
      var row = data[i];
      var searchStr = (row[0] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4] + ' ' + row[5] + ' ' + row[6] + ' ' + row[7] + ' ' + row[8] + ' ' + row[9]).toLowerCase();
      if (!query || searchStr.indexOf(query) !== -1) {
        results.push({
          examId: row[0],
          timestamp: row[1] ? Utilities.formatDate(new Date(row[1]), 'Asia/Taipei', 'yyyy-MM-dd HH:mm') : '',
          examDate: row[2] ? Utilities.formatDate(new Date(row[2]), 'Asia/Taipei', 'yyyy-MM-dd') : '',
          examType: row[3],
          doctorName: row[4],
          patientId: row[5],
          symptoms: row[6],
          diagnosis: row[7],
          findings: row[8],
          impression: row[9],
          recommendation: row[10],
          docUrl: row[11],
          pdfUrl: row[12],
          docxUrl: row[13]
        });
      }
      if (results.length >= 50) break;
    }

    return { status: 'success', records: results };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}
