import type { AttendanceEventType, Language } from './types'

export const translations: Record<Language, {
  hospitalName: string
  stationName: string
  subtitle: string
  tabs: {
    clockin: string
    dashboard: string
    reports: string
  }
  theme: {
    dark: string
    light: string
  }
  searchPlaceholder: string
  keyboardHint: string
  selectStaffFirst: string
  selectedStaff: string
  doctorBadge: string
  foreignBadge: string
  supervisorBadge: string
  actions: Record<AttendanceEventType, string>
  actionDescriptions: Record<AttendanceEventType, string>
  categories: {
    all: string
    nurse: string
    cna: string
    fcna: string
    doctor_spec: string
    support: string
  }
  recentPunchesTitle: string
  liveStatus: string
  online: string
  offline: string
  offlineQueueCount: string
  punchSuccess: string
  countdownClose: string
  closeBtn: string
  manualOverrideBtn: string
  manualOverrideTitle: string
  reasonLabel: string
  confirmBtn: string
  cancelBtn: string
  errorNotFound: string
  errorNetwork: string
  doctorRoundNote: string
  reports: {
    title: string
    subtitle: string
    periodLabel: string
    excelTitle: string
    excelDesc: string
    excelBtn: string
    wordTitle: string
    wordDesc: string
    wordBtn: string
    tableTitle: string
    printBtn: string
  }
}> = {
  'zh-TW': {
    hospitalName: '陽明醫院附設護理之家',
    stationName: '3F 護理站打卡簽到處',
    subtitle: '員工出勤與巡診打卡系統 (電腦網頁版)',
    tabs: {
      clockin: '護理站打卡',
      dashboard: '出勤即時看板',
      reports: '出勤與統計報表',
    },
    theme: {
      dark: 'Dark',
      light: 'Light',
    },
    searchPlaceholder: '鍵盤鍵入工號 (如 YM-DOC-01 / YM-NUR-01) 或姓名搜尋...',
    keyboardHint: '快捷鍵: [Enter] 選擇人員 | [1] 上班 | [2] 下班 | [3] 巡診 | [4] 外出 | [5] 返回',
    selectStaffFirst: '請先鍵入工號或從名單點選同仁',
    selectedStaff: '已選取同仁',
    doctorBadge: '兼任醫師',
    foreignBadge: '外籍照服員',
    supervisorBadge: '負責人/主管',
    actions: {
      CHECK_IN: '上班簽到',
      CHECK_OUT: '下班簽退',
      CLINICAL_ROUND_SIGN_IN: '醫師巡診簽到',
      BREAK_OUT: '中途外出',
      BREAK_IN: '外出返回',
      ON_DUTY_SIGN_IN: '夜/假值班簽到',
      ON_DUTY_SIGN_OUT: '夜/假值班簽退',
    },
    actionDescriptions: {
      CHECK_IN: '開始當日班次',
      CHECK_OUT: '結束當日班次',
      CLINICAL_ROUND_SIGN_IN: '朱醫師 3F 病房訪視在場簽到',
      BREAK_OUT: '用餐或公出暫離',
      BREAK_IN: '公出或休息結束返回',
      ON_DUTY_SIGN_IN: '夜間/假日值班到勤',
      ON_DUTY_SIGN_OUT: '夜間/假日值班結束',
    },
    categories: {
      all: '全部人員 (28)',
      nurse: '護理人員 (6)',
      cna: '本國照服員 (6)',
      fcna: '外籍照服員 (8)',
      doctor_spec: '兼任醫師/專職 (5)',
      support: '總務/廚工/兼任 (3)',
    },
    recentPunchesTitle: '今日護理站出勤動態',
    liveStatus: '即時看板',
    online: '系統連線中',
    offline: '離線模式 (暫存於本機)',
    offlineQueueCount: '筆待同步紀錄',
    punchSuccess: '打卡簽到成功！',
    countdownClose: '秒後自動返回待機',
    closeBtn: '完成 (Esc)',
    manualOverrideBtn: '主管例外代打卡',
    manualOverrideTitle: '主管例外打卡 / 特殊原因備註',
    reasonLabel: '例外打卡原因說明 (必填)',
    confirmBtn: '確認打卡',
    cancelBtn: '取消',
    errorNotFound: '查無此員工工號，請確認後重新鍵入',
    errorNetwork: '網路連線異常，已自動排入本機離線佇列',
    doctorRoundNote: '註：醫師病房簽到僅記錄病房層級在場證據，不含病患個資',
    reports: {
      title: '護理之家出勤與統計報表中心',
      subtitle: '提供全院 28 名同仁出勤工時四指標、打卡明細流水與朱醫師巡診紀錄匯出',
      periodLabel: '統計資料區間',
      excelTitle: '出勤工時與打卡流水 Excel (.xlsx)',
      excelDesc: '包含「出勤統計總表」、「打卡明細流水」與「朱醫師巡診專區」多工作表整合試算表。',
      excelBtn: '下載 Excel 報表 (.xlsx)',
      wordTitle: '出勤與巡診統計月報 Word (.docx)',
      wordDesc: '依據醫療院所規格排版，包含機構合規聲明、同仁工時總覽、醫師巡診清單與主管簽章欄。',
      wordBtn: '下載 Word 統計報表 (.docx)',
      tableTitle: '本月出勤與工時即時彙總表 (28名同仁)',
      printBtn: '列印出勤總表',
    },
  },
  'vi': {
    hospitalName: 'Viện Dưỡng Lão Bệnh Viện Dương Minh',
    stationName: 'Trạm Y Tá Tầng 3 - Điểm Chấm Công',
    subtitle: 'Hệ Thống Điểm Danh & Chấm Công Nhân Viên',
    tabs: {
      clockin: 'Chấm Công',
      dashboard: 'Bảng Trực Tuyến',
      reports: 'Báo Cáo Thống Kê',
    },
    theme: {
      dark: 'Tối (Dark)',
      light: 'Sáng (Light)',
    },
    searchPlaceholder: 'Nhập mã nhân viên (VD: YM-FCNA-01) hoặc tìm theo tên...',
    keyboardHint: 'Phím tắt: [Enter] Chọn | [1] Vào Ca | [2] Tan Ca | [3] Khám Bệnh | [4] Ra Ngoài | [5] Quay Lại',
    selectStaffFirst: 'Vui lòng nhập mã hoặc chọn tên nhân viên từ danh sách',
    selectedStaff: 'Nhân viên đã chọn',
    doctorBadge: 'Bác sĩ kiêm nhiệm',
    foreignBadge: 'Hộ lý nước ngoài',
    supervisorBadge: 'Người phụ trách',
    actions: {
      CHECK_IN: 'Vào Ca (Check In)',
      CHECK_OUT: 'Tan Ca (Check Out)',
      CLINICAL_ROUND_SIGN_IN: 'Bác Sĩ Khám Bệnh',
      BREAK_OUT: 'Ra Ngoài Tạm Thời',
      BREAK_IN: 'Quay Lại Làm Việc',
      ON_DUTY_SIGN_IN: 'Trực Đêm / Ngày Lễ Vào',
      ON_DUTY_SIGN_OUT: 'Trực Đêm / Ngày Lễ Ra',
    },
    actionDescriptions: {
      CHECK_IN: 'Bắt đầu ca làm việc hôm nay',
      CHECK_OUT: 'Kết thúc ca làm việc hôm nay',
      CLINICAL_ROUND_SIGN_IN: 'Bác sĩ Chu ký nhận thăm khám',
      BREAK_OUT: 'Ra ngoài ăn uống hoặc có việc',
      BREAK_IN: 'Quay lại tiếp tục ca làm',
      ON_DUTY_SIGN_IN: 'Điểm danh vào ca trực',
      ON_DUTY_SIGN_OUT: 'Kết thúc ca trực',
    },
    categories: {
      all: 'Tất Cả (28)',
      nurse: 'Y Tá (6)',
      cna: 'Hộ Lý Trong Nước (6)',
      fcna: 'Hộ Lý Nước Ngoài (8)',
      doctor_spec: 'Bác Sĩ / Chuyên Môn (5)',
      support: 'Hậu Cần / Khác (3)',
    },
    recentPunchesTitle: 'Nhật Ký Chấm Công Hôm Nay',
    liveStatus: 'Bảng Trực Tuyến',
    online: 'Đang Kết Nối',
    offline: 'Chế Độ Offline (Lưu Tạm)',
    offlineQueueCount: 'bản ghi chờ đồng bộ',
    punchSuccess: 'Chấm Công Thành Công!',
    countdownClose: 'giây để trở về màn hình chính',
    closeBtn: 'Đóng (Esc)',
    manualOverrideBtn: 'Chấm Công Ngoại Lệ',
    manualOverrideTitle: 'Chấm Công Ngoại Lệ Của Quản Lý',
    reasonLabel: 'Lý do chấm công ngoại lệ (Bắt buộc)',
    confirmBtn: 'Xác Nhận',
    cancelBtn: 'Hủy',
    errorNotFound: 'Không tìm thấy mã nhân viên, vui lòng kiểm tra lại',
    errorNetwork: 'Lỗi mạng, đã lưu tạm vào bộ nhớ máy',
    doctorRoundNote: 'Ghi chú: Điểm danh thăm khám chỉ ghi nhận sự hiện diện tại phòng',
    reports: {
      title: 'Trung Tâm Báo Cáo Chấm Công & Thống Kê',
      subtitle: 'Xuất dữ liệu giờ làm việc, lịch sử chấm công và nhật ký khám bệnh của Bác sĩ Chu',
      periodLabel: 'Khoảng thời gian thống kê',
      excelTitle: 'Báo Cáo Chấm Công Excel (.xlsx)',
      excelDesc: 'Bao gồm bảng tổng hợp giờ làm, nhật ký chấm công chi tiết và chuyên mục thăm khám của bác sĩ.',
      excelBtn: 'Tải Báo Cáo Excel (.xlsx)',
      wordTitle: 'Báo Cáo Thống Kê Tháng Word (.docx)',
      wordDesc: 'Định dạng tài liệu y tế chuẩn với phần tổng quan, chi tiết thăm khám và chữ ký xác nhận.',
      wordBtn: 'Tải Báo Cáo Word (.docx)',
      tableTitle: 'Bảng Thống Kê Giờ Làm Hiện Tại (28 nhân viên)',
      printBtn: 'In Bảng Báo Cáo',
    },
  },
  'id': {
    hospitalName: 'Panti Jompo RS Yangming',
    stationName: 'Pos Perawat Lantai 3 - Absensi',
    subtitle: 'Sistem Absensi & Tanda Tangan Karyawan',
    tabs: {
      clockin: 'Absensi Karyawan',
      dashboard: 'Dashboard Langsung',
      reports: 'Laporan & Statistik',
    },
    theme: {
      dark: 'Gelap (Dark)',
      light: 'Terang (Light)',
    },
    searchPlaceholder: 'Ketik NIP (cth: YM-FCNA-01) atau cari nama...',
    keyboardHint: 'Pintasan: [Enter] Pilih | [1] Masuk | [2] Pulang | [3] Visit Dokter | [4] Keluar | [5] Kembali',
    selectStaffFirst: 'Silakan ketik NIP atau klik nama karyawan',
    selectedStaff: 'Karyawan Terpilih',
    doctorBadge: 'Dokter Paruh Waktu',
    foreignBadge: 'Caregiver Asing',
    supervisorBadge: 'Penanggung Jawab',
    actions: {
      CHECK_IN: 'Absen Masuk (Check In)',
      CHECK_OUT: 'Absen Pulang (Check Out)',
      CLINICAL_ROUND_SIGN_IN: 'Visit Dokter',
      BREAK_OUT: 'Keluar Sementara',
      BREAK_IN: 'Kembali Bekerja',
      ON_DUTY_SIGN_IN: 'Absen Jaga Malam/Libur',
      ON_DUTY_SIGN_OUT: 'Selesai Jaga Malam/Libur',
    },
    actionDescriptions: {
      CHECK_IN: 'Mulai shift kerja hari ini',
      CHECK_OUT: 'Selesai shift kerja hari ini',
      CLINICAL_ROUND_SIGN_IN: 'Dr. Chu tanda tangan visit bangsal',
      BREAK_OUT: 'Istirahat makan atau urusan luar',
      BREAK_IN: 'Kembali dari istirahat',
      ON_DUTY_SIGN_IN: 'Mulai jadwal piket',
      ON_DUTY_SIGN_OUT: 'Selesai jadwal piket',
    },
    categories: {
      all: 'Semua (28)',
      nurse: 'Perawat (6)',
      cna: 'Caregiver Lokal (6)',
      fcna: 'Caregiver Asing (8)',
      doctor_spec: 'Dokter / Ahli (5)',
      support: 'Staf Pendukung (3)',
    },
    recentPunchesTitle: 'Log Absensi Hari Ini',
    liveStatus: 'Status Terkini',
    online: 'Terhubung',
    offline: 'Mode Offline (Disimpan Sementara)',
    offlineQueueCount: 'antrean tersimpan',
    punchSuccess: 'Absensi Berhasil!',
    countdownClose: 'detik kembali ke awal',
    closeBtn: 'Selesai (Esc)',
    manualOverrideBtn: 'Absensi Manual Supervisor',
    manualOverrideTitle: 'Penggantian Manual Supervisor',
    reasonLabel: 'Alasan absensi manual (Wajib diisi)',
    confirmBtn: 'Konfirmasi',
    cancelBtn: 'Batal',
    errorNotFound: 'NIP tidak ditemukan, silakan periksa kembali',
    errorNetwork: 'Koneksi terputus, data tersimpan sementara secara lokal',
    doctorRoundNote: 'Catatan: Visit dokter hanya mencatat kehadiran di lantai 3',
    reports: {
      title: 'Pusat Laporan Absensi & Statistik',
      subtitle: 'Ekspor data jam kerja, log absensi, dan riwayat visit dr. Chu untuk 28 staf',
      periodLabel: 'Rentang Periode Data',
      excelTitle: 'Laporan Jam Kerja Excel (.xlsx)',
      excelDesc: 'Lembar kerja multi-sheet lengkap: Rekapitulasi Jam Kerja, Log Absensi, dan Bagian Khusus Visit Dokter.',
      excelBtn: 'Unduh Laporan Excel (.xlsx)',
      wordTitle: 'Laporan Statistik Bulanan Word (.docx)',
      wordDesc: 'Format dokumen medis profesional lengkap dengan deklarasi kepatuhan dan kolom tanda tangan pimpinan.',
      wordBtn: 'Unduh Laporan Word (.docx)',
      tableTitle: 'Ringkasan Jam Kerja Staf Saat Ini (28 Staf)',
      printBtn: 'Cetak Laporan',
    },
  },
  'en': {
    hospitalName: 'Yangming Hospital Nursing Home',
    stationName: '3F Nursing Station Clock-In Terminal',
    subtitle: 'Staff Attendance & Clinical Round Sign-In System',
    tabs: {
      clockin: 'Clock-In Terminal',
      dashboard: 'Live Dashboard',
      reports: 'Reports & Analytics',
    },
    theme: {
      dark: 'Dark',
      light: 'Light',
    },
    searchPlaceholder: 'Type Employee ID (e.g. YM-DOC-01 / YM-NUR-01) or search by name...',
    keyboardHint: 'Shortcuts: [Enter] Select | [1] Check-in | [2] Check-out | [3] Round | [4] Break-out | [5] Break-in',
    selectStaffFirst: 'Please enter Employee ID or select a staff member from the list',
    selectedStaff: 'Selected Staff',
    doctorBadge: 'Attending Physician',
    foreignBadge: 'Foreign Caregiver',
    supervisorBadge: 'Director / Supervisor',
    actions: {
      CHECK_IN: 'Check In',
      CHECK_OUT: 'Check Out',
      CLINICAL_ROUND_SIGN_IN: 'Doctor Round Sign-in',
      BREAK_OUT: 'Break Out',
      BREAK_IN: 'Break In',
      ON_DUTY_SIGN_IN: 'On-Duty Sign In',
      ON_DUTY_SIGN_OUT: 'On-Duty Sign Out',
    },
    actionDescriptions: {
      CHECK_IN: 'Start daily work shift',
      CHECK_OUT: 'Finish daily work shift',
      CLINICAL_ROUND_SIGN_IN: 'Dr. Chu 3F ward clinical round presence',
      BREAK_OUT: 'Meal or temporary leave',
      BREAK_IN: 'Return from break or errand',
      ON_DUTY_SIGN_IN: 'Start night / holiday duty',
      ON_DUTY_SIGN_OUT: 'End night / holiday duty',
    },
    categories: {
      all: 'All Staff (28)',
      nurse: 'Nurses (6)',
      cna: 'Local CNAs (6)',
      fcna: 'Foreign CNAs (8)',
      doctor_spec: 'Physician & Specialists (5)',
      support: 'General Affairs / Kitchen (3)',
    },
    recentPunchesTitle: "Today's Live Punch Log",
    liveStatus: 'Live Station Board',
    online: 'Online',
    offline: 'Offline Mode (Locally Cached)',
    offlineQueueCount: 'pending punches in queue',
    punchSuccess: 'Punch Recorded Successfully!',
    countdownClose: 'seconds to standby',
    closeBtn: 'Close (Esc)',
    manualOverrideBtn: 'Supervisor Override',
    manualOverrideTitle: 'Supervisor Exception Manual Override',
    reasonLabel: 'Override reason (Required)',
    confirmBtn: 'Confirm Punch',
    cancelBtn: 'Cancel',
    errorNotFound: 'Employee ID not found, please check and try again',
    errorNetwork: 'Network error, punch queued locally for automatic sync',
    doctorRoundNote: 'Note: Doctor round sign-in records ward-level presence only',
    reports: {
      title: 'Attendance & Statistical Report Center',
      subtitle: 'Export work hours, raw punch logs, and Dr. Chu clinical round records for all 28 staff members',
      periodLabel: 'Report Date Range',
      excelTitle: 'Attendance Work Hours Excel (.xlsx)',
      excelDesc: 'Includes multi-sheet workbook: Summary, Punch Event Logs, and Clinical Rounds section.',
      excelBtn: 'Download Excel Report (.xlsx)',
      wordTitle: 'Monthly Statistical Report Word (.docx)',
      wordDesc: 'Clinical document format with compliance disclaimers, metrics overview, and signature section.',
      wordBtn: 'Download Word Report (.docx)',
      tableTitle: 'Current Month Attendance Summary (28 Staff Members)',
      printBtn: 'Print Report',
    },
  },
}
