import type { UploadedImage } from '../types';

interface ImagePreviewProps {
  images: UploadedImage[];
  onRemove: (id: string) => void;
}

export function ImagePreview({ images, onRemove }: ImagePreviewProps) {
  if (images.length === 0) return null;

  return (
    <div className="image-preview" role="list" aria-label="アップロード済み画像">
      {images.map((image) => (
        <div key={image.id} className="image-preview__item" role="listitem">
          <img
            src={image.previewUrl}
            alt={image.file.name}
            className="image-preview__thumbnail"
          />
          <button
            type="button"
            className="image-preview__remove"
            onClick={() => onRemove(image.id)}
            aria-label={`${image.file.name} を削除`}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            </svg>
          </button>
          <span className="image-preview__name">{image.file.name}</span>
        </div>
      ))}
    </div>
  );
}
