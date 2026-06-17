<?php

declare(strict_types=1);

namespace DfcTest;

class Fixtures
{
    /**
     * Load a JSON-LD fixture file.
     *
     * @throws \RuntimeException
     */
    public static function loadFixture(string $fixturePath, string $fixturesDir): array
    {
        if ($fixturePath === '*') {
            throw new \RuntimeException('Wildcard fixture path not supported');
        }

        $fullPath = rtrim($fixturesDir, '/') . '/' . $fixturePath;
        if (!file_exists($fullPath)) {
            throw new \RuntimeException("Fixture not found: {$fullPath}");
        }

        $contents = file_get_contents($fullPath);
        if ($contents === false) {
            throw new \RuntimeException("Failed to read fixture: {$fullPath}");
        }

        $data = json_decode($contents, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($data)) {
            throw new \RuntimeException("Fixture is not a JSON object/array: {$fullPath}");
        }

        return $data;
    }

    /**
     * Load an inline test input from the spec.
     */
    public static function loadInlineInput(array $inputData): array
    {
        return $inputData;
    }
}
