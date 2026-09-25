---
layout: archive
title: ""
permalink: /services/
author_profile: true
---

**Academic Services**
=====

{% include service-list.html items=site.data.services.academic %}

<p class="dated-label">Invited Reviewer for Journals and Magazines</p>

<ul class="dated-rows dated-single">
{%- for r in site.data.services.reviewer %}
<li><span><a href="{{ r.url }}">{{ r.name }}</a>{% if r.detail %} <span class="dated-extra">· {{ r.detail }}</span>{% endif %}</span></li>
{%- endfor %}
</ul>

## Other Activities

{% include service-list.html items=site.data.services.other %}
