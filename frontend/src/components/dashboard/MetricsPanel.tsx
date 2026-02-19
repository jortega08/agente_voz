"use client";

import { useEffect, useState } from "react";
import { apiClient, MetricsSummary } from "@/lib/api";

export function MetricsPanel() {
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .getMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-medium mb-4">Metrics</h2>
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-medium mb-4">Metrics</h2>
        <p className="text-sm text-gray-500">No data available yet.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 space-y-4">
      <h2 className="text-lg font-medium">Metrics</h2>

      <div className="grid grid-cols-2 gap-3">
        <MetricCard
          label="Total Conversations"
          value={metrics.total_conversations}
        />
        <MetricCard
          label="Completed"
          value={metrics.completed_conversations}
        />
        <MetricCard
          label="Avg Duration"
          value={
            metrics.avg_duration_seconds
              ? `${Math.round(metrics.avg_duration_seconds)}s`
              : "N/A"
          }
        />
        <MetricCard
          label="Acceptance Rate"
          value={
            metrics.acceptance_rate != null
              ? `${(metrics.acceptance_rate * 100).toFixed(1)}%`
              : "N/A"
          }
        />
      </div>

      {Object.keys(metrics.emotional_distribution).length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-2">
            Emotional Distribution
          </h3>
          <div className="space-y-1">
            {Object.entries(metrics.emotional_distribution).map(
              ([emotion, count]) => (
                <div
                  key={emotion}
                  className="flex justify-between text-sm text-gray-600"
                >
                  <span className="capitalize">{emotion}</span>
                  <span>{count}</span>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function MetricCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="bg-gray-50 rounded-md p-3">
      <p className="text-xs text-gray-500">{label}</p>
      <p className="text-xl font-semibold">{value}</p>
    </div>
  );
}
