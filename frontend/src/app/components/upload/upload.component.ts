import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RagApiService } from '../../services/rag-api.service';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss'],
})
export class UploadComponent {
  @Input() sessionId = '';
  @Output() uploaded = new EventEmitter<void>();
  selectedFile: File | null = null;
  uploading = false;
  message = '';
  error = '';

  constructor(private ragApi: RagApiService) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFile = input.files?.[0] ?? null;
    this.message = this.selectedFile ? `Selected: ${this.selectedFile.name}` : '';
    this.error = '';
  }

  upload(): void {
    if (!this.sessionId || !this.selectedFile) {
      this.error = 'Select a PDF file first.';
      return;
    }
    this.uploading = true;
    this.error = '';
    this.message = 'Uploading and indexing PDF...';
    this.ragApi.uploadPdf(this.sessionId, this.selectedFile).subscribe({
      next: (result) => {
        this.uploading = false;
        this.message = `${result.filename} indexed (${result.chunks_indexed} chunks).`;
        this.selectedFile = null;
        this.uploaded.emit();
      },
      error: (err) => {
        this.uploading = false;
        this.error = err?.error?.detail || 'Upload failed. Please try again.';
        this.message = '';
      },
    });
  }
}
