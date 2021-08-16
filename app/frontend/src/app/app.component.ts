import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { User } from './models';
import { DmsStorageApiService } from './services/dms-storage-api.service';


@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.less']
})
export class AppComponent {
  title = 'dms-storage';
  currentUser!: User | null;

  constructor(
    private router: Router,
    private storageService: DmsStorageApiService
  ) {
    this.storageService.currentUser.subscribe( x => this.currentUser = x);
  }
}
