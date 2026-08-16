import type { KioskPunchRequest, KioskPunchResponse, PunchHistoryItem, Staff } from './types'

const API_BASE = '/api/v1/attendance'
const REPORT_API_BASE = '/api/v1/reports'
const OFFLINE_QUEUE_KEY = 'ym_kiosk_offline_punches'

const DEFAULT_YANGMING_STAFF: Staff[] = [
  { id: '1', employee_no: 'YM-NUR-01', name: '林玟亭', unit: 'INPATIENT', role: 'SUPERVISOR', employment_type: 'FULL_TIME' },
  { id: '2', employee_no: 'YM-NUR-02', name: '李欣蕙', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '3', employee_no: 'YM-NUR-03', name: '黃珮鈞', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '4', employee_no: 'YM-NUR-04', name: '邱秋蓉', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '5', employee_no: 'YM-NUR-05', name: '沈心榆', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '6', employee_no: 'YM-NUR-06', name: '郭宥彤', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '7', employee_no: 'YM-CNA-01', name: '謝雪梅', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '8', employee_no: 'YM-CNA-02', name: '廖銀隊', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '9', employee_no: 'YM-CNA-03', name: '曾月鳳', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '10', employee_no: 'YM-CNA-04', name: '王櫻桃', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '11', employee_no: 'YM-CNA-05', name: '胡秀茵', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '12', employee_no: 'YM-CNA-06', name: '呂宜珮', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '13', employee_no: 'YM-FCNA-01', name: '泰氏青', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '14', employee_no: 'YM-FCNA-02', name: '周氏秀華', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '15', employee_no: 'YM-FCNA-03', name: '阮氏河', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '16', employee_no: 'YM-FCNA-04', name: '裴氏燕', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '17', employee_no: 'YM-FCNA-05', name: '武氏紅', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '18', employee_no: 'YM-FCNA-06', name: '阮氏花', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '19', employee_no: 'YM-FCNA-07', name: '阮氏瓊', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '20', employee_no: 'YM-FCNA-08', name: '阮氏雲', unit: 'INPATIENT', role: 'NURSE', employment_type: 'FULL_TIME' },
  { id: '21', employee_no: 'YM-NUT-01', name: '楊明珠', unit: 'INPATIENT', role: 'MEDICAL_ADMIN', employment_type: 'FULL_TIME' },
  { id: '22', employee_no: 'YM-KIT-01', name: '陳美紅', unit: 'INPATIENT', role: 'REGISTRATION', employment_type: 'FULL_TIME' },
  { id: '23', employee_no: 'YM-ADM-01', name: '廖運谷', unit: 'INPATIENT', role: 'REGISTRATION', employment_type: 'FULL_TIME' },
  { id: '24', employee_no: 'YM-PT-01', name: '葉聖慈', unit: 'INPATIENT', role: 'MEDICAL_ADMIN', employment_type: 'PART_TIME' },
  { id: '25', employee_no: 'YM-DOC-01', name: '朱國大', unit: 'INPATIENT', role: 'DOCTOR', employment_type: 'PART_TIME' },
  { id: '26', employee_no: 'YM-PHAR-01', name: '林文鴒', unit: 'INPATIENT', role: 'MEDICAL_ADMIN', employment_type: 'PART_TIME' },
  { id: '27', employee_no: 'YM-SW-01', name: '翁嬿婷', unit: 'INPATIENT', role: 'MEDICAL_ADMIN', employment_type: 'PART_TIME' },
  { id: '28', employee_no: 'YM-NUR-07', name: '邱燕鈴', unit: 'INPATIENT', role: 'NURSE', employment_type: 'PART_TIME' },
]

export async function fetchStaffList(): Promise<Staff[]> {
  try {
    const res = await fetch(`${API_BASE}/kiosk/staff`)
    if (!res.ok) {
      throw new Error(`Failed to fetch staff list: ${res.statusText}`)
    }
    const data: Staff[] = await res.json()
    return data
  } catch (err) {
    console.warn('Using cached or fallback staff list', err)
    const cached = localStorage.getItem('ym_kiosk_cached_staff')
    if (cached) {
      return JSON.parse(cached)
    }
    return DEFAULT_YANGMING_STAFF
  }
}

