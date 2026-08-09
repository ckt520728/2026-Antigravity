/**
 * Clinical Documentation & Admission Note System — v6.0
 * 2026 Google Spark x Google Apps Script Cloud Engine
 *
 * Master Log        : Google Sheets (Master_AdmissionNotes / Master_Exams + per-type tabs)
 * Official Reports  : Google Docs (with PDF & Word export URLs)
 * Access Control    : passcode gate + stateless signed session token (see AUTH section)
 *
 * Author: Antigravity AI / Claude Code for Dr. Kwo-Ta Chu
 *
 * IMPORTANT — every client-callable function takes the session `token` as its FIRST
 * argument. Adding a new callable function? Guard it with `authFail_(token)`.
 */

var SPREADSHEET_ID = '1UIJZdR7rPHOPlgNC6w8g7SV3AL0kIW3mGSGRkJZWfWY';
var TZ = 'Asia/Taipei';

/* ==========================================================================
 * AUTH — passcode gate
 *
 * The passcode is never stored in source. It lives in Script Properties as a
 * salted SHA-256 hash. To change it, open the Apps Script editor, select
 * `setAppPasscode` in the function dropdown, edit NEW_PASSCODE below, Run once.
 *
 * Session tokens are stateless and signed: "<expiryMillis>.<sha256(salt|exp|hash)>".
 * They therefore survive CacheService eviction, and changing the passcode
 * instantly invalidates every outstanding token.
 * ========================================================================== */

/**
 * MASTER SWITCH for the passcode gate.
 *
 *   false — anyone with the link goes straight into the app (current setting).
 *   true  — the login screen is shown and every data function requires a valid token.
 *
 * To turn the gate back on later:
 *   1. set AUTH_ENABLED = true here
 *   2. run `setAppPasscode` once from the editor to set the passcode
 *   3. clasp push + redeploy with -i <deploymentId>
 * The whole auth implementation below stays intact while the switch is off,
 * so re-enabling is a one-line change.
 */
var AUTH_ENABLED = false;

var PROP_PASSCODE_HASH = 'APP_PASSCODE_HASH';
var PROP_PASSCODE_SALT = 'APP_PASSCODE_SALT';
var DEFAULT_PASSCODE = 'Spark2026';          // used only until setAppPasscode() is run
var SESSION_HOURS = 12;
var MAX_FAILED_ATTEMPTS = 8;                  // per 15 min window

/** Client asks this on boot to decide whether to show the login screen. */
function getAuthConfig() {
  return { status: 'success', authEnabled: AUTH_ENABLED };
}

/**
 * Run this manually from the Apps Script editor to change the entry passcode.
 * Edit NEW_PASSCODE, press Run, then check the execution log.
 */
function setAppPasscode() {
  var NEW_PASSCODE = '請在這裡填入新密碼';

  if (!NEW_PASSCODE || NEW_PASSCODE === '請在這裡填入新密碼') {
    Logger.log('❌ 請先把 NEW_PASSCODE 改成你要的密碼，再按 Run。');
    return;
  }
  if (NEW_PASSCODE.length < 6) {
    Logger.log('❌ 密碼太短，請至少 6 個字元。');
    return;
  }
  var props = PropertiesService.getScriptProperties();
  props.setProperty(PROP_PASSCODE_HASH, sha256Hex_(getSalt_() + '::' + NEW_PASSCODE));
  Logger.log('✅ 密碼已更新。所有已登入的裝置會立刻登出，需要用新密碼重新進入。');
}

function sha256Hex_(str) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, str, Utilities.Charset.UTF_8);
  var hex = '';
  for (var i = 0; i < bytes.length; i++) {
    hex += ('0' + (bytes[i] & 0xFF).toString(16)).slice(-2);
  }
  return hex;
}

function getSalt_() {
  var props = PropertiesService.getScriptProperties();
  var salt = props.getProperty(PROP_PASSCODE_SALT);
  if (!salt) {
    salt = Utilities.getUuid();
    props.setProperty(PROP_PASSCODE_SALT, salt);
  }
  return salt;
}

function getPasscodeHash_() {
  var props = PropertiesService.getScriptProperties();
  var hash = props.getProperty(PROP_PASSCODE_HASH);
  if (!hash) {
    hash = sha256Hex_(getSalt_() + '::' + DEFAULT_PASSCODE);
    props.setProperty(PROP_PASSCODE_HASH, hash);
  }
  return hash;
}

