# TDesign MiniProgram - Navigation Components

## Navbar

Top navigation bar between status bar and content.

### Registration

```json
{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | String | - | Page title |
| `fixed` | Boolean | `true` | Fixed position |
| `left-arrow` | Boolean | `false` | Show back arrow |
| `delta` | Number | `1` | Back navigation depth |
| `placeholder` | Boolean | `false` | Reserve space when fixed |
| `safe-area-inset-top` | Boolean | `true` | Top safe area |
| `animation` | Boolean | `true` | Enable animation |
| `z-index` | Number | `1` | Stack order |

### Slots

| Slot | Description |
|------|-------------|
| `title` | Custom title |
| `left` | Left content |
| `capsule` | Left capsule area |

### Events

| Event | Description |
|-------|-------------|
| `go-back` | Back arrow clicked |

### Examples

```html
<!-- Basic navbar -->
<t-navbar title="Page Title" left-arrow bind:go-back="goBack" />

<!-- With placeholder -->
<t-navbar title="Fixed Navbar" left-arrow placeholder />

<!-- Custom left -->
<t-navbar title="Custom">
  <view slot="left">
    <t-icon name="home" bind:click="goHome" />
  </view>
</t-navbar>

<!-- No back arrow -->
<t-navbar title="Home Page" />

<!-- Custom title -->
<t-navbar left-arrow>
  <view slot="title" class="custom-title">
    <t-icon name="search" />
    <text>Search</text>
  </view>
</t-navbar>
```

```javascript
Page({
  goBack() {
    wx.navigateBack();
  },

  goHome() {
    wx.switchTab({ url: '/pages/index/index' });
  }
});
```

---

## TabBar

Bottom tab bar for module switching.

### Registration

```json
{
  "usingComponents": {
    "t-tab-bar": "tdesign-miniprogram/tab-bar/tab-bar",
    "t-tab-bar-item": "tdesign-miniprogram/tab-bar-item/tab-bar-item"
  }
}
```

### TabBar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number/Array | - | Active tab value |
| `fixed` | Boolean | `true` | Fixed at bottom |
| `shape` | String | `normal` | Options: `normal`, `round` |
| `theme` | String | `normal` | Options: `normal`, `tag` |
| `safe-area-inset-bottom` | Boolean | `true` | Bottom safe area |
| `z-index` | Number | `1` | Stack order |

### TabBarItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number | - | Item identifier |
| `icon` | String/Object | - | Icon configuration |
| `badge-props` | Object | - | Badge configuration |
| `sub-tab-bar` | Array | - | Secondary menu items |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Tab changed |

### Examples

```html
<!-- Basic tab bar -->
<t-tab-bar value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-bar-item value="home" icon="home">Home</t-tab-bar-item>
  <t-tab-bar-item value="discover" icon="browse">Discover</t-tab-bar-item>
  <t-tab-bar-item value="cart" icon="cart" badge-props="{{ {count: 5} }}">Cart</t-tab-bar-item>
  <t-tab-bar-item value="profile" icon="user">Profile</t-tab-bar-item>
</t-tab-bar>

<!-- Round shape -->
<t-tab-bar value="{{activeTab}}" shape="round" bind:change="onTabChange">
  <t-tab-bar-item value="0" icon="home">Home</t-tab-bar-item>
  <t-tab-bar-item value="1" icon="browse">Browse</t-tab-bar-item>
  <t-tab-bar-item value="2" icon="user">Me</t-tab-bar-item>
</t-tab-bar>

<!-- Icon only -->
<t-tab-bar value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-bar-item value="0" icon="home" />
  <t-tab-bar-item value="1" icon="browse" />
  <t-tab-bar-item value="2" icon="user" />
