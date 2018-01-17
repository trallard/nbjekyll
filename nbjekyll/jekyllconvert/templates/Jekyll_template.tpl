{% extends 'markdown.tpl' %}

{# custom header for jekyll post #}
{%- block header -%}
---
layout: notebook
title: "{{resources['metadata']['name']}}"
tags:
update_date: [-date-]
code_version: [-sha1-]
author: [-author-]
validation_pass: '[-validated-]'
badge: "https://img.shields.io/badge/notebook-[-badge-]"
---
<br />


{%- if "widgets" in nb.metadata -%}
<script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
{%- endif-%}
{%- endblock header -%}


{% block in_prompt -%}
{%- if cell.execution_count is defined -%}
{%- if resources.global_content_filter.include_input_prompt-%}
<font color='#808080'> In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]:</font>
{%- else -%}
<font color='#808080'> In&nbsp;[&nbsp;]: </font>
{%- endif -%}
{%- endif -%}
{%- endblock in_prompt %}


{# Images will be saved in the custom path #}
{% block data_svg %}
<img src="{{ output.metadata.filenames['image/svg+xml'] | jekyllpath }}" alt="svg" />
{% endblock data_svg %}

{% block data_png %}
<img src="{{ output.metadata.filenames['image/png'] | jekyllpath }}" alt="png"/>
{% endblock data_png %}

{% block data_jpg %}
<img src="{{ output.metadata.filenames['image/jpeg'] | jekyllpath }}" alt="jpeg" />
{% endblock data_jpg %}

{# cells containing markdown text only #}
{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) }}
{% endblock markdowncell %}

{# headings #}
{% block headingcell scoped %}
{{ '#' * cell.level }} {{ cell.source | replace('\n', ' ') }}
{% endblock headingcell %}

{% block stream -%}
{% endblock stream %}

{# latex data block#}
{% block data_latex %}
{{ output.data['text/latex'] }}
{% endblock data_latex %}

{% block data_text scoped %}
{{ output.data['text/plain'] | indent }}
{% endblock data_text %}

{% block data_html scoped -%}

{{ output.data['text/html'] }}

{%- endblock data_html %}

{% block data_markdown scoped -%}
{{ output.data['text/markdown'] | markdown2html }}

{%- endblock data_markdown %}
