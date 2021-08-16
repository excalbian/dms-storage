export class User {
  id!: number;
  username!: string;
  displayname!: string;
  email!: string;
  token!: string;
  is_active: boolean = false;
  is_banned: boolean = false;
  is_admin: boolean = false;
  can_report: boolean = false;
  can_configure: boolean = false;
  can_ban: boolean = false;
  next_use: Date = new Date('9999-12-31 23:59:59');
  exp: number = 0;
}
