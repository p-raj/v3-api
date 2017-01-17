"""
Process : Every Process is connected with a resource and itself it is blind.
          For every action it asks his Resource for instructions.
"""

RESOURCE_UPSTREAM_URL = 'http://local.veris.in:8000/resource/{resource_token}/{operation}/'