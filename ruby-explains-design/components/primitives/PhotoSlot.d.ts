export interface PhotoSlotProps {
  /** Image URL. Without it a striped placeholder shows */
  src?: string;
  /** Placeholder caption describing the photo to drop in */
  label?: string;
  /** px on the 1080 canvas. Default 580 */
  height?: number;
  alt?: string;
}
export declare function PhotoSlot(props: PhotoSlotProps): JSX.Element;
