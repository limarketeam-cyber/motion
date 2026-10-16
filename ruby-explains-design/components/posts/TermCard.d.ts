/**
 * @startingPoint section="Instagram" subtitle="Text-only single-term post, 1080×1350" viewport="700x400"
 */
export interface TermCardProps {
  /** e.g. "مبانی بازاریابی" */
  category: string;
  /** e.g. "No.012" */
  number: string;
  /** English term, e.g. "Conversion Rate" */
  termEn: string;
  /** Persian term, 1–3 words */
  termFa: string;
  /** Friendly 1–2 sentence definition, spoken Persian */
  definition: string;
  /** Default "فرمول" */
  boxLabel?: string;
  /** Optional formula/example line; omit to hide the box */
  boxValue?: string;
  note?: string;
  icon?: string;
}
export declare function TermCard(props: TermCardProps): JSX.Element;
