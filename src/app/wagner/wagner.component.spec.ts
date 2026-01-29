import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WagnerComponent } from './wagner.component';

describe('WagnerComponent', () => {
  let component: WagnerComponent;
  let fixture: ComponentFixture<WagnerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WagnerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WagnerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
