# Radio 单选框

# Radio 单选框

### 介绍

在一组备选项中进行单选。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { RadioGroup, Radio } from 'vant';

const app = createApp();
app.use(Radio);
app.use(RadioGroup);
```

## 代码演示

### 基础用法

通过 `v-model` 绑定值当前选中项的 name。

```html
<van-radio-group v-model="checked">
<van-radio name="1">单选框 1</van-radio>
<van-radio name="2">单选框 2</van-radio>
</van-radio-group>
```

```js
import { ref } from 'vue';

export default {
setup() {
const checked = ref('1');
return { checked };
},
};
```

### 水平排列

将 `direction` 属性设置为 `horizontal` 后，单选框组会变成水平排列。

```html
<van-radio-group v-model="checked" direction="horizontal">
<van-radio name="1">单选框 1</van-radio>
<van-radio name="2">单选框 2</van-radio>
</van-radio-group>
```

### 禁用状态

通过 `disabled` 属性禁止选项切换，在 `Radio` 上设置 `disabled` 可以禁用单个选项。

```html
<van-radio-group v-model="checked" disabled>
<van-radio name="1">单选框 1</van-radio>
<van-radio name="2">单选框 2</van-radio>
</van-radio-group>
```

### 自定义形状

`shape` 属性可选值为 `square` 和 `dot`，单选框形状分别对应方形和圆点形。

```html
<van-radio-group v-model="checked" shape="square">
<van-radio name="1">单选框 1</van-radio>
<van-radio name="2">单选框 2</van-radio>
</van-radio-group>

<van-radio-group v-model="checked" shape="dot">
<van-radio name="1">Radio 1</van-radio>
<van-radio name="2">Radio 2</van-radio>
</van-radio-group>
```

### 自定义颜色

通过 `checked-color` 属性设置选中状态的图标颜色。

```html
<van-radio-group v-model="checked">
<van-radio name="1" checked-color="#ee0a24">单选框 1</van-radio>
<van-radio name="2" checked-color="#ee0a24">单选框 2</van-radio>
</van-radio-group>
```

### 自定义大小

通过 `icon-size` 属性可以自定义图标的大小。

```html
<van-radio-group v-model="checked">
<van-radio name="1" icon-size="24px">单选框 1</van-radio>
<van-radio name="2" icon-size="24px">单选框 2</van-radio>
</van-radio-group>
```

### 自定义图标

通过 `icon` 插槽自定义图标，并通过 `slotProps` 判断是否为选中状态。

```html
<van-radio-group v-model="checked">
<van-radio name="1">
单选框 1
<template #icon="props">
<img class="img-icon" :src="props.checked ? activeIcon : inactiveIcon" />
</template>
</van-radio>
<van-radio name="2">
单选框 2
<template #icon="props">
<img class="img-icon" :src="props.checked ? activeIcon : inactiveIcon" />
</template>
</van-radio>
</van-radio-group>

<style>
.img-icon {
height: 20px;
}
</style>
```

```js
import { ref } from 'vue';

export default {
setup() {
const checked = ref('1');
return {
checked,
activeIcon:
'https://fastly.jsdelivr.net/npm/@vant/assets/user-active.png',
inactiveIcon:
'https://fastly.jsdelivr.net/npm/@vant/assets/user-inactive.png',
};
},
};
```

### 左侧文本

将 `label-position` 属性设置为 `'left'`，可以将文本位置调整到单选框左侧。

```html
<van-radio-group v-model="checked">
<van-radio name="1" label-position="left">单选框 1</van-radio>
<van-radio name="2" label-position="left">单选框 2</van-radio>
</van-radio-group>
```

### 禁用文本点击

设置 `label-disabled` 属性后，点击图标以外的内容不会触发单选框切换。

```html
<van-radio-group v-model="checked">
<van-radio name="1" label-disabled>单选框 1</van-radio>
<van-radio name="2" label-disabled>单选框 2</van-radio>
</van-radio-group>
```

### 搭配单元格组件使用

搭配单元格组件使用时，需要再引入 `Cell` 和 `CellGroup` 组件。

```html
<van-radio-group v-model="checked">
<van-cell-group inset>
<van-cell title="单选框 1" clickable @click="checked = '1'">
<template #right-icon>
<van-radio name="1" />
</template>
</van-cell>
<van-cell title="单选框 2" clickable @click="checked = '2'">
<template #right-icon>
<van-radio name="2" />
</template>
</van-cell>
</van-cell-group>
</van-radio-group>
```

## API

### Radio Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| name | 标识符，通常为一个唯一的字符串或数字 | any | - |
| shape | 形状，可选值为`square``dot` | string | `round` |
| disabled | 是否为禁用状态 | boolean | `false` |
| label-disabled | 是否禁用文本内容点击 | boolean | `false` |
| label-position | 文本位置，可选值为`left` | string | `right` |
| icon-size | 图标大小，默认单位为`px` | number \| string | `20px` |
| checked-color | 选中状态颜色 | string | `#1989fa` |

### RadioGroup Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中项的标识符 | any | - |
| disabled | 是否禁用所有单选框 | boolean | `false` |
| direction | 排列方向，可选值为`horizontal` | string | `vertical` |
| icon-size | 所有单选框的图标大小，默认单位为`px` | number \| string | `20px` |
| checked-color | 所有单选框的选中状态颜色 | string | `#1989fa` |
| shape`v4.6.3` | 形状，可选值为`square``dot` | string | `round` |

### Radio Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击单选框时触发 | event: MouseEvent |

### RadioGroup Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 当绑定值变化时触发的事件 | name: string |

### Radio Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| default | 自定义文本 | { checked: boolean, disabled: boolean } |
| icon | 自定义图标 | { checked: boolean, disabled: boolean } |

### 类型定义

组件导出以下类型定义：

```ts
import type {
RadioProps,
RadioShape,
RadioGroupProps,
RadioLabelPosition,
RadioGroupDirection,
} from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-radio-size | 20px | - |
| --van-radio-dot-size | 8px | 圆点到边界的距离 |
| --van-radio-border-color | var(--van-gray-5) | - |
| --van-radio-duration | var(--van-duration-fast) | - |
| --van-radio-label-margin | var(--van-padding-xs) | - |
| --van-radio-label-color | var(--van-text-color) | - |
| --van-radio-checked-icon-color | var(--van-primary-color) | - |
| --van-radio-disabled-icon-color | var(--van-gray-5) | - |
| --van-radio-disabled-label-color | var(--van-text-color-3) | - |
| --van-radio-disabled-background | var(--van-border-color) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)