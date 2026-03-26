import { useState, useCallback } from 'react';
import type { UploadedImage } from '../types';
import { generateReport } from '../services/api';

interface UseReportGeneratorReturn {
  report: string;
  isLoading: boolean;
  error: string | null;
  generateReportFromImages: (images: UploadedImage[]) => Promise<void>;
  setReport: (report: string) => void;
  clearError: () => void;
}

export function useReportGenerator(): UseReportGeneratorReturn {
  const [report, setReport] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateReportFromImages = useCallback(async (images: UploadedImage[]) => {
    if (images.length === 0) return;

    setIsLoading(true);
    setError(null);

    try {
      const files = images.map((img) => img.file);
      const response = await generateReport(files);
      setReport(response.report);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : '日報の生成に失敗しました。しばらくしてから再度お試しください';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => setError(null), []);

  return {
    report,
    isLoading,
    error,
    generateReportFromImages,
    setReport,
    clearError,
  };
}
