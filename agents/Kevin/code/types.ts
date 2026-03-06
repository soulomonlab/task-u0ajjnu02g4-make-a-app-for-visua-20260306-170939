export type InspectionStatus = 'pending' | 'pass' | 'fail';

export interface InspectionItem {
  id: string;
  imageUrl?: string; // optional; may be a signed URL
  status: InspectionStatus;
  createdAt: string; // ISO timestamp
  metadata?: Record<string, string>;
}

export interface InspectionListResponse {
  items: InspectionItem[];
  totalCount: number; // total across pages (if using offset/page)
  cursor?: string; // cursor for cursor-based pagination (optional)
}