</t-tab-bar>
```

```javascript
Page({
  data: { activeTab: 'home' },

  onTabChange(e) {
    const { value } = e.detail;
    this.setData({ activeTab: value });

    // Navigate if needed
    const routes = {
      home: '/pages/home/index',
      discover: '/pages/discover/index',
      profile: '/pages/profile/index'
    };

    if (routes[value]) {
      wx.switchTab({ url: routes[value] });
    }
  }
});
```

---

## Tabs

Tab navigation for content switching.

### Registration

```json
{
  "usingComponents": {
    "t-tabs": "tdesign-miniprogram/tabs/tabs",
    "t-tab-panel": "tdesign-miniprogram/tab-panel/tab-panel"
  }
}
```

### Tabs Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number | - | Active tab |
| `default-value` | String/Number | - | Default active (uncontrolled) |
| `theme` | String | `line` | Options: `line`, `tag`, `card` |
| `swipeable` | Boolean | `true` | Enable swipe |
| `sticky` | Boolean | `false` | Sticky header |
| `show-bottom-line` | Boolean | `true` | Show indicator line |
| `space-evenly` | Boolean | `true` | Equal tab spacing |
| `animation` | Object | - | Animation config |

### TabPanel Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number | - | Panel identifier |
| `label` | String | - | Tab label |
| `disabled` | Boolean | `false` | Disable tab |
| `icon` | String/Object | - | Tab icon |
| `badge-props` | Object | - | Badge config |
| `lazy` | Boolean | `false` | Lazy load content |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Tab changed |
| `click` | `{value}` | Tab clicked |
| `scroll` | `{scrollTop}` | Page scrolled (sticky mode) |

### Examples

```html
<!-- Basic tabs -->
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="Tab 1" value="0">Content 1</t-tab-panel>
  <t-tab-panel label="Tab 2" value="1">Content 2</t-tab-panel>
  <t-tab-panel label="Tab 3" value="2">Content 3</t-tab-panel>
</t-tabs>

<!-- Tag theme -->
<t-tabs value="{{activeTab}}" theme="tag" bind:change="onTabChange">
  <t-tab-panel label="All" value="all">All items</t-tab-panel>
  <t-tab-panel label="Pending" value="pending">Pending items</t-tab-panel>
  <t-tab-panel label="Completed" value="completed">Completed items</t-tab-panel>
</t-tabs>

<!-- With icons -->
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="Home" value="0" icon="home">Home content</t-tab-panel>
  <t-tab-panel label="List" value="1" icon="view-list">List content</t-tab-panel>
</t-tabs>

<!-- With badges -->
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="Messages" value="0" badge-props="{{ {count: 8} }}">Messages</t-tab-panel>
  <t-tab-panel label="Notifications" value="1" badge-props="{{ {dot: true} }}">Notifications</t-tab-panel>
</t-tabs>

<!-- Sticky tabs -->
<t-tabs value="{{activeTab}}" sticky bind:change="onTabChange">
  <t-tab-panel label="Section 1" value="0">Long content 1</t-tab-panel>
  <t-tab-panel label="Section 2" value="1">Long content 2</t-tab-panel>
</t-tabs>

<!-- Lazy loading -->
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="Tab 1" value="0" lazy>
    <expensive-component />
  </t-tab-panel>
  <t-tab-panel label="Tab 2" value="1" lazy>
    <another-expensive-component />
  </t-tab-panel>
</t-tabs>
```

---

## Steps

Progress steps indicator.

### Registration

```json
{
  "usingComponents": {
    "t-steps": "tdesign-miniprogram/steps/steps",
    "t-step-item": "tdesign-miniprogram/step-item/step-item"
  }
}
```

### Steps Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `current` | String/Number | - | Current step |
| `default-current` | String/Number | - | Default current (uncontrolled) |
| `layout` | String | `horizontal` | Options: `horizontal`, `vertical` |
| `readonly` | Boolean | `false` | Disable interaction |
| `theme` | String | `default` | Options: `default`, `dot` |
| `separator` | String | `line` | Options: `line`, `dashed`, `arrow` |

### StepItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | String | - | Step title |
| `content` | String | - | Step description |
| `icon` | String/Object | - | Custom icon |
| `status` | String | - | Options: `default`, `process`, `finish`, `error` |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{current, previous}` | Step changed |

### Examples

```html
<!-- Basic steps -->
<t-steps current="{{currentStep}}">
  <t-step-item title="Step 1" content="Description" />
  <t-step-item title="Step 2" content="Description" />
  <t-step-item title="Step 3" content="Description" />
</t-steps>

<!-- Vertical layout -->
<t-steps current="{{currentStep}}" layout="vertical">
  <t-step-item title="Order Placed" content="2024-01-15 10:30" />
  <t-step-item title="Payment Confirmed" content="2024-01-15 10:35" />
  <t-step-item title="Shipping" content="In progress" />
  <t-step-item title="Delivered" content="Pending" />
</t-steps>

<!-- Dot theme -->
<t-steps current="{{currentStep}}" theme="dot">
  <t-step-item title="Start" />
  <t-step-item title="Progress" />
  <t-step-item title="Complete" />
</t-steps>

<!-- With error status -->
<t-steps current="{{1}}">
  <t-step-item title="Step 1" status="finish" />
  <t-step-item title="Step 2" status="error" content="Payment failed" />
  <t-step-item title="Step 3" />
</t-steps>
```

