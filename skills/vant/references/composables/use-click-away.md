# useClickAway

# useClickAway

### 介绍

监听点击元素外部的事件。

## 代码演示

### 基本用法

```html
<div ref="root" />
```

```js
import { ref } from 'vue';
import { useClickAway } from '@vant/use';

export default {
setup() {
const root = ref();
useClickAway(root, () => {
console.log('click outside!');
});

return { root };
},
};
```

### 自定义事件

通过 `eventName` 选项可以自定义需要监听的事件类型。

```html
<div ref="root" />
```

```js
import { ref } from 'vue';
import { useClickAway } from '@vant/use';

export default {
setup() {
const root = ref();
useClickAway(
root,
() => {
console.log('touch outside!');
},
{ eventName: 'touchstart' },
);

return { root };
},
};
```

## API

### 类型定义

```ts
type Options = {
eventName?: string;
};

function useClickAway(
target:
| Element
| Ref<Element | undefined>
| Array<Element | Ref<Element | undefined>>,
listener: EventListener,
options?: Options,
): void;
```

### 参数

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| target | 绑定事件的元素，支持传入数组来绑定多个元素 | Element \| Ref<Element> \| Array<Element \| Ref<Element>> | - |
| listener | 点击外部时触发的回调函数 | EventListener | - |
| options | 可选的配置项 | Options | 见下表 |

### Options

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| eventName | 监听的事件类型 | string | `click` |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)