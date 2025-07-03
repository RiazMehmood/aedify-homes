'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signIn } from 'next-auth/react';
import { FaGoogle } from 'react-icons/fa';

const SignInPage = () => {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const res = await signIn('credentials', {
      redirect: false, // handle redirect manually
      email,
      password,
    });

    setLoading(false);

    if (res?.ok) {
      // Redirect handled by NextAuth callbacks (based on onboarding flag)
      router.push('/redirect');
    } else {
      alert('Invalid credentials');
    }
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="flex flex-col w-full max-w-lg p-8 bg-white rounded-3xl shadow-lg">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Sign in to your account</h1>
        <p className="text-gray-500 mb-6">Welcome back! Please enter your credentials.</p>

        <form className="space-y-5" onSubmit={handleSignIn}>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full p-3 mt-2 mb-2 bg-yellow-400 text-gray-900 font-bold rounded-lg hover:bg-yellow-500"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <button
          onClick={() => signIn('google', { callbackUrl: '/redirect' })}
          className="w-full flex items-center justify-center hover:bg-gray-300 gap-3 p-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 font-medium"
        >
          <FaGoogle className="text-red-500" />
          Continue with Google
        </button>

        <p className="mt-6 text-sm text-gray-600 text-center">
          Don’t have an account?{' '}
          <a href="/signup" className="font-medium text-yellow-600 hover:underline">
            Sign Up
          </a>
        </p>
      </div>
    </main>
  );
};

export default SignInPage;