function issueToken_() {
  var exp = new Date().getTime() + SESSION_HOURS * 3600 * 1000;
  return exp + '.' + sha256Hex_(getSalt_() + '|' + exp + '|' + getPasscodeHash_());
}

function isValidToken_(token) {
  if (!token) return false;
  var parts = String(token).split('.');
  if (parts.length !== 2) return false;
  var exp = parseInt(parts[0], 10);
  if (!exp || exp < new Date().getTime()) return false;
  return sha256Hex_(getSalt_() + '|' + exp + '|' + getPasscodeHash_()) === parts[1];
}

/** Returns an error envelope when the token is bad, otherwise null. */
function authFail_(token) {
  if (!AUTH_ENABLED) return null;
  if (isValidToken_(token)) return null;
  return { status: 'auth_required', message: '登入已逾期，請重新輸入密碼。' };
}

function attemptKey_() {
  var who = '';
  try { who = Session.getTemporaryActiveUserKey() || ''; } catch (e) {}
  return 'login_fail_' + (who || 'anon');
}

/**
 * Client entry point for the login screen.
 * @param {string} passcode
 * @return {{status:string, token:(string|undefined), expiresAt:(number|undefined), message:(string|undefined)}}
 */
function authenticate(passcode) {
  if (!AUTH_ENABLED) {
    return { status: 'success', token: '', expiresAt: 0, message: '密碼保護目前為關閉狀態' };
  }
  var cache = CacheService.getScriptCache();
  var key = attemptKey_();
  var fails = parseInt(cache.get(key) || '0', 10);

  if (fails >= MAX_FAILED_ATTEMPTS) {
    return { status: 'error', message: '嘗試次數過多，請等 15 分鐘後再試。' };
  }

  if (sha256Hex_(getSalt_() + '::' + String(passcode || '')) !== getPasscodeHash_()) {
    cache.put(key, String(fails + 1), 900);
    Utilities.sleep(700); // slow down brute force
    return { status: 'error', message: '密碼不正確。' };
  }

  cache.remove(key);
  var token = issueToken_();
  return {
    status: 'success',
    token: token,
    expiresAt: parseInt(token.split('.')[0], 10),
    message: '登入成功'
  };
}

/** Lets a returning browser confirm a stored token is still good. */
function verifySession(token) {
  if (!AUTH_ENABLED) return { status: 'success', expiresAt: 0 };
  return isValidToken_(token)
    ? { status: 'success', expiresAt: parseInt(String(token).split('.')[0], 10) }
    : { status: 'auth_required' };
}

/* ==========================================================================
 * INFRASTRUCTURE
 * ========================================================================== */

function getSpreadsheet() {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    if (ss) return ss;
  } catch (e) {}
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}

function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('臨床醫療紀錄與報告系統 | Clinical Documentation System')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

/**
 * Get or create a sheet tab. Headers are only written when the tab is brand new,
 * so existing logs keep their column order — append new columns at the END of
 * the header array, never in the middle.
 */
function getOrCreateSheet(ss, sheetName, headers) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) sheet = ss.insertSheet(sheetName);
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

/** Resolve the Drive folder that holds this project's generated reports. */
function getReportsFolder_(folderName) {
  var ss = getSpreadsheet();
  var ssFile = DriveApp.getFileById(ss.getId());
  var parentFolder = ssFile.getParents().hasNext() ? ssFile.getParents().next() : DriveApp.getRootFolder();
  var it = parentFolder.getFoldersByName(folderName);
  return it.hasNext() ? it.next() : parentFolder.createFolder(folderName);
}

function docLinks_(docId) {
  return {
    docId: docId,
    docUrl: 'https://docs.google.com/document/d/' + docId + '/edit',
    pdfUrl: 'https://docs.google.com/document/d/' + docId + '/export?format=pdf',
    docxUrl: 'https://docs.google.com/document/d/' + docId + '/export?format=docx'
  };
}

function getSheetNameForType(examType) {
  switch (examType) {
    case 'Echocardiogram': return '心臟超音波_Echo';
    case 'Abdominal Sonography': return '腹部超音波_AbdominalSono';
    case 'UGI Endoscopy': return '上消化道內視鏡_UGI';
    case 'LGI Endoscopy': return '下消化道內視鏡_LGI';
    default: return '其他檢查_Other';
  }
}

/* ==========================================================================
 * CLINICAL EXAM REPORTS
 * ========================================================================== */

