import * as fs from 'fs';
import * as path from 'path';

/**
 * Load a JSON-LD fixture file.
 */
export function loadFixture(fixturePath: string, fixturesDir: string): Record<string, any> {
  if (fixturePath === '*') {
    throw new Error('Wildcard fixture path not supported');
  }

  const fullPath = path.join(fixturesDir, fixturePath);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Fixture not found: ${fullPath}`);
  }

  const contents = fs.readFileSync(fullPath, 'utf-8');
  return JSON.parse(contents);
}

/**
 * Load an inline test input from the spec.
 */
export function loadInlineInput(inputData: Record<string, any>): Record<string, any> {
  return inputData;
}
