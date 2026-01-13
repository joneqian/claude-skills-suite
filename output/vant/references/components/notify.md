# Notify 消息提示

# Notify 消息提示

### 介绍

在页面顶部展示消息提示，支持组件调用和函数调用两种方式。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { Notify } from 'vant';

const app = createApp();
app.use(Notify);
```

### 函数调用

为了便于使用 `Notify`，Vant 提供了一系列辅助函数，通过辅助函数可以快速唤起全局的消息提示。

比如使用 `showNotify` 函数，调用后会直接在页面中渲染对应的提示。

```js
import { showNotify } from 'vant';

showNotify({ message: '提示' });
```

## 代码演示

### 基础用法

```js
import { showNotify, closeNotify } from 'vant';

// 3 秒后自动关闭
showNotify('通知内容');

// 主动关闭
closeNotify();
```

### 通知类型

支持 `primary`、`success`、`warning`、`danger` 四种通知类型，默认为 `danger`。

```js
import { showNotify } from 'vant';

// 主要通知
showNotify({ type: 'primary', message: '通知内容' });

// 成功通知
showNotify({ type: 'success', message: '通知内容' });

// 危险通知
showNotify({ type: 'danger', message: '通知内容' });

// 警告通知
showNotify({ type: 'warning', message: '通知内容' });
```

### 自定义通知

自定义消息通知的颜色、位置和展示时长。

```js
import { showNotify } from 'vant';

showNotify({
message: '自定义颜色',
color: '#ad0000',
background: '#ffe1e1',
});

showNotify({
message: '自定义位置',
position: 'bottom',
});

showNotify({
message: '自定义时长',
duration: 1000,
});
```

### 使用 Notify 组件

如果需要在 Notify 内嵌入组件或其他自定义内容，可以直接使用 Notify 组件，并使用默认插槽进行定制。使用前需要通过 `app.use` 等方式注册组件。

```html
<van-button type="primary" text="组件调用" @click="showNotify" />
<van-notify v-model:show="show" type="success">
<van-icon name="bell" style="margin-right: 4px;" />
<span>通知内容</span>
</van-notify>
```

```js
import { ref } from 'vue';

export default {
setup() {
const show = ref(false);

const showNotify = () => {
show.value = true;
setTimeout(() => {
show.value = false;
}, 2000);
};

return {
show,
showNotify,
};
},
};
```

## API

### 方法

Vant 中导出了以下 Notify 相关的辅助函数：

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| showNotify | 在页面顶部展示 Notify | `NotifyOptions \| string` | notify 实例 |
| closeNotify | 关闭当前展示的 Notify | - | `void` |
| setNotifyDefaultOptions | 修改默认配置，影响所有的`showNotify`调用 | `NotifyOptions` | `void` |
| resetNotifyDefaultOptions | 重置默认配置，影响所有的`showNotify`调用 | - | `void` |

### NotifyOptions

调用 `showNotify` 等方法时，支持传入以下选项：

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| type | 类型，可选值为`primary``success``warning` | NotifyType | `danger` |
| message | 展示文案，支持通过`\n`换行 | string | - |
| duration | 展示时长(ms)，值为 0 时，notify 不会消失 | number \| string | `3000` |
| zIndex | 将组件的 z-index 层级设置为一个固定值 | number \| string | `2000+` |
| position | 弹出位置，可选值为`bottom` | NotifyPosition | `top` |
| color | 字体颜色 | string | `white` |
| background | 背景颜色 | string | - |
| className | 自定义类名 | string \| Array \| object | - |
| lockScroll | 是否锁定背景滚动 | boolean | `false` |
| teleport | 指定挂载的节点，等同于 Teleport 组件的to 属性 | string \| Element | - |
| onClick | 点击时的回调函数 | (event: MouseEvent): void | - |
| onOpened | 完全展示后的回调函数 | () => void | - |
| onClose | 关闭时的回调函数 | () => void | - |

### Props

通过组件调用 `Notify` 时，支持以下 Props：

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:show | 是否显示通知 | boolean | `false` |
| type | 类型，可选值为`primary``success``warning` | NotifyType | `danger` |
| message | 展示文案，支持通过`\n`换行 | string | - |
| z-index | 将组件的 z-index 层级设置为一个固定值 | number \| string | `2000+` |
| position | 弹出位置，可选值为`bottom` | NotifyPosition | `top` |
| color | 字体颜色 | string | `white` |
| background | 背景颜色 | string | - |
| class-name | 自定义类名 | string \| Array \| object | - |
| lock-scroll | 是否锁定背景滚动 | boolean | `false` |
| teleport | 指定挂载的节点，等同于 Teleport 组件的to 属性 | string \| Element | - |

### Events

通过组件调用 `Notify` 时，支持以下事件：

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| click | 点击时的回调函数 | event: MouseEvent |
| close | 关闭时的回调函数 | - |
| opened | 完全展示后的回调函数 | - |

### Slots

通过组件调用 `Notify` 时，支持以下插槽：

| 名称 | 说明 |
| --- | --- |
| default | 自定义内容 |

### 类型定义

组件导出以下类型定义：

```ts
import type {
NotifyType,
NotifyProps,
NotifyOptions,
NotifyPosition,
} from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-notify-text-color | var(--van-white) | - |
| --van-notify-padding | var(--van-padding-xs) var(--van-padding-md) | - |
| --van-notify-font-size | var(--van-font-size-md) | - |
| --van-notify-line-height | var(--van-line-height-md) | - |
| --van-notify-primary-background | var(--van-primary-color) | - |
| --van-notify-success-background | var(--van-success-color) | - |
| --van-notify-danger-background | var(--van-danger-color) | - |
| --van-notify-warning-background | var(--van-warning-color) | - |

## 常见问题

### 引用 showNotify 时出现编译报错？

如果引用 `showNotify` 方法时出现以下报错，说明项目中使用了 `babel-plugin-import` 插件，导致代码被错误编译。

```bash
These dependencies were not found:

* vant/es/show-notify in ./src/xxx.js
* vant/es/show-notify/style in ./src/xxx.js
```

Vant 从 4.0 版本开始不再支持 `babel-plugin-import` 插件，请参考 [迁移指南](#/zh-CN/migrate-from-v3#yi-chu-babel-plugin-import) 移除该插件。

[浙ICP备2021036118号](https://beian.miit.gov.cn/)