/**
 * Save an examination record: Sheets log + Google Doc + PDF/Word links.
 * @param {string} token session token
 * @param {Object} record
 */
function saveExamRecord(token, record) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    var ss = getSpreadsheet();
    var timestamp = new Date();
    var examId = 'EXAM-' + Utilities.formatDate(timestamp, TZ, 'yyyyMMdd-HHmmss');

    record = record || {};
    var examType = record.examType || 'Unspecified';
    var doctorName = record.doctorName || '朱國大醫師 (Dr. Kwo-Ta Chu)';
    var examDate = record.examDate || Utilities.formatDate(timestamp, TZ, 'yyyy-MM-dd');
    var patientId = record.patientId || 'ANON-' + Math.floor(1000 + Math.random() * 9000);
    var patientName = record.patientName || '';
    var symptoms = record.symptoms || '';
    var diagnosis = record.diagnosis || '';
    var findings = record.findings || '';
    var impression = record.impression || '';
    var recommendation = record.recommendation || '';
    var indication = record.indication || '';
    var technique = record.technique || '';
    var comparison = record.comparison || '';
    var rawStructuredData = JSON.stringify(record.structuredDetails || {});

    var docResult = createGoogleDocReport(record, examId, timestamp);

    // Columns 1-15 are the v5.0 layout and MUST stay in place; 16-19 are v6.0 additions.
    var masterHeaders = [
      '檢查編號 (Exam ID)', '登錄時間 (Timestamp)', '檢查日期 (Exam Date)', '檢查項目 (Exam Type)',
      '操作醫師 (Operator Doctor)', '病歷代碼 (Patient Code)', '臨床症狀 (Clinical Symptoms)',
      '初步診斷 (Tentative Diagnosis)', '影像所見 (Image Findings)', '檢查結論 (Impression)',
      '建議與處置 (Recommendations)', 'Google Doc 報告網址', 'PDF 下載網址', 'Word 下載網址',
      '明細數據 JSON',
      '病患姓名 (Patient Name)', '臨床適應症 (Indication)', '檢查技術 (Technique)', '比較影像 (Comparison)'
    ];

    var masterSheet = getOrCreateSheet(ss, 'Master_Exams', masterHeaders);
    masterSheet.appendRow([
      examId, timestamp, examDate, examType, doctorName, patientId, symptoms, diagnosis,
      findings, impression, recommendation,
      docResult.docUrl, docResult.pdfUrl, docResult.docxUrl, rawStructuredData,
      patientName, indication, technique, comparison
    ]);

    var specificHeaders = [
      '檢查編號', '登錄時間', '檢查日期', '操作醫師', '病歷代碼',
      '臨床症狀與診斷', '影像所見與結果', '檢查結論與處置建議',
      'Google Doc 連結', 'PDF 下載連結', 'Word 下載連結'
    ];
    var specificSheet = getOrCreateSheet(ss, getSheetNameForType(examType), specificHeaders);
    specificSheet.appendRow([
      examId, timestamp, examDate, doctorName, patientId,
      '症狀: ' + symptoms + ' | 診斷: ' + diagnosis,
      findings,
      '結論: ' + impression + ' | 處置: ' + recommendation,
      docResult.docUrl, docResult.pdfUrl, docResult.docxUrl
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
    return { status: 'error', message: '儲存失敗：' + err.toString() };
  }
}

/**
 * Generate the formal Google Doc exam report.
 * Section order follows the RSNA structured-report layout:
 * demographics → clinical history/indication → technique → comparison → findings → impression → recommendation.
 */
