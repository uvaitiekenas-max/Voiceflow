'use client';

import { useState, useEffect } from 'react';
import Navbar from '@/components/Navbar';
import AICallModal from '@/components/AICallModal';
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

export default function ProductDetailClient({ product }: { product: Product }) {
  const [showModal, setShowModal] = useState(false);
  const [twilioNumber, setTwilioNumber] = useState('');
  const emoji = CATEGORY_EMOJI[product.category] || '🔧';

  useEffect(() => {
    fetch('/api/config')
      .then((res) => res.json())
      .then((data) => {
        if (data.voice?.twilioPhoneNumber) {
          setTwilioNumber(data.voice.twilioPhoneNumber);
        }
      });
  }, []);

  return (
    <>
      <Navbar />
      <main>
        <div className="container">
          {/* Breadcrumb */}
          <div
            className="flex items-center gap-2 text-small text-muted"
            style={{ padding: '24px 0 0' }}
          >
            <a href="/" style={{ color: 'var(--color-primary)' }}>
              Katalogas
            </a>
            <span>›</span>
            <span>{product.category}</span>
            <span>›</span>
            <span style={{ color: 'var(--color-text-primary)' }}>{product.name}</span>
          </div>

          <div className="product-detail">
            {/* Image */}
            <div>
              <div className="product-image-main" aria-label={product.name}>
                {emoji}
              </div>
              {/* Tags */}
              <div className="flex gap-2 mt-3" style={{ flexWrap: 'wrap' }}>
                {product.tags.map((tag) => (
                  <span key={tag} className="badge badge-neutral">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Info */}
            <div className="product-info-section">
              {/* Category + condition */}
              <div className="flex items-center gap-2">
                <span className="page-tag" style={{ marginBottom: 0 }}>
                  {product.category}
                </span>
                <span className={`badge ${conditionVariant(product.condition)}`}>
                  {product.condition}
                </span>
              </div>

              <h1 className="product-name-large">{product.name}</h1>

              {/* Price */}
              <div>
                <div className="product-price-large">
                  {product.price} {product.currency}
                </div>
                <div className="text-small text-muted" style={{ marginTop: 4 }}>
                  {product.stock > 1
                    ? `Sandėlyje: ${product.stock} vnt.`
                    : product.stock === 1
                    ? '⚡ Paskutinis likutis!'
                    : '❌ Nebėra sandėlyje'}
                </div>
              </div>

              {/* Description */}
              <p style={{ fontSize: '0.9rem', lineHeight: 1.7, color: 'var(--color-text-secondary)' }}>
                {product.description}
              </p>

              {/* Spec table */}
              <div className="spec-table">
                <div className="spec-row">
                  <div className="spec-key">Markė</div>
                  <div className="spec-val">{product.make}</div>
                </div>
                <div className="spec-row">
                  <div className="spec-key">Modelis</div>
                  <div className="spec-val">{product.model}</div>
                </div>
                <div className="spec-row">
                  <div className="spec-key">Metai</div>
                  <div className="spec-val">
                    {product.yearFrom} – {product.yearTo}
                  </div>
                </div>
                <div className="spec-row">
                  <div className="spec-key">OEM kodas</div>
                  <div className="spec-val">
                    <code style={{ fontSize: '0.82rem', color: 'var(--color-accent)' }}>
                      {product.oemCode}
                    </code>
                  </div>
                </div>
                {product.color && product.color !== '–' && (
                  <div className="spec-row">
                    <div className="spec-key">Spalva</div>
                    <div className="spec-val">{product.color}</div>
                  </div>
                )}
                <div className="spec-row">
                  <div className="spec-key">Dalies ID</div>
                  <div className="spec-val">
                    <code style={{ fontSize: '0.82rem', color: 'var(--color-text-muted)' }}>
                      {product.id}
                    </code>
                  </div>
                </div>
              </div>

              {/* CTA */}
              <div>
                <button
                  id="btn-ai-consultant"
                  className="btn btn-primary btn-lg"
                  style={{ width: '100%' }}
                  onClick={() => setShowModal(true)}
                >
                  🎙️ Kalbėti su AI konsultantu
                </button>
                
                {twilioNumber && (
                  <a
                    href={`tel:${twilioNumber}`}
                    className="btn btn-ghost btn-lg mt-2"
                    style={{ 
                      width: '100%', 
                      border: '1px solid var(--color-border)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px'
                    }}
                  >
                    📞 Skambinti konsultantui
                  </a>
                )}

                <p
                  className="text-small text-muted"
                  style={{ textAlign: 'center', marginTop: 8 }}
                >
                  Rokas padės patikrinti suderinamumą ir atsakys į klausimus lietuviškai
                </p>
              </div>

              {/* Disclaimer */}
              <div
                style={{
                  padding: '12px 16px',
                  background: 'rgba(245, 158, 11, 0.06)',
                  border: '1px solid rgba(245, 158, 11, 0.2)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: '0.78rem',
                  color: 'var(--color-warning)',
                  lineHeight: 1.5,
                }}
              >
                ⚠️ Suderinamumas patvirtinamas tik pagal tikslų OEM kodą. AI konsultantas
                negali garantuoti tinkamumas be pilnų automobilio duomenų.
              </div>
            </div>
          </div>
        </div>
      </main>

      {showModal && (
        <AICallModal product={product} onClose={() => setShowModal(false)} />
      )}
    </>
  );
}
