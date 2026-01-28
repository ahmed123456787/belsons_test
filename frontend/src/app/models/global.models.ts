export interface NewsArticle {
  id?: number;
  source: {
    id: string | null;
    name: string;
  };
  author: string | null;
  title: string;
  description: string;
  url: string;
  urlToImage: string | null;
  publishedAt: string;
  content: string;
  category?: string;
  country?: string;
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
  count: number;
  total_pages: number;
  current_page: number;
  page_size: number;
  results: [
    {
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
  ];
}
