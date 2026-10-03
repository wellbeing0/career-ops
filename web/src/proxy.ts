import { hostedAllowed } from "@/lib/hosted/policy.mjs";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import {
  checkRequest,
  parseAllowedHosts,
  parseAllowedOrigins,
} from "@/lib/origin-guard.mjs";

// Single choke point over the API surface. Every /api request is gated on the
// same-origin + loopback guard before it can reach a route handler (which may
// spawn a child process or write the user's files). See origin-guard.mjs for
// the two-layer rationale (F1 drive-by CSRF, F2 LAN reachability).
//
// Opt in to extra hosts (e.g. a trusted LAN box) with a comma/space separated
// CAREER_OPS_WEB_ALLOWED_HOSTS; unset means loopback only.
//
// Opt in to extra *origins* the same way with CAREER_OPS_ALLOWED_ORIGINS;
// unset means none, which is the default and leaves the guard as strict as it
// was. It is what a local companion client needs: a browser extension calls
// from a chrome-extension:// origin, which Fetch Metadata always reports as
// "cross-site", so every one of its requests is refused otherwise.
export function proxy(req: NextRequest) {
  const hosted = process.env.CAREER_OPS_HOSTED === "1";
  const pathname = req.nextUrl.pathname;
  if (hosted) {
    if (!hostedAllowed(pathname, req.method)) return NextResponse.json({ error: "Capability disabled in hosted editing mode" }, { status: 403 });
    // Loopback services accept only requests carrying the gateway's private shared key.
    if (!process.env.CAREER_OPS_GATEWAY_TOKEN || req.headers.get("x-career-gateway") !== process.env.CAREER_OPS_GATEWAY_TOKEN) return NextResponse.json({ error: "Authentication gateway required" }, { status: 401 });
  }
  if (!hosted && !pathname.startsWith("/api/")) return NextResponse.next();
  const decision = checkRequest({
    secFetchSite: req.headers.get("sec-fetch-site"),
    origin: req.headers.get("origin"),
    host: req.headers.get("host"),
    allowedHosts: parseAllowedHosts(process.env.CAREER_OPS_WEB_ALLOWED_HOSTS),
    allowedOrigins: parseAllowedOrigins(process.env.CAREER_OPS_ALLOWED_ORIGINS),
  });
  if (!decision.ok) {
    return NextResponse.json({ error: decision.reason }, { status: decision.status });
  }
  if (!hosted) return NextResponse.next();
  const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
  const csp = `default-src 'self'; script-src 'self' 'nonce-${nonce}' 'strict-dynamic'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self'`;
  const headers = new Headers(req.headers); headers.set('x-nonce', nonce); headers.set('Content-Security-Policy', csp);
  const response = NextResponse.next({ request: { headers } });
  response.headers.set('Content-Security-Policy',csp); response.headers.set('Cache-Control','private, no-store');
  return response;
}

export const config = { matcher: "/:path*" };
