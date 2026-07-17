import { Injectable } from '@angular/core';

const SESSION_KEY = 'doc_rag_session_id';

@Injectable({ providedIn: 'root' })
export class SessionService {
  getSessionId(): string | null { return localStorage.getItem(SESSION_KEY); }
  setSessionId(sessionId: string): void { localStorage.setItem(SESSION_KEY, sessionId); }
  clearSessionId(): void { localStorage.removeItem(SESSION_KEY); }
}
