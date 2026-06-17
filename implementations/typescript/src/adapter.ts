export interface TestAdapter {
  platformName(): string;

  /**
   * Parse a JSON-LD document into the platform's native structure.
   */
  parseJsonLd(data: Record<string, any>): any;

  /**
   * Serialize native structure back to a JSON-LD document.
   */
  serializeJsonLd(data: any): Record<string, any>;

  /**
   * Validate a JSON-LD document against its context.
   * Returns an array of error strings (empty if valid).
   */
  validate(data: Record<string, any>): string[];

  /**
   * Expand a JSON-LD document.
   */
  expand(data: Record<string, any>): Promise<any>;

  /**
   * Compact expanded JSON-LD using a context.
   */
  compact(data: any, context: Record<string, any>): Promise<Record<string, any>>;

  /**
   * Flatten a JSON-LD document.
   */
  flatten(data: Record<string, any>): Promise<Record<string, any>>;
}
