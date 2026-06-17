# frozen_string_literal: true

require "yaml"
require "json"

FIXTURES_DIR = File.expand_path("../../../fixtures", __dir__)
SPEC_PATH = File.expand_path("../../../spec/tests.yaml", __dir__)

RSpec.configure do |config|
  config.formatter = :documentation
  config.formatter = RSpec::Core::Formatters::JUnitFormatter if ENV["CI"]

  config.before(:suite) do
    @@spec = YAML.safe_load_file(SPEC_PATH)
    @@fixtures_dir = FIXTURES_DIR
  end

  config.before(:each) do
    @fixtures_dir = @@fixtures_dir
    @spec = @@spec
  end

  def load_fixture(relative_path)
    full_path = File.join(@fixtures_dir, relative_path)
    JSON.parse(File.read(full_path))
  end

  def dfc_spec
    @spec["specs"].find { |s| s["name"] == "dfc-interop" }
  end

  def jsonld_spec
    @spec["specs"].find { |s| s["name"] == "jsonld-interop" }
  end
end