function createGoogleDocReport(record, examId, timestamp) {
  var reportsFolder = getReportsFolder_('臨床檢查報告_GoogleDocs');

  var docTitle = '臨床檢查報告_' + String(record.examType || 'Exam').replace(/\s+/g, '_') +
    '_' + (record.patientId || 'ANON') + '_' + Utilities.formatDate(timestamp, TZ, 'yyyyMMdd_HHmm');
  var doc = DocumentApp.create(docTitle);
  var body = doc.getBody();

  body.setMarginTop(40).setMarginBottom(40).setMarginLeft(48).setMarginRight(48);

  body.appendParagraph('2026 Google Spark 臨床醫學中心')
    .setFontSize(10).setForegroundColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  body.appendParagraph('臨床檢查報告書\nMedical Examination Report')
    .setFontSize(18).setBold(true).setAlignment(DocumentApp.HorizontalAlignment.CENTER).setForegroundColor('#1e293b');

  body.appendParagraph('【 ' + (record.examType || '') + ' 】')
    .setFontSize(13).setBold(true).setAlignment(DocumentApp.HorizontalAlignment.CENTER).setForegroundColor('#4f46e5');

  body.appendHorizontalRule();

  var metaTable = body.appendTable([
    ['報告編號 (Exam ID)', examId, '檢查日期 (Date)', record.examDate || ''],
    ['病患姓名 (Name)', record.patientName || '—', '病歷代碼 (Patient ID)', record.patientId || ''],
    ['操作醫師 (Operator)', record.doctorName || '', '報告狀態 (Status)', '已核發 (Completed)'],
    ['產出時間 (Generated)', Utilities.formatDate(timestamp, TZ, 'yyyy-MM-dd HH:mm'), '', '']
  ]);
  metaTable.setBorderColor('#cbd5e1');

  body.appendParagraph('\n一、臨床適應症與病史 (Clinical Indication & History)')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('• 臨床適應症：' + (record.indication || record.symptoms || '無特定適應症描述')).setFontSize(10.5);
  body.appendParagraph('• 臨床症狀與主訴：' + (record.symptoms || '無')).setFontSize(10.5);
  body.appendParagraph('• 初步診斷：' + (record.diagnosis || '無')).setFontSize(10.5);

  body.appendParagraph('\n二、檢查技術與比較影像 (Technique & Comparison)')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('• 檢查技術：' + (record.technique || '依標準作業流程執行')).setFontSize(10.5);
  body.appendParagraph('• 比較影像：' + (record.comparison || 'No prior study available for comparison.')).setFontSize(10.5);

  body.appendParagraph('\n三、詳細所見 (Findings)')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph(record.findings || '無特別註明影像所見')
    .setFontSize(10).setFontFamily('Consolas');

  body.appendParagraph('\n四、檢查結論與處置建議 (Impression & Recommendations)')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('【檢查結論】' + (record.impression || '無特別異常'))
    .setFontSize(11).setBold(true).setForegroundColor('#0f172a');
  body.appendParagraph('【處置與建議】' + (record.recommendation || '定期臨床追蹤')).setFontSize(10.5);

  body.appendHorizontalRule();

  body.appendParagraph('\n報告操作醫師簽章： ______________________ (' + (record.doctorName || '') + ')\n' +
    '(本報告由系統自動歸檔至 Google 雲端硬碟與資料庫流水帳)')
    .setFontSize(9.5).setForegroundColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  doc.saveAndClose();
  DriveApp.getFileById(doc.getId()).moveTo(reportsFolder);
  return docLinks_(doc.getId());
}

/**
 * Recent exam records + dashboard counters.
 * @param {string} token
 * @param {number} limit
 */
function getRecentRecords(token, limit) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    limit = limit || 20;
    var ss = getSpreadsheet();
    var masterSheet = ss.getSheetByName('Master_Exams');
    var empty = { status: 'success', records: [], stats: { total: 0, echo: 0, sono: 0, ugi: 0, lgi: 0 } };
    if (!masterSheet) return empty;

    var data = masterSheet.getDataRange().getValues();
    if (data.length <= 1) return empty;

    var records = [];
    var stats = { total: data.length - 1, echo: 0, sono: 0, ugi: 0, lgi: 0 };

    for (var i = data.length - 1; i >= 1; i--) {
      var row = data[i];
      var type = row[3];
      if (type === 'Echocardiogram') stats.echo++;
      else if (type === 'Abdominal Sonography') stats.sono++;
      else if (type === 'UGI Endoscopy') stats.ugi++;
      else if (type === 'LGI Endoscopy') stats.lgi++;
      if (records.length < limit) records.push(mapExamRow_(row));
    }
    return { status: 'success', records: records, stats: stats };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

function mapExamRow_(row) {
  return {
    examId: row[0],
    timestamp: row[1] ? Utilities.formatDate(new Date(row[1]), TZ, 'yyyy-MM-dd HH:mm') : '',
    examDate: row[2] ? Utilities.formatDate(new Date(row[2]), TZ, 'yyyy-MM-dd') : '',
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
    docxUrl: row[13],
    patientName: row[15] || '',
    indication: row[16] || ''
  };
}

/**
 * Keyword search across exam records.
 * @param {string} token
 * @param {string} query
 */
