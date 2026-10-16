/**
 * @startingPoint section="Instagram" subtitle="Reels cover 1080×1920, text inside 4:5 crop" viewport="700x400"
 */
export interface ReelsCoverProps {
  /** Ink chip, default "ریلز · ۶۰ ثانیه" */
  tag?: string;
  termEn: string;
  termFa: string;
  /** Optional geometric graphic under the term. Default none */
  graphic?: 'none' | 'funnel';
  /** Dashed 4:5 crop guide — turn off before export */
  showSafeZone?: boolean;
  handle?: string;
}
export declare function ReelsCover(props: ReelsCoverProps): JSX.Element;
