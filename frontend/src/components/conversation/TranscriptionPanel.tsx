"use client";

export interface Message {
  role: "agent" | "user" | "system";
  content: string;
  timestamp: string;
}

interface Props {
  messages: Message[];
}

export function TranscriptionPanel({ messages }: Props) {
  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        <p>Waiting for conversation to start...</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[70%] px-4 py-2 rounded-lg ${
              msg.role === "user"
                ? "bg-primary-600 text-white"
                : msg.role === "agent"
                  ? "bg-gray-200 text-gray-900"
                  : "bg-yellow-100 text-yellow-800 text-xs"
            }`}
          >
            <p className="text-sm">{msg.content}</p>
            <p
              className={`text-xs mt-1 ${
                msg.role === "user" ? "text-primary-200" : "text-gray-400"
              }`}
            >
              {new Date(msg.timestamp).toLocaleTimeString()}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
