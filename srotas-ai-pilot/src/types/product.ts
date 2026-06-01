export interface Product {
  id: string;
  slug: string;
  name: string;
  category: string;
  make: string;
  model: string;
  yearFrom: number;
  yearTo: number;
  oemCode: string;
  condition: string;
  price: number;
  currency: string;
  stock: number;
  color: string;
  description: string;
  images: string[];
  tags: string[];
}
