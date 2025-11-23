import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Providers } from "./providers";

const gabarito = localFont({
  src: "../public/fonts/Gabarito-variable.ttf",
});

export const metadata: Metadata = {
  title: "Restaurant Success Predictor",
  description: "SEC Project",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${gabarito.className} antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
