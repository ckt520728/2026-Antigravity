export type StaffRole =
  | 'SUPERVISOR'
  | 'NURSE'
  | 'NURSE_SPECIALIST'
  | 'DOCTOR'
  | 'MEDICAL_ADMIN'
  | 'REGISTRATION'
  | 'ACCOUNTANT'
  | 'HR'
  | 'SYSTEM_ADMIN'

export type Unit = 'INPATIENT' | 'OPD' | 'ER' | 'ADMINISTRATION' | 'OTHER'

export type EmploymentType = 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'LOCUM'

export type AttendanceEventType =
  | 'CHECK_IN'
  | 'CHECK_OUT'
  | 'BREAK_OUT'
  | 'BREAK_IN'
  | 'ON_DUTY_SIGN_IN'
  | 'ON_DUTY_SIGN_OUT'
  | 'CLINICAL_ROUND_SIGN_IN'

export type Language = 'zh-TW' | 'en' | 'vi' | 'id'
export type Theme = 'dark' | 'light'
export type TabType = 'clockin' | 'dashboard' | 'reports'

export interface Staff {
  id: string
  employee_no: string
  name: string
  unit: Unit | string
  role: StaffRole | string
  employment_type: EmploymentType | string
  category?: string
}

export interface KioskPunchRequest {
  employee_no: string
  event_type: AttendanceEventType
  station_id?: string
  ward_code?: string | null
  override_reason?: string | null
  client_event_uid?: string
  occurred_at?: string
}

export interface KioskPunchResponse {
  event_id: string
  employee_no: string
  name: string
  role: string
  event_type: AttendanceEventType
  occurred_at: string
  ward_code?: string | null
  station_id?: string | null
  message: string
}

export interface PunchHistoryItem {
  id: string
  staff_id: string
  employee_no: string
  name: string
  role: string
  event_type: AttendanceEventType
  occurred_at: string
  ward_code?: string | null
  source: string
}
