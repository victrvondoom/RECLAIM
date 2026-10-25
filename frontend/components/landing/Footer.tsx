import Link from "next/link";
import { DOMAINS } from "@/lib/aperture/tokens";

export default function Footer() {
  return (
    <footer
      style={{
        position: "relative",
        zIndex: 1,
        borderTop: "2px solid #231f1d",
        backgroundColor: "#fcfaf5",
        padding: "3.5rem 1.5rem 2.5rem",
        fontFamily: "var(--font-mono)",
        fontSize: "0.75rem",
        color: "var(--bone)",
      }}
    >
      <div style={{ maxWidth: "1100px", margin: "0 auto", display: "flex", flexWrap: "wrap", gap: "2.5rem", justifyContent: "space-between" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.25rem" }}>
            <span style={{ letterSpacing: "0.08em", fontWeight: 800, fontSize: "0.95rem" }}>RESOLVE</span>
            <span style={{ fontSize: "0.65rem", padding: "0.15rem 0.45rem", borderRadius: "3px", background: "#fef3c7", color: "#92400e", fontWeight: 700, border: "1px solid #231f1d" }}>Wispr Flow</span>
          </div>
          <div style={{ color: "#b45309", fontSize: "0.75rem", fontWeight: 700, marginBottom: "0.4rem" }}>
            Whisper and solve using Wispr Flow
          </div>
          <div style={{ color: "#575147", maxWidth: "300px", lineHeight: 1.6, fontWeight: 500 }}>
            Voice-first multi-agent consumer justice and automated dispute resolution across {DOMAINS.length} regulated domains.
          </div>
        </div>
        <div style={{ display: "flex", gap: "3rem", flexWrap: "wrap" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            <span style={{ opacity: 0.5, marginBottom: "0.25rem" }}>PRODUCT</span>
            <a href="#how-it-works" className="aperture-nav-link">How it works</a>
            <a href="#live-demo" className="aperture-nav-link">Live demo</a>
            <a href="#metrics" className="aperture-nav-link">Metrics</a>
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            <span style={{ opacity: 0.5, marginBottom: "0.25rem" }}>PLATFORM</span>
            <Link href="/dashboard" className="aperture-nav-link">Dashboard</Link>
            <Link href="/dashboard/new" className="aperture-nav-link">New Analysis</Link>
          </div>
        </div>
      </div>
      <div style={{ maxWidth: "1100px", margin: "2rem auto 0", opacity: 0.45 }}>
        &copy; {new Date().getFullYear()} RESOLVE.
      </div>
    </footer>
  );
}
