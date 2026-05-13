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

  const resetInsight = () => {
    setText("");
    setError(null);
  };

  const cancelInsight = () => {
    abortRef.current?.abort();
    setLoading(false);
  };

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

      if (!res.body) throw new Error("No stream body");

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
          if (!line.startsWith("data:")) continue;

          const jsonStr = line.replace("data:", "").trim();
          if (!jsonStr) continue;

          try {
            const event: InsightEvent = JSON.parse(jsonStr);

            if (event.type === "chunk") {
              setText((prev) => prev + event.content);
            }

            if (event.type === "error") {
              setError(event.message);
            }

            if (event.type === "end") {
              setLoading(false);
            }
          } catch {
            // ignore bad chunks
          }
        }
      }
    } catch (e: any) {
      setError(e.message);
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