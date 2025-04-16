# ThinkAlike API Summary

*This documentation was automatically generated on {{ generation_date }}*

This document provides a comprehensive overview of all API endpoints in the ThinkAlike platform, organized by category.

{% for category, endpoints in endpoints_by_category.items() %}
## {{ category.replace('_', ' ').title() }} Endpoints

| Method | Path | Function | Description |
|--------|------|----------|-------------|
{% for endpoint in endpoints %}
| {{ endpoint.method }} | `{{ endpoint.path }}` | {{ endpoint.function }} | {{ endpoint.description.split('\n')[0] }} |
{% endfor %}

{% endfor %}