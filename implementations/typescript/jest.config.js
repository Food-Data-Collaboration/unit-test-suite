/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: '../../results/node-jsonld',
      outputName: 'results.xml',
      classNameTemplate: '{classname}',
      titleTemplate: '{title}'
    }]
  ]
};
