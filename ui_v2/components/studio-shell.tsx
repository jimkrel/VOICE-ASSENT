"use client"

import { usePathname } from "next/navigation"
import { WorkspaceSidebar, type WorkspaceTool } from "@/components/workspace-sidebar"
import { WorkspaceTopBar } from "@/components/workspace-topbar"
import { WorkspaceMobileNav } from "@/components/workspace-sidebar"
import { WorkspaceSettingsPanel } from "@/components/workspace-settings-panel"
import { useVoiceStudio } from "@/components/voice-studio-context"

export function StudioShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const {
    selectedVoiceId,
    setSelectedVoiceId,
    voices,
    settings,
    setSettings,
    history,
    searchValue,
    setSearchValue,
    mobileSettingsOpen,
    setMobileSettingsOpen,
  } = useVoiceStudio()

  const activeTool: WorkspaceTool = pathname.includes("voice-creation")
    ? "voice-creation"
    : pathname.includes("voice-changer")
      ? "voice-changer"
      : pathname.includes("voice-library")
        ? "voice-library"
        : "text-to-speech"

  const showSettings = activeTool === "text-to-speech" || activeTool === "voice-changer"

  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground lg:h-screen lg:min-h-0 lg:overflow-hidden">
      <div className="flex min-h-0 flex-1">
        <WorkspaceSidebar
          activeTool={activeTool}
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
          <WorkspaceMobileNav activeTool={activeTool} />

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
              {children}
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
