// types/next-auth.d.ts

import NextAuth from "next-auth";
import { JWT as DefaultJWT } from "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name?: string | null;
      email?: string | null;
      image?: string | null;
      onboardingComplete?: boolean;
      accessToken?: string;
      role: string;
    };
  }

  interface User {
    id: string;
    email?: string | null;
    name?: string | null;
    onboardingComplete?: boolean;
  }
}

declare module "next-auth/jwt" {
  interface JWT extends DefaultJWT {
    id?: string;
    email?: string;
    accessToken?: string;
    onboardingComplete?: boolean;
  }
}
