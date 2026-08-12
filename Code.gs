/**
 * Clinical Documentation & Admission Note System — v6.8
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

/**
 * Hospital name printed in the admission-note letterhead (top of the body) and in
 * the slim continuation header. Change this one line to re-brand for another hospital.
 */
var HOSPITAL_NAME = '陽明醫院';

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
 *   false — anyone with the link goes straight into the app.
 *   true  — the login screen is shown and every data function requires a valid
 *           token (current setting).
 *
 * ⚠️ ON since 2026-08-12, because the form collects 身分證號碼 and the /exec URL
 * is published in a PUBLIC repo. Do not switch this back to false while the link
 * is shared with staff.
 *
 * ⚠️ REMAINING STEP FOR THE OWNER: until `setAppPasscode` is run once from the
 * editor, the passcode falls back to DEFAULT_PASSCODE below — which is readable
 * in the public repo. Run it to set a real passcode.
 */
var AUTH_ENABLED = true;

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
      '入院檢驗與影像 (Labs & Imaging)', '問題清單 JSON (Problem List)',
      '身分證號碼 (National ID)', '出生日期 (Birth Date)', '住院史 (Hospitalization History)'
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
      JSON.stringify(record.problemList || []),
      record.nationalId || '',
      record.birthDate || '',
      record.hospitalizationHistory || ''
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
    logDiagnostic_('saveAdmissionNoteRecord', err);
    return { status: 'error', message: '住院病歷儲存失敗：' + err.toString() };
  }
}

/**
 * Generate the formal Google Doc admission note.
 *
 * Layout mirrors the hospital's paper ADMISSION NOTE form (see
 * 02_參考資料/Admission Note_format): a bordered three-column letterhead in the
 * repeating page header, then 中文(English)： section headings in the order
 * 主訴 → 現在病歷 → 過去病史 → 藥物過敏 → 家族史 → 系統回顧 → 理學檢查 →
 * 檢驗報告 → 檢查報告 → 初步診斷 → 治療及計劃 → 主治醫師.
 */
