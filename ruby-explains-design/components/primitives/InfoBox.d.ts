export interface InfoBoxProps {
  /** Small mono label: "فرمول" | "مثال" | "نکته". Default "فرمول" */
  label?: string;
  /** One short line, max ~30 characters */
  children: React.ReactNode;
}
export declare function InfoBox(props: InfoBoxProps): JSX.Element;
