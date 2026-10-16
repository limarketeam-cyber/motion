export interface IconProps {
  /** Lucide icon name, e.g. "bookmark", "megaphone" */
  name: string;
  /** px on the 1080 canvas. Default 36 */
  size?: number;
  /** CSS color. Default var(--ink) */
  color?: string;
  style?: React.CSSProperties;
}
export declare function Icon(props: IconProps): JSX.Element;