function searchRecords(token, query) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    query = (query || '').toLowerCase().trim();
    var ss = getSpreadsheet();
    var masterSheet = ss.getSheetByName('Master_Exams');
    if (!masterSheet) return { status: 'success', records: [] };

    var data = masterSheet.getDataRange().getValues();
    var results = [];

    for (var i = data.length - 1; i >= 1; i--) {
      var row = data[i];
      var searchStr = (row[0] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4] + ' ' + row[5] + ' ' +
        row[6] + ' ' + row[7] + ' ' + row[8] + ' ' + row[9] + ' ' + (row[15] || '')).toLowerCase();
      if (!query || searchStr.indexOf(query) !== -1) results.push(mapExamRow_(row));
      if (results.length >= 50) break;
    }
    return { status: 'success', records: results };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

/* ==========================================================================
 * TRANSLATION
 * ========================================================================== */

/**
 * Translate Chinese clinical dictation into English via the built-in LanguageApp.
 * @param {string} token
 * @param {string} text
 */
function translateChineseToEnglish(token, text) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    if (!text || String(text).trim() === '') return { status: 'success', translatedText: '' };
    return { status: 'success', originalText: text, translatedText: LanguageApp.translate(text, 'zh-TW', 'en') };
  } catch (err) {
    try {
      return { status: 'success', originalText: text, translatedText: LanguageApp.translate(text, '', 'en') };
    } catch (e2) {
      return { status: 'error', message: '翻譯失敗：' + err.toString() };
    }
  }
}

/* ==========================================================================
 * ADMISSION NOTES
 * ========================================================================== */

/**
 * Save an admission note: Sheets log + Google Doc + PDF/Word links.
 * @param {string} token
 * @param {Object} record
 */
function saveAdmissionNoteRecord(token, record) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    var ss = getSpreadsheet();
    var timestamp = new Date();
    var noteId = 'ADM-' + Utilities.formatDate(timestamp, TZ, 'yyyyMMdd-HHmmss');

    record = record || {};
    var doctorName = record.doctorName || '朱國大醫師 (Dr. Kwo-Ta Chu)';
    var examDate = record.examDate || Utilities.formatDate(timestamp, TZ, 'yyyy-MM-dd');
    var patientId = record.patientId || 'ANON-' + Math.floor(1000 + Math.random() * 9000);
    var patientName = record.patientName || 'Anonymous Patient';
    var ageGender = record.ageGender || 'Unspecified';
    var wardBed = record.wardBed || 'Outpatient/ER';
    var department = record.department || 'Nephrology / Internal Medicine';

    var docResult = createAdmissionNoteDocReport(record, noteId, timestamp);

    // Columns 1-18 are the v5.0 layout and MUST stay in place; 19-26 are v6.0 additions.
    var headers = [
      '病歷編號 (Note ID)', '登錄時間 (Timestamp)', '入院日期 (Admission Date)', '病歷號 (MRN)',
      '病患姓名 (Patient Name)', '年齡/性別 (Age/Gender)', '病房/床號 (Ward/Bed)',
      '主治醫師 (Attending Doctor)', '診斷科別 (Department)', '主訴 (Chief Complaint)',
      '現在病史 (Present Illness)', '過去病史與過敏 (PMH & Allergies)', '理學檢查 (Physical Exam)',
      '初步診斷 (Impression)', '治療計畫 (Plan)', 'Google Doc 網址', 'PDF 下載網址', 'Word 下載網址',
      '手術史 (Past Surgical History)', '目前用藥 (Current Medications)', '家族史 (Family History)',
      '個人社會史 (Social History)', '系統回顧 (Review of Systems)', '生命徵象 (Vital Signs)',
      '入院檢驗與影像 (Labs & Imaging)', '問題清單 JSON (Problem List)'
    ];

    var sheet = getOrCreateSheet(ss, 'Master_AdmissionNotes', headers);
    sheet.appendRow([
      noteId, timestamp, examDate, patientId, patientName, ageGender, wardBed,
      doctorName, department,
      record.chiefComplaint || '',
      record.presentIllness || '',
      'PMH: ' + (record.pastHistory || '') + ' | Allergy: ' + (record.allergies || 'NKDA'),
      record.physicalExam || '',
      record.impression || '',
      record.plan || '',
      docResult.docUrl, docResult.pdfUrl, docResult.docxUrl,
      record.surgicalHistory || '',
      record.medications || '',
      record.familyHistory || '',
      record.socialHistory || '',
      record.reviewOfSystems || '',
      record.vitalSigns || '',
      record.labsImaging || '',
      JSON.stringify(record.problemList || [])
    ]);

    return {
      status: 'success',
      noteId: noteId,
      docUrl: docResult.docUrl,
      pdfUrl: docResult.pdfUrl,
      docxUrl: docResult.docxUrl,
      message: '住院病歷紀錄已登錄至試算表，並已生成正式 Google Doc / PDF / Word 報告！'
    };
  } catch (err) {
    return { status: 'error', message: '住院病歷儲存失敗：' + err.toString() };
  }
}