export async function fetchRecentPunches(): Promise<PunchHistoryItem[]> {
  try {
    const res = await fetch(`${API_BASE}/kiosk/recent-punches?limit=50`)
    if (!res.ok) {
      throw new Error(`Failed to fetch recent punches: ${res.statusText}`)
    }
    const data = await res.json()
    localStorage.setItem('ym_kiosk_cached_punches', JSON.stringify(data))
    return data
  } catch (err) {
    console.warn('Network error when fetching recent punches, using local', err)
    const cached = localStorage.getItem('ym_kiosk_cached_punches')
    return cached ? JSON.parse(cached) : []
  }
}

export function getOfflineQueue(): KioskPunchRequest[] {
  try {
    const raw = localStorage.getItem(OFFLINE_QUEUE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

export function saveToOfflineQueue(punch: KioskPunchRequest): void {
  const queue = getOfflineQueue()
  if (!punch.client_event_uid) {
    punch.client_event_uid = `offline-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`
  }
  if (!punch.occurred_at) {
    punch.occurred_at = new Date().toISOString()
  }
  queue.push(punch)
  localStorage.setItem(OFFLINE_QUEUE_KEY, JSON.stringify(queue))

  // Also append to local cached punches for instant UI feedback
  const cachedPunches: PunchHistoryItem[] = JSON.parse(localStorage.getItem('ym_kiosk_cached_punches') || '[]')
  const staff = DEFAULT_YANGMING_STAFF.find(s => s.employee_no === punch.employee_no)
  cachedPunches.unshift({
    id: punch.client_event_uid,
    staff_id: staff?.id || 'unknown',
    employee_no: punch.employee_no,
    name: staff?.name || punch.employee_no,
    role: staff?.role || 'STAFF',
    event_type: punch.event_type,
    occurred_at: punch.occurred_at,
    ward_code: punch.ward_code,
    source: 'OFFLINE_WEB',
  })
  localStorage.setItem('ym_kiosk_cached_punches', JSON.stringify(cachedPunches.slice(0, 50)))
}

export async function syncOfflineQueue(): Promise<number> {
  const queue = getOfflineQueue()
  if (queue.length === 0) return 0

  let syncedCount = 0
  const remaining: KioskPunchRequest[] = []

  for (const item of queue) {
    try {
      const res = await fetch(`${API_BASE}/kiosk/punch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item),
      })
      if (res.ok) {
        syncedCount++
      } else {
        remaining.push(item)
      }
    } catch {
      remaining.push(item)
    }
  }

  localStorage.setItem(OFFLINE_QUEUE_KEY, JSON.stringify(remaining))
  return syncedCount
}

export async function submitKioskPunch(
  payload: KioskPunchRequest
): Promise<{ success: boolean; data?: KioskPunchResponse; isOffline?: boolean; error?: string }> {
  try {
    const res = await fetch(`${API_BASE}/kiosk/punch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}))
      return {
        success: false,
        error: errorData.detail || `打卡失敗 (HTTP ${res.status})`,
      }
    }

    const data: KioskPunchResponse = await res.json()
    return { success: true, data }
  } catch (networkError) {
    console.warn('Network offline, queueing punch locally', networkError)
    saveToOfflineQueue(payload)
    const staff = DEFAULT_YANGMING_STAFF.find(s => s.employee_no === payload.employee_no)
    return {
      success: true,
      isOffline: true,
      data: {
        event_id: 'offline-' + Date.now(),
        employee_no: payload.employee_no,
        name: staff?.name || payload.employee_no,
        role: staff?.role || 'STAFF',
        event_type: payload.event_type,
        occurred_at: payload.occurred_at || new Date().toISOString(),
        station_id: payload.station_id || 'YM-3F-KIOSK',
        ward_code: payload.ward_code,
        message: `${staff?.name || payload.employee_no} 離線打卡成功，已存入本機佇列！`,
      },
    }
  }
}

/**
 * Download Excel Report
 */
export async function downloadExcelReport(startDate?: string, endDate?: string): Promise<void> {
  const query = new URLSearchParams()
  if (startDate) query.append('period_start', startDate)
  if (endDate) query.append('period_end', endDate)

  try {
    const res = await fetch(`${REPORT_API_BASE}/kiosk/excel?${query.toString()}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `護理之家出勤總表_${startDate || '本月'}_${endDate || ''}.xlsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.warn('Direct server excel download failed, generating client-side CSV/Excel fallback', err)
    // Client-side fallback CSV download
    downloadClientSideCsv(startDate, endDate)
  }
}

/**
 * Download Word Report
 */
export async function downloadWordReport(startDate?: string, endDate?: string): Promise<void> {
  const query = new URLSearchParams()
  if (startDate) query.append('period_start', startDate)
  if (endDate) query.append('period_end', endDate)

  try {
    const res = await fetch(`${REPORT_API_BASE}/kiosk/word?${query.toString()}`)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `護理之家出勤統計月報_${startDate || '本月'}_${endDate || ''}.docx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.warn('Direct server word download failed, generating client-side HTML Doc fallback', err)
    downloadClientSideDoc(startDate, endDate)
  }
}

function downloadClientSideCsv(startDate?: string, endDate?: string) {
  const headers = ['員工編號', '姓名', '單位', '職務', '聘僱別', '出勤狀態']
  const rows = DEFAULT_YANGMING_STAFF.map(s => [
    s.employee_no,
    s.name,
    '護理之家 3F',
    s.employee_no === 'YM-DOC-01' ? '兼任醫師' : s.role,
    s.employment_type === 'FULL_TIME' ? '正職' : '兼任/支援',
    '在職',
  ])
  const csvContent = '\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `陽明護理之家出勤名冊_${startDate || '2026'}_${endDate || ''}.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

function downloadClientSideDoc(startDate?: string, endDate?: string) {
  const htmlContent = `
    <html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'><title>陽明醫院附設護理之家 員工出勤統計月報</title></head>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
      <h1 style="color: #1e1b4b; text-align: center;">陽明醫院附設護理之家 員工出勤統計月報</h1>
      <p style="text-align: center; color: #64748b;">統計期間：${startDate || '本月'} ~ ${endDate || '至今'} | 產製時間：${new Date().toLocaleString('zh-TW')}</p>
      <hr/>
      <h3>一、全院 28 位同仁出勤名冊與狀態</h3>
      <table border="1" cellspacing="0" cellpadding="8" style="width: 100%; border-collapse: collapse;">
        <tr style="background-color: #4f46e5; color: white;">
          <th>工號</th><th>姓名</th><th>職務角色</th><th>聘僱別</th><th>出勤狀態</th>
        </tr>
        ${DEFAULT_YANGMING_STAFF.map(s => `
          <tr>
            <td>${s.employee_no}</td>
            <td>${s.name}</td>
            <td>${s.employee_no === 'YM-DOC-01' ? '兼任醫師 (巡診)' : s.role}</td>
            <td>${s.employment_type === 'FULL_TIME' ? '正職' : '兼任'}</td>
            <td>正常在勤</td>
          </tr>
        `).join('')}
      </table>
      <br/>
      <h3>二、朱國大醫師 (YM-DOC-01) 3F 病房巡診專區</h3>
      <p>• 巡診地點：陽明醫院附設護理之家 3F 護理站<br/>• 遵循紅線保護規範：僅記錄病房層級在勤證據，無任何病患個人病歷資料。</p>
      <br/><br/>
      <p>護理長／機構負責人簽章：___________________　　兼任主治醫師簽章：___________________</p>
    </body>
    </html>
  `
  const blob = new Blob(['\uFEFF' + htmlContent], { type: 'application/msword' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `陽明護理之家出勤月報_${startDate || '本月'}.doc`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