function createAdmissionNoteDocReport(record, noteId, timestamp) {
  var reportsFolder = getReportsFolder_('住院病歷報告_GoogleDocs');

  var docTitle = 'AdmissionNote_' + (record.patientId || 'ANON') + '_' +
    Utilities.formatDate(timestamp, TZ, 'yyyyMMdd_HHmm');
  var doc = DocumentApp.create(docTitle);
  var body = doc.getBody();

  body.setMarginTop(40).setMarginBottom(40).setMarginLeft(48).setMarginRight(48);

  // Full letterhead at the top of the body (renders in Doc, PDF *and* Word), plus a
  // slim text-only page header so continuation pages stay identifiable. See
  // buildAdmissionLetterhead_ for why this is not in the page header.
  buildAdmissionLetterhead_(body, record);
  buildAdmissionPageHeader_(doc, record);

  // 主訴 / 現在病歷
  appendHospitalSection_(body, '主訴', 'Chief Complaints');
  appendHospitalLine_(body, record.chiefComplaint || '—');

  // Present Illness is a narrative paragraph, not a list of labelled fragments.
  appendHospitalSection_(body, '現在病歷', 'Present Illness');
  toNarrativeParagraphs_(record.presentIllness).forEach(function (para) {
    appendHospitalLine_(body, para);
  });

  // 過去病史 — the form's four fixed subheadings
  appendHospitalSection_(body, '過去病史', 'Past History');
  appendHospitalLine_(body, 'Past history :');
  appendHospitalLine_(body, '1. Disease : ' + (record.pastHistory || 'Non-contributory.'), 36);
  appendHospitalLine_(body, '2. History of trauma or surgery : ' + (record.surgicalHistory || 'Denied.'), 36);
  appendHospitalLine_(body, '3. History of hospitalization : ' + (record.hospitalizationHistory || 'Denied.'), 36);
  appendHospitalLine_(body, '4. Home medication reviews : ' + (record.medications || 'None.'), 36);

  // Personal History belongs here on 陽明醫院's form — under 過去病史, not 家族史.
  // The frontend composes the numbered block; fall back to socialHistory for
  // records saved before the field existed.
  if (record.personalHistory) {
    appendHospitalLine_(body, 'Personal History :');
    String(record.personalHistory).split('\n').forEach(function (line) {
      if (line) appendHospitalLine_(body, line, 36);
    });
  } else if (record.socialHistory) {
    appendHospitalLine_(body, 'Personal History :');
    appendHospitalLine_(body, record.socialHistory, 36);
  }

  appendHospitalSection_(body, '藥物過敏', 'Drug Allergy');
  appendHospitalLine_(body, record.allergies || 'The patient is not allergic to any type of food or medicine.');

  appendHospitalSection_(body, '家族史', 'Family History');
  appendHospitalLine_(body, record.familyHistory || 'There was no family history of hereditary or oncologic disease.');

  appendHospitalSection_(body, '系統回顧', 'Review of Systems');
  appendHospitalLine_(body, 'Review of systems');
  appendHospitalLine_(body, record.reviewOfSystems || '—', 36);

  appendHospitalSection_(body, '理學檢查', 'Physical Examination');
  appendHospitalLine_(body, 'Vital sign: ' + (record.vitalSigns || '—'));
  appendHospitalLine_(body, record.physicalExam || '—');

  // 檢驗報告 / 檢查報告 — English headings, same as every other section
  appendHospitalSection_(body, '檢驗報告', 'Laboratory Data');
  appendHospitalLine_(body, record.labsReport || record.labsImaging || 'Pending.');

  appendHospitalSection_(body, '檢查報告', 'Imaging and Other Studies');
  appendHospitalLine_(body, record.studiesReport || 'Pending.');

  // 初步診斷 / 治療及計劃 — numbered, from the problem list
  var problems = record.problemList || [];

  appendHospitalSection_(body, '初步診斷', 'Impression');
  if (problems.length) {
    for (var i = 0; i < problems.length; i++) {
      appendHospitalLine_(body, (i + 1) + '.' + ((problems[i] || {}).problem || 'Unnamed problem'), 36);
    }
  } else {
    appendHospitalLine_(body, record.impression || 'Pending initial diagnostic evaluations.', 36);
  }

  appendHospitalSection_(body, '治療及計劃', 'Management and Plan');
  if (problems.length) {
    var planNo = 0;
    for (var j = 0; j < problems.length; j++) {
      var pl = String((problems[j] || {}).plan || '').split('\n');
      for (var k = 0; k < pl.length; k++) {
        var line = pl[k].replace(/^\s*\d+[.)]\s*/, '').trim();
        if (line) appendHospitalLine_(body, (++planNo) + '.' + line, 36);
      }
    }
    if (!planNo) appendHospitalLine_(body, '1.Routine admission care.', 36);
  } else {
    appendHospitalLine_(body, record.plan || 'Routine admission care.', 36);
  }

  // 主治醫師 signature block, right-aligned as on the form
  styleP_(body.appendParagraph(''), { size: 10, before: 24 });
  styleP_(body.appendParagraph('主治醫師：' + (record.doctorName || '')),
    { size: 10.5, align: DocumentApp.HorizontalAlignment.RIGHT, before: 18 });
  styleP_(body.appendParagraph('Note ID: ' + noteId + '　|　' +
    Utilities.formatDate(timestamp, TZ, 'yyyy-MM-dd HH:mm')),
    { size: 8, align: DocumentApp.HorizontalAlignment.RIGHT, before: 6 })
    .setForegroundColor('#808080');

  // DocumentApp.create() seeds the body with one empty paragraph that would push the
  // letterhead down a line. Removed last, once there is other content, so the body is
  // never left as a bare table. Cosmetic — never let it fail the whole document.
  try {
    var seed = body.getChild(0);
    if (body.getNumChildren() > 1 &&
        seed.getType() === DocumentApp.ElementType.PARAGRAPH &&
        seed.asParagraph().getText() === '') {
      seed.removeFromParent();
    }
  } catch (e) {
    logDiagnostic_('removeSeedParagraph', e);
  }

  doc.saveAndClose();
  DriveApp.getFileById(doc.getId()).moveTo(reportsFolder);
  return docLinks_(doc.getId());
}

/**
 * Append a failure to a `_Diagnostics` tab so problems that only appear inside a
 * generated document can be inspected afterwards, instead of surfacing as a toast
 * the user has to relay by hand. Never throws — diagnostics must not break callers.
 */
