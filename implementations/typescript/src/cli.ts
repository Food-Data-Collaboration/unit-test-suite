import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';
import { loadFixture } from './fixtures';

export interface SpecOptions {
  spec: string;
  fixtures: string;
  resultsDir: string;
  platformName: string;
}

export function parseOptions(): SpecOptions {
  const rootPath = path.resolve(__dirname, '../..');
  const options: SpecOptions = {
    spec: path.join(rootPath, 'spec', 'tests.yaml'),
    fixtures: path.join(rootPath, 'fixtures'),
    resultsDir: path.join(rootPath, 'results'),
    platformName: 'node-jsonld'
  };

  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--spec':
        options.spec = args[++i];
        break;
      case '--fixtures':
        options.fixtures = args[++i];
        break;
      case '--results-dir':
        options.resultsDir = args[++i];
        break;
      case '--platform-name':
        options.platformName = args[++i];
        break;
    }
  }

  return options;
}

export function loadSpec(specPath: string): any {
  const contents = fs.readFileSync(specPath, 'utf-8');
  return yaml.parse(contents);
}

export function rootPath(): string {
  return path.resolve(__dirname, '../..');
}

export function fixturesDir(): string {
  return path.join(rootPath(), 'fixtures');
}

export function specPath(): string {
  return path.join(rootPath(), 'spec', 'tests.yaml');
}
