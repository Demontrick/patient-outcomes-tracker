import { useState, useRef } from "react";

type InsightEvent =
  | { type: "start" }
  | { type: "chunk"; content: string }
  | { type: "end" }
  | { type: "error"; message: string };

export function usePatientInsight() {
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [activePatientId, setActivePatientId] = useState<number | null>(null);

  const abortRef = useRef<AbortController | null>(null);

  // -------------------------
  // RESET
  // -------------------------
  const resetInsight = () => {
    setText("");
    setError(null);
  };

  // -------------------------
  // CANCEL STREAM
  // -------------------------
  const cancelInsight = () => {
    abortRef.current?.abort();
    setLoading(false);
  };

  // -------------------------
  // CLEAN + TRANSFORM EVENTS
  // -------------------------
  const processEvent = (raw: string) => {
    if (!raw) return;

    try {
      const event: InsightEvent = JSON.parse(raw);

      switch (event.type) {
        case "chunk":
          setText((prev) => prev + event.content);
          break;

        case "error":
          setError(event.message);
          break;

        case "end":
          setLoading(false);
          break;

        default:
          break;
      }
    } catch {
      // -------------------------
      // RAW TEXT FALLBACK
      // -------------------------
      const cleaned = raw
        .replace(/^data:/gm, "")
        .replace(/\{"type":"start"\}/g, "")
        .replace(/\{"type":"end"\}/g, "")
        .trim();

      if (cleaned) {
        setText((prev) => prev + cleaned);
      }
    }
  };

  // -------------------------
  // MAIN STREAM HANDLER
  // -------------------------
  const getInsight = async (patientId: number) => {
    setLoading(true);
    setText("");
    setError(null);
    setActivePatientId(patientId);

    abortRef.current?.abort();
    abortRef.current = new AbortController();

    try {
      const res = await fetch(
        `http://localhost:8000/patients/${patientId}/insight`,
        {
          method: "POST",
          signal: abortRef.current.signal,
        }
      );

      if (!res.ok) {
        throw new Error(`Request failed: ${res.status}`);
      }

      if (!res.body) {
        throw new Error("No response body");
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");

        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;

          // Remove SSE prefix
          const cleanedLine = line.replace(/^data:\s*/, "").trim();

          processEvent(cleanedLine);
        }
      }

      // Process remaining buffer
      if (buffer.trim()) {
        const cleanedBuffer = buffer.replace(/^data:\s*/, "").trim();

        processEvent(cleanedBuffer);
      }
    } catch (e: any) {
      if (e.name !== "AbortError") {
        setError(e.message || "Failed to generate insight");
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    getInsight,
    cancelInsight,
    resetInsight,
    loading,
    text,
    error,
    activePatientId,
  };
}