const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Debtor {
  id: string;
  external_id: string | null;
  name: string;
  original_amount: number;
  negotiable_amount: number;
  days_past_due: number;
  risk_profile: string;
  emotional_profile: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface DebtorCreate {
  name: string;
  original_amount: number;
  negotiable_amount: number;
  days_past_due: number;
  risk_profile: string;
  emotional_profile?: string;
  notes?: string;
}

export interface Conversation {
  id: string;
  debtor_id: string;
  status: string;
  strategy: string;
  emotional_state_detected: string | null;
  negotiation_result: string | null;
  offered_amount: number | null;
  accepted_amount: number | null;
  duration_seconds: number | null;
  started_at: string;
  ended_at: string | null;
}

export interface ConversationMessage {
  id: string;
  conversation_id: string;
  role: string;
  content: string;
  emotional_tone: string | null;
  confidence: number | null;
  timestamp: string;
}

export interface ConversationDetail extends Conversation {
  messages: ConversationMessage[];
}

export interface ConversationCreate {
  debtor_id: string;
  strategy: string;
}

export interface MetricsSummary {
  total_conversations: number;
  completed_conversations: number;
  avg_duration_seconds: number | null;
  acceptance_rate: number | null;
  emotional_distribution: Record<string, number>;
  strategy_effectiveness: Record<string, number>;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API error ${res.status}: ${error}`);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const apiClient = {
  createDebtor: (data: DebtorCreate) =>
    request<Debtor>("/debtors/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listDebtors: () => request<Debtor[]>("/debtors/"),

  getDebtor: (id: string) => request<Debtor>(`/debtors/${id}`),

  createConversation: (data: ConversationCreate) =>
    request<Conversation>("/conversations/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  listConversations: () => request<Conversation[]>("/conversations/"),

  getConversation: (id: string) =>
    request<ConversationDetail>(`/conversations/${id}`),

  getMetrics: () => request<MetricsSummary>("/metrics/summary"),
};
