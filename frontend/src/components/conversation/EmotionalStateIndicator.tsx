"use client";

interface Props {
  state: string;
}

const STATE_CONFIG: Record<string, { color: string; description: string }> = {
  cooperative: {
    color: "bg-green-500",
    description: "The person is receptive and willing to discuss options.",
  },
  defensive: {
    color: "bg-yellow-500",
    description: "The person is guarded and skeptical. Build trust gradually.",
  },
  aggressive: {
    color: "bg-red-500",
    description: "The person is hostile. Stay calm and professional.",
  },
  evasive: {
    color: "bg-orange-500",
    description: "The person avoids engagement. Be patient and informative.",
  },
  anxious: {
    color: "bg-purple-500",
    description: "The person is stressed. Prioritize reassurance.",
  },
  unknown: {
    color: "bg-gray-400",
    description: "Analyzing emotional state...",
  },
};

export function EmotionalStateIndicator({ state }: Props) {
  const config = STATE_CONFIG[state] || STATE_CONFIG.unknown;

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-gray-700">Emotional State</h3>
      <div className="flex items-center gap-2">
        <span className={`w-3 h-3 rounded-full ${config.color}`} />
        <span className="text-sm font-medium capitalize">{state}</span>
      </div>
      <p className="text-xs text-gray-500">{config.description}</p>
    </div>
  );
}
