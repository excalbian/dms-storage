import { TestBed } from '@angular/core/testing';

import { DmsStorageApiService } from './dms-storage-api.service';

describe('DmsStorageApiService', () => {
  let service: DmsStorageApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DmsStorageApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
