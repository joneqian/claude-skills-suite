# Vue - Composition Api

**Pages:** 6

---

## Composition API: Lifecycle Hooks {#composition-api-lifecycle-hooks}

**URL:** llms-txt#composition-api:-lifecycle-hooks-{#composition-api-lifecycle-hooks}

**Contents:**
- onMounted() {#onmounted}
- onUpdated() {#onupdated}
- onUnmounted() {#onunmounted}
- onBeforeMount() {#onbeforemount}
- onBeforeUpdate() {#onbeforeupdate}
- onBeforeUnmount() {#onbeforeunmount}
- onErrorCaptured() {#onerrorcaptured}
- onRenderTracked() <sup class="vt-badge dev-only" /> {#onrendertracked}
- onRenderTriggered() <sup class="vt-badge dev-only" /> {#onrendertriggered}
- onActivated() {#onactivated}

:::info Usage Note
All APIs listed on this page must be called synchronously during the `setup()` phase of a component. See [Guide - Lifecycle Hooks](/guide/essentials/lifecycle) for more details.
:::

## onMounted() {#onmounted}

Registers a callback to be called after the component has been mounted.

A component is considered mounted after:

- All of its synchronous child components have been mounted (does not include async components or components inside `<Suspense>` trees).

- Its own DOM tree has been created and inserted into the parent container. Note it only guarantees that the component's DOM tree is in-document if the application's root container is also in-document.

This hook is typically used for performing side effects that need access to the component's rendered DOM, or for limiting DOM-related code to the client in a [server-rendered application](/guide/scaling-up/ssr).

**This hook is not called during server-side rendering.**

Accessing an element via template ref:

## onUpdated() {#onupdated}

Registers a callback to be called after the component has updated its DOM tree due to a reactive state change.

A parent component's updated hook is called after that of its child components.

This hook is called after any DOM update of the component, which can be caused by different state changes, because multiple state changes can be batched into a single render cycle for performance reasons. If you need to access the updated DOM after a specific state change, use [nextTick()](/api/general#nexttick) instead.

**This hook is not called during server-side rendering.**

:::warning
  Do not mutate component state in the updated hook - this will likely lead to an infinite update loop!
  :::

Accessing updated DOM:

## onUnmounted() {#onunmounted}

Registers a callback to be called after the component has been unmounted.

A component is considered unmounted after:

- All of its child components have been unmounted.

- All of its associated reactive effects (render effect and computed / watchers created during `setup()`) have been stopped.

Use this hook to clean up manually created side effects such as timers, DOM event listeners or server connections.

**This hook is not called during server-side rendering.**

## onBeforeMount() {#onbeforemount}

Registers a hook to be called right before the component is to be mounted.

When this hook is called, the component has finished setting up its reactive state, but no DOM nodes have been created yet. It is about to execute its DOM render effect for the first time.

**This hook is not called during server-side rendering.**

## onBeforeUpdate() {#onbeforeupdate}

Registers a hook to be called right before the component is about to update its DOM tree due to a reactive state change.

This hook can be used to access the DOM state before Vue updates the DOM. It is also safe to modify component state inside this hook.

**This hook is not called during server-side rendering.**

## onBeforeUnmount() {#onbeforeunmount}

Registers a hook to be called right before a component instance is to be unmounted.

When this hook is called, the component instance is still fully functional.

**This hook is not called during server-side rendering.**

## onErrorCaptured() {#onerrorcaptured}

Registers a hook to be called when an error propagating from a descendant component has been captured.

Errors can be captured from the following sources:

- Component renders
  - Event handlers
  - Lifecycle hooks
  - `setup()` function
  - Watchers
  - Custom directive hooks
  - Transition hooks

The hook receives three arguments: the error, the component instance that triggered the error, and an information string specifying the error source type.

:::tip
  In production, the 3rd argument (`info`) will be a shortened code instead of the full information string. You can find the code to string mapping in the [Production Error Code Reference](/error-reference/#runtime-errors).
  :::

You can modify component state in `onErrorCaptured()` to display an error state to the user. However, it is important that the error state should not render the original content that caused the error; otherwise the component will be thrown into an infinite render loop.

The hook can return `false` to stop the error from propagating further. See error propagation details below.

**Error Propagation Rules**

- By default, all errors are still sent to the application-level [`app.config.errorHandler`](/api/application#app-config-errorhandler) if it is defined, so that these errors can still be reported to an analytics service in a single place.

- If multiple `errorCaptured` hooks exist on a component's inheritance chain or parent chain, all of them will be invoked on the same error, in the order of bottom to top. This is similar to the bubbling mechanism of native DOM events.

- If the `errorCaptured` hook itself throws an error, both this error and the original captured error are sent to `app.config.errorHandler`.

- An `errorCaptured` hook can return `false` to prevent the error from propagating further. This is essentially saying "this error has been handled and should be ignored." It will prevent any additional `errorCaptured` hooks or `app.config.errorHandler` from being invoked for this error.

## onRenderTracked() <sup class="vt-badge dev-only" /> {#onrendertracked}

Registers a debug hook to be called when a reactive dependency has been tracked by the component's render effect.

**This hook is development-mode-only and not called during server-side rendering.**

- **See also** [Reactivity in Depth](/guide/extras/reactivity-in-depth)

## onRenderTriggered() <sup class="vt-badge dev-only" /> {#onrendertriggered}

Registers a debug hook to be called when a reactive dependency triggers the component's render effect to be re-run.

**This hook is development-mode-only and not called during server-side rendering.**

- **See also** [Reactivity in Depth](/guide/extras/reactivity-in-depth)

## onActivated() {#onactivated}

Registers a callback to be called after the component instance is inserted into the DOM as part of a tree cached by [`<KeepAlive>`](/api/built-in-components#keepalive).

**This hook is not called during server-side rendering.**

- **See also** [Guide - Lifecycle of Cached Instance](/guide/built-ins/keep-alive#lifecycle-of-cached-instance)

## onDeactivated() {#ondeactivated}

Registers a callback to be called after the component instance is removed from the DOM as part of a tree cached by [`<KeepAlive>`](/api/built-in-components#keepalive).

**This hook is not called during server-side rendering.**

- **See also** [Guide - Lifecycle of Cached Instance](/guide/built-ins/keep-alive#lifecycle-of-cached-instance)

## onServerPrefetch() <sup class="vt-badge" data-text="SSR only" /> {#onserverprefetch}

Registers an async function to be resolved before the component instance is to be rendered on the server.

If the callback returns a Promise, the server renderer will wait until the Promise is resolved before rendering the component.

This hook is only called during server-side rendering can be used to perform server-only data fetching.

- **See also** [Server-Side Rendering](/guide/scaling-up/ssr)

---
url: /api/composition-api-setup.md
---

**Examples:**

Example 1 (ts):
```ts
function onMounted(callback: () => void, target?: ComponentInternalInstance | null): void
```

Example 2 (vue):
```vue
<script setup>
  import { ref, onMounted } from 'vue'

  const el = ref()

  onMounted(() => {
    el.value // <div>
  })
  </script>

  <template>
    <div ref="el"></div>
  </template>
```

Example 3 (ts):
```ts
function onUpdated(callback: () => void, target?: ComponentInternalInstance | null): void
```

Example 4 (vue):
```vue
<script setup>
  import { ref, onUpdated } from 'vue'

  const count = ref(0)

  onUpdated(() => {
    // text content should be the same as current `count.value`
    console.log(document.getElementById('count').textContent)
  })
  </script>

  <template>
    <button id="count" @click="count++">{{ count }}</button>
  </template>
```

---

## Composition API: Helpers {#composition-api-helpers}

**URL:** llms-txt#composition-api:-helpers-{#composition-api-helpers}

**Contents:**
- useAttrs() {#useattrs}
- useSlots() {#useslots}
- useModel() {#usemodel}
- useTemplateRef() <sup class="vt-badge" data-text="3.5+" /> {#usetemplateref}
- useId() <sup class="vt-badge" data-text="3.5+" /> {#useid}

## useAttrs() {#useattrs}

Returns the `attrs` object from the [Setup Context](/api/composition-api-setup#setup-context), which includes the [fallthrough attributes](/guide/components/attrs#fallthrough-attributes) of the current component. This is intended to be used in `<script setup>` where the setup context object is not available.

## useSlots() {#useslots}

Returns the `slots` object from the [Setup Context](/api/composition-api-setup#setup-context), which includes parent passed slots as callable functions that return Virtual DOM nodes. This is intended to be used in `<script setup>` where the setup context object is not available.

If using TypeScript, [`defineSlots()`](/api/sfc-script-setup#defineslots) should be preferred instead.

## useModel() {#usemodel}

This is the underlying helper that powers [`defineModel()`](/api/sfc-script-setup#definemodel). If using `<script setup>`, `defineModel()` should be preferred instead.

- Only available in 3.4+

`useModel()` can be used in non-SFC components, e.g. when using raw `setup()` function. It expects the `props` object as the first argument, and the model name as the second argument. The optional third argument can be used to declare custom getter and setter for the resulting model ref. Note that unlike `defineModel()`, you are responsible for declaring the props and emits yourself.

## useTemplateRef() <sup class="vt-badge" data-text="3.5+" /> {#usetemplateref}

Returns a shallow ref whose value will be synced with the template element or component with a matching ref attribute.

- **See also**
  - [Guide - Template Refs](/guide/essentials/template-refs)
  - [Guide - Typing Template Refs](/guide/typescript/composition-api#typing-template-refs) <sup class="vt-badge ts" />
  - [Guide - Typing Component Template Refs](/guide/typescript/composition-api#typing-component-template-refs) <sup class="vt-badge ts" />

## useId() <sup class="vt-badge" data-text="3.5+" /> {#useid}

Used to generate unique-per-application IDs for accessibility attributes or form elements.

IDs generated by `useId()` are unique-per-application. It can be used to generate IDs for form elements and accessibility attributes. Multiple calls in the same component will generate different IDs; multiple instances of the same component calling `useId()` will also have different IDs.

IDs generated by `useId()` are also guaranteed to be stable across the server and client renders, so they can be used in SSR applications without leading to hydration mismatches.

If you have more than one Vue application instance of the same page, you can avoid ID conflicts by giving each app an ID prefix via [`app.config.idPrefix`](/api/application#app-config-idprefix).

:::warning Caution
  `useId()` should not be called inside a `computed()` property as it may cause instance conflicts. Instead, declare the ID outside of `computed()` and reference it within the computed function.
  :::

---
url: /api/composition-api-lifecycle.md
---

**Examples:**

Example 1 (ts):
```ts
function useAttrs(): Record<string, unknown>
```

Example 2 (ts):
```ts
function useSlots(): Record<string, (...args: any[]) => VNode[]>
```

Example 3 (ts):
```ts
function useModel(
    props: Record<string, any>,
    key: string,
    options?: DefineModelOptions
  ): ModelRef

  type DefineModelOptions<T = any> = {
    get?: (v: T) => any
    set?: (v: T) => any
  }

  type ModelRef<T, M extends PropertyKey = string, G = T, S = T> = Ref<G, S> & [
    ModelRef<T, M, G, S>,
    Record<M, true | undefined>
  ]
```

Example 4 (js):
```js
export default {
    props: ['count'],
    emits: ['update:count'],
    setup(props) {
      const msg = useModel(props, 'count')
      msg.value = 1
    }
  }
```

---

## Composition API: <br>Dependency Injection {#composition-api-dependency-injection}

**URL:** llms-txt#composition-api:-<br>dependency-injection-{#composition-api-dependency-injection}

**Contents:**
- provide() {#provide}
- inject() {#inject}
- hasInjectionContext() {#has-injection-context}

## provide() {#provide}

Provides a value that can be injected by descendant components.

`provide()` takes two arguments: the key, which can be a string or a symbol, and the value to be injected.

When using TypeScript, the key can be a symbol casted as `InjectionKey` - a Vue provided utility type that extends `Symbol`, which can be used to sync the value type between `provide()` and `inject()`.

Similar to lifecycle hook registration APIs, `provide()` must be called synchronously during a component's `setup()` phase.

- **See also**
  - [Guide - Provide / Inject](/guide/components/provide-inject)
  - [Guide - Typing Provide / Inject](/guide/typescript/composition-api#typing-provide-inject) <sup class="vt-badge ts" />

## inject() {#inject}

Injects a value provided by an ancestor component or the application (via `app.provide()`).

The first argument is the injection key. Vue will walk up the parent chain to locate a provided value with a matching key. If multiple components in the parent chain provide the same key, the one closest to the injecting component will "shadow" those higher up the chain and its value will be used. If no value with matching key was found, `inject()` returns `undefined` unless a default value is provided.

The second argument is optional and is the default value to be used when no matching value was found.

The second argument can also be a factory function that returns values that are expensive to create. In this case, `true` must be passed as the third argument to indicate that the function should be used as a factory instead of the value itself.

Similar to lifecycle hook registration APIs, `inject()` must be called synchronously during a component's `setup()` phase.

When using TypeScript, the key can be of type of `InjectionKey` - a Vue-provided utility type that extends `Symbol`, which can be used to sync the value type between `provide()` and `inject()`.

Assuming a parent component has provided values as shown in the previous `provide()` example:

- **See also**
  - [Guide - Provide / Inject](/guide/components/provide-inject)
  - [Guide - Typing Provide / Inject](/guide/typescript/composition-api#typing-provide-inject) <sup class="vt-badge ts" />

## hasInjectionContext() {#has-injection-context}

- Only supported in 3.3+

Returns true if [inject()](#inject) can be used without warning about being called in the wrong place (e.g. outside of `setup()`). This method is designed to be used by libraries that want to use `inject()` internally without triggering a warning to the end user.

---
url: /api/composition-api-helpers.md
---

**Examples:**

Example 1 (ts):
```ts
function provide<T>(key: InjectionKey<T> | string, value: T): void
```

Example 2 (vue):
```vue
<script setup>
  import { ref, provide } from 'vue'
  import { countSymbol } from './injectionSymbols'

  // provide static value
  provide('path', '/project/')

  // provide reactive value
  const count = ref(0)
  provide('count', count)

  // provide with Symbol keys
  provide(countSymbol, count)
  </script>
```

Example 3 (ts):
```ts
// without default value
  function inject<T>(key: InjectionKey<T> | string): T | undefined

  // with default value
  function inject<T>(key: InjectionKey<T> | string, defaultValue: T): T

  // with factory
  function inject<T>(
    key: InjectionKey<T> | string,
    defaultValue: () => T,
    treatDefaultAsFactory: true
  ): T
```

Example 4 (vue):
```vue
<script setup>
  import { inject } from 'vue'
  import { countSymbol } from './injectionSymbols'

  // inject static value without default
  const path = inject('path')

  // inject reactive value
  const count = inject('count')

  // inject with Symbol keys
  const count2 = inject(countSymbol)

  // inject with default value
  const bar = inject('path', '/default-path')

  // inject with function default value
  const fn = inject('function', () => {})

  // inject with default value factory
  const baz = inject('factory', () => new ExpensiveObject(), true)
  </script>
```

---

## Conditional Rendering {#conditional-rendering}

**URL:** llms-txt#conditional-rendering-{#conditional-rendering}

**Contents:**
- `v-if` {#v-if}
- `v-else` {#v-else}
- `v-else-if` {#v-else-if}
- `v-if` on `<template>` {#v-if-on-template}
- `v-show` {#v-show}
- `v-if` vs. `v-show` {#v-if-vs-v-show}
- `v-if` with `v-for` {#v-if-with-v-for}

<div class="options-api">
  <VueSchoolLink href="https://vueschool.io/lessons/conditional-rendering-in-vue-3" title="Free Vue.js Conditional Rendering Lesson"/>
</div>

<div class="composition-api">
  <VueSchoolLink href="https://vueschool.io/lessons/vue-fundamentals-capi-conditionals-in-vue" title="Free Vue.js Conditional Rendering Lesson"/>
</div>

<script setup>
import { ref } from 'vue'
const awesome = ref(true)
</script>

The directive `v-if` is used to conditionally render a block. The block will only be rendered if the directive's expression returns a truthy value.

## `v-else` {#v-else}

You can use the `v-else` directive to indicate an "else block" for `v-if`:

<div class="demo">
  <button @click="awesome = !awesome">Toggle</button>
  <h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>
</div>

<div class="composition-api">

[Try it in the Playground](https://play.vuejs.org/#eNpFjkEOgjAQRa8ydIMulLA1hegJ3LnqBskAjdA27RQXhHu4M/GEHsEiKLv5mfdf/sBOxux7j+zAuCutNAQOyZtcKNkZbQkGsFjBCJXVHcQBjYUSqtTKERR3dLpDyCZmQ9bjViiezKKgCIGwM21BGBIAv3oireBYtrK8ZYKtgmg5BctJ13WLPJnhr0YQb1Lod7JaS4G8eATpfjMinjTphC8wtg7zcwNKw/v5eC1fnvwnsfEDwaha7w==)

</div>
<div class="options-api">

[Try it in the Playground](https://play.vuejs.org/#eNpFjj0OwjAMha9iMsEAFWuVVnACNqYsoXV/RJpEqVOQqt6DDYkTcgRSWoplWX7y56fXs6O1u84jixlvM1dbSoXGuzWOIMdCekXQCw2QS5LrzbQLckje6VEJglDyhq1pMAZyHidkGG9hhObRYh0EYWOVJAwKgF88kdFwyFSdXRPBZidIYDWvgqVkylIhjyb4ayOIV3votnXxfwrk2SPU7S/PikfVfsRnGFWL6akCbeD9fLzmK4+WSGz4AA5dYQY=)

A `v-else` element must immediately follow a `v-if` or a `v-else-if` element - otherwise it will not be recognized.

## `v-else-if` {#v-else-if}

The `v-else-if`, as the name suggests, serves as an "else if block" for `v-if`. It can also be chained multiple times:

Similar to `v-else`, a `v-else-if` element must immediately follow a `v-if` or a `v-else-if` element.

## `v-if` on `<template>` {#v-if-on-template}

Because `v-if` is a directive, it has to be attached to a single element. But what if we want to toggle more than one element? In this case we can use `v-if` on a `<template>` element, which serves as an invisible wrapper. The final rendered result will not include the `<template>` element.

`v-else` and `v-else-if` can also be used on `<template>`.

## `v-show` {#v-show}

Another option for conditionally displaying an element is the `v-show` directive. The usage is largely the same:

The difference is that an element with `v-show` will always be rendered and remain in the DOM; `v-show` only toggles the `display` CSS property of the element.

`v-show` doesn't support the `<template>` element, nor does it work with `v-else`.

## `v-if` vs. `v-show` {#v-if-vs-v-show}

`v-if` is "real" conditional rendering because it ensures that event listeners and child components inside the conditional block are properly destroyed and re-created during toggles.

`v-if` is also **lazy**: if the condition is false on initial render, it will not do anything - the conditional block won't be rendered until the condition becomes true for the first time.

In comparison, `v-show` is much simpler - the element is always rendered regardless of initial condition, with CSS-based toggling.

Generally speaking, `v-if` has higher toggle costs while `v-show` has higher initial render costs. So prefer `v-show` if you need to toggle something very often, and prefer `v-if` if the condition is unlikely to change at runtime.

## `v-if` with `v-for` {#v-if-with-v-for}

When `v-if` and `v-for` are both used on the same element, `v-if` will be evaluated first. See the [list rendering guide](list#v-for-with-v-if) for details.

::: warning Note
It's **not** recommended to use `v-if` and `v-for` on the same element due to implicit precedence. Refer to [list rendering guide](list#v-for-with-v-if) for details.
:::

---
url: /guide/essentials/application.md
---

**Examples:**

Example 1 (unknown):
```unknown
## `v-else` {#v-else}

You can use the `v-else` directive to indicate an "else block" for `v-if`:
```

Example 2 (unknown):
```unknown
<div class="demo">
  <button @click="awesome = !awesome">Toggle</button>
  <h1 v-if="awesome">Vue is awesome!</h1>
  <h1 v-else>Oh no 😢</h1>
</div>

<div class="composition-api">

[Try it in the Playground](https://play.vuejs.org/#eNpFjkEOgjAQRa8ydIMulLA1hegJ3LnqBskAjdA27RQXhHu4M/GEHsEiKLv5mfdf/sBOxux7j+zAuCutNAQOyZtcKNkZbQkGsFjBCJXVHcQBjYUSqtTKERR3dLpDyCZmQ9bjViiezKKgCIGwM21BGBIAv3oireBYtrK8ZYKtgmg5BctJ13WLPJnhr0YQb1Lod7JaS4G8eATpfjMinjTphC8wtg7zcwNKw/v5eC1fnvwnsfEDwaha7w==)

</div>
<div class="options-api">

[Try it in the Playground](https://play.vuejs.org/#eNpFjj0OwjAMha9iMsEAFWuVVnACNqYsoXV/RJpEqVOQqt6DDYkTcgRSWoplWX7y56fXs6O1u84jixlvM1dbSoXGuzWOIMdCekXQCw2QS5LrzbQLckje6VEJglDyhq1pMAZyHidkGG9hhObRYh0EYWOVJAwKgF88kdFwyFSdXRPBZidIYDWvgqVkylIhjyb4ayOIV3votnXxfwrk2SPU7S/PikfVfsRnGFWL6akCbeD9fLzmK4+WSGz4AA5dYQY=)

</div>

A `v-else` element must immediately follow a `v-if` or a `v-else-if` element - otherwise it will not be recognized.

## `v-else-if` {#v-else-if}

The `v-else-if`, as the name suggests, serves as an "else if block" for `v-if`. It can also be chained multiple times:
```

Example 3 (unknown):
```unknown
Similar to `v-else`, a `v-else-if` element must immediately follow a `v-if` or a `v-else-if` element.

## `v-if` on `<template>` {#v-if-on-template}

Because `v-if` is a directive, it has to be attached to a single element. But what if we want to toggle more than one element? In this case we can use `v-if` on a `<template>` element, which serves as an invisible wrapper. The final rendered result will not include the `<template>` element.
```

Example 4 (unknown):
```unknown
`v-else` and `v-else-if` can also be used on `<template>`.

## `v-show` {#v-show}

Another option for conditionally displaying an element is the `v-show` directive. The usage is largely the same:
```

---

## Options: Composition {#options-composition}

**URL:** llms-txt#options:-composition-{#options-composition}

**Contents:**
- provide {#provide}
- inject {#inject}
- mixins {#mixins}
- extends {#extends}

## provide {#provide}

Provide values that can be injected by descendant components.

`provide` and [`inject`](#inject) are used together to allow an ancestor component to serve as a dependency injector for all its descendants, regardless of how deep the component hierarchy is, as long as they are in the same parent chain.

The `provide` option should be either an object or a function that returns an object. This object contains the properties that are available for injection into its descendants. You can use Symbols as keys in this object.

Using a function to provide per-component state:

Note in the above example, the provided `msg` will NOT be reactive. See [Working with Reactivity](/guide/components/provide-inject#working-with-reactivity) for more details.

- **See also** [Provide / Inject](/guide/components/provide-inject)

Declare properties to inject into the current component by locating them from ancestor providers.

The `inject` option should be either:

- An array of strings, or
  - An object where the keys are the local binding name and the value is either:
    - The key (string or Symbol) to search for in available injections, or
    - An object where:
      - The `from` property is the key (string or Symbol) to search for in available injections, and
      - The `default` property is used as fallback value. Similar to props default values, a factory function is needed for object types to avoid value sharing between multiple component instances.

An injected property will be `undefined` if neither a matching property nor a default value was provided.

Note that injected bindings are NOT reactive. This is intentional. However, if the injected value is a reactive object, properties on that object do remain reactive. See [Working with Reactivity](/guide/components/provide-inject#working-with-reactivity) for more details.

Using an injected value as the default for a prop:

Using an injected value as data entry:

Injections can be optional with default value:

If it needs to be injected from a property with a different name, use `from` to denote the source property:

Similar to prop defaults, you need to use a factory function for non-primitive values:

- **See also** [Provide / Inject](/guide/components/provide-inject)

An array of option objects to be mixed into the current component.

The `mixins` option accepts an array of mixin objects. These mixin objects can contain instance options like normal instance objects, and they will be merged against the eventual options using the certain option merging logic. For example, if your mixin contains a `created` hook and the component itself also has one, both functions will be called.

Mixin hooks are called in the order they are provided, and called before the component's own hooks.

:::warning No Longer Recommended
  In Vue 2, mixins were the primary mechanism for creating reusable chunks of component logic. While mixins continue to be supported in Vue 3, [Composable functions using Composition API](/guide/reusability/composables) is now the preferred approach for code reuse between components.
  :::

## extends {#extends}

A "base class" component to extend from.

Allows one component to extend another, inheriting its component options.

From an implementation perspective, `extends` is almost identical to `mixins`. The component specified by `extends` will be treated as though it were the first mixin.

However, `extends` and `mixins` express different intents. The `mixins` option is primarily used to compose chunks of functionality, whereas `extends` is primarily concerned with inheritance.

As with `mixins`, any options (except for `setup()`) will be merged using the relevant merge strategy.

:::warning Not Recommended for Composition API
  `extends` is designed for Options API and does not handle the merging of the `setup()` hook.

In Composition API, the preferred mental model for logic reuse is "compose" over "inheritance". If you have logic from a component that needs to be reused in another one, consider extracting the relevant logic into a [Composable](/guide/reusability/composables#composables).

If you still intend to "extend" a component using Composition API, you can call the base component's `setup()` in the extending component's `setup()`:

---
url: /api/options-lifecycle.md
---

**Examples:**

Example 1 (ts):
```ts
interface ComponentOptions {
    provide?: object | ((this: ComponentPublicInstance) => object)
  }
```

Example 2 (js):
```js
const s = Symbol()

  export default {
    provide: {
      foo: 'foo',
      [s]: 'bar'
    }
  }
```

Example 3 (js):
```js
export default {
    data() {
      return {
        msg: 'foo'
      }
    }
    provide() {
      return {
        msg: this.msg
      }
    }
  }
```

Example 4 (ts):
```ts
interface ComponentOptions {
    inject?: ArrayInjectOptions | ObjectInjectOptions
  }

  type ArrayInjectOptions = string[]

  type ObjectInjectOptions = {
    [key: string | symbol]:
      | string
      | symbol
      | { from?: string | symbol; default?: any }
  }
```

---

## Composition API FAQ {#composition-api-faq}

**URL:** llms-txt#composition-api-faq-{#composition-api-faq}

**Contents:**
- What is Composition API? {#what-is-composition-api}
- Why Composition API? {#why-composition-api}
  - Better Logic Reuse {#better-logic-reuse}
  - More Flexible Code Organization {#more-flexible-code-organization}
  - Better Type Inference {#better-type-inference}
  - Smaller Production Bundle and Less Overhead {#smaller-production-bundle-and-less-overhead}
- Relationship with Options API {#relationship-with-options-api}
  - Trade-offs {#trade-offs}
  - Does Composition API cover all use cases? {#does-composition-api-cover-all-use-cases}
  - Can I use both APIs in the same component? {#can-i-use-both-apis-in-the-same-component}

:::tip
This FAQ assumes prior experience with Vue - in particular, experience with Vue 2 while primarily using Options API.
:::

## What is Composition API? {#what-is-composition-api}

<VueSchoolLink href="https://vueschool.io/lessons/introduction-to-the-vue-js-3-composition-api" title="Free Composition API Lesson"/>

Composition API is a set of APIs that allows us to author Vue components using imported functions instead of declaring options. It is an umbrella term that covers the following APIs:

- [Reactivity API](/api/reactivity-core), e.g. `ref()` and `reactive()`, that allows us to directly create reactive state, computed state, and watchers.

- [Lifecycle Hooks](/api/composition-api-lifecycle), e.g. `onMounted()` and `onUnmounted()`, that allow us to programmatically hook into the component lifecycle.

- [Dependency Injection](/api/composition-api-dependency-injection), i.e. `provide()` and `inject()`, that allow us to leverage Vue's dependency injection system while using Reactivity APIs.

Composition API is a built-in feature of Vue 3 and [Vue 2.7](https://blog.vuejs.org/posts/vue-2-7-naruto.html). For older Vue 2 versions, use the officially maintained [`@vue/composition-api`](https://github.com/vuejs/composition-api) plugin. In Vue 3, it is also primarily used together with the [`<script setup>`](/api/sfc-script-setup) syntax in Single-File Components. Here's a basic example of a component using Composition API:

Despite an API style based on function composition, **Composition API is NOT functional programming**. Composition API is based on Vue's mutable, fine-grained reactivity paradigm, whereas functional programming emphasizes immutability.

If you are interested in learning how to use Vue with Composition API, you can set the site-wide API preference to Composition API using the toggle at the top of the left sidebar, and then go through the guide from the beginning.

## Why Composition API? {#why-composition-api}

### Better Logic Reuse {#better-logic-reuse}

The primary advantage of Composition API is that it enables clean, efficient logic reuse in the form of [Composable functions](/guide/reusability/composables). It solves [all the drawbacks of mixins](/guide/reusability/composables#vs-mixins), the primary logic reuse mechanism for Options API.

Composition API's logic reuse capability has given rise to impressive community projects such as [VueUse](https://vueuse.org/), an ever-growing collection of composable utilities. It also serves as a clean mechanism for easily integrating stateful third-party services or libraries into Vue's reactivity system, for example [immutable data](/guide/extras/reactivity-in-depth#immutable-data), [state machines](/guide/extras/reactivity-in-depth#state-machines), and [RxJS](/guide/extras/reactivity-in-depth#rxjs).

### More Flexible Code Organization {#more-flexible-code-organization}

Many users love that we write organized code by default with Options API: everything has its place based on the option it falls under. However, Options API poses serious limitations when a single component's logic grows beyond a certain complexity threshold. This limitation is particularly prominent in components that need to deal with multiple **logical concerns**, which we have witnessed first hand in many production Vue 2 apps.

Take the folder explorer component from Vue CLI's GUI as an example: this component is responsible for the following logical concerns:

- Tracking current folder state and displaying its content
- Handling folder navigation (opening, closing, refreshing...)
- Handling new folder creation
- Toggling show favorite folders only
- Toggling show hidden folders
- Handling current working directory changes

The [original version](https://github.com/vuejs/vue-cli/blob/a09407dd5b9f18ace7501ddb603b95e31d6d93c0/packages/@vue/cli-ui/src/components/folder/FolderExplorer.vue#L198-L404) of the component was written in Options API. If we give each line of code a color based on the logical concern it is dealing with, this is how it looks:

<img alt="folder component before" src="./images/options-api.png" width="129" height="500" style="margin: 1.2em auto">

Notice how code dealing with the same logical concern is forced to be split under different options, located in different parts of the file. In a component that is several hundred lines long, understanding and navigating a single logical concern requires constantly scrolling up and down the file, making it much more difficult than it should be. In addition, if we ever intend to extract a logical concern into a reusable utility, it takes quite a bit of work to find and extract the right pieces of code from different parts of the file.

Here's the same component, before and after the [refactor into Composition API](https://gist.github.com/yyx990803/8854f8f6a97631576c14b63c8acd8f2e):

![folder component after](./images/composition-api-after.png)

Notice how the code related to the same logical concern can now be grouped together: we no longer need to jump between different options blocks while working on a specific logical concern. Moreover, we can now move a group of code into an external file with minimal effort, since we no longer need to shuffle the code around in order to extract them. This reduced friction for refactoring is key to the long-term maintainability in large codebases.

### Better Type Inference {#better-type-inference}

In recent years, more and more frontend developers are adopting [TypeScript](https://www.typescriptlang.org/) as it helps us write more robust code, make changes with more confidence, and provides a great development experience with IDE support. However, the Options API, originally conceived in 2013, was designed without type inference in mind. We had to implement some [absurdly complex type gymnastics](https://github.com/vuejs/core/blob/44b95276f5c086e1d88fa3c686a5f39eb5bb7821/packages/runtime-core/src/componentPublicInstance.ts#L132-L165) to make type inference work with the Options API. Even with all this effort, type inference for Options API can still break down for mixins and dependency injection.

This had led many developers who wanted to use Vue with TS to lean towards Class API powered by `vue-class-component`. However, a class-based API heavily relies on ES decorators, a language feature that was only a stage 2 proposal when Vue 3 was being developed in 2019. We felt it was too risky to base an official API on an unstable proposal. Since then, the decorators proposal has gone through yet another complete overhaul, and finally reached stage 3 in 2022. In addition, class-based API suffers from logic reuse and organization limitations similar to Options API.

In comparison, Composition API utilizes mostly plain variables and functions, which are naturally type friendly. Code written in Composition API can enjoy full type inference with little need for manual type hints. Most of the time, Composition API code will look largely identical in TypeScript and plain JavaScript. This also makes it possible for plain JavaScript users to benefit from partial type inference.

### Smaller Production Bundle and Less Overhead {#smaller-production-bundle-and-less-overhead}

Code written in Composition API and `<script setup>` is also more efficient and minification-friendly than Options API equivalent. This is because the template in a `<script setup>` component is compiled as a function inlined in the same scope of the `<script setup>` code. Unlike property access from `this`, the compiled template code can directly access variables declared inside `<script setup>`, without an instance proxy in between. This also leads to better minification because all the variable names can be safely shortened.

## Relationship with Options API {#relationship-with-options-api}

### Trade-offs {#trade-offs}

Some users moving from Options API found their Composition API code less organized, and concluded that Composition API is "worse" in terms of code organization. We recommend users with such opinions to look at that problem from a different perspective.

It is true that Composition API no longer provides the "guard rails" that guide you to put your code into respective buckets. In return, you get to author component code like how you would write normal JavaScript. This means **you can and should apply any code organization best practices to your Composition API code as you would when writing normal JavaScript**. If you can write well-organized JavaScript, you should also be able to write well-organized Composition API code.

Options API does allow you to "think less" when writing component code, which is why many users love it. However, in reducing the mental overhead, it also locks you into the prescribed code organization pattern with no escape hatch, which can make it difficult to refactor or improve code quality in larger scale projects. In this regard, Composition API provides better long term scalability.

### Does Composition API cover all use cases? {#does-composition-api-cover-all-use-cases}

Yes in terms of stateful logic. When using Composition API, there are only a few options that may still be needed: `props`, `emits`, `name`, and `inheritAttrs`.

Since 3.3 you can directly use `defineOptions` in `<script setup>` to set the component name or `inheritAttrs` property

If you intend to exclusively use Composition API (along with the options listed above), you can shave a few kbs off your production bundle via a [compile-time flag](/api/compile-time-flags) that drops Options API related code from Vue. Note this also affects Vue components in your dependencies.

### Can I use both APIs in the same component? {#can-i-use-both-apis-in-the-same-component}

Yes. You can use Composition API via the [`setup()`](/api/composition-api-setup) option in an Options API component.

However, we only recommend doing so if you have an existing Options API codebase that needs to integrate with new features / external libraries written with Composition API.

### Will Options API be deprecated? {#will-options-api-be-deprecated}

No, we do not have any plan to do so. Options API is an integral part of Vue and the reason many developers love it. We also realize that many of the benefits of Composition API only manifest in larger-scale projects, and Options API remains a solid choice for many low-to-medium-complexity scenarios.

## Relationship with Class API {#relationship-with-class-api}

We no longer recommend using Class API with Vue 3, given that Composition API provides great TypeScript integration with additional logic reuse and code organization benefits.

## Comparison with React Hooks {#comparison-with-react-hooks}

Composition API provides the same level of logic composition capabilities as React Hooks, but with some important differences.

React Hooks are invoked repeatedly every time a component updates. This creates a number of caveats that can confuse even seasoned React developers. It also leads to performance optimization issues that can severely affect development experience. Here are some examples:

- Hooks are call-order sensitive and cannot be conditional.

- Variables declared in a React component can be captured by a hook closure and become "stale" if the developer fails to pass in the correct dependencies array. This leads to React developers relying on ESLint rules to ensure correct dependencies are passed. However, the rule is often not smart enough and over-compensates for correctness, which leads to unnecessary invalidation and headaches when edge cases are encountered.

- Expensive computations require the use of `useMemo`, which again requires manually passing in the correct dependencies array.

- Event handlers passed to child components cause unnecessary child updates by default, and require explicit `useCallback` as an optimization. This is almost always needed, and again requires a correct dependencies array. Neglecting this leads to over-rendering apps by default and can cause performance issues without realizing it.

- The stale closure problem, combined with Concurrent features, makes it difficult to reason about when a piece of hooks code is run, and makes working with mutable state that should persist across renders (via `useRef`) cumbersome.

> Note: some of the above issues that are related to memoization can be resolved by the upcoming [React Compiler](https://react.dev/learn/react-compiler).

In comparison, Vue Composition API:

- Invokes `setup()` or `<script setup>` code only once. This makes the code align better with the intuitions of idiomatic JavaScript usage as there are no stale closures to worry about. Composition API calls are also not sensitive to call order and can be conditional.

- Vue's runtime reactivity system automatically collects reactive dependencies used in computed properties and watchers, so there's no need to manually declare dependencies.

- No need to manually cache callback functions to avoid unnecessary child updates. In general, Vue's fine-grained reactivity system ensures child components only update when they need to. Manual child-update optimizations are rarely a concern for Vue developers.

We acknowledge the creativity of React Hooks, and it is a major source of inspiration for Composition API. However, the issues mentioned above do exist in its design and we noticed Vue's reactivity model happens to provide a way around them.

---
url: /api/composition-api-dependency-injection.md
---

**Examples:**

Example 1 (vue):
```vue
<script setup>
import { ref, onMounted } from 'vue'

// reactive state
const count = ref(0)

// functions that mutate state and trigger updates
function increment() {
  count.value++
}

// lifecycle hooks
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>

<template>
  <button @click="increment">Count is: {{ count }}</button>
</template>
```

---
