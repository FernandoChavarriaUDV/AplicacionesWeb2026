import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Sergio } from './sergio';

describe('Sergio', () => {
  let component: Sergio;
  let fixture: ComponentFixture<Sergio>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Sergio]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Sergio);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
