"use client"

import { useCallback, useEffect, useState } from "react"
import { TextToSpeechWorkspace } from "@/components/text-to-speech-workspace"
import { VoiceChangerWorkspace } from "@/components/voice-changer-workspace"
import { VoiceCreationWorkspace } from "@/components/voice-creation-workspace"
import { VoiceLibraryWorkspace } from "@/components/voice-library-workspace"
import { WorkspaceSettingsPanel } from "@/components/workspace-settings-panel"
import {
  WorkspaceMobileNav,
  WorkspaceSidebar,
  type WorkspaceTool,
} from "@/components/workspace-sidebar"
import { WorkspaceTopBar } from "@/components/workspace-topbar"
import {
  defaultVoiceSettings,
  voiceCatalog,
  type HistoryItem,
  type VoiceProfile,
  type VoiceSettings,
} from "@/lib/voice-catalog"

export function VoiceWorkspace({
  initialTool = "text-to-speech",
}: {
  initialTool?: WorkspaceTool
} = {}) {
  const [activeTool, setActiveTool] = useState<WorkspaceTool>(initialTool)
  const [searchValue, setSearchValue] = useState("")
  const [mobileSettingsOpen, setMobileSettingsOpen] = useState(false)
  const [selectedVoiceId, setSelectedVoiceId] = useState("hope")
  const [voices, setVoices] = useState<VoiceProfile[]>(voiceCatalog)
  const [settings, setSettings] = useState<VoiceSettings>(defaultVoiceSettings)
  const [history, setHistory] = useState<HistoryItem[]>([])

  const showSettings = activeTool === "text-to-speech" || activeTool === "voice-changer"

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

  useEffect(() => {
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search)
      const tab = params.get("tab") as WorkspaceTool | null
      if (
        tab === "text-to-speech" ||
        tab === "voice-creation" ||
        tab === "voice-changer" ||
        tab === "voice-library"
      ) {
        setActiveTool(tab)
      }
    }
    fetchVoices()
    fetchHistory()
  }, [fetchVoices, fetchHistory])

  function handleToolSelect(tool: WorkspaceTool) {
    setActiveTool(tool)
    setMobileSettingsOpen(false)
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href)
      url.searchParams.set("tab", tool)
      window.history.replaceState({}, "", url.toString())
    }
  }

  function useVoiceForScript(voiceId: string) {
    setSelectedVoiceId(voiceId)
    handleToolSelect("text-to-speech")
  }

  function handleVoiceCreated(newVoice: VoiceProfile) {
    setVoices((prev) => {
      const exists = prev.some((v) => v.id === newVoice.id)
      return exists ? prev.map((v) => (v.id === newVoice.id ? newVoice : v)) : [...prev, newVoice]
    })
    setSelectedVoiceId(newVoice.id)
    fetchHistory()
  }

  function handleVoiceDeleted(deletedId: string) {
    setVoices((prev) => prev.filter((v) => v.id !== deletedId))
    if (selectedVoiceId === deletedId) {
      setSelectedVoiceId("hope")
    }
    fetchVoices()
  }

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground lg:h-screen lg:min-h-0 lg:overflow-hidden">
      <div className="flex min-h-0 flex-1">
        <WorkspaceSidebar
          activeTool={activeTool}
          onSelect={handleToolSelect}
          searchValue={searchValue}
        />

        <div className="flex min-h-0 min-w-0 flex-1 flex-col">
          <WorkspaceTopBar
            activeTool={activeTool}
            searchValue={searchValue}
            onSearchChange={setSearchValue}
            showSettings={showSettings}
            mobileSettingsOpen={mobileSettingsOpen}
            onToggleMobileSettings={() => setMobileSettingsOpen((open) => !open)}
          />
          <WorkspaceMobileNav activeTool={activeTool} onSelect={handleToolSelect} />

          <div className="flex min-h-0 flex-1 flex-col xl:flex-row">
            {showSettings && mobileSettingsOpen ? (
              <WorkspaceSettingsPanel
                activeTool={activeTool}
                selectedVoiceId={selectedVoiceId}
                onSelectVoice={setSelectedVoiceId}
                voices={voices}
                settings={settings}
                onChangeSettings={setSettings}
                history={history}
                className="h-[42vh] max-h-[42vh] shrink-0 border-b border-border bg-card xl:hidden"
              />
            ) : null}

            <main
              id="workspace"
              className="min-h-[540px] min-w-0 flex-1 overflow-y-auto bg-background xl:min-h-0"
            >
              {activeTool === "text-to-speech" ? (
                <TextToSpeechWorkspace
                  selectedVoiceId={selectedVoiceId}
                  settings={settings}
                  onGenerated={fetchHistory}
                />
              ) : null}
              {activeTool === "voice-creation" ? (
                <VoiceCreationWorkspace
                  selectedVoiceId={selectedVoiceId}
                  onVoiceCreated={handleVoiceCreated}
                  onUseVoice={useVoiceForScript}
                  onGenerated={fetchHistory}
                />
              ) : null}
              {activeTool === "voice-changer" ? (
                <VoiceChangerWorkspace
                  selectedVoiceId={selectedVoiceId}
                  settings={settings}
                  onGenerated={fetchHistory}
                />
              ) : null}
              {activeTool === "voice-library" ? (
                <VoiceLibraryWorkspace
                  selectedVoiceId={selectedVoiceId}
                  onSelectVoice={setSelectedVoiceId}
                  onUseVoice={useVoiceForScript}
                  onCreateNewVoice={() => handleToolSelect("voice-creation")}
                  onVoiceDeleted={handleVoiceDeleted}
                  voices={voices}
                />
              ) : null}
            </main>

            {showSettings ? (
              <WorkspaceSettingsPanel
                activeTool={activeTool}
                selectedVoiceId={selectedVoiceId}
                onSelectVoice={setSelectedVoiceId}
                voices={voices}
                settings={settings}
                onChangeSettings={setSettings}
                history={history}
                className="hidden h-full w-[280px] shrink-0 border-l border-border bg-card 2xl:w-[300px] xl:flex"
              />
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}