/**
 * Generate the formal Google Doc admission note.
 * Section order follows the standard teaching-hospital H&P:
 * demographics → CC → HPI → PMH/PSH/Meds/Allergy → FHx/SHx → ROS → Vitals+PE → Labs → A&P.
 */
function createAdmissionNoteDocReport(record, noteId, timestamp) {
  var reportsFolder = getReportsFolder_('住院病歷報告_GoogleDocs');

  var docTitle = 'AdmissionNote_' + (record.patientId || 'ANON') + '_' +
    Utilities.formatDate(timestamp, TZ, 'yyyyMMdd_HHmm');
  var doc = DocumentApp.create(docTitle);
  var body = doc.getBody();

  body.setMarginTop(40).setMarginBottom(40).setMarginLeft(48).setMarginRight(48);

  body.appendParagraph('2026 Google Spark Medical Center — Admission Record')
    .setFontSize(9.5).setForegroundColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  body.appendParagraph('ADMISSION NOTE\n住院病歷紀錄書')
    .setFontSize(18).setBold(true).setAlignment(DocumentApp.HorizontalAlignment.CENTER).setForegroundColor('#0f172a');

  body.appendHorizontalRule();

  var metaTable = body.appendTable([
    ['Patient Name (姓名)', record.patientName || 'N/A', 'MRN / Chart No (病歷號)', record.patientId || 'N/A'],
    ['Age / Gender (年齡/性別)', record.ageGender || 'N/A', 'Admission Date (入院日期)', record.examDate || 'N/A'],
    ['Ward / Bed (病房床號)', record.wardBed || 'N/A', 'Attending Doctor (主治醫師)', record.doctorName || 'Dr. Kwo-Ta Chu'],
    ['Department (診斷科別)', record.department || 'Nephrology', 'Note Record ID (報告編號)', noteId],
    ['Informant (病史提供者)', record.informant || 'Patient', 'Reliability (可信度)', record.reliability || 'Reliable']
  ]);
  metaTable.setBorderColor('#cbd5e1');

  appendDocSection_(body, '1. CHIEF COMPLAINT (CC)', record.chiefComplaint || 'No chief complaint provided.');
  appendDocSection_(body, '2. HISTORY OF PRESENT ILLNESS (HPI)', record.presentIllness || 'No detailed history of present illness.');

  body.appendParagraph('\n3. PAST HISTORY, MEDICATIONS & ALLERGIES')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('• Past Medical History: ' + (record.pastHistory || 'Non-contributory.')).setFontSize(10.5);
  body.appendParagraph('• Past Surgical History: ' + (record.surgicalHistory || 'Denied.')).setFontSize(10.5);
  body.appendParagraph('• Current Medications: ' + (record.medications || 'None reported on admission.')).setFontSize(10.5);
  body.appendParagraph('• Allergies: ' + (record.allergies || 'No Known Drug Allergy (NKDA)')).setFontSize(10.5);

  body.appendParagraph('\n4. FAMILY & SOCIAL HISTORY')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('• Family History: ' + (record.familyHistory || 'Non-contributory.')).setFontSize(10.5);
  body.appendParagraph('• Social History: ' + (record.socialHistory || 'Non-contributory.')).setFontSize(10.5);

  appendDocSection_(body, '5. REVIEW OF SYSTEMS (ROS)',
    record.reviewOfSystems || 'A complete 10-system review was performed and is negative except as noted in the HPI.');

  body.appendParagraph('\n6. VITAL SIGNS & PHYSICAL EXAMINATION')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph('• Vital Signs: ' + (record.vitalSigns || 'Not recorded.')).setFontSize(10.5);
  body.appendParagraph(record.physicalExam || 'Physical examination unremarkable.').setFontSize(10.5);

  appendDocSection_(body, '7. ADMISSION LABORATORY & IMAGING',
    record.labsImaging || 'Pending at the time of admission.');

  body.appendParagraph('\n8. IMPRESSION & ADMISSION PLAN (Problem-based)')
    .setFontSize(12).setBold(true).setForegroundColor('#1e293b');

  var problems = record.problemList || [];
  if (problems.length) {
    for (var i = 0; i < problems.length; i++) {
      var p = problems[i] || {};
      body.appendParagraph('# ' + (i + 1) + '. ' + (p.problem || 'Unnamed problem'))
        .setFontSize(11).setBold(true).setForegroundColor('#0f172a');
      body.appendParagraph('    Plan: ' + (p.plan || 'To be determined.')).setFontSize(10.5).setBold(false);
    }
  } else {
    body.appendParagraph('【Impression / Tentative Diagnosis】\n' + (record.impression || 'Pending initial diagnostic evaluations.'))
      .setFontSize(11).setBold(true).setForegroundColor('#0f172a');
    body.appendParagraph('【Therapeutic & Workup Plan】\n' + (record.plan || 'Routine admission care.'))
      .setFontSize(10.5).setBold(false);
  }

  body.appendHorizontalRule();

  body.appendParagraph('\nAttending / Admitting Physician: ______________________ (' + (record.doctorName || 'Dr. Kwo-Ta Chu') + ')\n' +
    'Electronically recorded in the 2026 Google Spark Cloud Registry at ' +
    Utilities.formatDate(timestamp, TZ, 'yyyy-MM-dd HH:mm'))
    .setFontSize(9).setForegroundColor('#64748b').setAlignment(DocumentApp.HorizontalAlignment.RIGHT);

  doc.saveAndClose();
  DriveApp.getFileById(doc.getId()).moveTo(reportsFolder);
  return docLinks_(doc.getId());
}

