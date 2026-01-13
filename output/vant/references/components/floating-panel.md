# FloatingPanel 浮动面板

# FloatingPanel 浮动面板

### 介绍

浮动在页面底部的面板，可以上下拖动来浏览内容，常用于提供额外的功能或信息。请升级 `vant` 到 >= 4.5.0 版本来使用该组件。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { FloatingPanel } from 'vant';

const app = createApp();
app.use(FloatingPanel);
```

## 代码演示

### 基础用法

FloatingPanel 的默认高度为 `100px`，用户可以拖动来展开面板，使高度达到 `60%` 的屏幕高度。

```html
<van-floating-panel>
<van-cell-group>
<van-cell
v-for="i in 26"
:key="i"
:title="String.fromCharCode(i + 64)"
size="large"
/>
</van-cell-group>
</van-floating-panel>
```

### 自定义锚点

你可以通过 `anchors` 属性来设置 FloatingPanel 的锚点位置，并通过 `v-model:height` 来控制当前面板的显示高度。

比如，使面板的高度在 `100px`、40% 屏幕高度和 70% 屏幕高度三个位置停靠：

```html
<van-floating-panel v-model:height="height" :anchors="anchors">
<div style="text-align: center; padding: 15px">
<p>面板显示高度 {{ height.toFixed(0) }} px</p>
</div>
</van-floating-panel>
```

```js
import { ref } from 'vue';

export default {
setup() {
const anchors = [
100,
Math.round(0.4 * window.innerHeight),
Math.round(0.7 * window.innerHeight),
];
const height = ref(anchors[0]);

return { anchors, height };
},
};
```

### 仅头部拖拽

默认情况下，FloatingPanel 的头部区域和内容区域都可以被拖拽，你可以通过 `content-draggable` 属性来禁用内容区域的拖拽。

```html
<van-floating-panel :content-draggable="false">
<div style="text-align: center; padding: 15px">
<p>内容不可拖拽</p>
</div>
</van-floating-panel>
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:height | 当前面板的显示高度 | number \| string | `0` |
| anchors | 设置自定义锚点, 单位`px` | number[] | `[100, window.innerHeight * 0.6]` |
| duration | 动画时长，单位秒，设置为 0 可以禁用动画 | number \| string | `0.3` |
| content-draggable | 允许拖拽内容容器 | boolean | `true` |
| lock-scroll`v4.6.4` | 当不拖拽时，是否锁定背景滚动 | boolean | `false` |
| safe-area-inset-bottom | 是否开启底部安全区适配 | boolean | `true` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| height-change | 面板显示高度改变且结束拖动后触发 | { height: number } |

### Slots

| Name | Description |
| --- | --- |
| default | 自定义面板内容 |
| header | 自定义面板标头 |

### 类型定义

组件导出以下类型定义：

```ts
import type { FloatingPanelProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| Name | Default Value | Description |
| --- | --- | --- |
| --van-floating-panel-border-radius | 16px | - |
| --van-floating-panel-header-height | 30px | - |
| --van-floating-panel-z-index | 999 | - |
| --van-floating-panel-background | var(--van-background-2) | - |
| --van-floating-panel-bar-width | 20px | - |
| --van-floating-panel-bar-height | 3px | - |
| --van-floating-panel-bar-color | var(--van-gray-5) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)