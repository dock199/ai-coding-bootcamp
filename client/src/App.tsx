import { useState, useCallback } from 'react';
import type { UploadedImage } from './types';
import { useReportGenerator } from './hooks/useReportGenerator';
import { ImageUploader } from './components/ImageUploader';
import { ImagePreview } from './components/ImagePreview';
import { GenerateButton } from './components/GenerateButton';
import { ReportEditor } from './components/ReportEditor';
import { CopyButton } from './components/CopyButton';
import { ErrorMessage } from './components/ErrorMessage';
import './App.css';

function App() {
  const [images, setImages] = useState<UploadedImage[]>([]);
  const {
    report,
    isLoading,
    error,
    generateReportFromImages,
    setReport,
    clearError,
  } = useReportGenerator();

  const handleImagesAdded = useCallback((newImages: UploadedImage[]) => {
    setImages((prev) => [...prev, ...newImages]);
  }, []);

  const handleRemoveImage = useCallback((id: string) => {
    setImages((prev) => {
      const target = prev.find((img) => img.id === id);
      if (target) URL.revokeObjectURL(target.previewUrl);
      return prev.filter((img) => img.id !== id);
    });
  }, []);

  const handleGenerate = useCallback(() => {
    generateReportFromImages(images);
  }, [images, generateReportFromImages]);

  return (
    <div className="app">
      <header className="app__header">
        <h1 className="app__title">日報生成</h1>
        <p className="app__subtitle">
          スクリーンショットから、AIが日報を自動作成します
        </p>
      </header>

      <main className="app__main">
        <section className="app__upload-section">
          <ImageUploader onImagesAdded={handleImagesAdded} />
          <ImagePreview images={images} onRemove={handleRemoveImage} />
        </section>

        <div className="app__actions">
          <GenerateButton
            onClick={handleGenerate}
            disabled={images.length === 0}
            isLoading={isLoading}
          />
        </div>

        <ErrorMessage message={error} onDismiss={clearError} />

        {report && (
          <section className="app__report-section">
            <div className="app__report-header">
              <h2 className="app__report-title">日報</h2>
              <CopyButton text={report} />
            </div>
            <ReportEditor value={report} onChange={setReport} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
