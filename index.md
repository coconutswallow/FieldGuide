---
layout: default
title: Monster Compendium
---

# D&D Monster Compendium

Welcome to the monster compendium! Browse through our collection of creatures organized by type.

{% assign monsters_by_category = site.monsters | where_exp:"item", "item.category != null" | group_by: 'category' | sort: 'name' %}

{% for category in monsters_by_category %}
## {{ category.name }}

{% raw %}
<div class="monster-list">
{% endraw %}

{% assign sorted = category.items | sort: 'title' %}
{% for monster in sorted %}
{% raw %}
  <div class="monster-card">
{% endraw %}
    <h3><a href="{{ monster.url | relative_url }}">{{ monster.title }}</a></h3>
    {% if monster.cr %}
    <p class="monster-cr">CR {{ monster.cr }}</p>
    {% endif %}
    {% if monster.type %}
    <p class="monster-type">{{ monster.type }}</p>
    {% endif %}
{% raw %}
  </div>
{% endraw %}
{% endfor %}
{% raw %}
</div>
{% endraw %}
{% endfor %}
