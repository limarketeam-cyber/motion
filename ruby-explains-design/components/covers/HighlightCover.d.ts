/**
 * @startingPoint section="Instagram" subtitle="Ink circle with lime line icon" viewport="700x170"
 */
export interface HighlightCoverProps {
  /** Lucide icon name */
  icon: string;
  /** Persian label under the circle (preview only; Instagram sets its own) */
  label?: string;
  /** Circle diameter px. Default 240 */
  size?: number;
}
export declare function HighlightCover(props: HighlightCoverProps): JSX.Element;