function appendDocSection_(body, heading, text) {
  body.appendParagraph('\n' + heading).setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph(text).setFontSize(10.5).setBold(false);
}

/**
 * Recent admission notes for the dashboard.
 * @param {string} token
 * @param {number} limit
 */
function getRecentAdmissionNotes(token, limit) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    limit = limit || 20;
    var ss = getSpreadsheet();
    var sheet = ss.getSheetByName('Master_AdmissionNotes');
    if (!sheet) return { status: 'success', records: [] };

    var data = sheet.getDataRange().getValues();
    if (data.length <= 1) return { status: 'success', records: [] };

    var records = [];
    for (var i = data.length - 1; i >= 1 && records.length < limit; i--) {
      records.push(mapAdmissionRow_(data[i]));
    }
    return { status: 'success', records: records };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

function mapAdmissionRow_(row) {
  return {
    noteId: row[0],
    timestamp: row[1] ? Utilities.formatDate(new Date(row[1]), TZ, 'yyyy-MM-dd HH:mm') : '',
    examDate: row[2] ? Utilities.formatDate(new Date(row[2]), TZ, 'yyyy-MM-dd') : '',
    patientId: row[3],
    patientName: row[4],
    ageGender: row[5],
    wardBed: row[6],
    doctorName: row[7],
    department: row[8],
    chiefComplaint: row[9],
    presentIllness: row[10],
    impression: row[13],
    plan: row[14],
    docUrl: row[15],
    pdfUrl: row[16],
    docxUrl: row[17]
  };
}

/**
 * Keyword search across admission notes.
 * Searches note ID, admission date, MRN, patient name, age/gender, ward/bed,
 * attending, department, chief complaint, present illness and impression.
 * @param {string} token
 * @param {string} query
 */
function searchAdmissionNotes(token, query) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    query = (query || '').toLowerCase().trim();
    var ss = getSpreadsheet();
    var sheet = ss.getSheetByName('Master_AdmissionNotes');
    if (!sheet) return { status: 'success', records: [] };

    var data = sheet.getDataRange().getValues();
    var results = [];

    for (var i = data.length - 1; i >= 1; i--) {
      var row = data[i];
      var haystack = [
        row[0], row[2], row[3], row[4], row[5], row[6],
        row[7], row[8], row[9], row[10], row[13]
      ].join(' ').toLowerCase();
      if (!query || haystack.indexOf(query) !== -1) results.push(mapAdmissionRow_(row));
      if (results.length >= 50) break;
    }
    return { status: 'success', records: results };
  } catch (err) {
    return { status: 'error', message: err.toString() };
  }
}

