<?php

declare(strict_types=1);

namespace DfcTest\Tests;

use PHPUnit\Framework\TestCase;
use DfcTest\Fixtures;

abstract class BaseTestCase extends TestCase
{
    protected static string $fixturesDir;
    protected static array $spec;

    public static function setUpBeforeClass(): void
    {
        $rootPath = realpath(__DIR__ . '/../../../../../');
        self::$fixturesDir = $rootPath . '/fixtures';
        self::$spec = \Symfony\Component\Yaml\Yaml::parseFile($rootPath . '/spec/tests.yaml');
    }

    protected function loadFixture(string $relativePath): array
    {
        return Fixtures::loadFixture($relativePath, self::$fixturesDir);
    }

    protected function dfcSpec(): array
    {
        foreach (self::$spec['specs'] as $suite) {
            if ($suite['name'] === 'dfc-interop') {
                return $suite;
            }
        }
        throw new \RuntimeException('DFC spec not found');
    }

    protected function jsonldSpec(): array
    {
        foreach (self::$spec['specs'] as $suite) {
            if ($suite['name'] === 'jsonld-interop') {
                return $suite;
            }
        }
        throw new \RuntimeException('JSON-LD spec not found');
    }
}
