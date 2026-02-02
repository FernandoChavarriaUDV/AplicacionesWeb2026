import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Jhonatan } from './jhonatan';

describe('Jhonatan', () => {
  let component: Jhonatan;
  let fixture: ComponentFixture<Jhonatan>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Jhonatan]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Jhonatan);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
