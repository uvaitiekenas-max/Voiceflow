import type { Metadata } from 'next';
import './globals.css';
import { VoiceProvider } from '@/components/VoiceProvider';

export const metadata: Metadata = {
  title: 'Srotas – Naudotų Auto Dalių Platforma',
  description:
    'Profesionali naudotų automobilių dalių platforma su AI pardavimo konsultantu lietuvių kalba.',
  keywords: ['auto dalys', 'naudotos dalys', 'automobilių dalys', 'srotas'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="lt">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body>
        <VoiceProvider>
          {children}
        </VoiceProvider>
      </body>
    </html>
  );
}
