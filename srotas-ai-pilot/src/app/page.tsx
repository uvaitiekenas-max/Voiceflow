import Navbar from '@/components/Navbar';
import ProductCard from '@/components/ProductCard';
import productsData from '@/data/products.json';
import type { Product } from '@/types/product';

const products = productsData as Product[];

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <div className="container">
          <div className="page-header">
            <div className="page-tag">🔧 Katalogas</div>
            <h1 className="page-title">
              Naudotų auto dalių <span>platforma</span>
            </h1>
            <p className="page-subtitle">
              Kokybiškas naudotas auto dalis su AI konsultanto pagalba. Raskite tinkamą detalę
              savo automobiliui.
            </p>
          </div>

          {/* Stats row */}
          <div className="flex gap-4 mb-6" style={{ flexWrap: 'wrap' }}>
            <div className="badge badge-success">✅ {products.length} dalių sandėlyje</div>
            <div className="badge badge-primary">🤖 AI konsultantas lietuvių kalba</div>
            <div className="badge badge-neutral">⚡ Greitas pristatymas Lietuvoje</div>
          </div>

          <div className="divider" />

          {/* Product grid */}
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </main>
    </>
  );
}
