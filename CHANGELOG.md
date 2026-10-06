# Changelog

All notable changes to MaryDubai Multi-Agent System.

## [1.0.0] - 2026-10-05

### Added
- 7 specialized agents:
  - RAGTimeManager (with SQLite vector store)
  - LegalConsultant
  - LoopBreaker
  - TemporalEdge
  - FinancialInvestment
  - MathPhysics
  - WalletSecurity
- Unified CLI entry point (main.py)
- Strict Human-in-the-Loop (HITL) approval gates
- Shared infrastructure:
  - GeminiEmbedder (API-based)
  - LocalHashEmbedder (offline)
  - SQLiteVectorStore with cosine similarity
- Index Builder CLI (index_builder.py)
- Session decision logging for all agents

### Testing
- 74 unit/integration tests
- 100% pass rate
- Security tests for HITL bypass prevention
- Edge case coverage (empty input, unicode, large docs)

### Documentation
- README.md with full usage guide
- TEST_RESULTS.md
- Inline Arabic comments in all agents

### Known Limitations
- LocalHashEmbedder gives ~0.1 similarity scores
- GeminiEmbedder recommended for production
- No web UI (CLI only)
- Single-user, no authentication
