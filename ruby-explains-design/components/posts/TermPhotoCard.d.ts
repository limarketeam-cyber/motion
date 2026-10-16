/**
 * @startingPoint section="Instagram" subtitle="Single-term post with real photo, 1080×1350" viewport="700x400"
 */
export interface TermPhotoCardProps {
  category: string;
  number: string;
  termEn: string;
  termFa: string;
  definition: string;
  /** Photo URL; placeholder shown if omitted */
  photoSrc?: string;
  photoLabel?: string;
  note?: string;
  icon?: string;
}
export declare function TermPhotoCard(props: TermPhotoCardProps): JSX.Element;
