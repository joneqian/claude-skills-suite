# Slider 滑块

# Slider 滑块

### 介绍

滑动输入条，用于在给定的范围内选择一个值。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Slider } from 'vant';

const app = createApp();
app.use(Slider);
```

## 代码演示

### 基础用法

```html
<van-slider v-model="value" @change="onChange" />
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const value = ref(50);
const onChange = (value) => showToast('当前值：' + value);
return {
value,
onChange,
};
},
};
```

### 双滑块

添加 `range` 属性就可以开启双滑块模式，确保 `value` 的值是一个数组。

```html
<van-slider v-model="value" range @change="onChange" />
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
// 双滑块模式时，值必须是数组
const value = ref([10, 50]);
const onChange = (value) => showToast('当前值：' + value);
return {
value,
onChange,
};
},
};
```

### 指定选择范围

```html
<van-slider v-model="value" :min="-50" :max="50" />
```

### 禁用

```html
<van-slider v-model="value" disabled />
```

### 指定步长

```html
<van-slider v-model="value" :step="10" />
```

### 自定义样式

```html
<van-slider v-model="value" bar-height="4px" active-color="#ee0a24" />
```

### 自定义按钮

```html
<van-slider v-model="value">
<template #button>
<div class="custom-button">{{ value }}</div>
</template>
</van-slider>

<style>
.custom-button {
width: 26px;
color: #fff;
font-size: 10px;
line-height: 18px;
text-align: center;
background-color: var(--van-primary-color);
border-radius: 100px;
}
</style>
```

### 垂直方向

设置 `vertical` 属性后，滑块会垂直展示，且高度为 100% 父元素高度。

```html
<div :style="{ height: '150px' }">
<van-slider v-model="value" vertical @change="onChange" />
<van-slider
v-model="value2"
range
vertical
style="margin-left: 100px;"
@change="onChange"
/>
</div>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const value = ref(50);
const value2 = ref([10, 50]);
const onChange = (value) => showToast('当前值：' + value);
return {
value,
value2,
onChange,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前进度百分比，在双滑块模式下为数组格式 | number \| [number, number] | `0` |
| max | 最大值 | number \| string | `100` |
| min | 最小值 | number \| string | `0` |
| step | 步长 | number \| string | `1` |
| bar-height | 进度条高度，默认单位为`px` | number \| string | `2px` |
| button-size | 滑块按钮大小，默认单位为`px` | number \| string | `24px` |
| active-color | 进度条激活态颜色 | string | `#1989fa` |
| inactive-color | 进度条非激活态颜色 | string | `#e5e5e5` |
| range | 是否开启双滑块模式 | boolean | `false` |
| reverse | 是否将进度条反转 | boolean | `false` |
| disabled | 是否禁用滑块 | boolean | `false` |
| readonly | 是否为只读状态，只读状态下无法修改滑块的值 | boolean | `false` |
| vertical | 是否垂直展示 | boolean | `false` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:model-value | 进度变化时实时触发 | value: number |
| change | 进度变化且结束拖动后触发 | value: number |
| drag-start | 开始拖动时触发 | event: TouchEvent |
| drag-end | 结束拖动时触发 | event: TouchEvent |

### Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| button | 自定义滑块按钮 | { value: number, dragging: boolean } |
| left-button | 自定义左侧滑块按钮（双滑块模式下） | { value: number, dragging: boolean, dragIndex?: number } |
| right-button | 自定义右侧滑块按钮（双滑块模式下） | { value: number, dragging: boolean, dragIndex?: number } |

### 类型定义

组件导出以下类型定义：

```ts
import type { SliderProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-slider-active-background | var(--van-primary-color) | - |
| --van-slider-inactive-background | var(--van-gray-3) | - |
| --van-slider-disabled-opacity | var(--van-disabled-opacity) | - |
| --van-slider-bar-height | 2px | - |
| --van-slider-button-width | 24px | - |
| --van-slider-button-height | 24px | - |
| --van-slider-button-radius | 50% | - |
| --van-slider-button-background | var(--van-white) | - |
| --van-slider-button-shadow | 0 1px 2px rgba(0, 0, 0, 0.5) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)