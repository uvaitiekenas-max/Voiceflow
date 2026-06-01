import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import productsData from '@/data/products.json';
import type { Product } from '@/types/product';
import ProductDetailClient from './ProductDetailClient';

const products = productsData as Product[];

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return products.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const product = products.find((p) => p.slug === slug);
  if (!product) return { title: 'Nerasta' };

  return {
    title: `${product.name} – ${product.make} ${product.model} | Srotas`,
    description: product.description,
  };
}

export default async function ProductDetailPage({ params }: Props) {
  const { slug } = await params;
  const product = products.find((p) => p.slug === slug);

  if (!product) notFound();

  return <ProductDetailClient product={product} />;
}
