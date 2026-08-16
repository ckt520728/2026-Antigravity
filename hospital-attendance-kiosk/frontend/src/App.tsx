import { useState, useEffect, useRef, useMemo } from 'react'
import {
  CheckCircle2,
  Building2,
  Search,
  Stethoscope,
  LogIn,
  LogOut,
  Coffee,
  RotateCcw,
  ShieldCheck,
  Wifi,
  WifiOff,
  UserCheck,
  Moon,
  Sun,
  FileSpreadsheet,
  FileText,
  Printer,
  Calendar,
  Activity,
  Download,
} from 'lucide-react'
import type {
  Staff,
  AttendanceEventType,
  Language,
  Theme,
  TabType,
  PunchHistoryItem,
  KioskPunchResponse,
} from './types'
import { translations } from './i18n'
import {
  fetchStaffList,
  fetchRecentPunches,
  submitKioskPunch,
  getOfflineQueue,
  syncOfflineQueue,
  downloadExcelReport,
  downloadWordReport,
} from './api'
import './App.css'

export default function App() {
  // Theme & Language State
  const [theme, setTheme] = useState<Theme>(() => {
    return (localStorage.getItem('ym_kiosk_theme') as Theme) || 'dark'
  })
  const [lang, setLang] = useState<Language>('zh-TW')
  const [currentTab, setCurrentTab] = useState<TabType>('clockin')
  const t = translations[lang]

  // System & Staff State
  const [staffList, setStaffList] = useState<Staff[]>([])
  const [recentPunches, setRecentPunches] = useState<PunchHistoryItem[]>([])
  const [selectedStaff, setSelectedStaff] = useState<Staff | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [activeCategory, setActiveCategory] = useState<string>('all')
  const [isOnline, setIsOnline] = useState<boolean>(navigator.onLine)
  const [offlineCount, setOfflineCount] = useState<number>(getOfflineQueue().length)

  // Report Dates
  const [startDate, setStartDate] = useState<string>(() => {
    const d = new Date()
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-01`
  })
  const [endDate, setEndDate] = useState<string>(() => {
    const d = new Date()
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  })
  const [reportSearchQuery, setReportSearchQuery] = useState('')
  const [isExportingExcel, setIsExportingExcel] = useState(false)
  const [isExportingWord, setIsExportingWord] = useState(false)

  // Feedback & Modal
  const [successResult, setSuccessResult] = useState<KioskPunchResponse | null>(null)
  const [countdown, setCountdown] = useState<number>(5)
  const [manualModalOpen, setManualModalOpen] = useState(false)
  const [manualReason, setManualReason] = useState('')
  const [manualEventType, setManualEventType] = useState<AttendanceEventType>('CHECK_IN')
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Real-time Clock
  const [currentTime, setCurrentTime] = useState<Date>(new Date())
  const searchInputRef = useRef<HTMLInputElement>(null)

  // Apply Theme attribute to <html>
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('ym_kiosk_theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  // Web Audio Chime on success
  const playSuccessChime = () => {
    try {
      const AudioContext = window.AudioContext || (window as unknown as { webkitAudioContext: typeof window.AudioContext }).webkitAudioContext
      if (!AudioContext) return
      const ctx = new AudioContext()
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = 'sine'
      osc.frequency.setValueAtTime(587.33, ctx.currentTime) // D5
      osc.frequency.setValueAtTime(880, ctx.currentTime + 0.1) // A5
      gain.gain.setValueAtTime(0.15, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4)
      osc.connect(gain)
      gain.connect(ctx.destination)
      osc.start()
      osc.stop(ctx.currentTime + 0.4)
    } catch {
      // AudioContext may require user gesture
    }
  }

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        const staff = await fetchStaffList()
        setStaffList(staff)
        localStorage.setItem('ym_kiosk_cached_staff', JSON.stringify(staff))
      } catch (err) {
        console.error('Failed to load staff', err)
      }

      try {
        const punches = await fetchRecentPunches()
        setRecentPunches(punches)
      } catch (err) {
        console.error('Failed to load punches', err)
      }
    }
    loadData()

    // Clock interval
    const clockTimer = setInterval(() => setCurrentTime(new Date()), 1000)

    // Online / Offline listeners
    const handleOnline = () => {
      setIsOnline(true)
      syncOfflineQueue().then((synced) => {
        if (synced > 0) {
          setOfflineCount(getOfflineQueue().length)
          fetchRecentPunches().then(setRecentPunches)
        }
      })
    }
    const handleOffline = () => setIsOnline(false)

    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    return () => {
      clearInterval(clockTimer)
      window.removeEventListener('online', handleOnline)
      window.removeEventListener('offline', handleOffline)
    }
  }, [])

  // Auto countdown for success modal
  useEffect(() => {
    if (!successResult) return
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          setSuccessResult(null)
          setSelectedStaff(null)
          setSearchQuery('')
          if (searchInputRef.current) searchInputRef.current.focus()
          return 5
        }
        return prev - 1
      })
    }, 1000)
    return () => clearInterval(timer)
  }, [successResult])

  // Filtered staff list for Clock-In tab
  const filteredStaff = useMemo(() => {
    return staffList.filter((s) => {
      const q = searchQuery.toLowerCase().trim()
      const matchesSearch =
        !q ||
        s.name.toLowerCase().includes(q) ||
        s.employee_no.toLowerCase().includes(q)

      if (!matchesSearch) return false

      if (activeCategory === 'nurse') return s.employee_no.includes('-NUR-')
      if (activeCategory === 'cna') return s.employee_no.includes('-CNA-')
      if (activeCategory === 'fcna') return s.employee_no.includes('-FCNA-')
      if (activeCategory === 'doctor_spec')
        return (
          s.employee_no.includes('-DOC-') ||
          s.employee_no.includes('-PT-') ||
          s.employee_no.includes('-PHAR-') ||
          s.employee_no.includes('-NUT-')
        )
      if (activeCategory === 'support')
        return (
          s.employee_no.includes('-ADM-') ||
          s.employee_no.includes('-KIT-') ||
          s.employee_no.includes('-SW-') ||
          s.employee_no.includes('-HN-')
        )

      return true
    })
  }, [staffList, searchQuery, activeCategory])

  // Filtered staff list for Report Center table
  const reportFilteredStaff = useMemo(() => {
    const q = reportSearchQuery.toLowerCase().trim()
    if (!q) return staffList
    return staffList.filter(
      (s) =>
        s.name.toLowerCase().includes(q) ||
        s.employee_no.toLowerCase().includes(q) ||
        (s.role && s.role.toLowerCase().includes(q))
    )
  }, [staffList, reportSearchQuery])

  // Execute Punch
  const handlePunch = async (
    eventType: AttendanceEventType,
    overrideReason?: string
  ) => {
    if (!selectedStaff) return
    setIsSubmitting(true)

    const payload = {
      employee_no: selectedStaff.employee_no,
      event_type: eventType,
      station_id: 'YM-3F-KIOSK',
      ward_code: eventType === 'CLINICAL_ROUND_SIGN_IN' ? '3F-NH' : undefined,
      override_reason: overrideReason,
    }

    const res = await submitKioskPunch(payload)
    setIsSubmitting(false)

    if (res.success && res.data) {
      playSuccessChime()
      setSuccessResult(res.data)
      setCountdown(5)
      setOfflineCount(getOfflineQueue().length)
      fetchRecentPunches().then(setRecentPunches)
    } else {
      alert(res.error || '打卡過程發生異常，請重試')
    }
  }

  // Keyboard navigation & shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (successResult) {
        if (e.key === 'Escape' || e.key === 'Enter') {
          setSuccessResult(null)
          setSelectedStaff(null)
          setSearchQuery('')
          if (searchInputRef.current) searchInputRef.current.focus()
        }
        return
      }

      if (manualModalOpen) {
        if (e.key === 'Escape') setManualModalOpen(false)
        return
      }

      if (currentTab !== 'clockin') return

      if (document.activeElement === searchInputRef.current) {
        if (e.key === 'Enter' && filteredStaff.length > 0) {
          e.preventDefault()
          setSelectedStaff(filteredStaff[0])
          setSearchQuery('')
        }
        return
      }

      if (selectedStaff && !isSubmitting) {
        if (e.key === '1') {
          e.preventDefault()
          handlePunch('CHECK_IN')
        } else if (e.key === '2') {
          e.preventDefault()
          handlePunch('CHECK_OUT')
        } else if (e.key === '3') {
          e.preventDefault()
          handlePunch('CLINICAL_ROUND_SIGN_IN')
        } else if (e.key === '4') {
          e.preventDefault()
          handlePunch('BREAK_OUT')
        } else if (e.key === '5') {
          e.preventDefault()
          handlePunch('BREAK_IN')
        } else if (e.key === 'Escape') {
          setSelectedStaff(null)
          if (searchInputRef.current) searchInputRef.current.focus()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [selectedStaff, filteredStaff, successResult, manualModalOpen, isSubmitting, currentTab])

  // Handle Report Downloads
  const handleDownloadExcel = async () => {
    setIsExportingExcel(true)
    await downloadExcelReport(startDate, endDate)
    setIsExportingExcel(false)
  }

  const handleDownloadWord = async () => {
    setIsExportingWord(true)
    await downloadWordReport(startDate, endDate)
    setIsExportingWord(false)
  }

  return (
    <div className="kiosk-container">
      {/* Header Bar */}
      <header className="header-bar">
        {/* Brand */}
        <div className="brand">
          <div className="brand-icon">
            <Building2 size={24} />
          </div>
          <div className="brand-title">
            <h1>{t.hospitalName}</h1>
            <p>
              <span>{t.stationName}</span>
              <span className="station-badge">Station: YM-3F-KIOSK</span>
            </p>
          </div>
        </div>

        {/* Nav Tabs */}
        <nav className="nav-tabs">
          <button
            className={`tab-btn ${currentTab === 'clockin' ? 'active' : ''}`}
            onClick={() => setCurrentTab('clockin')}
          >
            <LogIn size={16} />
            <span>{t.tabs.clockin}</span>
          </button>
          <button
            className={`tab-btn ${currentTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentTab('dashboard')}
          >
            <Activity size={16} />
            <span>{t.tabs.dashboard}</span>
          </button>
          <button
            className={`tab-btn ${currentTab === 'reports' ? 'active' : ''}`}
            onClick={() => setCurrentTab('reports')}
          >
            <FileSpreadsheet size={16} />
            <span>{t.tabs.reports}</span>
          </button>
        </nav>

        {/* Header Tools */}
        <div className="header-tools">
          {/* Dark / Light Toggle */}
          <button
            className="theme-toggle-btn"
            onClick={toggleTheme}
            title={theme === 'dark' ? '切換為淺色模式 (Light)' : '切換為深色模式 (Dark)'}
          >
            {theme === 'dark' ? (
              <>
                <Sun size={15} color="#f59e0b" />
                <span>{t.theme.light}</span>
              </>
            ) : (
              <>
                <Moon size={15} color="#6366f1" />
                <span>{t.theme.dark}</span>
              </>
            )}
          </button>

          {/* Status Pill */}
          <div className={`status-pill ${isOnline ? 'online' : 'offline'}`}>
            {isOnline ? <Wifi size={13} /> : <WifiOff size={13} />}
            <span>
              {isOnline
                ? t.online
                : `${t.offline} (${offlineCount})`}
            </span>
          </div>

          {/* Language Selector */}
          <div className="lang-selector">
            <button
              className={`lang-btn ${lang === 'zh-TW' ? 'active' : ''}`}
              onClick={() => setLang('zh-TW')}
            >
              中文
            </button>
            <button
              className={`lang-btn ${lang === 'vi' ? 'active' : ''}`}
              onClick={() => setLang('vi')}
            >
              Tiếng Việt
            </button>
            <button
              className={`lang-btn ${lang === 'id' ? 'active' : ''}`}
              onClick={() => setLang('id')}
            >
              Indonesia
            </button>
            <button
              className={`lang-btn ${lang === 'en' ? 'active' : ''}`}
              onClick={() => setLang('en')}
            >
              EN
            </button>
          </div>

          {/* Clock */}
          <div className="clock-card">
            <div className="clock-time">
              {currentTime.toLocaleTimeString('zh-TW', { hour12: false })}
            </div>
            <div className="clock-date">
              {currentTime.toLocaleDateString('zh-TW', {
                month: '2-digit',
                day: '2-digit',
                weekday: 'short',
              })}
            </div>
          </div>
        </div>
      </header>

      {/* =========================================================================
          Tab 1: Clock-In Console
          ========================================================================= */}
      {currentTab === 'clockin' && (
        <main className="kiosk-main">
          {/* Left Column: Punch Console */}
          <section className="punch-panel">
            {/* Search Input Card */}
            <div className="search-card">
              <div className="input-wrapper">
                <Search className="search-icon" size={22} />
                <input
                  ref={searchInputRef}
                  type="text"
                  className="keyboard-input"
                  placeholder={t.searchPlaceholder}
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  autoFocus
                />
              </div>
              <div className="keyboard-hint-bar">
                <div>{t.keyboardHint}</div>
                {selectedStaff && (
                  <button
                    className="clear-selection-btn"
                    onClick={() => {
                      setSelectedStaff(null)
                      if (searchInputRef.current) searchInputRef.current.focus()
                    }}
                  >
                    清除選取 (Esc)
                  </button>
                )}
              </div>
            </div>

            {/* Selected Staff Hero Card */}
            {selectedStaff ? (
              <div className="selected-staff-card">
                <div className="staff-profile">
                  <div
                    className={`staff-avatar ${
                      selectedStaff.employee_no === 'YM-DOC-01' ? 'doctor' : ''
                    }`}
                  >
                    {selectedStaff.employee_no === 'YM-DOC-01' ? (
                      <Stethoscope size={28} />
                    ) : (
                      selectedStaff.name.slice(0, 1)
                    )}
                  </div>
                  <div>
                    <div className="staff-name-line">
                      <span className="staff-name">{selectedStaff.name}</span>
                      <span className="emp-no-badge">
                        {selectedStaff.employee_no}
                      </span>
                    </div>
                    <div className="staff-role-line">
                      <span
                        className={`role-tag ${
                          selectedStaff.employee_no === 'YM-DOC-01'
                            ? 'doctor-tag'
                            : selectedStaff.role === 'SUPERVISOR'
                            ? 'supervisor-tag'
                            : ''
                        }`}
                      >
                        {selectedStaff.employee_no === 'YM-DOC-01'
                          ? t.doctorBadge
                          : selectedStaff.role === 'SUPERVISOR'
                          ? t.supervisorBadge
                          : selectedStaff.employee_no.includes('-FCNA-')
                          ? t.foreignBadge
                          : selectedStaff.role}
                      </span>
                      <span className="role-tag">
                        {selectedStaff.employment_type === 'FULL_TIME'
                          ? '正職'
                          : '兼任/支援'}
                      </span>
                    </div>
                  </div>
                </div>

                {selectedStaff.employee_no === 'YM-DOC-01' && (
                  <div style={{ textAlign: 'right', fontSize: '12px', color: 'var(--doctor)' }}>
                    <strong>{t.doctorRoundNote}</strong>
                  </div>
                )}
              </div>
            ) : (
              <div
                style={{
                  padding: '16px 20px',
                  background: 'var(--card-bg)',
                  borderRadius: 'var(--radius-lg)',
                  border: '1px dashed var(--card-border)',
                  color: 'var(--text-muted)',
                  fontSize: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                }}
              >
                <UserCheck size={18} />
                <span>{t.selectStaffFirst}</span>
              </div>
            )}

            {/* Action Buttons Grid */}
            <div className="action-buttons-grid">
              {/* Check In */}
              <button
                className="action-btn btn-check-in"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => handlePunch('CHECK_IN')}
              >
                <div className="action-btn-header">
                  <LogIn size={22} color="var(--success)" />
                  <span className="shortcut-badge">[1]</span>
                </div>
                <span className="action-btn-title">{t.actions.CHECK_IN}</span>
                <span className="action-btn-desc">
                  {t.actionDescriptions.CHECK_IN}
                </span>
              </button>

              {/* Check Out */}
              <button
                className="action-btn btn-check-out"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => handlePunch('CHECK_OUT')}
              >
                <div className="action-btn-header">
                  <LogOut size={22} color="var(--danger)" />
                  <span className="shortcut-badge">[2]</span>
                </div>
                <span className="action-btn-title">{t.actions.CHECK_OUT}</span>
                <span className="action-btn-desc">
                  {t.actionDescriptions.CHECK_OUT}
                </span>
              </button>

              {/* Doctor Round Sign In (Prominent for Dr. Chu) */}
              <button
                className="action-btn btn-doctor-round"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => handlePunch('CLINICAL_ROUND_SIGN_IN')}
                style={{
                  boxShadow:
                    selectedStaff?.employee_no === 'YM-DOC-01'
                      ? '0 0 0 3px var(--doctor-border)'
                      : undefined,
                }}
              >
                <div className="action-btn-header">
                  <Stethoscope size={22} color="var(--doctor)" />
                  <span className="shortcut-badge">[3]</span>
                </div>
                <span className="action-btn-title">
                  {t.actions.CLINICAL_ROUND_SIGN_IN}
                </span>
                <span className="action-btn-desc">
                  {t.actionDescriptions.CLINICAL_ROUND_SIGN_IN}
                </span>
              </button>

              {/* Break Out */}
              <button
                className="action-btn btn-break-out"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => handlePunch('BREAK_OUT')}
              >
                <div className="action-btn-header">
                  <Coffee size={22} color="var(--warning)" />
                  <span className="shortcut-badge">[4]</span>
                </div>
                <span className="action-btn-title">{t.actions.BREAK_OUT}</span>
                <span className="action-btn-desc">
                  {t.actionDescriptions.BREAK_OUT}
                </span>
              </button>

              {/* Break In */}
              <button
                className="action-btn btn-break-in"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => handlePunch('BREAK_IN')}
              >
                <div className="action-btn-header">
                  <RotateCcw size={22} color="var(--info)" />
                  <span className="shortcut-badge">[5]</span>
                </div>
                <span className="action-btn-title">{t.actions.BREAK_IN}</span>
                <span className="action-btn-desc">
                  {t.actionDescriptions.BREAK_IN}
                </span>
              </button>

              {/* Manual Override */}
              <button
                className="action-btn btn-on-duty"
                disabled={!selectedStaff || isSubmitting}
                onClick={() => {
                  setManualReason('')
                  setManualModalOpen(true)
                }}
              >
                <div className="action-btn-header">
                  <ShieldCheck size={22} color="#a855f7" />
                  <span className="shortcut-badge">[M]</span>
                </div>
                <span className="action-btn-title">{t.manualOverrideBtn}</span>
                <span className="action-btn-desc">例外打卡與事由填寫</span>
              </button>
            </div>

            {/* Staff Roster Browser */}
            <div className="staff-browser-card">
              <div className="category-tabs">
                <button
                  className={`tab-btn ${activeCategory === 'all' ? 'active' : ''}`}
                  onClick={() => setActiveCategory('all')}
                >
                  {t.categories.all}
                </button>
                <button
                  className={`tab-btn ${
                    activeCategory === 'nurse' ? 'active' : ''
                  }`}
                  onClick={() => setActiveCategory('nurse')}
                >
                  {t.categories.nurse}
                </button>
                <button
                  className={`tab-btn ${
                    activeCategory === 'cna' ? 'active' : ''
                  }`}
                  onClick={() => setActiveCategory('cna')}
                >
                  {t.categories.cna}
                </button>
                <button
                  className={`tab-btn ${
                    activeCategory === 'fcna' ? 'active' : ''
                  }`}
                  onClick={() => setActiveCategory('fcna')}
                >
                  {t.categories.fcna}
                </button>
                <button
                  className={`tab-btn ${
                    activeCategory === 'doctor_spec' ? 'active' : ''
                  }`}
                  onClick={() => setActiveCategory('doctor_spec')}
                >
                  {t.categories.doctor_spec}
                </button>
                <button
                  className={`tab-btn ${
                    activeCategory === 'support' ? 'active' : ''
                  }`}
                  onClick={() => setActiveCategory('support')}
                >
                  {t.categories.support}
                </button>
              </div>

              {/* Staff Grid */}
              <div className="staff-grid">
                {filteredStaff.map((staff) => {
                  const isSelected = selectedStaff?.id === staff.id
                  const isDoctor = staff.employee_no === 'YM-DOC-01'
                  return (
                    <button
                      key={staff.id}
                      className={`staff-card ${isSelected ? 'selected' : ''}`}
                      onClick={() => {
                        setSelectedStaff(staff)
                        setSearchQuery('')
                      }}
                    >
                      <span className="card-emp-no">{staff.employee_no}</span>
                      <span className="card-name">
                        {staff.name} {isDoctor && '👨‍⚕️'}
                      </span>
                      <span className="card-role">
                        {isDoctor
                          ? '兼任醫師 (巡診)'
                          : staff.role === 'SUPERVISOR'
                          ? '護理長/負責人'
                          : staff.employee_no.includes('-FCNA-')
                          ? '外籍照服員'
                          : staff.role}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>
          </section>

          {/* Right Column: Live Sidebar */}
          <aside className="sidebar-panel">
            {/* Quick Stats Grid */}
            <div className="stats-grid">
              <div className="stat-box">
                <span className="stat-number" style={{ color: 'var(--success)' }}>
                  {
                    recentPunches.filter((p) => p.event_type === 'CHECK_IN')
                      .length
                  }
                </span>
                <span className="stat-label">今日到勤</span>
              </div>
              <div className="stat-box">
                <span className="stat-number" style={{ color: 'var(--doctor)' }}>
                  {
                    recentPunches.filter(
                      (p) => p.event_type === 'CLINICAL_ROUND_SIGN_IN'
                    ).length
                  }
                </span>
                <span className="stat-label">醫師巡診</span>
              </div>
              <div className="stat-box">
                <span className="stat-number" style={{ color: 'var(--warning)' }}>
                  {
                    recentPunches.filter((p) => p.event_type === 'BREAK_OUT')
                      .length
                  }
                </span>
                <span className="stat-label">外出中</span>
              </div>
            </div>

            {/* Recent Activity List */}
            <div className="recent-activity-card">
              <div className="activity-header">
                <span>{t.recentPunchesTitle}</span>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  護理站即時流水
                </span>
              </div>

              <div className="activity-list">
                {recentPunches.length === 0 ? (
                  <div
                    style={{
                      padding: '40px 20px',
                      textAlign: 'center',
                      color: 'var(--text-muted)',
                      fontSize: '13px',
                    }}
                  >
                    今日尚無打卡紀錄
                  </div>
                ) : (
                  recentPunches.map((item) => (
                    <div key={item.id} className="activity-item">
                      <div>
                        <div className="activity-name">{item.name}</div>
                        <div className="activity-time">
                          {new Date(item.occurred_at).toLocaleTimeString('zh-TW', {
                            hour12: false,
                          })}{' '}
                          • {item.employee_no}
                        </div>
                      </div>
                      <span
                        className={`event-type-badge badge-${item.event_type.toLowerCase()}`}
                      >
                        {t.actions[item.event_type] || item.event_type}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </aside>
        </main>
      )}

      {/* =========================================================================
          Tab 2: Live Attendance Dashboard
          ========================================================================= */}
      {currentTab === 'dashboard' && (
        <section className="report-center-container">
          {/* Dashboard Summary Hero */}
          <div className="report-hero-card">
            <div>
              <h2 style={{ fontSize: '20px', fontWeight: 700 }}>
                {t.hospitalName} - 出勤即時監控看板
              </h2>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
                即時掌握全院 28 名同仁出勤動態、兼任醫師巡診在勤紀錄與外出狀態
              </p>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                className="theme-toggle-btn"
                onClick={() => fetchRecentPunches().then(setRecentPunches)}
              >
                <RotateCcw size={14} />
                <span>重新整理</span>
              </button>
            </div>
          </div>

          {/* Stats Big Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '14px' }}>
            <div className="stat-box" style={{ padding: '18px' }}>
              <span className="stat-label">在籍同仁總數</span>
              <span className="stat-number" style={{ color: 'var(--primary-soft)' }}>28</span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                陽明護理之家專用
              </span>
            </div>

            <div className="stat-box" style={{ padding: '18px' }}>
              <span className="stat-label">今日上班簽到人數</span>
              <span className="stat-number" style={{ color: 'var(--success)' }}>
                {recentPunches.filter((p) => p.event_type === 'CHECK_IN').length}
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                簽到正常完成
              </span>
            </div>

            <div className="stat-box" style={{ padding: '18px' }}>
              <span className="stat-label">兼任醫師巡診簽到</span>
              <span className="stat-number" style={{ color: 'var(--doctor)' }}>
                {
                  recentPunches.filter(
                    (p) => p.event_type === 'CLINICAL_ROUND_SIGN_IN'
                  ).length
                }
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                朱醫師 3F 病房訪視
              </span>
            </div>

            <div className="stat-box" style={{ padding: '18px' }}>
              <span className="stat-label">本機待同步離線紀錄</span>
              <span className="stat-number" style={{ color: 'var(--warning)' }}>
                {offlineCount}
              </span>
              <span style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                離線佇列保全中
              </span>
            </div>
          </div>

          {/* Activity Log Table */}
          <div className="report-table-card">
            <div className="table-title-row">
              <h3 style={{ fontSize: '16px', fontWeight: 700 }}>
                今日即時打卡與巡診流水清單 ({recentPunches.length} 筆)
              </h3>
            </div>

            <table className="data-table">
              <thead>
                <tr>
                  <th>時間</th>
                  <th>工號</th>
                  <th>同仁姓名</th>
                  <th>事件類型</th>
                  <th>站點代碼</th>
                  <th>巡診病房</th>
                  <th>打卡來源</th>
                </tr>
              </thead>
              <tbody>
                {recentPunches.length === 0 ? (
                  <tr>
                    <td colSpan={7} style={{ textAlign: 'center', padding: '30px', color: 'var(--text-muted)' }}>
                      今日尚無打卡流水資料
                    </td>
                  </tr>
                ) : (
                  recentPunches.map((item) => (
                    <tr key={item.id}>
                      <td style={{ fontFamily: 'monospace' }}>
                        {new Date(item.occurred_at).toLocaleTimeString('zh-TW', { hour12: false })}
                      </td>
                      <td style={{ fontWeight: 600, color: 'var(--primary-soft)' }}>
                        {item.employee_no}
                      </td>
                      <td style={{ fontWeight: 700 }}>
                        {item.name} {item.employee_no === 'YM-DOC-01' && '👨‍⚕️'}
                      </td>
                      <td>
                        <span className={`event-type-badge badge-${item.event_type.toLowerCase()}`}>
                          {t.actions[item.event_type] || item.event_type}
                        </span>
                      </td>
                      <td>YM-3F-KIOSK</td>
                      <td>{item.ward_code || '-'}</td>
                      <td style={{ color: 'var(--text-muted)' }}>{item.source || 'WEB'}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {/* =========================================================================
          Tab 3: Report & Export Center (Excel & Word)
          ========================================================================= */}
      {currentTab === 'reports' && (
        <section className="report-center-container">
          {/* Report Center Hero */}
          <div className="report-hero-card">
            <div className="report-hero-title">
              <h2>{t.reports.title}</h2>
              <p>{t.reports.subtitle}</p>
            </div>

            {/* Date Filters & Print */}
            <div className="date-filter-group">
              <Calendar size={16} color="var(--primary-soft)" />
              <span style={{ fontSize: '13px', fontWeight: 600 }}>{t.reports.periodLabel}:</span>
              <input
                type="date"
                className="date-input"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <span style={{ color: 'var(--text-muted)' }}>~</span>
              <input
                type="date"
                className="date-input"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
              <button
                className="theme-toggle-btn"
                style={{ marginLeft: '6px' }}
                onClick={() => window.print()}
                title="列印目前報表"
              >
                <Printer size={15} />
                <span>{t.reports.printBtn}</span>
              </button>
            </div>
          </div>

          {/* Export Action Cards (Excel & Word) */}
          <div className="export-cards-grid">
            {/* Excel Export Card */}
            <div className="export-card">
              <div className="export-card-header">
                <div className="export-icon-box excel">
                  <FileSpreadsheet size={26} />
                </div>
                <div className="export-card-body">
                  <h3>{t.reports.excelTitle}</h3>
                  <p>{t.reports.excelDesc}</p>
                </div>
              </div>
              <button
                className="export-btn excel"
                onClick={handleDownloadExcel}
                disabled={isExportingExcel}
              >
                <Download size={17} />
                <span>{isExportingExcel ? '正在產製 Excel...' : t.reports.excelBtn}</span>
              </button>
            </div>

            {/* Word Export Card */}
            <div className="export-card">
              <div className="export-card-header">
                <div className="export-icon-box word">
                  <FileText size={26} />
                </div>
                <div className="export-card-body">
                  <h3>{t.reports.wordTitle}</h3>
                  <p>{t.reports.wordDesc}</p>
                </div>
              </div>
              <button
                className="export-btn word"
                onClick={handleDownloadWord}
                disabled={isExportingWord}
              >
                <Download size={17} />
                <span>{isExportingWord ? '正在產製 Word...' : t.reports.wordBtn}</span>
              </button>
            </div>
          </div>

          {/* Staff Roster Overview Table */}
          <div className="report-table-card">
            <div className="table-title-row">
              <div>
                <h3 style={{ fontSize: '16px', fontWeight: 700 }}>
                  {t.reports.tableTitle}
                </h3>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  陽明醫院附設護理之家 • 符合影子模式與不碰病歷個資規範
                </span>
              </div>

              <div style={{ width: '260px' }}>
                <input
                  type="text"
                  className="date-input"
                  style={{ width: '100%' }}
                  placeholder="搜尋報表同仁或職務..."
                  value={reportSearchQuery}
                  onChange={(e) => setReportSearchQuery(e.target.value)}
                />
              </div>
            </div>

            <table className="data-table">
              <thead>
                <tr>
                  <th>員工編號</th>
                  <th>姓名</th>
                  <th>單位</th>
                  <th>職務角色</th>
                  <th>聘僱別</th>
                  <th>巡診／值班備註</th>
                  <th>狀態</th>
                </tr>
              </thead>
              <tbody>
                {reportFilteredStaff.map((s) => {
                  const isDoctor = s.employee_no === 'YM-DOC-01'
                  const isSupervisor = s.role === 'SUPERVISOR'
                  const isForeign = s.employee_no.includes('-FCNA-')
                  return (
                    <tr key={s.id} style={{ background: isDoctor ? 'var(--doctor-light)' : undefined }}>
                      <td style={{ fontFamily: 'monospace', fontWeight: 600 }}>{s.employee_no}</td>
                      <td style={{ fontWeight: 700 }}>
                        {s.name} {isDoctor && '👨‍⚕️'}
                      </td>
                      <td>護理之家 (3F)</td>
                      <td>
                        <span
                          className={`role-tag ${
                            isDoctor
                              ? 'doctor-tag'
                              : isSupervisor
                              ? 'supervisor-tag'
                              : ''
                          }`}
                        >
                          {isDoctor
                            ? '兼任主治醫師'
                            : isSupervisor
                            ? '護理長 / 負責人'
                            : isForeign
                            ? '外籍照服員'
                            : s.role}
                        </span>
                      </td>
                      <td>{s.employment_type === 'FULL_TIME' ? '正職' : '兼任 / 支援'}</td>
                      <td style={{ fontSize: '12px', color: isDoctor ? 'var(--doctor)' : 'var(--text-muted)' }}>
                        {isDoctor ? '定期病房巡診與在場簽到' : isForeign ? '日夜輪班照護' : '-'}
                      </td>
                      <td>
                        <span className="status-pill online" style={{ fontSize: '11px', display: 'inline-flex' }}>
                          在職納管
                        </span>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}

      {/* =========================================================================
          Modals & Overlays
          ========================================================================= */}

      {/* Punch Success Modal */}
      {successResult && (
        <div
          className="modal-overlay"
          onClick={() => {
            setSuccessResult(null)
            setSelectedStaff(null)
            if (searchInputRef.current) searchInputRef.current.focus()
          }}
        >
          <div
            className="success-modal-card"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="success-icon-box">
              <CheckCircle2 size={38} />
            </div>
            <h2 style={{ fontSize: '20px', fontWeight: 700, color: 'var(--text-main)' }}>
              {t.punchSuccess}
            </h2>
            <div style={{ color: 'var(--text-main)', fontSize: '14px', lineHeight: 1.6 }}>
              <strong>{successResult.message}</strong>
              <div
                style={{
                  marginTop: '8px',
                  fontSize: '12.5px',
                  color: 'var(--text-muted)',
                }}
              >
                時間：{new Date(successResult.occurred_at).toLocaleTimeString('zh-TW', { hour12: false })}
                {successResult.ward_code && ` • 巡診病房：${successResult.ward_code}`}
              </div>
            </div>

            <button
              className="export-btn"
              style={{
                width: '100%',
                background: 'var(--primary)',
                color: 'white',
                marginTop: '10px',
              }}
              onClick={() => {
                setSuccessResult(null)
                setSelectedStaff(null)
                if (searchInputRef.current) searchInputRef.current.focus()
              }}
            >
              {t.closeBtn}
            </button>

            <span className="countdown-bar">
              {countdown} {t.countdownClose}
            </span>
          </div>
        </div>
      )}

      {/* Manual Exception Modal */}
      {manualModalOpen && selectedStaff && (
        <div
          className="modal-overlay"
          onClick={() => setManualModalOpen(false)}
        >
          <div
            className="success-modal-card"
            style={{ width: '460px', textAlign: 'left', alignItems: 'stretch' }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3
              style={{
                fontSize: '18px',
                fontWeight: '700',
                marginBottom: '10px',
                color: 'var(--text-main)',
              }}
            >
              {t.manualOverrideTitle}
            </h3>

            <div style={{ marginBottom: '12px' }}>
              <label
                style={{
                  fontSize: '12.5px',
                  fontWeight: '600',
                  color: 'var(--text-muted)',
                  display: 'block',
                  marginBottom: '4px',
                }}
              >
                打卡對象
              </label>
              <div
                style={{
                  padding: '9px 12px',
                  background: 'var(--panel-inner)',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: '700',
                  border: '1px solid var(--card-border)',
                }}
              >
                {selectedStaff.name} ({selectedStaff.employee_no})
              </div>
            </div>

            <div style={{ marginBottom: '12px' }}>
              <label
                style={{
                  fontSize: '12.5px',
                  fontWeight: '600',
                  color: 'var(--text-muted)',
                  display: 'block',
                  marginBottom: '4px',
                }}
              >
                打卡動作型別
              </label>
              <select
                style={{
                  width: '100%',
                  padding: '9px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--card-border)',
                  background: 'var(--input-bg)',
                  color: 'var(--text-main)',
                }}
                value={manualEventType}
                onChange={(e) =>
                  setManualEventType(e.target.value as AttendanceEventType)
                }
              >
                <option value="CHECK_IN">上班簽到</option>
                <option value="CHECK_OUT">下班簽退</option>
                <option value="CLINICAL_ROUND_SIGN_IN">醫師巡診簽到</option>
                <option value="BREAK_OUT">中途外出</option>
                <option value="BREAK_IN">外出返回</option>
                <option value="ON_DUTY_SIGN_IN">夜/假值班簽到</option>
                <option value="ON_DUTY_SIGN_OUT">夜/假值班簽退</option>
              </select>
            </div>

            <div style={{ marginBottom: '16px' }}>
              <label
                style={{
                  fontSize: '12.5px',
                  fontWeight: '600',
                  color: 'var(--text-muted)',
                  display: 'block',
                  marginBottom: '4px',
                }}
              >
                {t.reasonLabel}
              </label>
              <textarea
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--card-border)',
                  background: 'var(--input-bg)',
                  color: 'var(--text-main)',
                  minHeight: '80px',
                }}
                placeholder="例如：公出長照會議、指紋機障礙主管手動簽核..."
                value={manualReason}
                onChange={(e) => setManualReason(e.target.value)}
              />
            </div>

            <div
              style={{
                display: 'flex',
                gap: '10px',
                justifyContent: 'flex-end',
              }}
            >
              <button
                className="clear-selection-btn"
                onClick={() => setManualModalOpen(false)}
              >
                {t.cancelBtn}
              </button>
              <button
                style={{
                  padding: '8px 18px',
                  background: 'var(--primary)',
                  color: 'white',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: '600',
                }}
                disabled={!manualReason.trim()}
                onClick={() => {
                  setManualModalOpen(false)
                  handlePunch(manualEventType, manualReason)
                }}
              >
                {t.confirmBtn}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
