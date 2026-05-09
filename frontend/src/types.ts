export interface Patient {
  id: number;
  name: string;
  age: number;
  condition: string;
  trend: "Improving" | "Stable" | "Deteriorating";
  current_score: number | null;
}

export interface Outcome {
  id: number;
  patient_id: number;
  score: number;
  timestamp: string;
}

export interface TrendData {
  trend: string;
  history: { score: number; timestamp: string }[];
  current_score: number;
}
