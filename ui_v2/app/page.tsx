import { redirect } from "next/navigation"

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ tab?: string }>
}) {
  const resolved = await searchParams
  const tab = resolved?.tab
  if (tab === "voice-creation") redirect("/voice-creation")
  if (tab === "voice-changer") redirect("/voice-changer")
  if (tab === "voice-library") redirect("/voice-library")
  redirect("/text-to-speech")
}
