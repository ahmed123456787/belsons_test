import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsService } from '../../services/news';
import { NewsArticle, FilterParams } from '../../models/global.models';
import { PaginationComponent } from '../pagination/pagination';
import { NewsCardComponent } from '../news-card/news-card';
import { SearchBarComponent } from '../search-bar/search-bar';
import { FilterBarComponent } from '../filter-bar/filter-bar';

@Component({
  selector: 'app-news-list',
  standalone: true,
  imports: [
    CommonModule,
    PaginationComponent,
    NewsCardComponent,
    SearchBarComponent,
    FilterBarComponent,
  ],
  templateUrl: './news-list.html',
})
export class NewsListComponent implements OnInit {
  articles: NewsArticle[] = [];
  loading = false;
  error = '';

  currentPage = 1;
  totalItems = 0;
  itemsPerPage = 50;

  filters: FilterParams = {};

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.loadNews();
  }

  loadNews(): void {
    this.loading = true;
    this.error = '';

    const params: FilterParams = {
      ...this.filters,
      page: this.currentPage,
    };

    this.newsService.getNews(params).subscribe({
      next: (response) => {
        this.articles = response.results || [];
        this.totalItems = response.count || 0;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load news. Please try again.';
        this.articles = [];
        this.totalItems = 0;
        this.loading = false;
        console.error('Error loading news:', err);
      },
      complete: () => {
        this.loading = false;
      },
    });
  }

  onSearch(query: string): void {
    this.filters.query = query;
    this.currentPage = 1;
    this.loadNews();
  }

  onFilterChange(filters: any): void {
    this.filters = { ...this.filters, ...filters };
    this.currentPage = 1;
    this.loadNews();
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadNews();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
