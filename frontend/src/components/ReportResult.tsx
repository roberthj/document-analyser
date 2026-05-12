import type { ReportAnalysis } from "../types";

function fmt(value: number | null, currency: string | null) {
  if (value == null) return "—";
  return `${value.toLocaleString("sv-SE")} ${currency ?? "SEK"}`;
}

function val(s: string | null | undefined) {
  return s ?? "—";
}

interface Props {
  data: ReportAnalysis;
}

export function ReportResult({ data }: Props) {
  const { association, loans, summary, notes } = data;

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", display: "flex", flexDirection: "column", gap: 32 }}>
      <section>
        <h2>Summary</h2>
        <p style={{ color: "#ccc", lineHeight: 1.6 }}>{summary}</p>
      </section>

      <section>
        <h2>Association</h2>
        <table style={tableStyle}>
          <tbody>
            <tr><td style={labelStyle}>Name</td><td>{val(association.name)}</td></tr>
            <tr><td style={labelStyle}>Org. number</td><td>{val(association.organization_number)}</td></tr>
            <tr><td style={labelStyle}>Address</td><td>{val(association.address)}</td></tr>
            <tr><td style={labelStyle}>Apartments</td><td>{association.num_apartments ?? "—"}</td></tr>
          </tbody>
        </table>

        {association.board_members.length > 0 && (
          <>
            <h3>Board</h3>
            <table style={tableStyle}>
              <thead>
                <tr>
                  <th style={thStyle}>Name</th>
                  <th style={thStyle}>Role</th>
                </tr>
              </thead>
              <tbody>
                {association.board_members.map((m, i) => (
                  <tr key={i}>
                    <td style={tdStyle}>{m.name}</td>
                    <td style={tdStyle}>{m.role}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </section>

      <section>
        <h2>Loans</h2>
        {loans.length === 0 ? (
          <p style={{ color: "#aaa" }}>No loans found.</p>
        ) : (
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={thStyle}>Lender</th>
                <th style={thStyle}>Amount</th>
                <th style={thStyle}>Interest rate</th>
                <th style={thStyle}>Interest reset date</th>
                <th style={thStyle}>Maturity date</th>
              </tr>
            </thead>
            <tbody>
              {loans.map((l, i) => (
                <tr key={i}>
                  <td style={tdStyle}>{l.lender}</td>
                  <td style={tdStyle}>{fmt(l.amount, l.currency)}</td>
                  <td style={tdStyle}>{val(l.interest_rate)}</td>
                  <td style={tdStyle}>{val(l.interest_reset_date)}</td>
                  <td style={tdStyle}>{val(l.maturity_date)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {notes.length > 0 && (
        <section>
          <h2 style={{ color: "#f0a500" }}>Flagged irregularities</h2>
          <ul style={{ color: "#f0a500", lineHeight: 1.8, paddingLeft: 20 }}>
            {notes.map((note, i) => <li key={i}>{note}</li>)}
          </ul>
        </section>
      )}
    </div>
  );
}

const tableStyle: React.CSSProperties = {
  width: "100%",
  borderCollapse: "collapse",
  fontSize: 14,
};

const thStyle: React.CSSProperties = {
  textAlign: "left",
  padding: "8px 12px",
  borderBottom: "1px solid #444",
  color: "#aaa",
  fontWeight: 600,
};

const tdStyle: React.CSSProperties = {
  padding: "8px 12px",
  borderBottom: "1px solid #2a2a2a",
};

const labelStyle: React.CSSProperties = {
  ...tdStyle,
  color: "#aaa",
  width: 160,
};
