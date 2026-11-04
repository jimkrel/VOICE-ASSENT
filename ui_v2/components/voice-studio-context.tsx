"use client"

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react"
import { useRouter } from "next/navigation"
import {
  defaultVoiceSettings,
  voiceCatalog,
  type HistoryItem,
  type VoiceProfile,
  type VoiceSettings,
} from "@/lib/voice-catalog"

export type HardwareTelemetry = {
  cpu: number
  gpu: number
  gpuTemp: number
  ram: number
  ramUsedGb: number
  ramTotalGb: number
  vramUsedGb: number
  vramTotalGb: number
  vramPct: number
  gpuName: string
  taskName?: string
  stage?: string
  status?: string
}

const defaultHardwareTelemetry: HardwareTelemetry = {
  cpu: 1,
  gpu: 0,
  gpuTemp: 45,
  ram: 50,
  ramUsedGb: 8.0,
  ramTotalGb: 16.0,
  vramUsedGb: 2.6,
  vramTotalGb: 4.0,
  vramPct: 65,
  gpuName: "NVIDIA GeForce GTX 1650",
  status: "idle",
  stage: "Sẵn sàng",
}

type VoiceStudioContextType = {
  selectedVoiceId: string
  setSelectedVoiceId: (id: string) => void
  voices: VoiceProfile[]
  setVoices: React.Dispatch<React.SetStateAction<VoiceProfile[]>>
  settings: VoiceSettings
  setSettings: React.Dispatch<React.SetStateAction<VoiceSettings>>
  history: HistoryItem[]
  searchValue: string
  setSearchValue: (val: string) => void
  mobileSettingsOpen: boolean
  setMobileSettingsOpen: React.Dispatch<React.SetStateAction<boolean>>
  telemetry: HardwareTelemetry
  fetchVoices: () => Promise<void>
  fetchHistory: () => Promise<void>
  deleteHistoryItem: (filename: string) => Promise<void>
  clearAllHistory: () => Promise<void>
  handleVoiceCreated: (newVoice: VoiceProfile) => void
  handleVoiceDeleted: (deletedId: string) => void
  useVoiceForScript: (voiceId: string) => void
}

const VoiceStudioContext = createContext<VoiceStudioContextType | null>(null)

export function VoiceStudioProvider({ children }: { children: ReactNode }) {
  const router = useRouter()
  const [selectedVoiceId, setSelectedVoiceId] = useState("minh-anh")
  const [voices, setVoices] = useState<VoiceProfile[]>(voiceCatalog)
  const [settings, setSettings] = useState<VoiceSettings>(defaultVoiceSettings)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [searchValue, setSearchValue] = useState("")
  const [mobileSettingsOpen, setMobileSettingsOpen] = useState(false)
  const [telemetry, setTelemetry] = useState<HardwareTelemetry>(defaultHardwareTelemetry)

  const fetchVoices = useCallback(async () => {
    try {
      const res = await fetch("/api/voices")
      if (!res.ok) return
      const data = await res.json()
      if (Array.isArray(data.voices) && data.voices.length > 0) {
        setVoices(data.voices)
      }
    } catch {
      // Fallback to built-in catalog if offline
    }
  }, [])

  const fetchHistory = useCallback(async () => {
    try {
      const res = await fetch("/api/history")
      if (!res.ok) return
      const data = await res.json()
      if (Array.isArray(data.history)) {
        setHistory(data.history)
      }
    } catch {
      // Ignore offline history fetch error
    }
  }, [])

  const deleteHistoryItem = useCallback(async (filename: string) => {
    try {
      const res = await fetch(`/api/history/${filename}`, { method: "DELETE" })
      if (!res.ok) return
      setHistory((prev) => prev.filter((item) => item.filename !== filename))
    } catch {
      // error handling
    }
  }, [])

  const clearAllHistory = useCallback(async () => {
    try {
      const res = await fetch("/api/history", { method: "DELETE" })
      if (!res.ok) return
      setHistory([])
    } catch {
      // error handling
    }
  }, [])

  const fetchTelemetry = useCallback(async () => {
    try {
      const res = await fetch("/api/system/metrics")
      if (!res.ok) return
      const data = await res.json()
      if (data && data.hardware) {
        setTelemetry({
          ...data.hardware,
          taskName: data.telemetry?.taskName,
          stage: data.telemetry?.stage,
          status: data.telemetry?.status,
        })
      }
    } catch {
      // Telemetry error
    }
  }, [])

  useEffect(() => {
    fetchVoices()
    fetchHistory()
    fetchTelemetry()

    // Smart Hardware Polling: Pauses when tab is inactive, relaxed interval (3.5s) to keep PC cool & smooth
    let isFetching = false
    const pollFn = async () => {
      if (typeof document !== "undefined" && document.hidden) {
        return // Tab in background -> zero CPU overhead
      }
      if (isFetching) return
      isFetching = true
      try {
        await fetchTelemetry()
      } finally {
        isFetching = false
      }
    }

    const timer = setInterval(pollFn, 3500)
    return () => clearInterval(timer)
  }, [fetchVoices, fetchHistory, fetchTelemetry])

  const handleVoiceCreated = useCallback(
    (newVoice: VoiceProfile) => {
      setVoices((prev) => {
        const exists = prev.some((v) => v.id === newVoice.id)
        return exists ? prev.map((v) => (v.id === newVoice.id ? newVoice : v)) : [...prev, newVoice]
      })
      setSelectedVoiceId(newVoice.id)
      fetchHistory()
    },
    [fetchHistory]
  )

  const handleVoiceDeleted = useCallback(
    (deletedId: string) => {
      setVoices((prev) => prev.filter((v) => v.id !== deletedId))
      setSelectedVoiceId((curr) => (curr === deletedId ? "minh-anh" : curr))
      fetchVoices()
    },
    [fetchVoices]
  )

  const useVoiceForScript = useCallback(
    (voiceId: string) => {
      setSelectedVoiceId(voiceId)
      router.push("/text-to-speech")
    },
    [router]
  )

  return (
    <VoiceStudioContext.Provider
      value={{
        selectedVoiceId,
        setSelectedVoiceId,
        voices,
        setVoices,
        settings,
        setSettings,
        history,
        searchValue,
        setSearchValue,
        mobileSettingsOpen,
        setMobileSettingsOpen,
        telemetry,
        fetchVoices,
        fetchHistory,
        deleteHistoryItem,
        clearAllHistory,
        handleVoiceCreated,
        handleVoiceDeleted,
        useVoiceForScript,
      }}
    >
      {children}
    </VoiceStudioContext.Provider>
  )
}

export function useVoiceStudio() {
  const context = useContext(VoiceStudioContext)
  if (!context) {
    throw new Error("useVoiceStudio must be used within a VoiceStudioProvider")
  }
  return context
}
