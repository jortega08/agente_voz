"use client";

import { useEffect, useState } from "react";
import { apiClient, ConversationDetail } from "@/lib/api";

interface Props {
  conversationId: string;
}

export function ContextPanel({ conversationId }: Props) {
  const [detail, setDetail] = useState<ConversationDetail | null>(null);

  useEffect(() => {
    apiClient
      .getConversation(conversationId)
      .then(setDetail)
      .catch(console.error);
  }, [conversationId]);

  if (!detail) {
    return (
      <div className="space-y-2">
        <h3 className="text-sm font-medium text-gray-700">Context</h3>
        <p className="text-xs text-gray-500">Loading...</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h3 className="text-sm font-medium text-gray-700">Conversation Context</h3>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-500">Status</span>
          <span className="capitalize font-medium">{detail.status}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-500">Strategy</span>
          <span className="capitalize font-medium">{detail.strategy}</span>
        </div>
        {detail.offered_amount != null && (
          <div className="flex justify-between">
            <span className="text-gray-500">Offered</span>
            <span className="font-medium">${detail.offered_amount}</span>
          </div>
        )}
        {detail.negotiation_result && (
          <div className="flex justify-between">
            <span className="text-gray-500">Result</span>
            <span className="capitalize font-medium">
              {detail.negotiation_result}
            </span>
          </div>
        )}
        {detail.duration_seconds != null && (
          <div className="flex justify-between">
            <span className="text-gray-500">Duration</span>
            <span className="font-medium">{detail.duration_seconds}s</span>
          </div>
        )}
      </div>
    </div>
  );
}
