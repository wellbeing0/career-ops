# Design

Read existing pipeline and added scan-history jobs separately from new search receipts; label freshness and processing status without claiming current liveness. Deduplicate by safe HTTPS URL.

Expose title include/exclude and location allow/block/always-allow/hard-block lists, retaining all other portals settings. Use independent configuration revision checks, shared workspace locking, automatic previous-version history, validation and restore. Never overwrite unsaved filters when search polling refreshes. Include portals content in new targeting revisions; accept legacy receipts with profile-only hashes. Show per-source filter breakdown and explicitly state wider web queries are not executed.

Repair only confirmed exact old source addresses using versioned owner-run activation, retaining source settings and candidate isolation. Verify official employer links and public API receipts, avoiding incorrect parent-company attribution.
