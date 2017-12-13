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

{# Images handling#}
{% block data_svg %}
{%- if output.svg_filename %}
<img src="{{ output.svg_filename | posix_path }}" alt="svg">
{%- else %}
{{ output.data['image/svg+xml'] }}
{%- endif %}
{%- endblock data_svg %}

{% block data_png scoped %}
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/png'] | posix_path }}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
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
 alt = 'png'>
{%- endblock data_png %}

{% block data_jpg scoped %}
<div class="output_jpeg output_subarea {{ extra_class }}">
{%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/jpeg'] | posix_path }}"
{%- else %}
<img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/jpeg') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/jpeg') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/jpeg') %}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_jpg %}