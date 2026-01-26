# Progress 进度条

# Progress 进度条

### 介绍

用于展示操作的当前进度。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Progress } from 'vant';

const app = createApp();
app.use(Progress);
```

## 代码演示

### 基础用法

进度条默认为蓝色，使用 `percentage` 属性来设置当前进度。

```html
<van-progress :percentage="50" />
```

### 线条粗细

通过 `stroke-width` 可以设置进度条的粗细。

```html
<van-progress :percentage="50" stroke-width="8" />
```

### 置灰

设置 `inactive` 属性后进度条将置灰。

```html
<van-progress inactive :percentage="50" />
```

### 样式定制

可以使用 `pivot-text` 属性自定义文字，`color` 属性自定义进度条颜色。

```html
<van-progress pivot-text="橙色" color="#f2826a" :percentage="25" />
<van-progress pivot-text="红色" color="#ee0a24" :percentage="50" />
<van-progress
:percentage="75"
pivot-text="紫色"
pivot-color="#7232dd"
color="linear-gradient(to right, #be99ff, #7232dd)"
/>
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| percentage | 进度百分比 | number \| string | `0` |
| stroke-width | 进度条粗细，默认单位为`px` | number \| string | `4px` |
| color | 进度条颜色 | string | `#1989fa` |
| track-color | 轨道颜色 | string | `#e5e5e5` |
| pivot-text | 进度文字内容 | string | 百分比 |
| pivot-color | 进度文字背景色 | string | 同进度条颜色 |
| text-color | 进度文字颜色 | string | `white` |
| inactive | 是否置灰 | boolean | `false` |
| show-pivot | 是否显示进度文字 | boolean | `true` |

### 类型定义

组件导出以下类型定义：

```ts
import type { ProgressProps, ProgressInstance } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-progress-height | 4px | - |
| --van-progress-color | var(--van-primary-color) | - |
| --van-progress-inactive-color | var(--van-gray-5) | - |
| --van-progress-background | var(--van-gray-3) | - |
| --van-progress-pivot-padding | 0 5px | - |
| --van-progress-pivot-text-color | var(--van-white) | - |
| --van-progress-pivot-font-size | var(--van-font-size-xs) | - |
| --van-progress-pivot-line-height | 1.6 | - |
| --van-progress-pivot-background | var(--van-primary-color) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)