import { DebtorForm } from "@/components/dashboard/DebtorForm";
import { MetricsPanel } from "@/components/dashboard/MetricsPanel";
import { ConversationList } from "@/components/dashboard/ConversationList";

export default function DashboardPage() {
  return (
    <div className="min-h-screen">
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-sm text-gray-500">
          Manage debtors, start conversations, and track metrics
        </p>
      </header>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <section className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-medium mb-4">New Conversation</h2>
            <DebtorForm />
          </section>

          <section className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-medium mb-4">Recent Conversations</h2>
            <ConversationList />
          </section>
        </div>

        <div>
          <MetricsPanel />
        </div>
      </div>
    </div>
  );
}
