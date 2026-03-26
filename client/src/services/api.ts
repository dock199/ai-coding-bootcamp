import type { ReportResponse, ApiError } from '../types';

export async function generateReport(files: File[]): Promise<ReportResponse> {
  const formData = new FormData();
  for (const file of files) {
    formData.append('files', file);
  }

  const response = await fetch('/api/generate-report', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error: ApiError = await response.json().catch(() => ({
      detail: '日報の生成に失敗しました。しばらくしてから再度お試しください',
    }));
    throw new Error(error.detail);
  }

  return response.json();
}
