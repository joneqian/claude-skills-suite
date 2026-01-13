# Tabbar 标签栏

# Tabbar 标签栏

### 介绍

底部导航栏，用于在不同页面之间进行切换。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Tabbar, TabbarItem } from 'vant';

const app = createApp();
app.use(Tabbar);
app.use(TabbarItem);
```

## 代码演示

### 基础用法

`v-model` 默认绑定选中标签的索引值，通过修改 `v-model` 即可切换选中的标签。

```html
<van-tabbar v-model="active">
<van-tabbar-item icon="home-o">标签</van-tabbar-item>
<van-tabbar-item icon="search">标签</van-tabbar-item>
<van-tabbar-item icon="friends-o">标签</van-tabbar-item>
<van-tabbar-item icon="setting-o">标签</van-tabbar-item>
</van-tabbar>
```

```js
import { ref } from 'vue';

export default {
setup() {
const active = ref(0);
return { active };
},
};
```

### 通过名称匹配

在标签指定 `name` 属性的情况下，`v-model` 的值为当前标签的 `name`。

```html
<van-tabbar v-model="active">
<van-tabbar-item name="home" icon="home-o">标签</van-tabbar-item>
<van-tabbar-item name="search" icon="search">标签</van-tabbar-item>
<van-tabbar-item name="friends" icon="friends-o">标签</van-tabbar-item>
<van-tabbar-item name="setting" icon="setting-o">标签</van-tabbar-item>
</van-tabbar>
```

```js
import { ref } from 'vue';

export default {
setup() {
const active = ref('home');
return { active };
},
};
```

### 徽标提示

设置 `dot` 属性后，会在图标右上角展示一个小红点；设置 `badge` 属性后，会在图标右上角展示相应的徽标。

```html
<van-tabbar v-model="active">
<van-tabbar-item icon="home-o">标签</van-tabbar-item>
<van-tabbar-item icon="search" dot>标签</van-tabbar-item>
<van-tabbar-item icon="friends-o" badge="5">标签</van-tabbar-item>
<van-tabbar-item icon="setting-o" badge="20">标签</van-tabbar-item>
</van-tabbar>
```

### 自定义图标

通过 `icon` 插槽自定义图标，可以通过 `slot-scope` 判断标签是否选中。

```html
<van-tabbar v-model="active">
<van-tabbar-item badge="3">
<span>自定义</span>
<template #icon="props">
<img :src="props.active ? icon.active : icon.inactive" />
</template>
</van-tabbar-item>
<van-tabbar-item icon="search">标签</van-tabbar-item>
<van-tabbar-item icon="setting-o">标签</van-tabbar-item>
</van-tabbar>
```

```js
import { ref } from 'vue';

export default {
setup() {
const active = ref(0);
const icon = {
active: 'https://fastly.jsdelivr.net/npm/@vant/assets/user-active.png',
inactive:
'https://fastly.jsdelivr.net/npm/@vant/assets/user-inactive.png',
};
return {
icon,
active,
};
},
};
```

### 自定义颜色

通过 `active-color` 属性设置选中标签的颜色，通过 `inactive-color` 属性设置未选中标签的颜色。

```html
<van-tabbar v-model="active" active-color="#ee0a24">
<van-tabbar-item icon="home-o">标签</van-tabbar-item>
<van-tabbar-item icon="search">标签</van-tabbar-item>
<van-tabbar-item icon="friends-o">标签</van-tabbar-item>
<van-tabbar-item icon="setting-o">标签</van-tabbar-item>
</van-tabbar>
```

### 监听切换事件

通过 `change` 事件来监听选中标签的变化。

```html
<van-tabbar v-model="active" @change="onChange">
<van-tabbar-item icon="home-o">标签 1</van-tabbar-item>
<van-tabbar-item icon="search">标签 2</van-tabbar-item>
<van-tabbar-item icon="friends-o">标签 3</van-tabbar-item>
<van-tabbar-item icon="setting-o">标签 4</van-tabbar-item>
</van-tabbar>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const active = ref(0);
const onChange = (index) => showToast(`标签 ${index}`);
return {
icon,
onChange,
};
},
};
```

### 路由模式

标签栏支持路由模式，用于搭配 Vue Router 使用。路由模式下会匹配页面路径和标签的 `to` 属性，并自动选中对应的标签。

```html
<router-view />

<van-tabbar route>
<van-tabbar-item replace to="/home" icon="home-o">标签</van-tabbar-item>
<van-tabbar-item replace to="/search" icon="search">标签</van-tabbar-item>
</van-tabbar>
```

## API

### Tabbar Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中标签的名称或索引值 | number \| string | `0` |
| fixed | 是否固定在底部 | boolean | `true` |
| border | 是否显示外边框 | boolean | `true` |
| z-index | 元素 z-index | number \| string | `1` |
| active-color | 选中标签的颜色 | string | `#1989fa` |
| inactive-color | 未选中标签的颜色 | string | `#7d7e80` |
| route | 是否开启路由模式 | boolean | `false` |
| placeholder | 固定在底部时，是否在标签位置生成一个等高的占位元素 | boolean | `false` |
| safe-area-inset-bottom | 是否开启底部安全区适配，设置 fixed 时默认开启 | boolean | `false` |
| before-change | 切换标签前的回调函数，返回`false`可阻止切换，支持返回 Promise | (name: number \| string) => boolean \| Promise<boolean> | - |

### Tabbar Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 切换标签时触发 | active: number \| string |

### TabbarItem Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 标签名称，作为匹配的标识符 | number \| string | 当前标签的索引值 |
| icon | 图标名称或图片链接，等同于 Icon 组件的name 属性 | string | - |
| icon-prefix | 图标类名前缀，等同于 Icon 组件的class-prefix 属性 | string | `van-icon` |
| dot | 是否显示图标右上角小红点 | boolean | `false` |
| badge | 图标右上角徽标的内容 | number \| string | - |
| badge-props | 自定义徽标的属性，传入的对象会被透传给Badge 组件的 props | BadgeProps | - |
| url | 点击后跳转的链接地址 | string | - |
| to | 点击后跳转的目标路由对象，等同于 Vue Router 的to 属性 | string \| object | - |
| replace | 是否在跳转时替换当前页面历史 | boolean | `false` |

### TabbarItem Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| icon | 自定义图标 | active: boolean |

### 类型定义

组件导出以下类型定义：

```ts
import type { TabbarProps, TabbarItemProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-tabbar-height | 50px | - |
| --van-tabbar-z-index | 1 | - |
| --van-tabbar-background | var(--van-background-2) | - |
| --van-tabbar-item-font-size | var(--van-font-size-sm) | - |
| --van-tabbar-item-text-color | var(--van-text-color) | - |
| --van-tabbar-item-active-color | var(--van-primary-color) | - |
| --van-tabbar-item-active-background | var(--van-background-2) | - |
| --van-tabbar-item-line-height | 1 | - |
| --van-tabbar-item-icon-size | 22px | - |
| --van-tabbar-item-icon-margin-bottom | var(--van-padding-base) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)