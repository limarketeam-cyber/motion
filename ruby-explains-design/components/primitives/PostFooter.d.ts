export interface PostFooterProps {
  /** Default "ruby.explains" */
  handle?: string;
  /** Short friendly CTA, e.g. "ذخیره‌ش کن، بعداً لازمت میشه" */
  note?: string;
  /** Lucide icon name: "bookmark" | "send" | "arrow-left" */
  icon?: string;
}
export declare function PostFooter(props: PostFooterProps): JSX.Element;
