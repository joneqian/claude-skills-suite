# Coupon 优惠券选择器

# Coupon 优惠券选择器

### 介绍

用于优惠券的兑换和选择。

### 引入

通过以下方式来全局注册组件，更多注册方式请参考[组件注册](#/zh-CN/advanced-usage#zu-jian-zhu-ce)。

```js
import { createApp } from 'vue';
import { CouponCell, CouponList } from 'vant';

const app = createApp();
app.use(CouponCell);
app.use(CouponList);
```

## 代码演示

### 基础用法

```html
<!-- 优惠券单元格 -->
<van-coupon-cell
:coupons="coupons"
:chosen-coupon="chosenCoupon"
@click="showList = true"
/>
<!-- 优惠券列表 -->
<van-popup
v-model:show="showList"
round
position="bottom"
style="height: 90%; padding-top: 4px;"
>
<van-coupon-list
:coupons="coupons"
:chosen-coupon="chosenCoupon"
:disabled-coupons="disabledCoupons"
@change="onChange"
@exchange="onExchange"
/>
</van-popup>
```

```js
import { ref } from 'vue';

export default {
setup() {
const coupon = {
available: 1,
condition: '无门槛\n最多优惠12元',
reason: '',
value: 150,
name: '优惠券名称',
startAt: 1489104000,
endAt: 1514592000,
valueDesc: '1.5',
unitDesc: '元',
};

const coupons = ref([coupon]);
const showList = ref(false);
const chosenCoupon = ref(-1);

const onChange = (index) => {
showList.value = false;
chosenCoupon.value = index;
};
const onExchange = (code) => {
coupons.value.push(coupon);
};

return {
coupons,
showList,
onChange,
onExchange,
chosenCoupon,
disabledCoupons: [coupon],
};
},
};
```

## API

### CouponCell Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| title | 单元格标题 | string | `优惠券` |
| chosen-coupon | 当前选中优惠券的索引 | number \| number[] | `-1` |
| coupons | 可用优惠券列表 | Coupon[] | `[]` |
| editable | 能否切换优惠券 | boolean | `true` |
| border | 是否显示内边框 | boolean | `true` |
| currency | 货币符号 | string | `¥` |

### CouponList Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:code | 当前输入的兑换码 | string | - |
| chosen-coupon | 当前选中优惠券的索引,支持多选（类型为`[]`） | number \| number[] | `-1` |
| coupons | 可用优惠券列表 | CouponInfo[] | `[]` |
| disabled-coupons | 不可用优惠券列表 | CouponInfo[] | `[]` |
| enabled-title | 可用优惠券列表标题 | string | `可使用优惠券` |
| disabled-title | 不可用优惠券列表标题 | string | `不可使用优惠券` |
| exchange-button-text | 兑换按钮文字 | string | `兑换` |
| exchange-button-loading | 是否显示兑换按钮加载动画 | boolean | `false` |
| exchange-button-disabled | 是否禁用兑换按钮 | boolean | `false` |
| exchange-min-length | 兑换码最小长度 | number | `1` |
| displayed-coupon-index | 滚动至特定优惠券位置 | number | - |
| show-close-button | 是否显示列表底部按钮 | boolean | `true` |
| close-button-text | 列表底部按钮文字 | string | `不使用优惠` |
| input-placeholder | 输入框文字提示 | string | `请输入优惠码` |
| show-exchange-bar | 是否展示兑换栏 | boolean | `true` |
| currency | 货币符号 | string | `¥` |
| empty-image | 列表为空时的占位图 | string | - |
| show-count | 是否展示可用 / 不可用数量 | boolean | `true` |

### CouponList Events

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 优惠券切换回调 | index, 选中优惠券的索引 |
| exchange | 兑换优惠券回调 | code, 兑换码 |

### CouponList Slots

| 名称 | 说明 |
| --- | --- |
| list-footer | 优惠券列表底部 |
| disabled-list-footer | 不可用优惠券列表底部 |
| list-button | 自定义底部按钮 |

### CouponInfo 数据结构

| 键名 | 说明 | 类型 |
| --- | --- | --- |
| id | 优惠券 id | string |
| name | 优惠券名称 | string |
| condition | 满减条件 | string |
| startAt | 卡有效开始时间 (时间戳, 单位秒) | number |
| endAt | 卡失效日期 (时间戳, 单位秒) | number |
| description | 描述信息，优惠券可用时展示 | string |
| reason | 不可用原因，优惠券不可用时展示 | string |
| value | 折扣券优惠金额，单位分 | number |
| valueDesc | 折扣券优惠金额文案 | string |
| unitDesc | 单位文案 | string |

### 类型定义

组件导出以下类型定义：

```ts
import type { CouponCellProps, CouponListProps, CouponInfo } from 'vant';
```

## 主题定制

### 样式变量

组件提供了下列 CSS 变量，可用于自定义样式，使用方法请参考 [ConfigProvider 组件](#/zh-CN/config-provider)。

| 名称 | 默认值 | 描述 |
| --- | --- | --- |
| --van-coupon-margin | 0 var(--van-padding-sm) var(--van-padding-sm) | - |
| --van-coupon-content-height | 84px | - |
| --van-coupon-content-padding | 14px 0 | - |
| --van-coupon-content-text-color | var(--van-text-color) | - |
| --van-coupon-background | var(--van-background-2) | - |
| --van-coupon-active-background | var(--van-active-color) | - |
| --van-coupon-radius | var(--van-radius-lg) | - |
| --van-coupon-shadow | 0 0 4px rgba(0, 0, 0, 0.1) | - |
| --van-coupon-head-width | 96px | - |
| --van-coupon-amount-color | var(--van-danger-color) | - |
| --van-coupon-amount-font-size | 30px | - |
| --van-coupon-currency-font-size | 40% | - |
| --van-coupon-name-font-size | var(--van-font-size-md) | - |
| --van-coupon-disabled-text-color | var(--van-text-color-2) | - |
| --van-coupon-description-padding | var(--van-padding-xs) var(--van-padding-md) | - |
| --van-coupon-description-border-color | var(--van-border-color) | - |
| --van-coupon-checkbox-color | var(--van-danger-color) | - |
| --van-coupon-list-background | var(--van-background) | - |
| --van-coupon-list-field-padding | 5px 0 5px var(--van-padding-md) | - |
| --van-coupon-list-exchange-button-height | 32px | - |
| --van-coupon-list-close-button-height | 40px | - |
| --van-coupon-list-empty-tip-color | var(--van-text-color-2) | - |
| --van-coupon-list-empty-tip-font-size | var(--van-font-size-md) | - |
| --van-coupon-list-empty-tip-line-height | var(--van-line-height-md) | - |
| --van-coupon-cell-selected-text-color | var(--van-text-color) | - |

[浙ICP备2021036118号](https://beian.miit.gov.cn/)