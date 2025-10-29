---
layout: default
title: Monster Compendium
---

# D&D Monster Compendium

Welcome to the monster compendium! Browse through our collection of creatures organized by type.

{% assign all_monsters = site.monsters | where_exp:"item", "item.category != null" %}
{% assign monsters_by_category = all_monsters | group_by: 'category' | sort: 'name' %}


{% for category in monsters_by_category %}
## {{ category.name }}

<div class="monster-list">
{% assign sorted = category.items | sort: 'title' %}
{% for monster in sorted %}
  <div class="monster-card">
    <h3><a href="{{ monster.url | relative_url }}">{{ monster.title }}</a></h3>
    {% if monster.cr %}
    <p class="monster-cr">CR {{ monster.cr }}</p>
    {% endif %}
    {% if monster.type %}
    <p class="monster-type">{{ monster.type }}</p>
    {% endif %}
  </div>
{% endfor %}
</div>
{% endfor %}