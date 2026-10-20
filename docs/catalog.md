---
title: Search & Filter – Open Source Ai catalog
description: Filter open-source AI agent and LLM projects by task, deployment, hardware, licence state and activity.
---
# Search & Filter

Filter by your constraints. Results are not ranked recommendations; they are listed alphabetically. Status and last commit come from the [weekly evidence refresh](freshness.md).

<form id="osa-filters" class="osa-filters" role="search" aria-label="Catalog filters" onsubmit="return false">
  <label for="f-q">Search projects</label>
  <input id="f-q" type="search" placeholder="name or description">
  <label for="f-category">Category</label>
  <select id="f-category"><option value="">Any</option></select>
  <label for="f-task">Task</label>
  <select id="f-task"><option value="">Any</option></select>
  <label for="f-deployment">Deployment</label>
  <select id="f-deployment"><option value="">Any</option></select>
  <label for="f-hardware">Hardware</label>
  <select id="f-hardware"><option value="">Any</option></select>
  <label for="f-license">Licence state</label>
  <select id="f-license"><option value="">Any</option></select>
  <label for="f-status">Activity</label>
  <select id="f-status"><option value="">Any</option><option value="recent">Commit in last 90 days</option><option value="active">Not archived</option><option value="archived">Archived</option></select>
  <button type="button" id="f-clear" class="md-button">Clear filters</button>
</form>

<p id="osa-count" role="status" aria-live="polite"></p>
<p id="osa-empty" hidden>No projects match these filters. Try removing a filter or <a href="#" id="f-clear-link">clear all filters</a>.</p>

<div class="osa-table-wrap">
<table id="osa-results">
<caption>Matching projects</caption>
<thead><tr><th scope="col">Project</th><th scope="col">What it does</th><th scope="col">Deployment</th><th scope="col">Hardware</th><th scope="col">Licence</th><th scope="col">Status</th><th scope="col">Last commit</th></tr></thead>
<tbody></tbody>
</table>
</div>
<noscript>JavaScript is needed for filtering. Browse the category pages from the navigation instead.</noscript>
