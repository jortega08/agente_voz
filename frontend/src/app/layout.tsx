import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agente Voz - AI Debt Collection Agent",
  description:
    "AI-powered voice agent for intelligent debt collection with empathetic communication",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen">{children}</body>
    </html>
  );
}
