# Picker 选择器

# Picker 选择器

### 介绍

提供多个选项集合供用户选择，支持单列选择、多列选择和级联选择，通常与[弹出层](#/zh-CN/popup)组件配合使用。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Picker } from 'vant';

const app = createApp();
app.use(Picker);
```

## 代码演示

### 基础用法

#### 选项配置

Picker 组件通过 `columns` 属性配置选项数据，`columns` 是一个包含字符串或对象的数组。

#### 顶部栏

顶部栏包含标题、确认按钮和取消按钮，点击确认按钮触发 `confirm` 事件，点击取消按钮触发 `cancel` 事件。

```html
<van-picker
title="标题"
:columns="columns"
@confirm="onConfirm"
@cancel="onCancel"
@change="onChange"
/>
```

```js
import { showToast } from 'vant';

export default {
setup() {
const columns = [
{ text: '杭州', value: 'Hangzhou' },
{ text: '宁波', value: 'Ningbo' },
{ text: '温州', value: 'Wenzhou' },
{ text: '绍兴', value: 'Shaoxing' },
{ text: '湖州', value: 'Huzhou' },
];
const onConfirm = ({ selectedValues }) => {
showToast(`当前值: ${selectedValues.join(',')}`);
};
const onChange = ({ selectedValues }) => {
showToast(`当前值: ${selectedValues.join(',')}`);
};
const onCancel = () => showToast('取消');

return {
columns,
onChange,
onCancel,
onConfirm,
};
},
};
```

### 搭配弹出层使用

在实际场景中，Picker 通常作为用于辅助表单填写，可以搭配 Popup 和 Field 实现该效果。

```html
<van-field
v-model="fieldValue"
is-link
readonly
label="城市"
placeholder="选择城市"
@click="showPicker = true"
/>
<van-popup v-model:show="showPicker" destroy-on-close round position="bottom">
<van-picker
:model-value="pickerValue"
:columns="columns"
@cancel="showPicker = false"
@confirm="onConfirm"
/>
</van-popup>
```

```js
import { ref } from 'vue';

export default {
setup() {
const columns = [
{ text: '杭州', value: 'Hangzhou' },
{ text: '宁波', value: 'Ningbo' },
{ text: '温州', value: 'Wenzhou' },
{ text: '绍兴', value: 'Shaoxing' },
{ text: '湖州', value: 'Huzhou' },
];
const fieldValue = ref('');
const showPicker = ref(false);
const pickerValue = ref<Numeric[]>([]);
const onConfirm = ({ selectedValues, selectedOptions }) => {
showPicker.value = false;
pickerValue.value = selectedValues;
fieldValue.value = selectedOptions[0].text;
};

return {
columns,
onConfirm,
fieldValue,
showPicker,
};
},
};
```

### 双向绑定

通过 `v-model` 可以绑定当前选中项的 `values`，修改 `v-model` 绑定的值时，Picker 的选中状态也会随之改变。

`v-model` 的值是一个数组，数组的第一位对应第一列选中项的 `value`，第二位对应第二列选中项的 `value`，以此类推。

```html
<van-picker v-model="selectedValues" title="标题" :columns="columns" />
```

```js
import { showToast } from 'vant';

export default {
setup() {
const columns = [
{ text: '杭州', value: 'Hangzhou' },
{ text: '宁波', value: 'Ningbo' },
{ text: '温州', value: 'Wenzhou' },
{ text: '绍兴', value: 'Shaoxing' },
{ text: '湖州', value: 'Huzhou' },
];
const selectedValues = ref(['Wenzhou']);

return {
columns,
selectedValues,
};
},
};
```

### 多列选择

`columns` 属性可以通过二维数组的形式配置多列选择。

```html
<van-picker title="标题" :columns="columns" />
```

```js
export default {
setup() {
const columns = [
// 第一列
[
{ text: '周一', value: 'Monday' },
{ text: '周二', value: 'Tuesday' },
{ text: '周三', value: 'Wednesday' },
{ text: '周四', value: 'Thursday' },
{ text: '周五', value: 'Friday' },
],
// 第二列
[
{ text: '上午', value: 'Morning' },
{ text: '下午', value: 'Afternoon' },
{ text: '晚上', value: 'Evening' },
],
];

return { columns };
},
};
```

### 级联选择

使用 `columns` 的 `children` 字段可以实现选项级联的效果。如果级联层级较多，推荐使用 [Cascader 级联选项组件](#/zh-CN/cascader)。

```html
<van-picker title="标题" :columns="columns" />
```

```js
export default {
setup() {
const columns = [
{
text: '浙江',
value: 'Zhejiang',
children: [
{
text: '杭州',
value: 'Hangzhou',
children: [
{ text: '西湖区', value: 'Xihu' },
{ text: '余杭区', value: 'Yuhang' },
],
},
{
text: '温州',
value: 'Wenzhou',
children: [
{ text: '鹿城区', value: 'Lucheng' },
{ text: '瓯海区', value: 'Ouhai' },
],
},
],
},
{
text: '福建',
value: 'Fujian',
children: [
{
text: '福州',
value: 'Fuzhou',
children: [
{ text: '鼓楼区', value: 'Gulou' },
{ text: '台江区', value: 'Taijiang' },
],
},
{
text: '厦门',
value: 'Xiamen',
children: [
{ text: '思明区', value: 'Siming' },
{ text: '海沧区', value: 'Haicang' },
],
},
],
},
];

return { columns };
},
};
```

> 级联选择的数据嵌套深度需要保持一致，如果部分选项没有子选项，可以使用空字符串进行占位。

### 禁用选项

选项可以为对象结构，通过设置 `disabled` 来禁用该选项。

```html
<van-picker :columns="columns" />
```

```js
export default {
setup() {
const columns = [
{ text: '杭州', value: 'Hangzhou', disabled: true },
{ text: '宁波', value: 'Ningbo' },
{ text: '温州', value: 'Wenzhou' },
];
return { columns };
},
};
```

### 加载状态

若选择器数据是异步获取的，可以通过 `loading` 属性显示加载提示。

```html
<van-picker :columns="columns" :loading="loading" />
```

```js
import { ref } from 'vue';

export default {
setup() {
const columns = ref([]);
const loading = ref(true);

setTimeout(() => {
columns.value = [{ text: '选项', value: 'option' }];
loading.value = false;
}, 1000);

return { columns, loading };
},
};
```

### 空状态

当数据为空时，可以使用 `empty` 插槽自定义空状态内容。

```html
<van-picker title="标题">
<template #empty>
<van-empty
image="https://fastly.jsdelivr.net/npm/@vant/assets/custom-empty-image.png"
image-size="80"
description="No data"
/>
</template>
</van-picker>
```

### 自定义 Columns 的结构

```html
<van-picker
title="标题"
:columns="columns"
:columns-field-names="customFieldName"
/>
```

```js
export default {
setup() {
const columns = [
{
cityName: '浙江',
cities: [
{
cityName: '杭州',
cities: [{ cityName: '西湖区' }, { cityName: '余杭区' }],
},
{
cityName: '温州',
cities: [{ cityName: '鹿城区' }, { cityName: '瓯海区' }],
},
],
},
{
cityName: '福建',
cities: [
{
cityName: '福州',
cities: [{ cityName: '鼓楼区' }, { cityName: '台江区' }],
},
{
cityName: '厦门',
cities: [{ cityName: '思明区' }, { cityName: '海沧区' }],
},
],
},
];

const customFieldName = {
text: 'cityName',
value: 'cityName',
children: 'cities',
};

return {
columns,
customFieldName,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中项对应的值 | number[] \| string[] | - |
| columns | 对象数组，配置每一列显示的数据 | PickerOption[] \| PickerOption[][] | `[]` |
| columns-field-names | 自定义`columns`结构中的字段 | object | `{ text: 'text', value: 'value', children: 'children' }` |
| title | 顶部栏标题 | string | - |
| confirm-button-text | 确认按钮文字，设置为空字符串可以隐藏按钮 | string | `确认` |
| cancel-button-text | 取消按钮文字，设置为空字符串可以隐藏按钮 | string | `取消` |
| toolbar-position | 顶部栏位置，可选值为`bottom` | string | `top` |
| loading | 是否显示加载状态 | boolean | `false` |
| readonly | 是否为只读状态，只读状态下无法切换选项 | boolean | `false` |
| show-toolbar | 是否显示顶部栏 | boolean | `true` |
| allow-html | 是否允许选项内容中渲染 HTML | boolean | `false` |
| option-height | 选项高度，支持`px``vw``vh``rem`单位，默认`px` | number \| string | `44` |
| visible-option-num | 可见的选项个数 | number \| string | `6` |
| swipe-duration | 快速滑动时惯性滚动的时长，单位`ms` | number \| string | `1000` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| confirm | 点击完成按钮时触发 | { selectedValues, selectedOptions, selectedIndexes } |
| cancel | 点击取消按钮时触发 | { selectedValues, selectedOptions, selectedIndexes } |
| change | 选中的选项改变时触发 | { selectedValues, selectedOptions, selectedIndexes, columnIndex } |
| click-option | 点击选项时触发 | { currentOption, selectedValues, selectedOptions, selectedIndexes, columnIndex } |
| scroll-into`v4.2.1` | 当用户通过点击或拖拽让一个选项滚动到中间的选择区域时触发 | { currentOption, columnIndex } |

### Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| toolbar | 自定义整个顶部栏的内容 | - |
| title | 自定义标题内容 | - |
| confirm | 自定义确认按钮内容 | - |
| cancel | 自定义取消按钮内容 | - |
| option | 自定义选项内容 | option: PickerOption, index: number |
| columns-top | 自定义选项上方内容 | - |
| columns-bottom | 自定义选项下方内容 | - |
| empty`v4.9.10` | 自定义空状态内容 | - |

### PickerOption 数据结构

| 键名 | 说明 | 类型 |
| --- | --- | --- |
| text | 选项文字内容 | string \| number |
| value | 选项对应的值 | string \| number |
| disabled | 是否禁用选项 | boolean |
| children | 级联选项 | PickerOption[] |
| className | 选项额外类名 | string \| Array \| object |

### 方法

通过 ref 可以获取到 Picker 实例并调用实例方法，详见[组件实例方法](#/zh-CN/advanced-usage#zu-jian-shi-li-fang-fa)。

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| confirm | 停止惯性滚动并触发`confirm`事件 | - | - |
| getSelectedOptions | 获取当前选中的选项 | - | (PickerOption \| undefined)[] |

### 类型定义

组件导出以下类型定义：

```ts
import type {
PickerProps,
PickerColumn,
PickerOption,
PickerInstance,
PickerFieldNames,
PickerToolbarPosition,
PickerCancelEventParams,
PickerChangeEventParams,
PickerConfirmEventParams,
} from 'vant';
```

`PickerInstance` 是组件实例的类型，用法如下：

```ts
import { ref } from 'vue';
import type { PickerInstance } from 'vant';

const pickerRef = ref<PickerInstance>();

pickerRef.value?.confirm();
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-picker-background | var(--van-background-2) | - |
| --van-picker-toolbar-height | 44px | - |
| --van-picker-title-font-size | var(--van-font-size-lg) | - |
| --van-picker-title-line-height | var(--van-line-height-md) | - |
| --van-picker-action-padding | 0 var(--van-padding-md) | - |
| --van-picker-action-font-size | var(--van-font-size-md) | - |
| --van-picker-confirm-action-color | var(--van-primary-color) | - |
| --van-picker-cancel-action-color | var(--van-text-color-2) | - |
| --van-picker-option-padding | 0 var(--van-padding-base) | - |
| --van-picker-option-font-size | var(--van-font-size-lg) | - |
| --van-picker-option-text-color | var(--van-text-color) | - |
| --van-picker-option-disabled-opacity | 0.3 | - |
| --van-picker-mask-color | linear-gradient | - |
| --van-picker-loading-icon-color | var(--van-primary-color) | - |
| --van-picker-loading-mask-color | rgba(255, 255, 255, 0.9) | - |

## 常见问题

### 在桌面端无法操作组件？

参见[桌面端适配](#/zh-CN/advanced-usage#zhuo-mian-duan-gua-pei)。

[浙ICP备2021036118号](https://beian.miit.gov.cn/)