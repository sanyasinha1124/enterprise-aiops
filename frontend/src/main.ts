import { bootstrapApplication } from '@angular/platform-browser';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, provideHttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
  <main class="page">
    <section class="hero">
      <p class="eyebrow">ENTERPRISEOPS AI</p>
      <h1>Agentic RAG for enterprise operations.</h1>
      <p class="subtitle">
        Ask about company policies, customers and orders. The backend uses Gemini,
        Qdrant retrieval and controlled tools.
      </p>
    </section>

    <section class="chat-card">
      <div class="messages">
        <div *ngFor="let m of messages" [class.user]="m.role === 'user'" class="message">
          <strong>{{ m.role === 'user' ? 'You' : 'EnterpriseOps AI' }}</strong>
          <p>{{ m.text }}</p>
        </div>
      </div>

      <form (ngSubmit)="send()">
        <textarea
          [(ngModel)]="question"
          name="question"
          rows="4"
          placeholder="Example: Can customer 1001 get a refund for order 5001?"></textarea>
        <button [disabled]="loading || !question.trim()">
          {{ loading ? 'Thinking…' : 'Ask EnterpriseOps' }}
        </button>
      </form>
    </section>
  </main>
  `,
  styles: [`
    :host { display:block; min-height:100vh; }
    .page { max-width: 1050px; margin:auto; padding:48px 22px; }
    .hero { margin-bottom:28px; }
    .eyebrow { letter-spacing:.18em; font-size:12px; opacity:.7; }
    h1 { font-size: clamp(38px, 6vw, 72px); line-height:1; margin:10px 0 18px; }
    .subtitle { max-width:720px; color:#b7bfd2; font-size:18px; line-height:1.6; }
    .chat-card { border:1px solid #263047; border-radius:24px; padding:20px; background:#111827; }
    .messages { min-height:280px; max-height:520px; overflow:auto; display:flex; flex-direction:column; gap:14px; }
    .message { padding:16px; border-radius:16px; background:#182235; max-width:88%; }
    .message.user { align-self:flex-end; background:#24324d; }
    .message p { white-space:pre-wrap; line-height:1.6; color:#dce3f1; }
    form { margin-top:18px; display:flex; gap:12px; flex-direction:column; }
    textarea { resize:vertical; border:1px solid #34415b; border-radius:14px; padding:14px; background:#0b1220; color:white; font:inherit; }
    button { border:0; border-radius:12px; padding:13px 18px; background:#e5b95c; color:#111827; font-weight:700; cursor:pointer; }
    button:disabled { opacity:.5; cursor:not-allowed; }
  `]
})
class AppComponent {
  question = '';
  loading = false;
  messages: { role: string; text: string }[] = [];

  constructor(private http: HttpClient) {}

  async send() {
    const question = this.question.trim();
    if (!question || this.loading) return;

    this.messages.push({ role: 'user', text: question });
    this.question = '';
    this.loading = true;

    try {
      const result: any = await firstValueFrom(
        this.http.post('http://127.0.0.1:8000/api/chat', { message: question })
      );

      this.messages.push({
        role: 'assistant',
        text: result.answer + (result.sources?.length
          ? `\n\nSources: ${result.sources.map((s: any) => s.title).join(', ')}`
          : '')
      });
    } catch (error) {
      this.messages.push({
        role: 'assistant',
        text: 'Could not reach the backend. Make sure FastAPI is running on port 8000.'
      });
    } finally {
      this.loading = false;
    }
  }
}

bootstrapApplication(AppComponent, {
  providers: [provideHttpClient()]
});
