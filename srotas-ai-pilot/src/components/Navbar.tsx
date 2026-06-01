'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="navbar">
      <div className="container navbar-inner">
        <Link href="/" className="navbar-logo">
          <div className="navbar-logo-icon">🔧</div>
          <span>Srotas</span>
        </Link>
        <div className="navbar-links">
          <Link href="/" className={`navbar-link ${pathname === '/' ? 'active' : ''}`}>
            Katalogas
          </Link>
          <Link
            href="/admin"
            className={`navbar-link ${pathname?.startsWith('/admin') ? 'active' : ''}`}
          >
            Admin
          </Link>
        </div>
      </div>
    </nav>
  );
}
