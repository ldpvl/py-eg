from ruamel.yaml import YAML

# Create YAML instance
yaml = YAML()

yaml.allow_duplicate_keys = True

# YAML with multiple merge anchors
yaml_content = """
defaults: &defaults
  environment: production
  timeout: 30
  retries: 3

logging: &logging
  log_level: info
  log_file: app.log
  format: json

database: &database
  host: localhost
  port: 5432

service1:
  <<: [*defaults, *logging, *database]
  name: user-service
  timeout: 60  # This overrides the default timeout
  host: db.prod.internal  # This overrides the default host

service2:
  <<: *defaults
  <<: *logging
  name: auth-service
  port: 3306  # This overrides the database port
"""

# Parse the YAML
data = yaml.load(yaml_content)

# Print the parsed data
print("Parsed data:")
print(data['service1'])
print("\nservice2:")
print(data['service2'])

# Dump back to YAML - merge keys are preserved!
print("\n--- YAML with preserved merge keys ---")
yaml.dump(data, open('output.yaml', 'w'))

# Or print to stdout
from io import StringIO
string_buffer = StringIO()
yaml.dump(data, string_buffer)
print(string_buffer.getvalue())