/* ==========================================================================
 * SELF TEST
 *
 * The web app cannot be exercised from the command line, so DocumentApp method
 * errors (e.g. `setFontColor` does not exist on a Paragraph — it is
 * `setForegroundColor`) only surface when a physician presses Save.
 *
 * Run `runSelfTest` from the Apps Script editor after any change to the report
 * generators. It drives the real production code paths with dummy data, then
 * trashes whatever it created. Read the result in the execution log.
 * ========================================================================== */

function runSelfTest() {
  var log = [];
  var created = [];

  function step(name, fn) {
    try {
      var r = fn();
      log.push('PASS  ' + name);
      return r;
    } catch (e) {
      log.push('FAIL  ' + name + '  ->  ' + (e && e.message ? e.message : e));
      return null;
    }
  }

  var now = new Date();

  step('getSpreadsheet()', function () { return getSpreadsheet().getName(); });

  step('token sign/verify round-trip', function () {
    var t = issueToken_();
    if (!isValidToken_(t)) throw new Error('freshly issued token failed validation');
    if (isValidToken_('0.deadbeef')) throw new Error('expired/forged token was accepted');
    return 'ok';
  });

  var examDoc = step('createGoogleDocReport() — every paragraph/table style call', function () {
    return createGoogleDocReport({
      examType: 'Echocardiogram', doctorName: 'Self Test', examDate: '2026-01-01',
      patientId: 'SELFTEST', patientName: 'Self Test', indication: 'self test',
      technique: 'self test', comparison: 'none', symptoms: 'self test',
      diagnosis: 'self test', findings: 'line1\nline2', impression: 'self test',
      recommendation: 'self test'
    }, 'SELFTEST-EXAM', now);
  });
  if (examDoc && examDoc.docId) created.push(examDoc.docId);

  var admDoc = step('createAdmissionNoteDocReport() — incl. problem-list branch', function () {
    return createAdmissionNoteDocReport({
      patientId: 'SELFTEST', patientName: 'Self Test', ageGender: '60yo Male',
      examDate: '2026-01-01', wardBed: 'A-1', doctorName: 'Self Test',
      department: 'Nephrology', informant: 'Patient', reliability: 'Reliable',
      chiefComplaint: 'self test', presentIllness: 'self test', pastHistory: 'self test',
      surgicalHistory: 'self test', medications: 'self test', allergies: 'NKDA',
      familyHistory: 'self test', socialHistory: 'self test', reviewOfSystems: 'self test',
      vitalSigns: 'self test', physicalExam: 'self test', labsImaging: 'self test',
      problemList: [{ problem: 'Problem 1', plan: '1. step one\n2. step two' }]
    }, 'SELFTEST-ADM', now);
  });
  if (admDoc && admDoc.docId) created.push(admDoc.docId);

  step('createAdmissionNoteDocReport() — empty problem-list fallback branch', function () {
    var d = createAdmissionNoteDocReport({
      patientId: 'SELFTEST', patientName: 'Self Test', examDate: '2026-01-01',
      impression: 'self test', plan: 'self test', problemList: []
    }, 'SELFTEST-ADM2', now);
    if (d && d.docId) created.push(d.docId);
    return 'ok';
  });

  step('export URL shape', function () {
    if (!examDoc) throw new Error('skipped — exam doc was not created');
    ['docUrl', 'pdfUrl', 'docxUrl'].forEach(function (k) {
      if (!examDoc[k] || examDoc[k].indexOf('docs.google.com/document/d/') === -1) {
        throw new Error('bad ' + k + ': ' + examDoc[k]);
      }
    });
    return 'ok';
  });

  step('LanguageApp.translate()', function () {
    return LanguageApp.translate('發燒三天', 'zh-TW', 'en');
  });

  var trashed = 0;
  created.forEach(function (id) {
    try { DriveApp.getFileById(id).setTrashed(true); trashed++; } catch (e) {}
  });
  log.push('CLEAN ' + trashed + '/' + created.length + ' test document(s) moved to trash');

  var failures = log.filter(function (l) { return l.indexOf('FAIL') === 0; }).length;
  log.push('');
  log.push(failures ? ('RESULT: ' + failures + ' FAILURE(S)') : 'RESULT: ALL PASSED');

  var out = log.join('\n');
  Logger.log(out);
  return out;
}
