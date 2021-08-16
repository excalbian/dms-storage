import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '../models';
import { DmsStorageApiService } from '../services/dms-storage-api.service';


@Component({
  templateUrl: 'home.component.html',
  styleUrls: ['./home.component.less'],
})
export class HomeComponent implements OnInit {
    currentUser: User | null;
    users = [];

    constructor(
        private storageService: DmsStorageApiService
    ) {
        this.currentUser = this.storageService.currentUserValue;
    }

    ngOnInit() {
    }

}
