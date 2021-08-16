import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import jwt_decode from 'jwt-decode';
import { User } from '../models/user';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DmsStorageApiService {
  private currentUserSubject: BehaviorSubject<User|null>;
  public currentUser: Observable<User|null>;

  constructor(private http: HttpClient) {
    let userinfo:string|null= localStorage.getItem('currentUser');
    let user = userinfo != null ? JSON.parse(userinfo) : null;

    this.currentUserSubject = new BehaviorSubject<User|null>(user);
    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue(): User | null {
      return this.currentUserSubject.value;
  }

  login(username: string, password: string) {
    let formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    return this.http.post<any>(environment.dmsStorageApiUrl + '/auth', formData)
      .pipe(map(t => {

        let decoded: User = jwt_decode(t.access_token);
        decoded.token = t.access_token;

        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('currentUser', JSON.stringify(decoded));
        this.currentUserSubject.next(decoded);
        return decoded;
      }));
  }

  logout() {
      // remove user from local storage and set current user to null
      localStorage.removeItem('currentUser');
      this.currentUserSubject.next(null);
  }
}
