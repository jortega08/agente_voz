"use client";

import { useState, useRef, useCallback } from "react";

interface Props {
  onAudioData: (data: Blob) => void;
  onDisconnect: () => void;
  isConnected: boolean;
}

export function VoiceControls({ onAudioData, onDisconnect, isConnected }: Props) {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          sampleRate: 16000,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm;codecs=opus",
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        onAudioData(blob);
        chunksRef.current = [];
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start(250); // collect data every 250ms
      setIsRecording(true);
    } catch (err) {
      console.error("Failed to start recording:", err);
    }
  }, [onAudioData]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  }, [isRecording]);

  return (
    <div className="flex items-center justify-center gap-4">
      <button
        onClick={isRecording ? stopRecording : startRecording}
        disabled={!isConnected}
        className={`px-6 py-3 rounded-full font-medium transition-colors ${
          isRecording
            ? "bg-red-500 hover:bg-red-600 text-white"
            : "bg-primary-600 hover:bg-primary-700 text-white"
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </button>

      <button
        onClick={onDisconnect}
        className="px-4 py-3 rounded-full border border-gray-300 text-gray-700 hover:bg-gray-100 transition-colors"
      >
        End Conversation
      </button>
    </div>
  );
}
