import { AuthService } from './../services/auth.service';
import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';

import { User } from '../models';
import { noop } from 'rxjs';



@Component({
  templateUrl: 'home.component.html',
  styleUrls: ['home.component.less'],
})
export class HomeComponent implements OnInit {
    currentUser: User | null = null;

    constructor(
        private authService: AuthService
    ) {
        this.authService.currentUser.subscribe( x => this.currentUser = x);
    }

    ngOnInit() {
      noop();
    }

}
