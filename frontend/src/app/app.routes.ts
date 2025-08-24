import { Routes } from '@angular/router';
import { QueryOptimizerComponent } from './query-optimizer/query-optimizer.component';

export const routes: Routes = [
  { path: '', component: QueryOptimizerComponent },
  { path: '**', redirectTo: '' }
]; 