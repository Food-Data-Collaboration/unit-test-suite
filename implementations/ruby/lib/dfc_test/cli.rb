# frozen_string_literal: true

require "optparse"
require "yaml"
require_relative "fixtures"

module DfcTest
  module CLI
    module_function

    def run(args = ARGV)
      options = parse_options(args)
      spec = load_spec(options[:spec])

      puts "Loaded spec with #{spec['specs'].length} test suites"
      spec["specs"].each do |suite|
        puts "  - #{suite['name']}: #{suite['tests'].length} tests"
      end

      puts "\nFixtures directory: #{options[:fixtures]}"
      puts "Results directory: #{options[:results_dir]}"
    end

    def parse_options(args)
      options = {
        spec: File.join(root_path, "spec", "tests.yaml"),
        fixtures: File.join(root_path, "fixtures"),
        results_dir: File.join(root_path, "results"),
        platform_name: "ruby-ofn"
      }

      OptionParser.new do |opts|
        opts.banner = "Usage: dfc-test-runner [options]"

        opts.on("--spec PATH", "Path to tests.yaml") do |v|
          options[:spec] = v
        end

        opts.on("--fixtures PATH", "Path to fixtures directory") do |v|
          options[:fixtures] = v
        end

        opts.on("--results-dir PATH", "Path to results directory") do |v|
          options[:results_dir] = v
        end

        opts.on("--platform-name NAME", "Platform name for results") do |v|
          options[:platform_name] = v
        end
      end.parse!(args)

      options
    end

    def load_spec(spec_path)
      YAML.safe_load_file(spec_path)
    end

    def root_path
      File.expand_path("../../..", __dir__)
    end
  end
end
