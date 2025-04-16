# {{ module_name.replace('_', ' ').title() }} Data Models

*This documentation was automatically generated on {{ generation_date }}*

These models define the database structure for ThinkAlike's {{ module_name.replace('_', ' ') }} functionality, implementing our principles of user sovereignty, radical transparency, and ethical data handling.

{% for model in models %}
## {{ model.name }}

{% if model.tablename %}**Table Name:** `{{ model.tablename }}`{% endif %}

{{ model.description }}

### Columns

| Name | Definition |
|------|------------|
{% for column in model.columns %}
| `{{ column.name }}` | {{ column.definition }} |
{% endfor %}

{% endfor %}