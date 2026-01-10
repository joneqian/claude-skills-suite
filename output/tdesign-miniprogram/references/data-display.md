# TDesign MiniProgram - Data Display Components

## Avatar

Display user profile images and information.

### Registration

```json
{
  "usingComponents": {
    "t-avatar": "tdesign-miniprogram/avatar/avatar",
    "t-avatar-group": "tdesign-miniprogram/avatar-group/avatar-group"
  }
}
```

### Avatar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `image` | String | - | Avatar image URL |
| `icon` | String/Object | - | Icon configuration |
| `shape` | String | `circle` | Options: `circle`, `round` |
| `size` | String | `medium` | Options: `small`, `medium`, `large` or custom (e.g., `48px`) |
| `alt` | String | - | Fallback text on image error |
| `badge-props` | Object | - | Badge configuration |
| `hide-on-load-failed` | Boolean | - | Hide on image load failure |

### AvatarGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `max` | Number | - | Max visible avatars |
| `cascading` | String | `left-up` | Stacking direction: `left-up`, `right-up` |
| `collapse-avatar` | String | - | Custom overflow text (default: `+N`) |
| `size` | String | - | Size for all avatars |
| `shape` | String | - | Shape for all avatars |

### Events

| Event | Description |
|-------|-------------|
| `error` | Image load failed |
| `collapsed-item-click` | Overflow indicator clicked |

### Examples

```html
<!-- Basic avatar -->
<t-avatar image="{{userAvatar}}" />

<!-- With fallback -->
<t-avatar image="{{userAvatar}}" alt="User" />

<!-- Icon avatar -->
<t-avatar icon="user" />

<!-- Different sizes -->
<t-avatar image="{{url}}" size="small" />
<t-avatar image="{{url}}" size="large" />
<t-avatar image="{{url}}" size="80px" />

<!-- With badge -->
<t-avatar image="{{url}}" badge-props="{{ {count: 5} }}" />

<!-- Avatar group -->
<t-avatar-group max="{{3}}">
  <t-avatar image="{{url1}}" />
  <t-avatar image="{{url2}}" />
  <t-avatar image="{{url3}}" />
  <t-avatar image="{{url4}}" />
</t-avatar-group>
```

---

## Image

Enhanced image display with loading and error states.

### Registration

```json
{
  "usingComponents": {
    "t-image": "tdesign-miniprogram/image/image"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | String | - | Image URL (required) |
| `mode` | String | `scaleToFill` | Scaling mode (same as native image) |
| `shape` | String | `square` | Options: `circle`, `round`, `square` |
| `width` | String/Number | - | Image width |
| `height` | String/Number | - | Image height |
| `lazy` | Boolean | `false` | Enable lazy loading |
| `loading` | String | `default` | Loading placeholder |
| `error` | String | `default` | Error fallback |
| `webp` | Boolean | `false` | WebP format support |

### Events

| Event | Description |
|-------|-------------|
| `load` | Image loaded successfully |
| `error` | Image load failed |

### Slots

| Slot | Description |
|------|-------------|
| `loading` | Custom loading placeholder |
| `error` | Custom error content |

### Examples

```html
<!-- Basic image -->
<t-image src="{{imageUrl}}" width="200" height="200" />

<!-- With shape -->
<t-image src="{{imageUrl}}" shape="circle" width="100" height="100" />
<t-image src="{{imageUrl}}" shape="round" width="200" height="150" />

<!-- Lazy loading -->
<t-image src="{{imageUrl}}" lazy width="300" height="200" />

<!-- Custom loading/error -->
<t-image src="{{imageUrl}}" width="200" height="200">
  <view slot="loading">Loading...</view>
  <view slot="error">Failed to load</view>
</t-image>

