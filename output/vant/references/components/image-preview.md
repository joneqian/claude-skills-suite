# ImagePreview 图片预览

# ImagePreview 图片预览

### 介绍

图片放大预览，支持组件调用和函数调用两种方式。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { ImagePreview } from 'vant';

const app = createApp();
app.use(ImagePreview);
```

### 函数调用

为了便于使用 `ImagePreview`，Vant 提供了一系列辅助函数，通过辅助函数可以快速唤起全局的图片预览组件。

比如使用 `showImagePreview` 函数，调用后会直接在页面中渲染对应的图片预览组件。

```js
import { showImagePreview } from 'vant';

showImagePreview(['https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg']);
```

## 代码演示

### 基础用法

在调用 `showImagePreview` 时，直接传入图片数组，即可展示图片预览。

```js
import { showImagePreview } from 'vant';

showImagePreview([
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
]);
```

### 指定初始位置

`showImagePreview` 支持传入配置对象，并通过 `startPosition` 选项指定图片的初始位置（索引值）。

```js
import { showImagePreview } from 'vant';

showImagePreview({
images: [
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
],
startPosition: 1,
});
```

### 展示关闭按钮

开启 `closeable` 选项后，会在弹出层的右上角显示关闭图标，并且可以通过 `close-icon` 属性自定义图标，使用`close-icon-position` 属性可以自定义图标位置。

```js
import { showImagePreview } from 'vant';

showImagePreview({
images: [
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
],
closeable: true,
});
```

### 监听关闭事件

通过 `onClose` 选项监听图片预览的关闭事件。

```js
import { showToast, showImagePreview } from 'vant';

showImagePreview({
images: [
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
],
onClose() {
showToast('关闭');
},
});
```

### 异步关闭

通过 `beforeClose` 属性可以传入一个回调函数，在图片预览关闭前进行特定操作。

```js
import { showImagePreview } from 'vant';

const instance = showImagePreview({
images: [
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
],
beforeClose: () => false,
});

setTimeout(() => {
// 调用实例上的 close 方法手动关闭图片预览
instance.close();
}, 2000);
```

### 使用 ImagePreview 组件

如果需要在 ImagePreview 内嵌入组件或其他自定义内容，可以直接使用 ImagePreview 组件，并使用 `index` 插槽进行定制。使用前需要通过 `app.use` 等方式注册组件。

```html
<van-image-preview v-model:show="show" :images="images" @change="onChange">
<template v-slot:index>第{{ index + 1 }}页</template>
</van-image-preview>
```

```js
import { ref } from 'vue';

export default {
setup() {
const show = ref(false);
const index = ref(0);
const images = [
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-1.jpeg',
'https://fastly.jsdelivr.net/npm/@vant/assets/apple-2.jpeg',
];
const onChange = (newIndex) => {
index.value = newIndex;
};

return {
show,
index,
images,
onChange,
};
},
};
```

### 使用 image 插槽

当以组件调用的方式使用 ImagePreview 时，可以通过 `image` 插槽来插入自定义的内容，比如展示一个视频内容。在这个例子中，你可以将 `close-on-click-image` 属性设置为 `false`，这样当你点击视频时就不会意外关闭预览了。

```html
<van-image-preview
v-model:show="show"
:images="images"
:close-on-click-image="false"
>
<template #image="{ src }">
<video style="width: 100%;" controls>
<source :src="src" />
</video>
</template>
</van-image-preview>
```

```js
import { ref } from 'vue';

