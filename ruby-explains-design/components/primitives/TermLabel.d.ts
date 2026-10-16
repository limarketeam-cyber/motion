export interface TermLabelProps {
  /** English term, e.g. "Conversion Rate" or "CTA · Call to Action" */
  children: React.ReactNode;
  /** lg = 48px (text post), sm = 40px (photo post). Default lg */
  size?: 'lg' | 'sm';
}
export declare function TermLabel(props: TermLabelProps): JSX.Element;