function logDiagnostic_(context, err) {
  try {
    var ss = getSpreadsheet();
    var sheet = ss.getSheetByName('_Diagnostics');
    if (!sheet) {
      sheet = ss.insertSheet('_Diagnostics');
      sheet.appendRow(['時間 (Timestamp)', '位置 (Context)', '錯誤 (Error)', '堆疊 (Stack)']);
      sheet.setFrozenRows(1);
    }
    sheet.appendRow([
      Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm:ss'),
      String(context),
      err && err.message ? err.message : String(err),
      err && err.stack ? String(err.stack).slice(0, 900) : ''
    ]);
  } catch (ignored) {}
}

function appendDocSection_(body, heading, text) {
  body.appendParagraph('\n' + heading).setFontSize(12).setBold(true).setForegroundColor('#1e293b');
  body.appendParagraph(text).setFontSize(10.5).setBold(false);
}

/* --------------------------------------------------------------------------
 * Hospital admission-note formatting helpers
 * -------------------------------------------------------------------------- */

/** Convert an ISO date (yyyy-MM-dd) to the ROC calendar form used on the form. */
function toRocDate_(iso) {
  if (!iso) return '';
  var d = new Date(String(iso) + 'T00:00:00');
  if (isNaN(d.getTime())) return String(iso);
  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  return (d.getFullYear() - 1911) + ' 年 ' + pad(d.getMonth() + 1) + ' 月 ' + pad(d.getDate()) + ' 日';
}

/** Apply a compact paragraph style; returns the paragraph for chaining. */
function styleP_(p, opts) {
  opts = opts || {};
  p.setFontSize(opts.size || 9).setBold(!!opts.bold);
  if (opts.align) p.setAlignment(opts.align);
  p.setSpacingBefore(opts.before || 0).setSpacingAfter(opts.after || 0);
  return p;
}

/**
 * Fill a table cell with several styled lines.
 * A cell always contains one empty paragraph, so the first line reuses it
 * rather than appending — otherwise every cell starts with a blank row.
 */
function setCellLines_(cell, lines) {
  var first = cell.getChild(0).asParagraph();
  first.setText(lines[0].text);
  styleP_(first, lines[0]);
  for (var i = 1; i < lines.length; i++) {
    styleP_(cell.appendParagraph(lines[i].text), lines[i]);
  }
  cell.setPaddingTop(2).setPaddingBottom(2).setPaddingLeft(5).setPaddingRight(5);
}

/**
 * Build the bordered letterhead block that repeats on every printed page,
 * matching the hospital's paper ADMISSION NOTE form:
 *
 *   +---------------------+------------------------+--------------+
 *   |      <醫院名稱>      | 病歷號 / 姓名 /         | 床號 / 生日 / |
 *   |   ADMISSION  NOTE   | 身分證號碼 / 住院日期    | 性別          |
 *   +---------------------+------------------------+--------------+
 *
 * Uses a real Google Docs header section so it repeats across pages.
 */
/**
 * The full three-column letterhead, appended to the TOP OF THE BODY.
 *
 * ⚠️ It used to live in the page header. Do not move it back. Google Docs drops a
 * TABLE inside a header when exporting to .docx, so the Word file came out with no
 * letterhead at all while the Doc and PDF looked correct — reported by Dr Chu
 * 2026-08-12 from a real note. In the body it renders identically in all three.
 * `buildAdmissionPageHeader_` still supplies a slim text-only continuation line,
 * which does survive the .docx export because it contains no table.
 */
function buildAdmissionLetterhead_(body, record) {
  var CENTER = DocumentApp.HorizontalAlignment.CENTER;
  var table = body.appendTable([['', '', '']]);
  table.setBorderColor('#000000').setBorderWidth(1);

  setCellLines_(table.getCell(0, 0), [
    { text: HOSPITAL_NAME, size: 16, bold: true, align: CENTER, before: 2 },
    { text: 'ADMISSION  NOTE', size: 12, bold: true, align: CENTER, after: 2 }
  ]);

  setCellLines_(table.getCell(0, 1), [
    { text: '病歷號：' + (record.patientId || '') },
    { text: '姓　　名：' + (record.patientName || '') },
    { text: '身分證號碼：' + (record.nationalId || '') },
    { text: '住院日期：' + toRocDate_(record.examDate) }
  ]);

  setCellLines_(table.getCell(0, 2), [
    { text: '床號：' + (record.wardBed || '') },
    { text: '生日：' + (record.birthDate || '') },
    { text: '性別：' + (record.gender || record.ageGender || '') }
  ]);

  table.setColumnWidth(0, 215).setColumnWidth(1, 190).setColumnWidth(2, 105);
  return table;
}

