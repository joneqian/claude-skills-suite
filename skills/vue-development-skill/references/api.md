# Vue - Api

**Pages:** 4

---

## Server-Side Rendering API {#server-side-rendering-api}

**URL:** llms-txt#server-side-rendering-api-{#server-side-rendering-api}

**Contents:**
- renderToString() {#rendertostring}
- renderToNodeStream() {#rendertonodestream}
- pipeToNodeWritable() {#pipetonodewritable}
- renderToWebStream() {#rendertowebstream}
- pipeToWebWritable() {#pipetowebwritable}
- renderToSimpleStream() {#rendertosimplestream}
- useSSRContext() {#usessrcontext}
- data-allow-mismatch <sup class="vt-badge" data-text="3.5+" /> {#data-allow-mismatch}

## renderToString() {#rendertostring}

- **Exported from `vue/server-renderer`**

### SSR Context {#ssr-context}

You can pass an optional context object, which can be used to record additional data during the render, for example [accessing content of Teleports](/guide/scaling-up/ssr#teleports):

Most other SSR APIs on this page also optionally accept a context object. The context object can be accessed in component code via the [useSSRContext](#usessrcontext) helper.

- **See also** [Guide - Server-Side Rendering](/guide/scaling-up/ssr)

## renderToNodeStream() {#rendertonodestream}

Renders input as a [Node.js Readable stream](https://nodejs.org/api/stream.html#stream_class_stream_readable).

- **Exported from `vue/server-renderer`**

:::tip Note
  This method is not supported in the ESM build of `vue/server-renderer`, which is decoupled from Node.js environments. Use [`pipeToNodeWritable`](#pipetonodewritable) instead.
  :::

## pipeToNodeWritable() {#pipetonodewritable}

Render and pipe to an existing [Node.js Writable stream](https://nodejs.org/api/stream.html#stream_writable_streams) instance.

- **Exported from `vue/server-renderer`**

## renderToWebStream() {#rendertowebstream}

Renders input as a [Web ReadableStream](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API).

- **Exported from `vue/server-renderer`**

:::tip Note
  In environments that do not expose `ReadableStream` constructor in the global scope, [`pipeToWebWritable()`](#pipetowebwritable) should be used instead.
  :::

## pipeToWebWritable() {#pipetowebwritable}

Render and pipe to an existing [Web WritableStream](https://developer.mozilla.org/en-US/docs/Web/API/WritableStream) instance.

- **Exported from `vue/server-renderer`**

This is typically used in combination with [`TransformStream`](https://developer.mozilla.org/en-US/docs/Web/API/TransformStream):

## renderToSimpleStream() {#rendertosimplestream}

Renders input in streaming mode using a simple readable interface.

- **Exported from `vue/server-renderer`**

## useSSRContext() {#usessrcontext}

A runtime API used to retrieve the context object passed to `renderToString()` or other server render APIs.

The retrieved context can be used to attach information that is needed for rendering the final HTML (e.g. head metadata).

## data-allow-mismatch <sup class="vt-badge" data-text="3.5+" /> {#data-allow-mismatch}

A special attribute that can be used to suppress [hydration mismatch](/guide/scaling-up/ssr#hydration-mismatch) warnings.

The value can limit the allowed mismatch to a specific type. Allowed values are:

- `text`
  - `children` (only allows mismatch for direct children)
  - `class`
  - `style`
  - `attribute`

If no value is provided, all types of mismatches will be allowed.

---
url: /api/sfc-css-features.md
---

**Examples:**

Example 1 (ts):
```ts
function renderToString(
    input: App | VNode,
    context?: SSRContext
  ): Promise<string>
```

Example 2 (js):
```js
import { createSSRApp } from 'vue'
  import { renderToString } from 'vue/server-renderer'

  const app = createSSRApp({
    data: () => ({ msg: 'hello' }),
    template: `<div>{{ msg }}</div>`
  })

  ;(async () => {
    const html = await renderToString(app)
    console.log(html)
  })()
```

Example 3 (js):
```js
const ctx = {}
  const html = await renderToString(app, ctx)

  console.log(ctx.teleports) // { '#teleported': 'teleported content' }
```

Example 4 (ts):
```ts
function renderToNodeStream(
    input: App | VNode,
    context?: SSRContext
  ): Readable
```

---

## Global API: General {#global-api-general}

**URL:** llms-txt#global-api:-general-{#global-api-general}

**Contents:**
- version {#version}
- nextTick() {#nexttick}
- defineComponent() {#definecomponent}
- defineAsyncComponent() {#defineasynccomponent}

## version {#version}

Exposes the current version of Vue.

## nextTick() {#nexttick}

A utility for waiting for the next DOM update flush.

When you mutate reactive state in Vue, the resulting DOM updates are not applied synchronously. Instead, Vue buffers them until the "next tick" to ensure that each component updates only once no matter how many state changes you have made.

`nextTick()` can be used immediately after a state change to wait for the DOM updates to complete. You can either pass a callback as an argument, or await the returned Promise.

<div class="composition-api">

</div>
  <div class="options-api">

- **See also** [`this.$nextTick()`](/api/component-instance#nexttick)

## defineComponent() {#definecomponent}

A type helper for defining a Vue component with type inference.

> Type is simplified for readability.

The first argument expects a component options object. The return value will be the same options object, since the function is essentially a runtime no-op for type inference purposes only.

Note that the return type is a bit special: it will be a constructor type whose instance type is the inferred component instance type based on the options. This is used for type inference when the returned type is used as a tag in TSX.

You can extract the instance type of a component (equivalent to the type of `this` in its options) from the return type of `defineComponent()` like this:

### Function Signature {#function-signature}

- Only supported in 3.3+

`defineComponent()` also has an alternative signature that is meant to be used with the Composition API and [render functions or JSX](/guide/extras/render-function.html).

Instead of passing in an options object, a function is expected instead. This function works the same as the Composition API [`setup()`](/api/composition-api-setup.html#composition-api-setup) function: it receives the props and the setup context. The return value should be a render function - both `h()` and JSX are supported:

The main use case for this signature is with TypeScript (and in particular with TSX), as it supports generics:

In the future, we plan to provide a Babel plugin that automatically infers and injects the runtime props (like for `defineProps` in SFCs) so that the runtime props declaration can be omitted.

### Note on webpack Treeshaking {#note-on-webpack-treeshaking}

Because `defineComponent()` is a function call, it could look like it would produce side-effects to some build tools, e.g. webpack. This will prevent the component from being tree-shaken even when the component is never used.

To tell webpack that this function call is safe to be tree-shaken, you can add a `/*#__PURE__*/` comment notation before the function call:

Note this is not necessary if you are using Vite, because Rollup (the underlying production bundler used by Vite) is smart enough to determine that `defineComponent()` is in fact side-effect-free without the need for manual annotations.

- **See also** [Guide - Using Vue with TypeScript](/guide/typescript/overview#general-usage-notes)

## defineAsyncComponent() {#defineasynccomponent}

Define an async component which is lazy loaded only when it is rendered. The argument can either be a loader function, or an options object for more advanced control of the loading behavior.

- **See also** [Guide - Async Components](/guide/components/async)

---
url: /glossary/index.md
---

**Examples:**

Example 1 (js):
```js
import { version } from 'vue'

  console.log(version)
```

Example 2 (ts):
```ts
function nextTick(callback?: () => void): Promise<void>
```

Example 3 (vue):
```vue
<script setup>
  import { ref, nextTick } from 'vue'

  const count = ref(0)

  async function increment() {
    count.value++

    // DOM not yet updated
    console.log(document.getElementById('counter').textContent) // 0

    await nextTick()
    // DOM is now updated
    console.log(document.getElementById('counter').textContent) // 1
  }
  </script>

  <template>
    <button id="counter" @click="increment">{{ count }}</button>
  </template>
```

Example 4 (vue):
```vue
<script>
  import { nextTick } from 'vue'

  export default {
    data() {
      return {
        count: 0
      }
    },
    methods: {
      async increment() {
        this.count++

        // DOM not yet updated
        console.log(document.getElementById('counter').textContent) // 0

        await nextTick()
        // DOM is now updated
        console.log(document.getElementById('counter').textContent) // 1
      }
    }
  }
  </script>

  <template>
    <button id="counter" @click="increment">{{ count }}</button>
  </template>
```

---

## Custom Elements API {#custom-elements-api}

**URL:** llms-txt#custom-elements-api-{#custom-elements-api}

**Contents:**
- defineCustomElement() {#definecustomelement}
- useHost() <sup class="vt-badge" data-text="3.5+"/> {#usehost}
- useShadowRoot() <sup class="vt-badge" data-text="3.5+"/> {#useshadowroot}
- this.$host <sup class="vt-badge" data-text="3.5+"/> {#this-host}

## defineCustomElement() {#definecustomelement}

This method accepts the same argument as [`defineComponent`](#definecomponent), but instead returns a native [Custom Element](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements) class constructor.

> Type is simplified for readability.

In addition to normal component options, `defineCustomElement()` also supports a number of options that are custom-elements-specific:

- **`styles`**: an array of inlined CSS strings for providing CSS that should be injected into the element's shadow root.

- **`configureApp`** <sup class="vt-badge" data-text="3.5+"/>: a function that can be used to configure the Vue app instance for the custom element.

- **`shadowRoot`** <sup class="vt-badge" data-text="3.5+"/>: `boolean`, defaults to `true`. Set to `false` to render the custom element without a shadow root. This means `<style>` in custom element SFCs will no longer be encapsulated.

- **`nonce`** <sup class="vt-badge" data-text="3.5+"/>: `string`, if provided, will be set as the `nonce` attribute on style tags injected to the shadow root.

Note that instead of being passed as part of the component itself, these options can also be passed via a second argument:

The return value is a custom element constructor that can be registered using [`customElements.define()`](https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry/define).

- [Guide - Building Custom Elements with Vue](/guide/extras/web-components#building-custom-elements-with-vue)

- Also note that `defineCustomElement()` requires [special config](/guide/extras/web-components#sfc-as-custom-element) when used with Single-File Components.

## useHost() <sup class="vt-badge" data-text="3.5+"/> {#usehost}

A Composition API helper that returns the host element of the current Vue custom element.

## useShadowRoot() <sup class="vt-badge" data-text="3.5+"/> {#useshadowroot}

A Composition API helper that returns the shadow root of the current Vue custom element.

## this.$host <sup class="vt-badge" data-text="3.5+"/> {#this-host}

An Options API property that exposes the host element of the current Vue custom element.

---
url: /api/custom-renderer.md
---

**Examples:**

Example 1 (ts):
```ts
function defineCustomElement(
    component:
      | (ComponentOptions & CustomElementsOptions)
      | ComponentOptions['setup'],
    options?: CustomElementsOptions
  ): {
    new (props?: object): HTMLElement
  }

  interface CustomElementsOptions {
    styles?: string[]

    // the following options are 3.5+
    configureApp?: (app: App) => void
    shadowRoot?: boolean
    nonce?: string
  }
```

Example 2 (js):
```js
import Element from './MyElement.ce.vue'

  defineCustomElement(Element, {
    configureApp(app) {
      // ...
    }
  })
```

Example 3 (js):
```js
import { defineCustomElement } from 'vue'

  const MyVueElement = defineCustomElement({
    /* component options */
  })

  // Register the custom element.
  customElements.define('my-vue-element', MyVueElement)
```

---

## Custom Renderer API {#custom-renderer-api}

**URL:** llms-txt#custom-renderer-api-{#custom-renderer-api}

**Contents:**
- createRenderer() {#createrenderer}

## createRenderer() {#createrenderer}

Creates a custom renderer. By providing platform-specific node creation and manipulation APIs, you can leverage Vue's core runtime to target non-DOM environments.

Vue's own `@vue/runtime-dom` is [implemented using the same API](https://github.com/vuejs/core/blob/main/packages/runtime-dom/src/index.ts). For a simpler implementation, check out [`@vue/runtime-test`](https://github.com/vuejs/core/blob/main/packages/runtime-test/src/index.ts) which is a private package for Vue's own unit testing.

---
url: /guide/essentials/event-handling.md
---

**Examples:**

Example 1 (ts):
```ts
function createRenderer<HostNode, HostElement>(
    options: RendererOptions<HostNode, HostElement>
  ): Renderer<HostElement>

  interface Renderer<HostElement> {
    render: RootRenderFunction<HostElement>
    createApp: CreateAppFunction<HostElement>
  }

  interface RendererOptions<HostNode, HostElement> {
    patchProp(
      el: HostElement,
      key: string,
      prevValue: any,
      nextValue: any,
      namespace?: ElementNamespace,
      parentComponent?: ComponentInternalInstance | null,
    ): void
    insert(el: HostNode, parent: HostElement, anchor?: HostNode | null): void
    remove(el: HostNode): void
    createElement(
      type: string,
      namespace?: ElementNamespace,
      isCustomizedBuiltIn?: string,
      vnodeProps?: (VNodeProps & { [key: string]: any }) | null,
    ): HostElement
    createText(text: string): HostNode
    createComment(text: string): HostNode
    setText(node: HostNode, text: string): void
    setElementText(node: HostElement, text: string): void
    parentNode(node: HostNode): HostElement | null
    nextSibling(node: HostNode): HostNode | null
    querySelector?(selector: string): HostElement | null
    setScopeId?(el: HostElement, id: string): void
    cloneNode?(node: HostNode): HostNode
    insertStaticContent?(
      content: string,
      parent: HostElement,
      anchor: HostNode | null,
      namespace: ElementNamespace,
      start?: HostNode | null,
      end?: HostNode | null,
    ): [HostNode, HostNode]
  }
```

Example 2 (js):
```js
import { createRenderer } from '@vue/runtime-core'

  const { render, createApp } = createRenderer({
    patchProp,
    insert,
    remove,
    createElement
    // ...
  })

  // `render` is the low-level API
  // `createApp` returns an app instance
  export { render, createApp }

  // re-export Vue core APIs
  export * from '@vue/runtime-core'
```

---
