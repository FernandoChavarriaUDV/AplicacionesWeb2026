import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Axel } from './axel';

describe('Axel', () => {
  let component: Axel;
  let fixture: ComponentFixture<Axel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Axel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Axel);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
