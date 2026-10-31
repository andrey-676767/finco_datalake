{# Usa el esquema indicado (silver, gold) tal cual, sin anteponer el del perfil. #}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {{- custom_schema_name | trim if custom_schema_name is not none else target.schema -}}
{%- endmacro %}
