"use client"

import { VoiceCreationWorkspace } from "@/components/voice-creation-workspace"
import { useVoiceStudio } from "@/components/voice-studio-context"

export default function VoiceCreationPage() {
  const {
    selectedVoiceId,
    handleVoiceCreated,
    useVoiceForScript,
    fetchHistory,
  } = useVoiceStudio()

  return (
    <VoiceCreationWorkspace
      selectedVoiceId={selectedVoiceId}
      onVoiceCreated={handleVoiceCreated}
      onUseVoice={useVoiceForScript}
      onGenerated={fetchHistory}
    />
  )
}
