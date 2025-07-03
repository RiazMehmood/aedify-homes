'use client';

import { useAuthRedirect } from '../hooks/useAuthRedirect';

const RedirectPage = () => {
  useAuthRedirect();
  return <div className="p-6 text-center">Redirecting...</div>;
};

export default RedirectPage;
