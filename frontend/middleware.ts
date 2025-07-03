import { NextRequest, NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

// Publicly accessible paths that don't require authentication
const PUBLIC_PATHS = ['/signin', '/signup', '/redirect', '/api/auth', '/favicon.ico', '/_next'];

// This middleware runs for every request
export async function middleware(req: NextRequest) {
  const token = await getToken({ req, secret: process.env.NEXTAUTH_SECRET });
  const { pathname } = req.nextUrl;

  // Check if request path is public
  const isPublic = PUBLIC_PATHS.some((path) => pathname.startsWith(path));

  console.log('🧪 [Middleware] Path:', pathname);
  console.log('🧪 [Middleware] Token:', token ? '✅ Authenticated' : '❌ Not Authenticated');
  console.log('🧪 [Middleware] Is Public Path:', isPublic);

  // Redirect to /signin if user is not authenticated and the path is not public
  if (!token && !isPublic) {
    const url = req.nextUrl.clone();
    url.pathname = '/signin';
    console.log('🔁 Redirecting to /signin');
    return NextResponse.redirect(url);
  }

  // Allow request to continue
  return NextResponse.next();
}

// This controls which routes the middleware should apply to
export const config = {
  matcher: ['/', '/((?!_next|api|favicon.ico).*)'], // include `/` explicitly
};
