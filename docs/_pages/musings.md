---
layout: archive
title: "Musings"
permalink: /musings/
author_profile: true
---

<!-- Lists every page with `musing: true` and a `date:` in its front matter, newest first,
     plus blog posts with `musing: true` (they stay in the blog too).
     An optional `description:` replaces the automatic excerpt. -->

Personal essays on life beyond travel: the big moments, and what I made of them.

{% assign musing_pages = site.pages | where: "musing", true %}
{% assign musing_posts = site.posts | where: "musing", true %}
{% comment %} Page and post dates have different types, so sort on "YYYYMMDD|kind|index" keys. {% endcomment %}
{% capture keys %}{% for m in musing_pages %}{{ m.date | date: "%Y%m%d" }}|page|{{ forloop.index0 }};{% endfor %}{% for m in musing_posts %}{{ m.date | date: "%Y%m%d" }}|post|{{ forloop.index0 }};{% endfor %}{% endcapture %}
{% assign keys = keys | split: ";" | sort | reverse %}
<ul class="dated-rows musings">
{% for key in keys %}
  {% assign k = key | split: "|" %}
  {% assign i = k[2] | plus: 0 %}
  {% if k[1] == "page" %}{% assign m = musing_pages[i] %}{% else %}{% assign m = musing_posts[i] %}{% endif %}
  <li>
    <time datetime="{{ m.date | date_to_xmlschema }}">{{ m.date | date: "%b %Y" }}</time>
    <div>
      <a class="musing-title" href="{{ m.url | relative_url }}">{{ m.title | strip }}</a>
      <p class="musing-excerpt">{% if m.description %}{{ m.description }}{% else %}{{ m.content | markdownify | split: "</p>" | first | strip_html | truncatewords: 40 }}{% endif %}</p>
    </div>
  </li>
{% endfor %}
</ul>
