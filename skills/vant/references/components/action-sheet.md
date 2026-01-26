# ActionSheet 动作面板

# ActionSheet 动作面板

### 介绍

底部弹起的模态面板，包含与当前情境相关的多个选项。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { ActionSheet } from 'vant';

const app = createApp();
app.use(ActionSheet);
```

## 代码演示

### 基础用法

动作面板通过 `actions` 属性来定义选项，`actions` 属性是一个由对象构成的数组，数组中的每个对象配置一列，对象格式见文档下方表格。

```html
<van-cell is-link title="基础用法" @click="show = true" />
<van-action-sheet v-model:show="show" :actions="actions" @select="onSelect" />
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const show = ref(false);
const actions = [
{ name: '选项一' },
{ name: '选项二' },
{ name: '选项三' },
];
const onSelect = (item) => {
// 默认情况下点击选项时不会自动收起
// 可以通过 close-on-click-action 属性开启自动收起
show.value = false;
showToast(item.name);
};

return {
show,
actions,
onSelect,
};
},
};
```

### 展示图标

使用 `actions` 的 `icon` 字段可以为选项设置图标。

```html
<van-cell is-link title="展示图标" @click="show = true" />
<van-action-sheet v-model:show="show" :actions="actions" @select="onSelect" />
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const show = ref(false);
const actions = [
{ name: '选项一', icon: 'cart-o' },
{ name: '选项二', icon: 'shop-o' },
{ name: '选项三', icon: 'star-o' },
];
const onSelect = (item) => {
show.value = false;
showToast(item.name);
};

return {
show,
actions,
onSelect,
};
},
};
```

### 展示取消按钮

设置 `cancel-text` 属性后，会在底部展示取消按钮，点击后关闭当前面板并触发 `cancel` 事件。

```html
<van-action-sheet
v-model:show="show"
:actions="actions"
cancel-text="取消"
close-on-click-action
@cancel="onCancel"
/>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const show = ref(false);
const actions = [
{ name: '选项一' },
{ name: '选项二' },
{ name: '选项三' },
];
const onCancel = () => showToast('取消');

return {
show,
actions,
onCancel,
};
},
};
```

### 展示描述信息

通过 `description` 可以在菜单顶部显示描述信息，通过选项的 `subname` 属性可以在选项文字的右侧展示描述信息。

```html
<van-action-sheet
v-model:show="show"
:actions="actions"
cancel-text="取消"
description="这是一段描述信息"
close-on-click-action
/>
```

```js
import { ref } from 'vue';

export default {
setup() {
const show = ref(false);
const actions = [
{ name: '选项一' },
{ name: '选项二' },
{ name: '选项三', subname: '描述信息' },
];

return {
show,
actions,
};
},
};
```

### 选项状态

可以通过 `loading` 和 `disabled` 将选项设置为加载状态或禁用状态，或者通过`color`设置选项的颜色

```html
<van-action-sheet
v-model:show="show"
:actions="actions"
cancel-text="取消"
close-on-click-action
/>
```

```js
import { ref } from 'vue';

export default {
setup() {
const show = ref(false);
const actions = [
{ name: '着色选项', color: '#ee0a24' },
{ name: '禁用选项', disabled: true },
{ name: '加载选项', loading: true },
];

return {
show,
actions,
};
},
};
```

### 自定义面板

通过插槽可以自定义面板的展示内容，同时可以使用`title`属性展示标题栏

```html
<van-action-sheet v-model:show="show" title="标题">
<div class="content">内容</div>
</van-action-sheet>

