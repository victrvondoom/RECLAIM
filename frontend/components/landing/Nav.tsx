"use client";

import Link from "next/link";

export default function Nav() {
  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 20,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0.85rem 1.75rem",
        backgroundColor: "#fcfaf5",
        borderBottom: "2px solid #231f1d",
        boxShadow: "0 2px 0px rgba(35, 31, 29, 0.05)",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: "0.15rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.95rem", letterSpacing: "0.08em", color: "var(--bone)", fontWeight: 800 }}>
            RESOLVE
          </span>
          <span
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "0.65rem",
              padding: "0.15rem 0.5rem",
              borderRadius: "4px",
              background: "#fef3c7",
              color: "#92400e",
              fontWeight: 700,
              border: "1.5px solid #231f1d",
              boxShadow: "1px 1px 0px #231f1d",
              letterSpacing: "0.04em",
            }}
          >
            Wispr Flow
          </span>
        </div>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.68rem", color: "#b45309", letterSpacing: "0.03em", fontWeight: 700 }}>
          Whisper &amp; solve using Wispr Flow
        </span>
      </div>
      <nav style={{ display: "flex", alignItems: "center", gap: "1.75rem" }}>
        <a href="#how-it-works" className="aperture-nav-link" style={{ fontWeight: 600 }}>How it works</a>
        <a href="#live-demo" className="aperture-nav-link" style={{ fontWeight: 600 }}>Live demo</a>
        <a href="#metrics" className="aperture-nav-link" style={{ fontWeight: 600 }}>Metrics</a>
        <Link
          href="/dashboard"
          className="aperture-nav-link"
          style={{ fontWeight: 600, opacity: 0.9 }}
        >
          Dashboard
        </Link>
        <Link
          href="/dashboard"
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "0.78rem",
            padding: "0.5rem 1rem",
            border: "2px solid #231f1d",
            borderRadius: "6px",
            color: "#1a1715",
            background: "#ffffff",
            fontWeight: 800,
            boxShadow: "2px 2px 0px #231f1d",
            textDecoration: "none",
            transition: "all 0.1s ease",
          }}
        >
          Enter Platform &rarr;
        </Link>
      </nav>
    </header>
  );
}
