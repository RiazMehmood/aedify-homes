import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import type { NextAuthOptions } from "next-auth";
import jwt from "jsonwebtoken";

export const authOptions: NextAuthOptions = {
  session: {
    strategy: "jwt",
  },

  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),

    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        try {
          const res = await fetch("http://localhost:8000/api/auth/signin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials?.email,
              password: credentials?.password,
            }),
          });

          if (!res.ok) return null;
          const data = await res.json();

          const check = await fetch("http://localhost:8000/api/auth/check-user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: data.email }),
          });

          if (!check.ok) return null;
          const checkData = await check.json();

          return {
            id: data.email,
            email: data.email,
            name: data.name ?? data.email,
            onboardingComplete: checkData.onboarding_complete ?? false,
            role: checkData.role, // Default to 'customer' if role is not set
          };
        } catch (err) {
          console.error("Credentials authorize error:", err);
          return null;
        }
      },
    }),
  ],

  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === "google") {
        try {
          await fetch("http://localhost:8000/api/auth/google", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: user.email, name: user.name }),
          });

          const check = await fetch("http://localhost:8000/api/auth/check-user", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: user.email }),
          });

          const data = await check.json();
          (user as any).onboardingComplete = data.onboarding_complete ?? false;
          (user as any).role = data.role; // Default to 'customer' if role is not set
        } catch (err) {
          console.error("Google sign-in error:", err);
          return false;
        }
      }

      return true;
    },

    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id ?? user.email ?? "";
        token.email = user.email ?? token.email ?? "";
        token.onboardingComplete = (user as any).onboardingComplete ?? false;
        token.role = (user as any).role; // Default to 'customer' if role is not set

        if (account?.provider === "google") {
          token.accessToken = account.id_token || account.access_token || "";
        } else {
          // ✅ Sign a JWT token manually for credentials login
          token.accessToken = jwt.sign(
            { email: token.email },
            process.env.NEXTAUTH_SECRET!,
            {
              algorithm: "HS256",
              expiresIn: "7d",
            }
          );
        }
         if (account?.provider === "credentials" || !account) {
        token.accessToken = jwt.sign(
          { email: user.email },
          process.env.NEXTAUTH_SECRET!,
          {
            algorithm: "HS256",
            expiresIn: "7d",
          }
        );
      } else {
        token.accessToken = account.id_token || account.access_token || "";
      }
        
        console.log("✅ JWT Callback Final Token:", token);
      }

      

      return token;
    },

    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.email = token.email;
        session.user.accessToken = token.accessToken ?? "";
        (session.user as any).onboardingComplete = token.onboardingComplete ?? false;
        (session.user as any).role = token.role; // Default to 'customer' if role is not set

        console.log("🔐 Session from useSession():", session);
        console.log("🔐 Session.accessToken:", session?.user?.accessToken);
        console.log("🔐 Session.role:", session?.user?.role);
      }

      return session;
    },

    redirect: async ({ baseUrl }) => baseUrl,
  },

  pages: {
    signIn: "/signin",
    newUser: "/redirect",
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };