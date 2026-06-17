# frozen_string_literal: true

module DfcTest
  # Base adapter class for platform-specific test implementations.
  # Subclass this and implement all methods to run the interop tests.
  class Adapter
    def platform_name
      raise NotImplementedError, "Subclass must implement #platform_name"
    end

    # Parse a JSON-LD hash into the platform's native structure.
    def parse_jsonld(data)
      raise NotImplementedError, "Subclass must implement #parse_jsonld"
    end

    # Serialize native structure back to a JSON-LD hash.
    def serialize_jsonld(data)
      raise NotImplementedError, "Subclass must implement #serialize_jsonld"
    end

    # Validate a JSON-LD document against its context.
    # Returns an array of error strings (empty if valid).
    def validate(data)
      raise NotImplementedError, "Subclass must implement #validate"
    end

    # Expand a JSON-LD document.
    def expand(data)
      raise NotImplementedError, "Subclass must implement #expand"
    end

    # Compact expanded JSON-LD using a context.
    def compact(data, context)
      raise NotImplementedError, "Subclass must implement #compact"
    end

    # Flatten a JSON-LD document.
    def flatten(data)
      raise NotImplementedError, "Subclass must implement #flatten"
    end
  end
end
