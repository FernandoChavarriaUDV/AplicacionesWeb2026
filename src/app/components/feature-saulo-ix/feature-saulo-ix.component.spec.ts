import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FeatureSauloIxComponent } from './feature-saulo-ix.component';

describe('FeatureSauloIxComponent', () => {
  let component: FeatureSauloIxComponent;
  let fixture: ComponentFixture<FeatureSauloIxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FeatureSauloIxComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FeatureSauloIxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
