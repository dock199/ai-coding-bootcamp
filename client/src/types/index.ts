export interface UploadedImage {
  id: string;
  file: File;
  previewUrl: string;
}

export interface ReportResponse {
  report: string;
}

export interface ApiError {
  detail: string;
}
