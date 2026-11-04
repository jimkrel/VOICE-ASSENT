"use client"

import { VoiceChangerWorkspace } from "@/components/voice-changer-workspace"
import { useVoiceStudio } from "@/components/voice-studio-context"

export default function VoiceChangerPage() {
  const {
    selectedVoiceId,
    setSelectedVoiceId,
    voices,
    settings,
    setSettings,
    fetchHistory,
  } = useVoiceStudio()

  return (
    <VoiceChangerWorkspace
      selectedVoiceId={selectedVoiceId}
      onSelectVoice={setSelectedVoiceId}
      voices={voices}
      settings={settings}
      onChangeSettings={setSettings}
      onGenerated={fetchHistory}
    />
  )
}
