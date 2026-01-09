---
name: vue-development-skill
description: Vue.js progressive JavaScript framework. Use for Vue components, reactivity, composition API, and frontend development.
---

# Vue Development Skill

Vue.js progressive javascript framework. use for vue components, reactivity, composition api, and frontend development., generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

- Working with vue
- Asking about vue features or APIs
- Implementing vue solutions
- Debugging vue code
- Learning vue best practices

## Quick Reference

### Common Patterns

_Quick reference patterns will be added as you use the skill._

### Example Code Patterns

**Example 1** (js):

```js
import { createApp } from 'vue';

createApp({
  data() {
    return {
      count: 0,
    };
  },
}).mount('#app');
```

**Example 2** (js):

```js
import { createApp, ref } from 'vue';

createApp({
  setup() {
    return {
      count: ref(0),
    };
  },
}).mount('#app');
```

**Example 3** (js):

```js
// Only works if using in-browser compilation.
// If using build tools, see config examples below.
app.config.compilerOptions.isCustomElement = (tag) => tag.includes('-');
```

**Example 4** (js):

```js
import { defineAsyncComponent } from 'vue';

const AsyncComp = defineAsyncComponent(() =>
  import('./components/MyComponent.vue')
);
```

**Example 5** (vue):

```vue
<script setup>
let count = $ref(0);

console.log(count);

function increment() {
  count++;
}
</script>

<template>
  <button @click="increment">{{ count }}</button>
</template>
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Api documentation
- **components.md** - Components documentation
- **composition_api.md** - Composition Api documentation
- **getting_started.md** - Getting Started documentation
- **other.md** - Other documentation
- **reactivity.md** - Reactivity documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features

Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples

The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/

Organized documentation extracted from official sources. These files contain:

- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/

Add helper scripts here for common automation tasks.

### assets/

Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:

1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
