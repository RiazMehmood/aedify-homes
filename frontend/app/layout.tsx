import type { Metadata } from "next";
import SessionWrapper from './components/SessionWrapper';
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Aedify Homes",
  description: `It comes from the Latin aedis ("dwelling, building") 
  and the English word "edify" (to instruct or improve). The name suggests an intelligent agent
   that not only finds but also educates and improves the home-buying process.`,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <SessionWrapper>
          {children}
        </SessionWrapper>

      </body>
    </html>
  );
}
