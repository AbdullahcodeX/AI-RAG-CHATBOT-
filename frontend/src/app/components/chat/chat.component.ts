import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ChatMessage } from '../../models/rag.models';
import { RagApiService } from '../../services/rag-api.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent implements OnChanges {
  @Input() sessionId = '';
  @Input() hasDocuments = false;
  messages: ChatMessage[] = [];
  question = '';
  loading = false;
  error = '';

  constructor(private ragApi: RagApiService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['hasDocuments'] && !this.hasDocuments) {
      this.messages = [{ role: 'system', content: 'Upload a PDF to start chatting with your documents.' }];
    }
  }

  send(): void {
    const trimmed = this.question.trim();
    if (!trimmed || this.loading || !this.sessionId) return;
    if (!this.hasDocuments) { this.error = 'Upload at least one PDF before asking questions.'; return; }
    this.error = '';
    this.messages.push({ role: 'user', content: trimmed });
    this.question = '';
    this.loading = true;
    this.ragApi.chat(this.sessionId, trimmed).subscribe({
      next: (result) => {
        this.loading = false;
        this.messages.push({ role: 'assistant', content: result.answer, sources: result.sources });
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.detail || 'Failed to get an answer.';
      },
    });
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); this.send(); }
  }
}
