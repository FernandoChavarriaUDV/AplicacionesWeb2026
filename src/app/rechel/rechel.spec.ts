import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Rechel } from './rechel';

describe('Rechel', () => {
  let component: Rechel;
  let fixture: ComponentFixture<Rechel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Rechel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Rechel);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
