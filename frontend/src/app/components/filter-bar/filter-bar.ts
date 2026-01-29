import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NewsService } from '../../services/news';

@Component({
  selector: 'app-filter-bar',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './filter-bar.html',
})
export class FilterBarComponent implements OnInit {
  @Output() filterChange = new EventEmitter<any>();

  categories: string[] = [];
  countries: any[] = [];
  sources: any[] = [];

  selectedCategory = '';
  selectedCountry = '';
  selectedSource = '';

  constructor(private newsService: NewsService) {}

  ngOnInit(): void {
    this.loadFilters();
  }

  loadFilters(): void {
    this.newsService.getCategories().subscribe((data) => (this.categories = data));
    this.newsService.getCountries().subscribe((data) => (this.countries = data));
    this.newsService.getSources().subscribe((data) => {
      this.sources = data;
      console.log(this.sources);
    });
  }

  onFilterChange(): void {
    this.filterChange.emit({
      category: this.selectedCategory,
      country: this.selectedCountry,
      source: this.selectedSource,
    });
  }

  clearFilters(): void {
    this.selectedCategory = '';
    this.selectedCountry = '';
    this.selectedSource = '';
    this.onFilterChange();
  }
}
