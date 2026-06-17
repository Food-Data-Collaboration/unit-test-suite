# frozen_string_literal: true

require "json"

module DfcTest
  module Fixtures
    module_function

    # Load a JSON-LD fixture file.
    # @param fixture_path [String] Path relative to fixtures directory
    # @param fixtures_dir [String] Absolute path to fixtures directory
    # @return [Hash] Parsed JSON-LD
    def load_fixture(fixture_path, fixtures_dir)
      raise ArgumentError, "Wildcard fixture path not supported" if fixture_path == "*"

      full_path = File.join(fixtures_dir, fixture_path)
      raise FileNotFoundError, "Fixture not found: #{full_path}" unless File.exist?(full_path)

      JSON.parse(File.read(full_path))
    end

    # Load an inline test input from the YAML spec.
    def load_inline_input(input_data)
      input_data
    end
  end
end
