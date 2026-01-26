# AddressList 地址列表

# AddressList 地址列表

### 介绍

展示地址信息列表。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { AddressList } from 'vant';

const app = createApp();
app.use(AddressList);
```

## 代码演示

### 基础用法

```html
<van-address-list
v-model="chosenAddressId"
:list="list"
:disabled-list="disabledList"
disabled-text="以下地址超出配送范围"
default-tag-text="默认"
@add="onAdd"
@edit="onEdit"
/>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const chosenAddressId = ref('1');
const list = [
{
id: '1',
name: '张三',
tel: '13000000000',
address: '浙江省杭州市西湖区文三路 138 号东方通信大厦 7 楼 501 室',
isDefault: true,
},
{
id: '2',
name: '李四',
tel: '1310000000',
address: '浙江省杭州市拱墅区莫干山路 50 号',
},
];
const disabledList = [
{
id: '3',
name: '王五',
tel: '1320000000',
address: '浙江省杭州市滨江区江南大道 15 号',
},
];

const onAdd = () => showToast('新增地址');
const onEdit = (item, index) => showToast('编辑地址:' + index);

return {
list,
onAdd,
onEdit,
disabledList,
chosenAddressId,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中地址的 id，支持多选（类型为`[]`） | number \| string \| number[] \| string[] | - |
| list | 地址列表 | AddressListAddress[] | `[]` |
| disabled-list | 不可配送地址列表 | AddressListAddress[] | `[]` |
| disabled-text | 不可配送提示文案 | string | - |
| switchable | 是否允许切换地址 | boolean | `true` |
| show-add-button | 是否显示底部按钮 | boolean | `true` |
| add-button-text | 底部按钮文字 | string | `新增地址` |
| default-tag-text | 默认地址标签文字 | string | - |
| right-icon`v4.5.0` | 右侧图标名称或图片链接，等同于 Icon 组件的name 属性 | string | `edit` |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| add | 点击新增按钮时触发 | - |
| edit | 点击编辑按钮时触发 | item: AddressListAddress, index: number |
| select | 切换选中的地址时触发 | item: AddressListAddress, index: number |
| edit-disabled | 编辑不可配送的地址时触发 | item: AddressListAddress, index: number |
| select-disabled | 选中不可配送的地址时触发 | item: AddressListAddress, index: number |
| click-item | 点击任意地址时触发 | item: AddressListAddress, index: number, { event } |

### AddressListAddress 数据结构

| 键名 | 说明 | 类型 |
| --- | --- | --- |
| id | 每条地址的唯一标识 | number \| string |
| name | 姓名 | string |
| tel | 手机号 | number \| string |
| address | 详细地址 | string |
| isDefault | 是否为默认地址 | boolean |

### Slots

| 名称 | 说明 | 参数 |
| --- | --- | --- |
| default | 在列表下方插入内容 | - |
| top | 在顶部插入内容 | - |
| item-bottom | 在列表项底部插入内容 | item: AddressListAddress |
| tag | 自定义列表项标签内容 | item: AddressListAddress |

### 类型定义

组件导出以下类型定义：

```ts
import type { AddressListProps, AddressListAddress } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-address-list-padding | var(--van-padding-sm) var(--van-padding-sm) 80px | - |
| --van-address-list-disabled-text-color | var(--van-text-color-2) | - |
| --van-address-list-disabled-text-padding | var(--van-padding-base) * 5 0 var(--van-padding-md) | - |
| --van-address-list-disabled-text-font-size | var(--van-font-size-md) | - |
| --van-address-list-disabled-text-line-height | var(--van-line-height-md) | - |
| --van-address-list-add-button-z-index | 999 | - |
| --van-address-list-item-padding | var(--van-padding-sm) | - |
| --van-address-list-item-text-color | var(--van-text-color) | - |
| --van-address-list-item-disabled-text-color | var(--van-text-color-3) | - |
| --van-address-list-item-font-size | 13px | - |
| --van-address-list-item-line-height | var(--van-line-height-sm) | - |
| --van-address-list-radio-color | var(--van-primary-color) | - |
| --van-address-list-edit-icon-size | 20px | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)