export interface NewsArticle {
  id?: number;
  source: {
    id: string | null;
    name?: string;
  };
  title: string;
  description: string;
  url: string;
  image_url: string | null;
  published_at: string;
  content: string;
  category_name?: string;
  country_name?: string;
}

export interface NewsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: NewsArticle[];
}

export interface FilterParams {
  category?: string;
  country?: string;
  source?: string;
  query?: string;
  page?: number;
}

export interface Category {
  id: number;
  name: string;
}

export interface Country {
  id: number;
  code: string;
  name: string;
}

export interface Source {
  id: number;
  source_id: string;
  name: string;
  description: string;
  url: string;
  category: {
    id: number;
    name: string;
  };
  language: string;
  country: string;
}
