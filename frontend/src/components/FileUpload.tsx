import { useRef, useState } from "react";

interface Props {
  onResult: (data: unknown) => void;
  onError: (msg: string) => void;
  loading: boolean;
  setLoading: (v: boolean) => void;
}

export function FileUpload({ onResult, onError, loading, setLoading }: Props) {
  const [fileName, setFileName] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  function handleFile(f: File) {
    setFileName(f.name);
    setFile(f);
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f?.type === "application/pdf") handleFile(f);
  }

  async function handleSubmit() {
    if (!file) return;
    setLoading(true);
    onError("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch("http://localhost:8000/annual-report/analyse", {
        method: "POST",
        body: form,
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail ?? "Request failed");
      }
      onResult(await res.json());
    } catch (e) {
      onError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 16 }}>
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => inputRef.current?.click()}
        style={{
          border: "2px dashed #555",
          borderRadius: 8,
          padding: "40px 60px",
          cursor: "pointer",
          textAlign: "center",
          background: "#1a1a1a",
          width: 320,
        }}
      >
        <p style={{ margin: 0, color: "#aaa" }}>
          {fileName ?? "Drop a PDF here or click to select"}
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          style={{ display: "none" }}
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
      </div>
      <button
        onClick={handleSubmit}
        disabled={!file || loading}
        style={{
          padding: "10px 32px",
          fontSize: 15,
          borderRadius: 6,
          border: "none",
          background: file && !loading ? "#646cff" : "#333",
          color: "#fff",
          cursor: file && !loading ? "pointer" : "not-allowed",
        }}
      >
        {loading ? "Analysing…" : "Analyse"}
      </button>
    </div>
  );
}
