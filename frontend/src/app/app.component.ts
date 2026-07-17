import { Component, OnInit } from '@angular/core';
import { SessionStatus } from './models/rag.models';
import { RagApiService } from './services/rag-api.service';
import { SessionService } from './services/session.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  sessionId = '';
  status: SessionStatus | null = null;
  loadingSession = true;
  error = '';

  constructor(private ragApi: RagApiService, private sessionService: SessionService) {}

  ngOnInit(): void {
    const existing = this.sessionService.getSessionId();
    if (existing) { this.sessionId = existing; this.refreshStatus(); return; }
    this.ragApi.createSession().subscribe({
      next: (result) => {
        this.sessionId = result.session_id;
        this.sessionService.setSessionId(this.sessionId);
        this.loadingSession = false;
        this.status = { session_id: this.sessionId, document_count: 0, chunk_count: 0, filenames: [] };
      },
      error: () => { this.loadingSession = false; this.error = 'Could not create a session. Is the backend running?'; },
    });
  }

  refreshStatus(): void {
    if (!this.sessionId) return;
    this.ragApi.getSessionStatus(this.sessionId).subscribe({
      next: (status) => { this.status = status; this.loadingSession = false; this.error = ''; },
      error: () => {
        this.ragApi.createSession().subscribe({
          next: (result) => {
            this.sessionId = result.session_id;
            this.sessionService.setSessionId(this.sessionId);
            this.status = { session_id: this.sessionId, document_count: 0, chunk_count: 0, filenames: [] };
            this.loadingSession = false;
          },
          error: () => { this.loadingSession = false; this.error = 'Could not connect to backend API.'; },
        });
      },
    });
  }

  onUploaded(): void { this.refreshStatus(); }

  clearSession(): void {
    if (!this.sessionId) return;
    this.ragApi.clearSession(this.sessionId).subscribe({
      next: () => { this.sessionService.clearSessionId(); this.sessionId = ''; this.status = null; this.ngOnInit(); },
      error: () => { this.error = 'Failed to clear session.'; },
    });
  }

  get hasDocuments(): boolean { return (this.status?.document_count ?? 0) > 0; }
}