export default {
setup() {
const show = ref(false);
const images = [
'https://www.w3school.com.cn/i/movie.ogg',
'https://www.w3school.com.cn/i/movie.ogg',
'https://www.w3school.com.cn/i/movie.ogg',
];
return {
show,
images,
};
},
};
```

当你通过 `image` 插槽自定义图片时，可以通过插槽的参数绑定 `style` 样式和 `onLoad` 回调函数，这可以让 `<img>` 标签支持图片缩放。

```html
<van-image-preview
v-model:show="show"
:images="images"
:close-on-click-image="false"
>
<template #image="{ src, style, onLoad }">
<img :src="src" :style="[{ width: '100%' }, style]" @load="onLoad" />
</template>
</van-image-preview>
```

## API

### 方法

Vant 中导出了以下 ImagePreview 相关的辅助函数：

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| showImagePreview | 展示一个全屏的图片预览组件 | string[] \| ImagePreviewOptions | ImagePreview 实例 |

### ImagePreviewOptions

调用 `showImagePreview` 方法时，支持传入以下选项：

| 参数名 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| images | 需要预览的图片 URL 数组 | string[] | `[]` |
| startPosition | 图片预览起始位置索引 | number \| string | `0` |
| swipeDuration | 动画时长，单位为`ms` | number \| string | `300` |
| showIndex | 是否显示页码 | boolean | `true` |
| showIndicators | 是否显示轮播指示器 | boolean | `false` |
| loop | 是否开启循环播放 | boolean | `true` |
| doubleScale`v4.7.2` | 是否启用双击缩放手势，禁用后，点击时会立即关闭图片预览 | boolean | `true` |
| onClose | 关闭时的回调函数 | Function | - |
| onChange | 切换图片时的回调函数，回调参数为当前索引 | Function | - |
| onScale | 缩放图片时的回调函数，回调参数为当前索引和当前缩放值组成的对象 | Function | - |
| beforeClose | 关闭前的回调函数，返回`false`可阻止关闭，支持返回 Promise | (active: number) => boolean \| Promise<boolean> | - |
| closeOnPopstate | 是否在页面回退时自动关闭 | boolean | `true` |
| closeOnClickImage`v4.8.3` | 是否在点击图片后关闭图片预览 | boolean | `true` |
| closeOnClickOverlay`v4.6.4` | 是否在点击遮罩层后关闭图片预览 | boolean | `true` |
| vertical`v4.8.6` | 是否开启纵向手势滑动 | boolean | `false` |
| className | 自定义类名 (应用在图片预览的弹出层) | string \| Array \| object | - |
| maxZoom | 手势缩放时，最大缩放比例 | number \| string | `3` |
| minZoom | 手势缩放时，最小缩放比例 | number \| string | `1/3` |
| closeable | 是否显示关闭图标 | boolean | `false` |
| closeIcon | 关闭图标名称或图片链接 | string | `clear` |
| closeIconPosition | 关闭图标位置，可选值为`top-left`<br>`bottom-left``bottom-right` | string | `top-right` |
| transition | 动画类名，等价于transition的`name`属性 | string | `van-fade` |
| overlayClass | 自定义遮罩层类名 | string \| Array \| object | - |
| overlayStyle | 自定义遮罩层样式 | object | - |
| teleport | 指定挂载的节点，等同于 Teleport 组件的to 属性 | string \| Element | - |

### Props

通过组件调用 `ImagePreview` 时，支持以下 Props：

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:show | 是否展示图片预览 | boolean | `false` |
| images | 需要预览的图片 URL 数组 | string[] | `[]` |
| start-position | 图片预览起始位置索引 | number \| string | `0` |
| swipe-duration | 动画时长，单位为 ms | number \| string | `300` |
| show-index | 是否显示页码 | boolean | `true` |
| show-indicators | 是否显示轮播指示器 | boolean | `false` |
| loop | 是否开启循环播放 | boolean | `true` |
| double-scale`v4.7.2` | 是否启用双击缩放手势，禁用后，点击时会立即关闭图片预览 | boolean | `true` |
| before-close | 关闭前的回调函数，返回`false`可阻止关闭，支持返回 Promise | (active: number) => boolean \| Promise<boolean> | - |
| close-on-popstate | 是否在页面回退时自动关闭 | boolean | `true` |
| close-on-click-image`v4.8.3` | 是否在点击图片后关闭图片预览 | boolean | `true` |
| close-on-click-overlay`v4.6.4` | 是否在点击遮罩层后关闭图片预览 | boolean | `true` |
| vertical`v4.8.6` | 是否开启纵向手势滑动 | boolean | `false` |
| class-name | 自定义类名 | string \| Array \| object | - |
| max-zoom | 手势缩放时，最大缩放比例 | number \| string | `3` |
| min-zoom | 手势缩放时，最小缩放比例 | number \| string | `1/3` |
| closeable | 是否显示关闭图标 | boolean | `false` |
| close-icon | 关闭图标名称或图片链接 | string | `clear` |
| close-icon-position | 关闭图标位置，可选值为`top-left`<br>`bottom-left``bottom-right` | string | `top-right` |
| transition | 动画类名，等价于transition的`name`属性 | string | `van-fade` |
| overlay-class | 自定义遮罩层类名 | string \| Array \| object | - |
| overlay-style | 自定义遮罩层样式 | object | - |
| teleport | 指定挂载的节点，等同于 Teleport 组件的to 属性 | string \| Element | - |

### Events

通过组件调用 `ImagePreview` 时，支持以下事件：

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| close | 关闭时触发 | { index: number, url: string } |
| closed | 关闭且且动画结束后触发 | - |
| change | 切换当前图片时触发 | index: number |
| scale | 缩放当前图片时触发 | { index: number, scale: number } |
| long-press | 长按当前图片时触发 | { index: number } |

### 方法

通过组件调用 `ImagePreview` 时，通过 ref 可以获取到 ImagePreview 实例并调用实例方法，详见[组件实例方法](#/zh-CN/advanced-usage#zu-jian-shi-li-fang-fa)。

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| resetScale`4.7.4` | 重置当前图片的缩放比 | - | - |
| swipeTo | 切换到指定位置 | index: number, options?: SwipeToOptions | - |

### 类型定义

组件导出以下类型定义：

```ts
import type {
ImagePreviewProps,
ImagePreviewOptions,
ImagePreviewInstance,
ImagePreviewScaleEventParams,
} from 'vant';
```

`ImagePreviewInstance` 是组件实例的类型，用法如下：

```ts
import { ref } from 'vue';
import type { ImagePreviewInstance } from 'vant';