<style>
.content {
padding: 16px 16px 160px;
}
</style>
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:show | 是否显示动作面板 | boolean | `false` |
| actions | 面板选项列表 | ActionSheetAction[] | `[]` |
| title | 顶部标题 | string | - |
| cancel-text | 取消按钮文字 | string | - |
| description | 选项上方的描述信息 | string | - |
| closeable | 是否显示关闭图标 | boolean | `true` |
| close-icon | 关闭图标名称或图片链接，等同于 Icon 组件的name 属性 | string | `cross` |
| duration | 动画时长，单位秒，设置为 0 可以禁用动画 | number \| string | `0.3` |
| z-index | 将面板的 z-index 层级设置为一个固定值 | number \| string | `2000+` |
| round | 是否显示圆角 | boolean | `true` |
| overlay | 是否显示遮罩层 | boolean | `true` |
| overlay-class | 自定义遮罩层类名 | string \| Array \| object | - |
| overlay-style | 自定义遮罩层样式 | object | - |
| lock-scroll | 是否锁定背景滚动 | boolean | `true` |
| lazy-render | 是否在显示弹层时才渲染节点 | boolean | `true` |
| close-on-popstate | 是否在页面回退时自动关闭 | boolean | `true` |
| close-on-click-action | 是否在点击选项后关闭 | boolean | `false` |
| close-on-click-overlay | 是否在点击遮罩层后关闭 | boolean | `true` |
| safe-area-inset-bottom | 是否开启底部安全区适配 | boolean | `true` |
| teleport | 指定挂载的节点，等同于 Teleport 组件的to 属性 | string \| Element | - |
| before-close | 关闭前的回调函数，返回`false`可阻止关闭，支持返回 Promise | (action: string) => boolean \| Promise<boolean> | - |

### Action 数据结构

`actions` 属性是一个由对象构成的数组，数组中的每个对象配置一列，对象可以包含以下值：

| 键名 | 说明 | 类型 |
| --- | --- | --- |
| name | 标题 | string |
| subname | 二级标题 | string |
| color | 选项文字颜色 | string |
| icon`v4.8.6` | 选项图标名称或图片链接 | string |
| className | 为对应列添加额外的 class | string \| Array \| object |
| loading | 是否为加载状态 | boolean |
| disabled | 是否为禁用状态 | boolean |
| callback | 点击时触发的回调函数 | action: ActionSheetAction |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| select | 点击选项时触发，禁用或加载状态下不会触发 | action: ActionSheetAction, index: number |
| cancel | 点击取消按钮时触发 | - |
| open | 打开面板时触发 | - |
| close | 关闭面板时触发 | - |
| opened | 打开面板且动画结束后触发 | - |
| closed | 关闭面板且动画结束后触发 | - |
| click-overlay | 点击遮罩层时触发 | event: MouseEvent |

### Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| default | 自定义面板的展示内容 | - |
| description | 自定义描述文案 | - |
| cancel | 自定义取消按钮内容 | - |
| action | 自定义选项内容 | { action: ActionSheetAction, index: number } |

### 类型定义

组件导出以下类型定义：

```ts
import type { ActionSheetProps, ActionSheetAction } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-action-sheet-max-height | 80% | - |
| --van-action-sheet-header-height | 48px | - |
| --van-action-sheet-header-font-size | var(--van-font-size-lg) | - |
| --van-action-sheet-description-color | var(--van-text-color-2) | - |
| --van-action-sheet-description-font-size | var(--van-font-size-md) | - |
| --van-action-sheet-description-line-height | var(--van-line-height-md) | - |
| --van-action-sheet-item-background | var(--van-background-2) | - |
| --van-action-sheet-item-font-size | var(--van-font-size-lg) | - |
| --van-action-sheet-item-line-height | var(--van-line-height-lg) | - |
| --van-action-sheet-item-text-color | var(--van-text-color) | - |
| --van-action-sheet-item-disabled-text-color | var(--van-text-color-3) | - |
| --van-action-sheet-item-icon-size | 18px | - |
| --van-action-sheet-item-icon-margin-right | var(--van-padding-xs) | - |
| --van-action-sheet-subname-color | var(--van-text-color-2) | - |
| --van-action-sheet-subname-font-size | var(--van-font-size-sm) | - |
| --van-action-sheet-subname-line-height | var(--van-line-height-sm) | - |
| --van-action-sheet-close-icon-size | 22px | - |
| --van-action-sheet-close-icon-color | var(--van-gray-5) | - |
| --van-action-sheet-close-icon-padding | 0 var(--van-padding-md) | - |
| --van-action-sheet-cancel-text-color | var(--van-gray-7) | - |
| --van-action-sheet-cancel-padding-top | var(--van-padding-xs) | - |
| --van-action-sheet-cancel-padding-color | var(--van-background) | - |
| --van-action-sheet-loading-icon-size | 22px | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)