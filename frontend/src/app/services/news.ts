import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { NewsResponse, FilterParams, Category, Country, Source } from '../models/global.models';

@Injectable({
  providedIn: 'root',
})
export class NewsService {
  private apiUrl = 'http://localhost:8000/apis/v1';

  constructor(private http: HttpClient) {}

  getNews(filters: FilterParams = {}): Observable<NewsResponse> {
    let params = new HttpParams();

    if (filters.category) params = params.set('category', filters.category);
    if (filters.country) params = params.set('country', filters.country);
    if (filters.source) params = params.set('source', filters.source);
    if (filters.query) params = params.set('search', filters.query);
    if (filters.page) params = params.set('page', filters.page.toString());

    return this.http.get<NewsResponse>(`${this.apiUrl}/news/`, { params });
  }

  getCategories(): Observable<string[]> {
    return this.http
      .get<Category[]>(`${this.apiUrl}/categories/`)
      .pipe(map((categories: Category[]) => categories.map((c) => c.name)));
  }

  getCountries(): Observable<string[]> {
    return this.http
      .get<Country[]>(`${this.apiUrl}/countries/`)
      .pipe(map((countries: Country[]) => countries.map((c) => c.name)));
  }

  getSources(): Observable<string[]> {
    return this.http
      .get<Source>(`${this.apiUrl}/sources/`)
      .pipe(map((response) => response.results.map((s) => s.name)));
  }
}
