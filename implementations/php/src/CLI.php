<?php

declare(strict_types=1);

namespace DfcTest;

use Symfony\Component\Yaml\Yaml;

class CLI
{
    public static function run(array $argv): int
    {
        $options = self::parseOptions($argv);
        $spec = self::loadSpec($options['spec']);

        echo "Loaded spec with " . count($spec['specs']) . " test suites\n";
        foreach ($spec['specs'] as $suite) {
            echo "  - {$suite['name']}: " . count($suite['tests']) . " tests\n";
        }

        echo "\nFixtures directory: {$options['fixtures']}\n";
        echo "Results directory: {$options['results_dir']}\n";

        return 0;
    }

    private static function parseOptions(array $argv): array
    {
        $rootPath = realpath(__DIR__ . '/../../..');
        $options = [
            'spec' => $rootPath . '/spec/tests.yaml',
            'fixtures' => $rootPath . '/fixtures',
            'results_dir' => $rootPath . '/results',
            'platform_name' => 'php-connector',
        ];

        $longopts  = ['spec:', 'fixtures:', 'results-dir:', 'platform-name:'];
        $opts = getopt('', $longopts);

        if (isset($opts['spec']))         $options['spec'] = $opts['spec'];
        if (isset($opts['fixtures']))     $options['fixtures'] = $opts['fixtures'];
        if (isset($opts['results-dir']))  $options['results_dir'] = $opts['results-dir'];
        if (isset($opts['platform-name']))$options['platform_name'] = $opts['platform-name'];

        return $options;
    }

    private static function loadSpec(string $specPath): array
    {
        return Yaml::parseFile($specPath);
    }
}