const imagePreviewRef = ref<ImagePreviewInstance>();

imagePreviewRef.value?.swipeTo(1);
```

### Slots

通过组件调用 `ImagePreview` 时，支持以下插槽：

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| index | 自定义页码内容 | { index: 当前图片的索引 } |
| cover | 自定义覆盖在图片预览上方的内容 | - |
| image | 自定义图片内容 | { src: 当前资源地址, onLoad: 加载图片函数, style: 当前图片样式 } |

### onClose 回调参数

| 参数名 | 说明 | 类型 |
| --- | --- | --- |
| url | 当前图片 URL | string |
| index | 当前图片的索引值 | number |

### onScale 回调参数

| 参数名 | 说明 | 类型 |
| --- | --- | --- |
| index | 当前图片的索引值 | number |
| scale | 当前图片的缩放值 | number |

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-image-preview-index-text-color | var(--van-white) | - |
| --van-image-preview-index-font-size | var(--van-font-size-md) | - |
| --van-image-preview-index-line-height | var(--van-line-height-md) | - |
| --van-image-preview-index-text-shadow | 0 1px 1px var(--van-gray-8) | - |
| --van-image-preview-overlay-background | rgba(0, 0, 0, 0.9) | - |
| --van-image-preview-close-icon-size | 22px | - |
| --van-image-preview-close-icon-color | var(--van-gray-5) | - |
| --van-image-preview-close-icon-margin | var(--van-padding-md) | - |
| --van-image-preview-close-icon-z-index | 1 | - |

## 常见问题

### 在桌面端无法操作组件？

参见[桌面端适配](#/zh-CN/advanced-usage#zhuo-mian-duan-gua-pei)。

### 引用 showImagePreview 时出现编译报错？

如果引用 `showImagePreview` 方法时出现以下报错，说明项目中使用了 `babel-plugin-import` 插件，导致代码被错误编译。

```bash
These dependencies were not found:

* vant/es/show-image-preview in ./src/xxx.js
* vant/es/show-image-preview/style in ./src/xxx.js
```

Vant 从 4.0 版本开始不再支持 `babel-plugin-import` 插件，请参考 [迁移指南](#/zh-CN/migrate-from-v3#yi-chu-babel-plugin-import) 移除该插件。

[浙ICP备2021036118号](https://beian.miit.gov.cn/)