---

## Indexes

Index navigation for alphabetical lists.

### Registration

```json
{
  "usingComponents": {
    "t-indexes": "tdesign-miniprogram/indexes/indexes",
    "t-indexes-anchor": "tdesign-miniprogram/indexes-anchor/indexes-anchor"
  }
}
```

### Indexes Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `index-list` | Array | `A-Z` | Index list |
| `sticky` | Boolean | `true` | Sticky headers |
| `sticky-offset` | Number | `0` | Sticky offset |
| `height` | String/Number | - | Container height |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `select` | `{index}` | Index selected |

### Examples

```html
<t-indexes bind:select="onIndexSelect">
  <t-indexes-anchor index="A">
    <t-cell title="Alice" />
    <t-cell title="Adam" />
  </t-indexes-anchor>
  <t-indexes-anchor index="B">
    <t-cell title="Bob" />
    <t-cell title="Betty" />
  </t-indexes-anchor>
  <t-indexes-anchor index="C">
    <t-cell title="Charlie" />
    <t-cell title="Carol" />
  </t-indexes-anchor>
</t-indexes>
```

---

## BackTop

Back to top button.

### Registration

```json
{
  "usingComponents": {
    "t-back-top": "tdesign-miniprogram/back-top/back-top"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `fixed` | Boolean | `true` | Fixed position |
| `icon` | String/Object | `backtop` | Custom icon |
| `text` | String | - | Button text |
| `theme` | String | `round` | Options: `round`, `half-round`, `round-dark`, `half-round-dark` |
| `visibility-height` | Number | `200` | Scroll height to show |

### Events

| Event | Description |
|-------|-------------|
| `to-top` | Scroll to top triggered |

### Examples

```html
<!-- Basic back-top -->
<t-back-top />

<!-- With text -->
<t-back-top text="Top" theme="half-round" />

<!-- Custom visibility -->
<t-back-top visibility-height="{{500}}" />

<!-- Custom icon -->
<t-back-top icon="arrow-up" />
```

---

## DropdownMenu

Dropdown navigation menu.

### Registration

```json
{
  "usingComponents": {
    "t-dropdown-menu": "tdesign-miniprogram/dropdown-menu/dropdown-menu",
    "t-dropdown-item": "tdesign-miniprogram/dropdown-item/dropdown-item"
  }
}
```

### DropdownMenu Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `show-overlay` | Boolean | `true` | Show overlay |
| `close-on-click-overlay` | Boolean | `true` | Close on overlay click |
| `z-index` | Number | `11600` | Stack order |
| `duration` | Number | `200` | Animation duration |

### DropdownItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number/Array | - | Selected value |
| `label` | String | - | Item label |
| `options` | Array | `[]` | Options list |
| `disabled` | Boolean | `false` | Disable item |
| `multiple` | Boolean | `false` | Multi-select mode |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Selection changed |
| `confirm` | `{value}` | Confirmed (multiple mode) |
| `reset` | - | Reset clicked |

### Examples

```html
<t-dropdown-menu>
  <t-dropdown-item
    value="{{filter1}}"
    label="Sort"
    options="{{sortOptions}}"
    bind:change="onSortChange"
  />
  <t-dropdown-item
    value="{{filter2}}"
    label="Category"
    options="{{categoryOptions}}"
    bind:change="onCategoryChange"
  />
</t-dropdown-menu>
```

```javascript
Page({
  data: {
    filter1: 'newest',
    filter2: 'all',
    sortOptions: [
      { label: 'Newest', value: 'newest' },
      { label: 'Price: Low to High', value: 'price_asc' },
      { label: 'Price: High to Low', value: 'price_desc' }
    ],
    categoryOptions: [
      { label: 'All', value: 'all' },
      { label: 'Electronics', value: 'electronics' },
      { label: 'Clothing', value: 'clothing' }
    ]
  },

  onSortChange(e) {
    this.setData({ filter1: e.detail.value });
  },

  onCategoryChange(e) {
    this.setData({ filter2: e.detail.value });
  }
});
```
