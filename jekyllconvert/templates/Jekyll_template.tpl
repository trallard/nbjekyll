{% extends "basic.tpl" %}

{# custom header for jekyll post #}
{%- block header -%}
---
layout: notebook
title: "{{resources['metadata']['name']}}"
tags:
update_date:
code_version: 1
validation_pass:
---
<br />
{%- if "widgets" in nb.metadata -%}
<script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
{%- endif-%}
{%- endblock header -%}

{% block in_prompt -%}
<div class="prompt input_prompt">
{%- if cell.execution_count is defined -%}
{%- if resources.global_content_filter.include_input_prompt-%}
<font color ='#00bcd4'>In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]: </font>
{%- else -%}
In&nbsp;[&nbsp;]:
{%- endif -%}
{%- endif -%}
</div>
{%- endblock in_prompt %}

{% block data_markdown scoped %}
{{ output.data['text/markdown'] }}
{% endblock data_markdown %}

{% block markdowncell scoped %}
{{ cell.source }}
{% endblock markdowncell %}

{% block data_html scoped -%}
{{ output.data['text/markdown'] | markdown2html }}
{%- endblock data_html %}

{# Images will be saved in the custom path #}
{% block data_svg %}
<img src="{{ output.svg_filename | jekyllpath }}" alt="svg" />
{% endblock data_svg %}

{% block data_png scoped %}
<div class="output_png output_subarea {{ extra_class }}">
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/png'] | jekyllpath}}"
{%- else %}
<img src="data:image/png,{{ output.data['image/png'] | jekyllpath  }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/png') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/png') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/png') %}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_png %}


{% block data_jpg %}
<img src="{{ output.metadata.filenames['image/jpeg'] | jekyllpath }}" alt="jpeg" />
{% endblock data_jpg %}