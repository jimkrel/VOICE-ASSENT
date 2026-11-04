"use client"

import { TextToSpeechWorkspace } from "@/components/text-to-speech-workspace"
import { useVoiceStudio } from "@/components/voice-studio-context"

export default function TextToSpeechPage() {
  const {
    selectedVoiceId,
    setSelectedVoiceId,
    voices,
    settings,
    setSettings,
    fetchHistory,
  } = useVoiceStudio()

  return (
    <TextToSpeechWorkspace
      selectedVoiceId={selectedVoiceId}
      onSelectVoice={setSelectedVoiceId}
      voices={voices}
      settings={settings}
      onChangeSettings={setSettings}
      onGenerated={fetchHistory}
    />
  )
}