/**
 * Slim continuation header — one line, NO table, so it survives .docx export.
 * Keeps every printed page identifiable if the note runs past page 1.
 */
function buildAdmissionPageHeader_(doc, record) {
  // Cosmetic only — the letterhead that matters is in the body. A failure here must
  // never stop the note from being generated, which is exactly what happened when
  // this called getChild(0) on a freshly added header that has no children yet.
  try {
    var header = doc.getHeader() || doc.addHeader();
    header.clear();

    var bits = [HOSPITAL_NAME + ' ADMISSION NOTE'];
    if (record.patientId) bits.push('病歷號：' + record.patientId);
    if (record.patientName) bits.push('姓名：' + record.patientName);
    if (record.wardBed) bits.push('床號：' + record.wardBed);

    // appendParagraph always works; getChild(0) does not.
    styleP_(header.appendParagraph(bits.join('　|　')), { size: 8 })
      .setForegroundColor('#666666');

    // clear() may leave an empty paragraph behind it; drop any leading blanks.
    while (header.getNumChildren() > 1) {
      var first = header.getChild(0);
      if (first.getType() === DocumentApp.ElementType.PARAGRAPH &&
          first.asParagraph().getText() === '') {
        first.removeFromParent();
      } else break;
    }
    return header;
  } catch (e) {
    logDiagnostic_('buildAdmissionPageHeader_', e);
    return null;
  }
}

/** Section heading in the hospital's 中文(English)： style. */
/**
 * Section heading. English only — by Dr Chu's instruction the note body carries no
 * Chinese; only the letterhead and the attending signature stay in Chinese.
 * The `zh` argument is kept so call sites still document which form section this is.
 */
function appendHospitalSection_(body, zh, en) {
  return styleP_(body.appendParagraph(en + ' :'),
    { size: 11, bold: true, before: 10, after: 2 });
}

/** Plain body line, indented like the handwritten form. */
/**
 * Turn a Present Illness written as stacked fragments into flowing narrative.
 *
 * The LQQOPERA quick-fill chips used to insert one labelled sentence per line
 * ("Onset: ...", "Associated symptoms: ..."), which printed as a pseudo-bulleted
 * list and repeated the same label three times in a row. A blank line still starts
 * a new paragraph; single line breaks are joined into prose, and any leading
 * "Label:" is stripped.
 *
 * @return {string[]} one string per paragraph; [] becomes ['—'].
 */
function toNarrativeParagraphs_(text) {
  var LABEL = /^\s*(Onset|Location and quality|Location|Quality|Severity|Associated symptoms|Associated|Aggravating factors|Relieving factors|Emergency department course|Timing|Radiation)\s*:\s*/i;
  var paras = String(text == null ? '' : text).split(/\n\s*\n+/);
  var out = [];
  for (var i = 0; i < paras.length; i++) {
    var lines = paras[i].split('\n');
    var parts = [];
    for (var j = 0; j < lines.length; j++) {
      var s = lines[j].replace(LABEL, '').replace(/^\s*[-•*]\s*/, '').trim();
      if (!s) continue;
      if (!/[.?!:;,]$/.test(s)) s += '.';
      parts.push(s);
    }
    if (parts.length) out.push(parts.join(' '));
  }
  return out.length ? out : ['—'];
}

