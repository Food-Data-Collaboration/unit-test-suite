<?php

declare(strict_types=1);

namespace DfcTest;

/**
 * Base adapter interface for platform-specific test implementations.
 * Implement all methods to run the interop tests on PHP.
 */
interface AdapterInterface
{
    public function platformName(): string;

    /**
     * Parse a JSON-LD array into the platform's native structure.
     */
    public function parseJsonLd(array $data): mixed;

    /**
     * Serialize native structure back to a JSON-LD array.
     */
    public function serializeJsonLd(mixed $data): array;

    /**
     * Validate a JSON-LD document against its context.
     * Returns an array of error strings (empty if valid).
     *
     * @return string[]
     */
    public function validate(array $data): array;

    /**
     * Expand a JSON-LD document.
     */
    public function expand(array $data): mixed;

    /**
     * Compact expanded JSON-LD using a context.
     */
    public function compact(mixed $data, array $context): array;

    /**
     * Flatten a JSON-LD document.
     */
    public function flatten(array $data): array;
}
