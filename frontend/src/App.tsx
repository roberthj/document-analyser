import { useState } from "react";
import { FileUpload } from "./components/FileUpload";
import { ReportResult } from "./components/ReportResult";
import type { ReportAnalysis } from "./types";

export default function App() {
  const [result, setResult] = useState<ReportAnalysis | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div style={{ minHeight: "100vh", background: "#0f0f0f", color: "#eee", fontFamily: "system-ui, sans-serif", padding: "40px 24px" }}>
      <div style={{ maxWidth: 800, margin: "0 auto" }}>
        <h1 style={{ textAlign: "center", marginBottom: 8 }}>Document Analyser</h1>
        <p style={{ textAlign: "center", color: "#888", marginBottom: 40 }}>
          Upload a PDF document to extract key information.
        </p>

        <FileUpload
          onResult={(data) => { setResult(data as ReportAnalysis); }}
          onError={setError}
          loading={loading}
          setLoading={setLoading}
        />

        {loading && (
          <p style={{ textAlign: "center", marginTop: 32, color: "#aaa" }}>
            Analysing report — this may take a few seconds…
          </p>
        )}

        {error && (
          <p style={{ textAlign: "center", marginTop: 24, color: "#f66" }}>{error}</p>
        )}

        {result && !loading && (
          <div style={{ marginTop: 48 }}>
            <ReportResult data={result} />
          </div>
        )}
      </div>
    </div>
  );
}
