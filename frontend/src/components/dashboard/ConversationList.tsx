"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiClient, Conversation } from "@/lib/api";

export function ConversationList() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .listConversations()
      .then(setConversations)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="text-sm text-gray-500">Loading conversations...</p>;
  }

  if (conversations.length === 0) {
    return (
      <p className="text-sm text-gray-500">
        No conversations yet. Start one above.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {conversations.map((conv) => (
        <Link
          key={conv.id}
          href={`/conversation/${conv.id}`}
          className="block p-3 border border-gray-200 rounded-md hover:bg-gray-50 transition-colors"
        >
          <div className="flex justify-between items-center">
            <div>
              <span className="text-sm font-medium">
                {conv.id.slice(0, 8)}...
              </span>
              <span className="ml-2 text-xs text-gray-500 capitalize">
                {conv.strategy}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <StatusBadge status={conv.status} />
              {conv.negotiation_result && (
                <ResultBadge result={conv.negotiation_result} />
              )}
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-1">
            {new Date(conv.started_at).toLocaleString()}
            {conv.duration_seconds && ` | ${conv.duration_seconds}s`}
          </p>
        </Link>
      ))}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    active: "bg-green-100 text-green-700",
    completed: "bg-blue-100 text-blue-700",
    abandoned: "bg-gray-100 text-gray-700",
    escalated: "bg-yellow-100 text-yellow-700",
  };

  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full ${colors[status] || "bg-gray-100 text-gray-700"}`}
    >
      {status}
    </span>
  );
}

function ResultBadge({ result }: { result: string }) {
  const colors: Record<string, string> = {
    accepted: "bg-green-100 text-green-700",
    rejected: "bg-red-100 text-red-700",
    pending: "bg-yellow-100 text-yellow-700",
  };

  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full ${colors[result] || "bg-gray-100 text-gray-700"}`}
    >
      {result}
    </span>
  );
}
