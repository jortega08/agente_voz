import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <h1 className="text-4xl font-bold mb-4">Agente Voz</h1>
        <p className="text-lg text-gray-600 mb-8">
          AI-powered voice agent for intelligent debt collection.
          Empathetic, legally compliant, and adaptive.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/dashboard"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Open Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}