function appendHospitalLine_(body, text, indent) {
  var p = styleP_(body.appendParagraph(text), { size: 10 });
  p.setIndentStart(indent || 18);
  return p;
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

/**
 * Rebuild an existing note's Doc / PDF / Word using the CURRENT formatting code,
 * then point the log row at the new files.
 *
 * Why this exists: the download links stored on a row are files that were rendered
 * at save time, so they never pick up later formatting fixes. Without this, checking
 * a format change means retyping a whole note — the draft is deliberately cleared on
 * a successful save so the next patient's form starts empty.
 *
 * ⚠️ Regeneration is LOSSY for three fields the log does not store separately:
 *   - personalHistory  → falls back to the logged socialHistory
 *   - labsReport / studiesReport → only the combined labsImaging column exists,
 *     so everything lands under Laboratory Data
 *   - gender → taken from ageGender
 * The original files are NOT deleted; the row is repointed at the new ones.
 */
function regenerateAdmissionNoteDoc(token, noteId) {
  var gate = authFail_(token);
  if (gate) return gate;

  try {
    if (!noteId) return { status: 'error', message: '缺少病歷編號。' };
    var ss = getSpreadsheet();
    var sheet = ss.getSheetByName('Master_AdmissionNotes');
    if (!sheet) return { status: 'error', message: '找不到 Master_AdmissionNotes 工作表。' };

    var data = sheet.getDataRange().getValues();
    var rowIndex = -1;
    for (var i = 1; i < data.length; i++) {
      if (String(data[i][0]) === String(noteId)) { rowIndex = i; break; }
    }
    if (rowIndex < 0) return { status: 'error', message: '找不到病歷編號 ' + noteId + '。' };

    var row = data[rowIndex];

    // Column 12 stores "PMH: <pastHistory> | Allergy: <allergies>" — split it back.
    var pmhCell = String(row[11] || '');
    var pastHistory = pmhCell, allergies = '';
    var sepAt = pmhCell.indexOf(' | Allergy: ');
    if (sepAt >= 0) {
      pastHistory = pmhCell.slice(0, sepAt);
      allergies = pmhCell.slice(sepAt + ' | Allergy: '.length);
    }
    pastHistory = pastHistory.replace(/^PMH:\s*/, '');

    var problemList = [];
    try { problemList = JSON.parse(row[25] || '[]') || []; } catch (e) { problemList = []; }

    var record = {
      patientId: row[3], patientName: row[4], ageGender: row[5], gender: row[5],
      wardBed: row[6], doctorName: row[7], department: row[8],
      examDate: row[2] ? Utilities.formatDate(new Date(row[2]), TZ, 'yyyy-MM-dd') : '',
      chiefComplaint: row[9],
      presentIllness: row[10],
      pastHistory: pastHistory,
      allergies: allergies,
      physicalExam: row[12],
      impression: row[13],
      plan: row[14],
      surgicalHistory: row[18],
      medications: row[19],
      familyHistory: row[20],
      socialHistory: row[21],
      reviewOfSystems: row[22],
      vitalSigns: row[23],
      labsReport: row[24],
      studiesReport: '',
      problemList: problemList,
      nationalId: row[26],
      birthDate: row[27],
      hospitalizationHistory: row[28]
    };

    var links = createAdmissionNoteDocReport(record, noteId, new Date());

    // Columns 16-18 (1-based) are docUrl / pdfUrl / docxUrl.
    sheet.getRange(rowIndex + 1, 16, 1, 3)
      .setValues([[links.docUrl, links.pdfUrl, links.docxUrl]]);

    return {
      status: 'success',
      noteId: noteId,
      docUrl: links.docUrl,
      pdfUrl: links.pdfUrl,
      docxUrl: links.docxUrl,
      message: '已用目前版本重新產生 ' + noteId + ' 的文件。'
    };
  } catch (err) {
    logDiagnostic_('regenerateAdmissionNoteDoc', err);
    return { status: 'error', message: '重新產生失敗：' + err.toString() };
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
      gender: 'Male', nationalId: 'SELFTEST', birthDate: '0500101',
      examDate: '2026-01-01', wardBed: 'A-1', doctorName: 'Self Test',
      department: 'Nephrology', informant: 'Patient', reliability: 'Reliable',
      chiefComplaint: 'self test', presentIllness: 'self test', pastHistory: 'self test',
      surgicalHistory: 'self test', hospitalizationHistory: 'self test',
      medications: 'self test', allergies: 'NKDA',
      familyHistory: 'self test', socialHistory: 'self test', reviewOfSystems: 'self test',
      vitalSigns: 'self test', physicalExam: 'self test',
      labsReport: 'self test', studiesReport: 'self test', labsImaging: 'self test',
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
