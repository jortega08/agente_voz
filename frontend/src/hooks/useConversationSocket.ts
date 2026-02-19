"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { Message } from "@/components/conversation/TranscriptionPanel";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export function useConversationSocket(conversationId: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [emotionalState, setEmotionalState] = useState("unknown");
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(
      `${WS_URL}/api/v1/ws/conversation/${conversationId}`
    );
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          content: "Connected to conversation.",
          timestamp: new Date().toISOString(),
        },
      ]);
    };

    ws.onmessage = (event) => {
      if (typeof event.data === "string") {
        const data = JSON.parse(event.data);

        if (data.type === "transcription") {
          setMessages((prev) => [
            ...prev,
            {
              role: data.role,
              content: data.content,
              timestamp: new Date().toISOString(),
            },
          ]);
        }

        if (data.type === "emotion") {
          setEmotionalState(data.emotion);
        }
      }
      // Binary data = audio response from agent (play it)
      if (event.data instanceof Blob) {
        const audioUrl = URL.createObjectURL(event.data);
        const audio = new Audio(audioUrl);
        audio.play().catch(console.error);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    ws.onerror = () => {
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [conversationId]);

  const sendAudio = useCallback((blob: Blob) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      blob.arrayBuffer().then((buffer) => {
        ws.send(buffer);
      });
    }
  }, []);

  const disconnect = useCallback(() => {
    const ws = wsRef.current;
    if (ws) {
      ws.close();
    }
  }, []);

  return {
    messages,
    emotionalState,
    isConnected,
    sendAudio,
    disconnect,
  };
}
