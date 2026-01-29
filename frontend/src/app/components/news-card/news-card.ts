import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NewsArticle } from '../../models/global.models';

@Component({
  selector: 'app-news-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news-card.html',
})
export class NewsCardComponent {
  @Input() article!: NewsArticle;

  openArticle(): void {
    window.open(this.article.url, '_blank');
  }

  getImageUrl(): string {
    return this.article.image_url || 'https://via.placeholder.com/400x200?text=No+Image';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long', // "January"
      day: 'numeric', // "29"
    });
  }
}
