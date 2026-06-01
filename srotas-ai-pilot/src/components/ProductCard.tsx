'use client';

import Link from 'next/link';
import type { Product } from '@/types/product';

const CATEGORY_EMOJI: Record<string, string> = {
  Veidrodėlis: '🪞',
  Žibintas: '💡',
  Bamperis: '🚗',
  Turbo: '⚡',
  Inžektorius: '⛽',
  Sparnas: '🛡️',
  Durys: '🚪',
  'Greičių dėžė': '⚙️',
  'Galinis žibintas': '🔴',
  Radiatorius: '🌡️',
};

function conditionVariant(condition: string) {
  if (condition.includes('labai geras')) return 'badge-success';
  if (condition.includes('geras')) return 'badge-primary';
  return 'badge-warning';
}

export default function ProductCard({ product }: { product: Product }) {
  const emoji = CATEGORY_EMOJI[product.category] || '🔧';

  return (
    <Link href={`/products/${product.slug}`}>
      <article className="product-card">
        {/* Image placeholder with emoji */}
        <div className="product-card-image" aria-label={product.name}>
          {emoji}
        </div>

        <div className="product-card-body">
          <div className="product-card-category">{product.category}</div>
          <h3 className="product-card-name">{product.name}</h3>
          <p className="product-card-make">
            {product.make} {product.model} &middot; {product.yearFrom}–{product.yearTo}
          </p>

          <div className="product-card-footer">
            <span className="product-card-price">
              {product.price} {product.currency}
            </span>
            <span className={`badge ${conditionVariant(product.condition)}`}>
              {product.condition}
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}
