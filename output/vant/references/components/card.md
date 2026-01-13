# Card 卡片

# Card 卡片

### 介绍

商品卡片，用于展示商品的图片、价格等信息。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Card } from 'vant';

const app = createApp();
app.use(Card);
```

## 代码演示

### 基础用法

```html
<van-card
num="2"
price="2.00"
desc="描述信息"
title="商品标题"
thumb="https://fastly.jsdelivr.net/npm/@vant/assets/ipad.jpeg"
/>
```

### 营销信息

通过 `origin-price` 设置商品原价，通过 `tag` 设置商品左上角标签。

```html
<van-card
num="2"
tag="标签"
price="2.00"
desc="描述信息"
title="商品标题"
thumb="https://fastly.jsdelivr.net/npm/@vant/assets/ipad.jpeg"
origin-price="10.00"
/>
```

### 自定义内容

`Card` 组件提供了多个插槽，可以灵活地自定义内容。

```html
<van-card
num="2"
price="2.00"
desc="描述信息"
title="商品标题"
thumb="https://fastly.jsdelivr.net/npm/@vant/assets/ipad.jpeg"
>
<template #tags>
<van-tag plain type="primary">标签</van-tag>
<van-tag plain type="primary">标签</van-tag>
</template>
<template #footer>
<van-button size="mini">按钮</van-button>
<van-button size="mini">按钮</van-button>
</template>
</van-card>
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| thumb | 左侧图片 URL | string | - |
| title | 标题 | string | - |
| desc | 描述 | string | - |
| tag | 图片角标 | string | - |
| num | 商品数量 | number \| string | - |
| price | 商品价格 | number \| string | - |
| origin-price | 商品划线原价 | number \| string | - |
| centered | 内容是否垂直居中 | boolean | `false` |
| currency | 货币符号 | string | `¥` |
| thumb-link | 点击左侧图片后跳转的链接地址 | string | - |
| lazy-load | 是否开启图片懒加载，须配合Lazyload组件使用 | boolean | `false` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击时触发 | event: MouseEvent |
| click-thumb | 点击自定义图片时触发 | event: MouseEvent |

### Slots

| 名称 | 说明 |
| --- | --- |
| title | 自定义标题 |
| desc | 自定义描述 |
| num | 自定义数量 |
| price | 自定义价格 |
| origin-price | 自定义商品原价 |
| price-top | 自定义价格上方区域 |
| bottom | 自定义价格下方区域 |
| thumb | 自定义图片 |
| tag | 自定义图片角标 |
| tags | 自定义描述下方标签区域 |
| footer | 自定义右下角内容 |

### 类型定义

组件导出以下类型定义：

```ts
import type { CardProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-card-padding | var(--van-padding-xs) var(--van-padding-md) | - |
| --van-card-font-size | var(--van-font-size-sm) | - |
| --van-card-text-color | var(--van-text-color) | - |
| --van-card-background | var(--van-background) | - |
| --van-card-thumb-size | 88px | - |
| --van-card-thumb-radius | var(--van-radius-lg) | - |
| --van-card-title-line-height | 16px | - |
| --van-card-desc-color | var(--van-text-color-2) | - |
| --van-card-desc-line-height | var(--van-line-height-md) | - |
| --van-card-price-color | var(--van-text-color) | - |
| --van-card-origin-price-color | var(--van-text-color-2) | - |
| --van-card-num-color | var(--van-text-color-2) | - |
| --van-card-origin-price-font-size | var(--van-font-size-xs) | - |
| --van-card-price-font-size | var(--van-font-size-sm) | - |
| --van-card-price-integer-font-size | var(--van-font-size-lg) | - |
| --van-card-price-font | var(--van-price-font) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)