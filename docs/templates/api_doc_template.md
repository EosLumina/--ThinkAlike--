# {{ module_name.replace('_', ' ').title() }} API Endpoints

*This documentation was automatically generated on {{ generation_date }}*

These endpoints implement ThinkAlike's {{ module_name.replace('_', ' ') }} functionality, embodying our principles of user sovereignty, radical transparency, and data minimization.

{% for endpoint in endpoints %}
## {{ endpoint.function }} `{{ endpoint.method }} {{ endpoint.path }}`

{{ endpoint.description }}

{% if endpoint.response_model %}
**Response Model:** `{{ endpoint.response_model }}`
{% endif %}

{% endfor %}