<!-- Different modes -->
<t-image src="{{url}}" mode="aspectFill" width="200" height="200" />
<t-image src="{{url}}" mode="aspectFit" width="200" height="200" />
```

---

## Swiper

Carousel/slider component.

### Registration

```json
{
  "usingComponents": {
    "t-swiper": "tdesign-miniprogram/swiper/swiper",
    "t-swiper-nav": "tdesign-miniprogram/swiper-nav/swiper-nav"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `list` | Array | - | Image/content array |
| `current` | Number | `0` | Active index |
| `autoplay` | Boolean | `true` | Enable auto play |
| `interval` | Number | `5000` | Autoplay interval (ms) |
| `duration` | Number | `300` | Animation duration (ms) |
| `loop` | Boolean | `true` | Enable circular loop |
| `direction` | String | `horizontal` | Options: `horizontal`, `vertical` |
| `height` | String/Number | `192` | Swiper height |
| `navigation` | Boolean/Object | `true` | Navigator configuration |

### Navigation Types

- `dots` - Dot indicators
- `dots-bar` - Bar-style dots
- `fraction` - Number fraction (1/5)
- `controls` - Prev/next buttons

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{current, source}` | Slide changed |
| `click` | `{index}` | Item clicked |
| `image-load` | - | Image loaded |

### Examples

```html
<!-- Basic swiper -->
<t-swiper list="{{images}}" />

<!-- With options -->
<t-swiper
  list="{{images}}"
  autoplay="{{true}}"
  interval="{{3000}}"
  loop="{{true}}"
  height="{{400}}"
/>

<!-- Dot navigation -->
<t-swiper list="{{images}}" navigation="{{ {type: 'dots'} }}" />

<!-- Fraction navigation -->
<t-swiper list="{{images}}" navigation="{{ {type: 'fraction'} }}" />

<!-- Vertical direction -->
<t-swiper list="{{images}}" direction="vertical" height="{{500}}" />

<!-- Custom navigation -->
<t-swiper list="{{images}}" current="{{currentIndex}}" bind:change="onSwiperChange">
  <t-swiper-nav slot="nav" type="dots" />
</t-swiper>
```

```javascript
Page({
  data: {
    images: [
      'https://example.com/image1.jpg',
      'https://example.com/image2.jpg',
      'https://example.com/image3.jpg'
    ]
  }
});
```

---

## Tag

Label tags for categorization.

### Registration

```json
{
  "usingComponents": {
    "t-tag": "tdesign-miniprogram/tag/tag"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | String | - | Tag text |
| `theme` | String | `default` | Options: `default`, `primary`, `warning`, `danger`, `success` |
| `variant` | String | `dark` | Options: `dark`, `light`, `outline`, `light-outline` |
| `size` | String | `medium` | Options: `small`, `medium`, `large` |
| `shape` | String | `square` | Options: `square`, `round`, `mark` |
| `closable` | Boolean | `false` | Show close button |
| `disabled` | Boolean | `false` | Disable tag |
| `icon` | String/Object | - | Left icon |
| `max-width` | String/Number | - | Max width (truncate with ellipsis) |

### Events

| Event | Description |
|-------|-------------|
| `click` | Tag clicked |
| `close` | Close button clicked |

### Examples

```html
<!-- Basic tags -->
<t-tag content="Default" />
<t-tag content="Primary" theme="primary" />
<t-tag content="Success" theme="success" />
<t-tag content="Warning" theme="warning" />
<t-tag content="Danger" theme="danger" />

<!-- Variants -->
<t-tag content="Dark" theme="primary" variant="dark" />
<t-tag content="Light" theme="primary" variant="light" />
<t-tag content="Outline" theme="primary" variant="outline" />

<!-- Shapes -->
<t-tag content="Square" shape="square" />
<t-tag content="Round" shape="round" />
<t-tag content="Mark" shape="mark" />

<!-- Closable -->
<t-tag content="Closable" closable bind:close="onClose" />

<!-- With icon -->
<t-tag content="Location" icon="location" />
```

---

## Progress

Progress indicator.

### Registration

```json
{
  "usingComponents": {
    "t-progress": "tdesign-miniprogram/progress/progress"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `percentage` | Number | `0` | Progress percentage (0-100) |
| `theme` | String | `line` | Options: `line`, `plump`, `circle` |
| `status` | String | - | Options: `success`, `warning`, `error`, `active` |
| `color` | String/Array/Object | - | Progress bar color |
| `track-color` | String | - | Track background color |
| `stroke-width` | String/Number | - | Bar thickness |
| `label` | Boolean/String | `true` | Show/custom label |

### Examples

```html
<!-- Basic progress -->
<t-progress percentage="{{60}}" />

<!-- With status -->
<t-progress percentage="{{100}}" status="success" />
<t-progress percentage="{{30}}" status="error" />

<!-- Circle theme -->
<t-progress theme="circle" percentage="{{75}}" />

<!-- Custom color -->
<t-progress percentage="{{50}}" color="#1890ff" />

<!-- Gradient color -->
<t-progress percentage="{{80}}" color="{{ {from: '#00ff00', to: '#0000ff'} }}" />

<!-- Custom label -->
<t-progress percentage="{{45}}" label="Loading..." />
```

---

## Skeleton

Loading placeholder.

### Registration

```json
{
  "usingComponents": {
    "t-skeleton": "tdesign-miniprogram/skeleton/skeleton"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `loading` | Boolean | `true` | Show skeleton |
| `animation` | String | `none` | Options: `none`, `gradient`, `flashed` |
| `theme` | String | `text` | Options: `text`, `paragraph`, `avatar`, `avatar-text`, `image`, `image-text` |
| `row-col` | Array | - | Custom row/column structure |

### Examples

```html
<!-- Text skeleton -->
<t-skeleton loading="{{isLoading}}" theme="text" />

<!-- Paragraph skeleton -->
<t-skeleton loading="{{isLoading}}" theme="paragraph" />

<!-- Avatar with text -->
<t-skeleton loading="{{isLoading}}" theme="avatar-text" animation="gradient" />

<!-- Custom structure -->
<t-skeleton loading="{{isLoading}}" row-col="{{rowCol}}">
  <view>Actual content here</view>
</t-skeleton>
```

```javascript
Page({
  data: {
    isLoading: true,
    rowCol: [
      { width: '100%', height: '200rpx' },
      [{ width: '40%' }, { width: '60%' }],
      { width: '100%' }
    ]
  }
});
```

---

## Empty

Empty state display.

### Registration

```json
{
  "usingComponents": {
    "t-empty": "tdesign-miniprogram/empty/empty"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `description` | String | - | Description text |
| `image` | String/Object | - | Image URL or icon |
| `action` | Object | - | Action button props |

### Examples

```html
<!-- Basic empty -->
<t-empty description="No data" />

<!-- With action -->
<t-empty
  description="No results found"
  action="{{ {content: 'Refresh', theme: 'primary'} }}"
  bind:action-click="onRefresh"
/>

<!-- Custom image -->
<t-empty description="No orders" image="/images/empty-order.png" />
```

---

## CountDown

Countdown timer.

### Registration

```json
{
  "usingComponents": {
    "t-count-down": "tdesign-miniprogram/count-down/count-down"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `time` | Number | - | Countdown time in ms |
| `format` | String | `HH:mm:ss` | Time format |
| `auto-start` | Boolean | `true` | Start automatically |
| `millisecond` | Boolean | `false` | Show milliseconds |
| `size` | String | `medium` | Options: `small`, `medium`, `large` |
| `theme` | String | `default` | Options: `default`, `round`, `square` |
| `split-with-unit` | Boolean | `false` | Split with unit labels |

### Events

| Event | Description |
|-------|-------------|
| `finish` | Countdown finished |
| `change` | Time changed |

### Methods

```javascript
const countDown = this.selectComponent('#countdown');
countDown.start();  // Start
countDown.pause();  // Pause
countDown.reset();  // Reset
```

### Examples

```html
<!-- Basic countdown -->
<t-count-down time="{{3600000}}" />

<!-- Custom format -->
<t-count-down time="{{time}}" format="DD天HH:mm:ss" />

<!-- With milliseconds -->
<t-count-down time="{{time}}" format="HH:mm:ss:SSS" millisecond />

<!-- Manual control -->
<t-count-down id="countdown" time="{{60000}}" auto-start="{{false}}" bind:finish="onFinish" />
<t-button bind:tap="startCountdown">Start</t-button>
```
