"use client";

import { useParams } from "next/navigation";
import { VoiceControls } from "@/components/conversation/VoiceControls";
import { TranscriptionPanel } from "@/components/conversation/TranscriptionPanel";
import { EmotionalStateIndicator } from "@/components/conversation/EmotionalStateIndicator";
import { ContextPanel } from "@/components/conversation/ContextPanel";
import { useConversationSocket } from "@/hooks/useConversationSocket";

export default function ConversationPage() {
  const params = useParams();
  const conversationId = params.id as string;

  const {
    messages,
    emotionalState,
    isConnected,
    sendAudio,
    disconnect,
  } = useConversationSocket(conversationId);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold">Live Conversation</h1>
          <p className="text-sm text-gray-500">Session: {conversationId}</p>
        </div>
        <div className="flex items-center gap-3">
          <span
            className={`inline-block w-2 h-2 rounded-full ${
              isConnected ? "bg-green-500" : "bg-red-500"
            }`}
          />
          <span className="text-sm text-gray-600">
            {isConnected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </header>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-0">
        <div className="lg:col-span-3 flex flex-col">
          <div className="flex-1 overflow-y-auto p-6">
            <TranscriptionPanel messages={messages} />
          </div>
          <div className="border-t border-gray-200 p-4 bg-white">
            <VoiceControls
              onAudioData={sendAudio}
              onDisconnect={disconnect}
              isConnected={isConnected}
            />
          </div>
        </div>

        <div className="border-l border-gray-200 bg-white p-4 space-y-4">
          <EmotionalStateIndicator state={emotionalState} />
          <ContextPanel conversationId={conversationId} />
        </div>
      </div>
    </div>
  );
}
