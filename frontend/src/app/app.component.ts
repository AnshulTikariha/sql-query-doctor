import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `
    <div class="container">
      <router-outlet></router-outlet>
      
      <!-- Footer -->
      <footer class="footer">
        <div class="footer-content">
          <div class="footer-left">
            <p>© 2025 Developer Viewpoint. All rights reserved.</p>
            <p class="footer-subtitle">Free source code available on GitHub (MIT Licensed).</p>
          </div>
          <p class="footer-right">Developed by <span class="developer-name">Anshul</span>.</p>
        </div>
      </footer>
    </div>
  `,
  styles: [`
    .container {
      padding-top: 20px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      margin: 0;
      padding-bottom: 0;
    }
    
    .footer {
      border-top: 1px solid #e5e7eb;
      background-color: rgba(255, 255, 255, 0.5);
      backdrop-filter: blur(8px);
      margin-top: auto;
      margin-bottom: 0;
      padding-bottom: 0;
      position: relative;
      bottom: 0;
      width: 100%;
    }
    
    .footer-content {
      max-width: 80rem;
      margin: 0 auto;
      padding: 1rem 1rem;
      font-size: 0.875rem;
      color: #4b5563;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    
    .footer-left {
      text-align: left;
    }
    
    .footer-subtitle {
      margin-top: 0.125rem;
    }
    
    .footer-right {
      text-align: right;
    }
    
    .developer-name {
      font-weight: 600;
    }
    
    @media (max-width: 640px) {
      .footer-content {
        flex-direction: column;
        gap: 1rem;
        text-align: center;
      }
      
      .footer-left, .footer-right {
        text-align: center;
      }
    }
  `]
})
export class AppComponent {
  title = 'SQL Query Doctor';
} 