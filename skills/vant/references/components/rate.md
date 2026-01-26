# Rate 评分

# Rate 评分

### 介绍

用于对事物进行评级操作。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Rate } from 'vant';

const app = createApp();
app.use(Rate);
```

## 代码演示

### 基础用法

通过 `v-model` 来绑定当前评分值。

```html
<van-rate v-model="value" />
```

```js
import { ref } from 'vue';

export default {
setup() {
const value = ref(3);
return { value };
},
};
```

### 自定义图标

通过 `icon` 属性设置选中时的图标，`void-icon` 属性设置未选中时的图标。

```html
<van-rate v-model="value" icon="like" void-icon="like-o" />
```

### 自定义样式

通过 `size` 属性设置图标大小，`color` 属性设置选中时的颜色，`void-color` 设置未选中时的颜色。

```html
<van-rate
v-model="value"
:size="25"
color="#ffd21e"
void-icon="star"
void-color="#eee"
/>
```

### 半星

设置 `allow-half` 属性后可以选中半星。

```html
<van-rate v-model="value" allow-half />
```

```js
import { ref } from 'vue';

export default {
setup() {
const value = ref(2.5);
return { value };
},
};
```

### 自定义数量

通过 `count` 属性设置评分总数。

```html
<van-rate v-model="value" :count="6" />
```

### 可清空

当 `clearable` 属性设置为 `true`，再次点击相同的值时，可以将值重置为 `0`。

```html
<van-rate v-model="value" clearable />
```

### 禁用状态

通过 `disabled` 属性来禁用评分。

```html
<van-rate v-model="value" disabled />
```

### 只读状态

通过 `readonly` 属性将评分设置为只读状态。

```html
<van-rate v-model="value" readonly />
```

### 只读状态显示小数

设置 `readonly` 和 `allow-half` 属性后，Rate 组件可以展示任意小数结果。

```html
<van-rate v-model="value" readonly allow-half />
```

```js
import { ref } from 'vue';

export default {
setup() {
const value = ref(3.3);
return { value };
},
};
```

### 监听 change 事件

评分变化时，会触发 `change` 事件。

```html
<van-rate v-model="value" @change="onChange" />
```

```javascript
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const value = ref(3);
const onChange = (value) => showToast('当前值：' + value);
return {
value,
onChange,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前分值 | number | - |
| count | 图标总数 | number \| string | `5` |
| size | 图标大小，默认单位为`px` | number \| string | `20px` |
| gutter | 图标间距，默认单位为`px` | number \| string | `4px` |
| color | 选中时的颜色 | string | `#ee0a24` |
| void-color | 未选中时的颜色 | string | `#c8c9cc` |
| disabled-color | 禁用时的颜色 | string | `#c8c9cc` |
| icon | 选中时的图标名称或图片链接，等同于 Icon 组件的name 属性 | string | `star` |
| void-icon | 未选中时的图标名称或图片链接，等同于 Icon 组件的name 属性 | string | `star-o` |
| icon-prefix | 图标类名前缀，等同于 Icon 组件的class-prefix 属性 | string | `van-icon` |
| allow-half | 是否允许半选 | boolean | `false` |
| clearable`v4.6.0` | 是否允许再次点击后清除 | boolean | `false` |
| readonly | 是否为只读状态，只读状态下无法修改评分 | boolean | `false` |
| disabled | 是否禁用评分 | boolean | `false` |
| touchable | 是否可以通过滑动手势选择评分 | boolean | `true` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 当前分值变化时触发的事件 | currentValue: number |

### 类型定义

组件导出以下类型定义：

```ts
import type { RateProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-rate-icon-size | 20px | - |
| --van-rate-icon-gutter | var(--van-padding-base) | - |
| --van-rate-icon-void-color | var(--van-gray-5) | - |
| --van-rate-icon-full-color | var(--van-danger-color) | - |
| --van-rate-icon-disabled-color | var(--van-gray-5) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)