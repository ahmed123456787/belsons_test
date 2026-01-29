import { Component } from '@angular/core';
import { NewsListComponent } from './components/news-list/news-list';

@Component({
  selector: 'app-root',
  imports: [NewsListComponent],
  templateUrl: './app.html',
})
export class App {}
