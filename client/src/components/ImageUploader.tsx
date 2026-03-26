import { useState, useCallback, useEffect, useRef } from 'react';
import type { UploadedImage } from '../types';

const ACCEPTED_TYPES = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];

interface ImageUploaderProps {
  onImagesAdded: (images: UploadedImage[]) => void;
}

function createUploadedImage(file: File): UploadedImage {
  return {
    id: crypto.randomUUID(),
    file,
    previewUrl: URL.createObjectURL(file),
  };
}

function filterValidImages(files: FileList | File[]): File[] {
  return Array.from(files).filter((f) => ACCEPTED_TYPES.includes(f.type));
}

export function ImageUploader({ onImagesAdded }: ImageUploaderProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(
    (files: FileList | File[]) => {
      const valid = filterValidImages(files);
      if (valid.length > 0) {
        onImagesAdded(valid.map(createUploadedImage));
      }
    },
    [onImagesAdded],
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      handleFiles(e.dataTransfer.files);
    },
    [handleFiles],
  );

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleClick = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files) {
        handleFiles(e.target.files);
        e.target.value = '';
      }
    },
    [handleFiles],
  );

  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      const items = e.clipboardData?.items;
      if (!items) return;

      const imageFiles: File[] = [];
      for (const item of items) {
        if (ACCEPTED_TYPES.includes(item.type)) {
          const file = item.getAsFile();
          if (file) imageFiles.push(file);
        }
      }
      if (imageFiles.length > 0) {
        handleFiles(imageFiles);
      }
    };

    document.addEventListener('paste', handlePaste);
    return () => document.removeEventListener('paste', handlePaste);
  }, [handleFiles]);

  return (
    <div
      className={`image-uploader ${isDragOver ? 'image-uploader--drag-over' : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={handleClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleClick();
        }
      }}
      role="button"
      tabIndex={0}
      aria-label="画像をドラッグ&ドロップ、クリック、またはクリップボードから貼り付けてアップロード"
    >
      <input
        ref={fileInputRef}
        type="file"
        accept={ACCEPTED_TYPES.join(',')}
        multiple
        onChange={handleFileInput}
        className="image-uploader__input"
        aria-hidden="true"
        tabIndex={-1}
      />
      <div className="image-uploader__content">
        <div className="image-uploader__icon" aria-hidden="true">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M24 8v32M8 24h32" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </div>
        <p className="image-uploader__text">
          スクリーンショットをドラッグ&ドロップ
        </p>
        <p className="image-uploader__sub-text">
          またはクリックして選択 ・ Ctrl+V で貼り付け
        </p>
        <p className="image-uploader__formats">
          PNG, JPEG, GIF, WebP
        </p>
      </div>
    </div>
  );
}
