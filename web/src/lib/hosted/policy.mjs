// The hosted mode permits only its bounded editor; upstream worker surfaces fail closed.
export function hostedAllowed(pathname, method) {
  if (pathname === '/api/hosted/documents') return method === 'GET';
  if (pathname === '/api/hosted' || pathname === '/api/hosted/search' || pathname === '/api/hosted/assistant') return ['GET','POST'].includes(method);
  return ['GET','HEAD'].includes(method) && (pathname === '/' || pathname.startsWith('/_next/static/'));
}
export function hostedConfig(env = process.env) {
  if (env.CAREER_OPS_HOSTED !== '1') return null;
  const candidate = env.CAREER_OPS_CANDIDATE;
  if (!['steve','brad'].includes(candidate) || env.NEXT_PUBLIC_HOSTED_BASE !== `/${candidate}/workspace` || !env.CAREER_OPS_ROOT?.startsWith('/') || !env.CAREER_OPS_CODE_ROOT?.startsWith('/')) throw new Error('Hosted candidate/root configuration is incomplete.');
  return { candidate, root: env.CAREER_OPS_ROOT, code: env.CAREER_OPS_CODE_ROOT };
}
