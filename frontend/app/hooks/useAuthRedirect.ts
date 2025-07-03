'use client';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

/**
 * Handles auth-based redirection:
 * - If not authenticated, redirects to /signin
 * - If authenticated, redirects to /chat or /onboarding
 */
export const useAuthRedirect = () => {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    // Wait for auth to be resolved
    if (status === 'loading') return;

    // No session, force to signin
    if (status === 'unauthenticated') {
      console.log('[AuthRedirect] No active session → redirecting to /signin');
      router.replace('/signin');
      return;
    }

    // Session exists, check onboarding state
    if (status === 'authenticated') {
      const onboarded = (session?.user as any)?.onboardingComplete;

      console.log(
        '[AuthRedirect] Authenticated session:',
        session?.user?.email,
        '| Onboarding complete?',
        onboarded
      );

      if (onboarded) {
        router.replace('/chat');
      } else {
        router.replace('/onboarding');
      }
    }
  }, [status, session, router]);
};
