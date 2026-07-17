import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ChatResult, SessionStatus, UploadResult } from '../models/rag.models';

@Injectable({ providedIn: 'root' })
export class RagApiService {
  private readonly baseUrl = environment.apiUrl;
  constructor(private http: HttpClient) {}

  createSession(): Observable<{ session_id: string }> {
    return this.http.post<{ session_id: string }>(`${this.baseUrl}/session`, {});
  }

  uploadPdf(sessionId: string, file: File): Observable<UploadResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);
    return this.http.post<UploadResult>(`${this.baseUrl}/upload`, formData);
  }

  chat(sessionId: string, question: string): Observable<ChatResult> {
    return this.http.post<ChatResult>(`${this.baseUrl}/chat`, { session_id: sessionId, question });
  }

  getSessionStatus(sessionId: string): Observable<SessionStatus> {
    return this.http.get<SessionStatus>(`${this.baseUrl}/session/${sessionId}`);
  }

  clearSession(sessionId: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.baseUrl}/session/${sessionId}`);
  }
}
