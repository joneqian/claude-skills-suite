# AddressEdit 地址编辑

# AddressEdit 地址编辑

### 介绍

地址编辑组件，用于新建、更新、删除地址信息。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { AddressEdit } from 'vant';

const app = createApp();
app.use(AddressEdit);
```

## 代码演示

### 基础用法

```html
<van-address-edit
:area-list="areaList"
show-delete
show-set-default
show-search-result
:search-result="searchResult"
:area-columns-placeholder="['请选择', '请选择', '请选择']"
@save="onSave"
@delete="onDelete"
@change-detail="onChangeDetail"
/>
```

```js
import { ref } from 'vue';
import { showToast } from 'vant';

export default {
setup() {
const searchResult = ref([]);

const onSave = () => showToast('save');
const onDelete = () => showToast('delete');
const onChangeDetail = (val) => {
if (val) {
searchResult.value = [
{
name: '黄龙万科中心',
address: '杭州市西湖区',
},
];
} else {
searchResult.value = [];
}
};

return {
onSave,
onDelete,
areaList,
searchResult,
onChangeDetail,
};
},
};
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| area-list | 地区列表 | object | - |
| area-columns-placeholder | 地区选择列占位提示文字 | string[] | `[]` |
| area-placeholder | 地区输入框占位提示文字 | string | `选择省 / 市 / 区` |
| address-info | 地址信息初始值 | AddressEditInfo | `{}` |
| search-result | 详细地址搜索结果 | AddressEditSearchItem[] | `[]` |
| show-delete | 是否显示删除按钮 | boolean | `false` |
| show-set-default | 是否显示默认地址栏 | boolean | `false` |
| show-search-result | 是否显示搜索结果 | boolean | `false` |
| show-area | 是否显示地区 | boolean | `true` |
| show-detail | 是否显示详细地址 | boolean | `true` |
| disable-area | 是否禁用地区选择 | boolean | `false` |
| save-button-text | 保存按钮文字 | string | `保存` |
| delete-button-text | 删除按钮文字 | string | `删除` |
| detail-rows | 详细地址输入框行数 | number \| string | `1` |
| detail-maxlength | 详细地址最大长度 | number \| string | `200` |
| is-saving | 是否显示保存按钮加载动画 | boolean | `false` |
| is-deleting | 是否显示删除按钮加载动画 | boolean | `false` |
| tel-validator | 手机号格式校验函数 | (val: string) => boolean | - |
| tel-maxlength | 手机号最大长度 | number \| string | - |
| validator | 自定义校验函数 | (key: string, val: string) => string | - |

### Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| save | 点击保存按钮时触发 | info: AddressEditInfo |
| focus | 输入框聚焦时触发 | key: string |
| change`v4.7.0` | 仅`name`和`tel`输入框值改变触发 | {key: string, value: string} |
| delete | 确认删除地址时触发 | info: AddressEditInfo |
| select-search | 选中搜索结果时触发 | value: string |
| click-area | 点击收件地区时触发 | - |
| change-area | 修改收件地区时触发 | selectedOptions: PickerOption[] |
| change-detail | 修改详细地址时触发 | value: string |
| change-default | 切换是否使用默认地址时触发 | checked: boolean |

### Slots

| 名称 | 说明 |
| --- | --- |
| default | 在邮政编码下方插入内容 |

### 方法

通过 ref 可以获取到 AddressEdit 实例并调用实例方法，详见[组件实例方法](#/zh-CN/advanced-usage#zu-jian-shi-li-fang-fa)。

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| setAddressDetail | 设置详细地址 | addressDetail: string | - |
| setAreaCode | 设置地区编号 | code: string | - |

### 类型定义

组件导出以下类型定义：

```ts
import type {
AddressEditInfo,
AddressEditProps,
AddressEditInstance,
AddressEditSearchItem,
} from 'vant';
```

`AddressEditInstance` 是组件实例的类型，用法如下：

```ts
import { ref } from 'vue';
import type { AddressEditInstance } from 'vant';

const addressEditRef = ref<AddressEditInstance>();

addressEditRef.value?.setAddressDetail('');
```

### AddressEditInfo 数据格式

注意：`AddressEditInfo` 仅作为初始值传入，表单最终内容可以在 save 事件中获取。

| key | 说明 | 类型 |
| --- | --- | --- |
| name | 姓名 | string |
| tel | 手机号 | string |
| province | 省份 | string |
| city | 城市 | string |
| county | 区县 | string |
| addressDetail | 详细地址 | string |
| areaCode | 地区编码，通过省市区选择获取（必填） | string |
| isDefault | 是否为默认地址 | boolean |

### AddressEditSearchItem 数据格式

| key | 说明 | 类型 |
| --- | --- | --- |
| name | 地名 | string |
| address | 详细地址 | string |

### 省市县列表数据格式

请参考 [Area 省市区选择](#/zh-CN/area) 组件。

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-address-edit-padding | var(--van-padding-sm) | - |
| --van-address-edit-buttons-padding | var(--van-padding-xl) var(--van-padding-base) | - |
| --van-address-edit-button-margin-bottom | var(--van-padding-sm) | - |
| --van-address-edit-button-font-size | var(--van-font-size-lg) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)