import * as path from 'path';
import { loadFixture, specPath, fixturesDir } from '../src/cli';

const FIXTURES_DIR = fixturesDir();
const SPEC_PATH = specPath();

let cachedSpec: any = null;

function getSpec(): any {
  if (!cachedSpec) {
    const fs = require('fs');
    const yaml = require('yaml');
    const contents = fs.readFileSync(SPEC_PATH, 'utf-8');
    cachedSpec = yaml.parse(contents);
  }
  return cachedSpec;
}

export function dfcSpec(): any {
  const spec = getSpec();
  const found = spec.specs.find((s: any) => s.name === 'dfc-interop');
  if (!found) throw new Error('DFC spec not found');
  return found;
}

export function jsonldSpec(): any {
  const spec = getSpec();
  const found = spec.specs.find((s: any) => s.name === 'jsonld-interop');
  if (!found) throw new Error('JSON-LD spec not found');
  return found;
}

export function fixture(relativePath: string): Record<string, any> {
  return loadFixture(relativePath, FIXTURES_DIR);
}
