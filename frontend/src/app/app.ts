import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NewsListComponent } from './components/news-list/news-list';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NewsListComponent],
  templateUrl: './app.html',
})
export class App {}
