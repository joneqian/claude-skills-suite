# ContactList 联系人列表

# ContactList 联系人列表

### 介绍

展示联系人列表。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { ContactList } from 'vant';

const app = createApp();
app.use(ContactList);
```

## 代码演示

### 基础用法

```html
<van-contact-list
v-model="chosenContactId"
:list="list"
default-tag-text="默认"
@add="onAdd"
@edit="onEdit"
@select="onSelect"
/>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const chosenContactId = ref('1');
const list = ref([
{
id: '1',
name: '张三',
tel: '13000000000',
isDefault: true,
},
{
id: '2',
name: '李四',
tel: '1310000000',
},
]);

const onAdd = () => showToast('新增');
const onEdit = (contact) => showToast('编辑' + contact.id);
const onSelect = (contact) => showToast('选择' + contact.id);

return {
list,
onAdd,
onEdit,
onSelect,
chosenContactId,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model | 当前选中联系人的 id | number \| string | - |
| list | 联系人列表 | ContactListItem[] | `[]` |
| add-text | 新建按钮文案 | string | `新建联系人` |
| default-tag-text | 默认联系人标签文案 | string | - |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| add | 点击新增按钮时触发 | - |
| edit | 点击编辑按钮时触发 | contact: ContactListItem，index: number |
| select | 切换选中的联系人时触发 | contact: ContactListItem，index: number |

### ContactListItem 数据结构

| 键名 | 说明 | 类型 |
| --- | --- | --- |
| id | 每位联系人的唯一标识 | number \| string |
| name | 联系人姓名 | string |
| tel | 联系人手机号 | number \| string |
| isDefault | 是否为默认联系人 | boolean \| undefined |

### 类型定义

组件导出以下类型定义：

```ts
import type { ContactListItem, ContactListProps } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-contact-list-padding | var(--van-padding-sm) var(--van-padding-sm) 80px | - |
| --van-contact-list-edit-icon-size | 16px | - |
| --van-contact-list-add-button-z-index | 999 | - |
| --van-contact-list-radio-color | var(--van-primary-color) | - |
| --van-contact-list-item-padding | var(--van-padding-md) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)