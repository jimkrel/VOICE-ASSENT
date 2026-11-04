"use client"

import { VoiceLibraryWorkspace } from "@/components/voice-library-workspace"
import { useVoiceStudio } from "@/components/voice-studio-context"

export default function VoiceLibraryPage() {
  const {
    selectedVoiceId,
    setSelectedVoiceId,
    useVoiceForScript,
    handleVoiceDeleted,
    voices,
  } = useVoiceStudio()

  return (
    <VoiceLibraryWorkspace
      selectedVoiceId={selectedVoiceId}
      onSelectVoice={setSelectedVoiceId}
      onUseVoice={useVoiceForScript}
      onVoiceDeleted={handleVoiceDeleted}
      voices={voices}
    />
  )
}
