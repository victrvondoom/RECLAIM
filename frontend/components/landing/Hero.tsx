"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { useSystemHealth } from "./useSystemHealth";
import CountUp from "./CountUp";

export default function Hero() {
  const { health, loading } = useSystemHealth();

  return (
    <section
      style={{
        position: "relative",
        zIndex: 1,
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        padding: "0 1.5rem",
      }}
    >
      <div style={{ maxWidth: "760px", margin: "0 auto", textAlign: "center", position: "relative", zIndex: 2 }}>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 0.9, y: 0 }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          style={{ fontFamily: "var(--font-mono)", fontSize: "0.8rem", letterSpacing: "0.14em", color: "#b45309", marginBottom: "1.25rem", fontWeight: 800 }}
        >
          AGENTIC AI RESOLVE &middot; WISPR &amp; SOLVE
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.08, ease: [0.16, 1, 0.3, 1] }}
          style={{
            fontFamily: "var(--font-display)",
            fontSize: "clamp(2.6rem, 6vw, 4.4rem)",
            lineHeight: 1.08,
            fontWeight: 400,
            color: "var(--bone)",
            marginBottom: "1.25rem",
          }}
        >
          Whisper and solve using Wispr Flow.
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 0.85, y: 0 }}
          transition={{ duration: 0.5, delay: 0.16, ease: [0.16, 1, 0.3, 1] }}
          style={{ fontSize: "1.05rem", lineHeight: 1.65, color: "var(--bone)", marginBottom: "2.25rem" }}
        >
          Speak or whisper your dispute in any tone or language. Wispr Flow automatically removes fillers, extracts facts, and structures legal telemetry—routing directly to autonomous multi-agent councils across 8 regulated domains.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.24, ease: [0.16, 1, 0.3, 1] }}
          style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}
        >
          <Link
            href="/dashboard/new"
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "0.85rem",
              padding: "0.85rem 1.6rem",
              borderRadius: "6px",
              background: "#f59e0b",
              color: "#1a1715",
              fontWeight: 800,
              border: "2px solid #231f1d",
              boxShadow: "3px 3px 0px #231f1d",
              textDecoration: "none",
              transition: "transform 0.08s ease, box-shadow 0.08s ease",
            }}
          >
            Whisper &amp; Solve Now &rarr;
          </Link>
          <a
            href="#live-demo"
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "0.85rem",
              padding: "0.85rem 1.6rem",
              borderRadius: "6px",
              border: "2px solid #231f1d",
              color: "#1a1715",
              background: "#ffffff",
              fontWeight: 700,
              boxShadow: "3px 3px 0px #231f1d",
              textDecoration: "none",
              transition: "transform 0.08s ease, box-shadow 0.08s ease",
            }}
          >
            Live Interactive Studio
          </a>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.32, ease: [0.16, 1, 0.3, 1] }}
          style={{
            marginTop: "2rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexWrap: "wrap",
            gap: "0.5rem",
          }}
        >
          <span style={{ fontFamily: "var(--font-mono)", fontSize: "0.72rem", color: "var(--bone)", opacity: 0.7, letterSpacing: "0.06em", fontWeight: 700 }}>
            QUICK SCENARIOS:
          </span>
          {[
            { label: "✈️ Flight Cancelled", q: "My flight was cancelled 2 hours prior to departure and the airline refused a refund." },
            { label: "💳 Double UPI ₹5k", q: "My bank charged me twice for the same UPI transaction of Rs 5,000 and refuses to reverse it." },
            { label: "🏥 Cataract Denied", q: "My health insurance claim of Rs 1,45,000 was denied for a pre-existing condition exclusion." },
            { label: "📱 Airtel Postpaid", q: "My telecom provider is billing me for a postpaid plan I cancelled two months ago." },
            { label: "🏢 RERA Possession", q: "My builder delayed possession of my flat by 18 months under RERA and refuses delay interest." },
          ].map((item) => (
            <Link
              key={item.label}
              href={`/dashboard/new?q=${encodeURIComponent(item.q)}`}
              style={{
                fontFamily: "var(--font-mono)",
                fontSize: "0.72rem",
                padding: "0.35rem 0.75rem",
                borderRadius: "5px",
                border: "1.5px solid #231f1d",
                background: "#ffffff",
                color: "#1a1715",
                textDecoration: "none",
                fontWeight: 700,
                boxShadow: "2px 2px 0px #231f1d",
                transition: "all 0.12s ease",
              }}
            >
              {item.label}
            </Link>
          ))}
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.5 }}
        style={{
          position: "absolute",
          bottom: "2rem",
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: "var(--font-mono)",
          fontSize: "0.78rem",
          color: "var(--bone)",
          opacity: 0.65,
        }}
      >
        {loading ? (
          "connecting to resolve..."
        ) : health ? (
          <>
            <CountUp value={health.vector_store.total_points ?? null} /> knowledge chunks indexed ·{" "}
            {health.vector_store.collections ?? 0} domain collections · {health.graph_store.events ?? 0} case events tracked
          </>
        ) : (
          "backend unreachable -- start the API to see live status"
        )}
      </motion.div>
    </section>
  );
}
