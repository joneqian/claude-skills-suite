# TDesign MiniProgram - Feedback Components

## Dialog

Modal dialog for important notifications or user confirmations.

### Registration

```json
{
  "usingComponents": {
    "t-dialog": "tdesign-miniprogram/dialog/dialog"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `visible` | Boolean | `false` | Control visibility |
| `title` | String | - | Dialog title |
| `content` | String | - | Dialog content |
| `confirm-btn` | String/Object | - | Confirm button config |
| `cancel-btn` | String/Object | - | Cancel button config |
| `close-btn` | Boolean/Object | `false` | Show close button |
| `button-layout` | String | `horizontal` | Options: `horizontal`, `vertical` |
| `close-on-overlay-click` | Boolean | `false` | Close on overlay click |
| `show-overlay` | Boolean | `true` | Show overlay |
| `z-index` | Number | `11500` | Stack order |

### Slots

| Slot | Description |
|------|-------------|
| `title` | Custom title |
| `content` | Custom content |
| `confirm-btn` | Custom confirm button |
| `cancel-btn` | Custom cancel button |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `confirm` | - | Confirm clicked |
| `cancel` | - | Cancel clicked |
| `close` | `{trigger}` | Dialog closed |
| `overlay-click` | - | Overlay clicked |

### Examples

```html
<!-- Basic dialog -->
<t-dialog
  visible="{{showDialog}}"
  title="Confirmation"
  content="Are you sure you want to delete this item?"
  confirm-btn="Delete"
  cancel-btn="Cancel"
  bind:confirm="onConfirm"
  bind:cancel="onCancel"
/>

<!-- Alert dialog (no cancel) -->
<t-dialog
  visible="{{showAlert}}"
  title="Notice"
  content="Your session has expired."
  confirm-btn="OK"
  bind:confirm="onAlertConfirm"
/>

<!-- Custom buttons -->
<t-dialog
  visible="{{showDialog}}"
  title="Choose Action"
  confirm-btn="{{ {content: 'Accept', theme: 'primary'} }}"
  cancel-btn="{{ {content: 'Decline', variant: 'outline'} }}"
/>

<!-- Vertical layout -->
<t-dialog
  visible="{{showDialog}}"
  title="Options"
  button-layout="vertical"
  confirm-btn="Primary Action"
  cancel-btn="Secondary Action"
/>

<!-- With input (slot) -->
<t-dialog visible="{{showInputDialog}}" title="Enter Name">
  <t-input slot="content" placeholder="Your name" value="{{name}}" bind:change="onNameChange" />
</t-dialog>
```

```javascript
Page({
  data: { showDialog: false },

  showConfirm() {
    this.setData({ showDialog: true });
  },

  onConfirm() {
    this.setData({ showDialog: false });
    // Perform action
  },

  onCancel() {
    this.setData({ showDialog: false });
  }
});
```

---

## Toast

Lightweight non-intrusive notifications.

### Registration

```json
{
  "usingComponents": {
    "t-toast": "tdesign-miniprogram/toast/toast"
  }
}
```

### Props (via function call)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `message` | String | - | Toast message |
| `theme` | String | - | Options: `loading`, `success`, `warning`, `error` |
| `duration` | Number | `2000` | Display duration (ms) |
| `icon` | String/Object | - | Custom icon |
| `placement` | String | `middle` | Options: `top`, `middle`, `bottom` |
| `direction` | String | `row` | Icon layout: `row`, `column` |
| `show-overlay` | Boolean | `false` | Show background overlay |
| `prevent-scroll-through` | Boolean | `false` | Block scroll/tap |

### API Usage

```javascript
import Toast from 'tdesign-miniprogram/toast/index';

// Basic toast
Toast({
  context: this,
  selector: '#toast',
  message: 'This is a toast'
});

// Success toast
Toast({
  context: this,
  selector: '#toast',
  message: 'Operation successful',
  theme: 'success',
  duration: 3000
});

// Loading toast
const loadingToast = Toast({
  context: this,
  selector: '#toast',
  message: 'Loading...',
  theme: 'loading',
  duration: -1  // Won't auto close
});

// Close loading toast
loadingToast.close();

// Error toast
Toast({
  context: this,
  selector: '#toast',
  message: 'Something went wrong',
  theme: 'error'
});
```

### Template Usage

```html
<!-- Add toast component to page -->
<t-toast id="toast" />

<!-- Multiple toasts -->
<t-toast id="successToast" />
<t-toast id="errorToast" />
```

---

## Popup

Slide-in overlay container.

### Registration

```json
{
  "usingComponents": {
    "t-popup": "tdesign-miniprogram/popup/popup"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `visible` | Boolean | `false` | Control visibility |
| `placement` | String | `top` | Options: `top`, `left`, `right`, `bottom`, `center` |
| `close-btn` | Boolean | - | Show close button |
| `close-on-overlay-click` | Boolean | `true` | Close on overlay click |
| `show-overlay` | Boolean | `true` | Show overlay |
| `prevent-scroll-through` | Boolean | `true` | Prevent background scroll |
| `duration` | Number | `240` | Animation duration (ms) |
| `z-index` | Number | `11500` | Stack order |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `visible-change` | `{visible, trigger}` | Visibility changed |

### Examples

```html
<!-- Bottom popup -->
<t-popup visible="{{showPopup}}" placement="bottom" bind:visible-change="onPopupChange">
  <view class="popup-content">
    <view class="title">Select Option</view>
    <t-cell title="Option 1" bind:click="selectOption" data-value="1" />
    <t-cell title="Option 2" bind:click="selectOption" data-value="2" />
  </view>
</t-popup>

<!-- Center popup -->
<t-popup visible="{{showCenter}}" placement="center">
  <view class="center-content">
    <text>Centered content</text>
  </view>
</t-popup>

<!-- Left drawer -->
<t-popup visible="{{showDrawer}}" placement="left" close-btn>
  <view class="drawer-content">
    <t-cell-group>
      <t-cell title="Menu Item 1" />
      <t-cell title="Menu Item 2" />
    </t-cell-group>
  </view>
</t-popup>
```

---

## Loading

Loading indicator.

### Registration

```json
{
  "usingComponents": {
    "t-loading": "tdesign-miniprogram/loading/loading"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `loading` | Boolean | `true` | Show loading |
| `theme` | String | `circular` | Options: `circular`, `spinner`, `dots` |
| `size` | String | `20px` | Indicator size |
| `text` | String | - | Loading text |
| `layout` | String | `horizontal` | Options: `horizontal`, `vertical` |
| `delay` | Number | `0` | Delay before showing (ms) |
| `duration` | Number | `800` | Animation duration (ms) |
| `fullscreen` | Boolean | `false` | Fullscreen loading |
| `indicator` | Boolean | `true` | Show indicator |
| `progress` | Number | - | Progress value |

### Slots

| Slot | Description |
|------|-------------|
| `default` / `text` | Custom text |
| `indicator` | Custom indicator |

### Examples

```html
<!-- Basic loading -->
<t-loading />

<!-- With text -->
<t-loading text="Loading..." />

<!-- Vertical layout -->
<t-loading text="Please wait" layout="vertical" />

<!-- Different themes -->
<t-loading theme="circular" />
<t-loading theme="spinner" />
<t-loading theme="dots" />

<!-- Fullscreen -->
<t-loading fullscreen loading="{{isLoading}}" text="Loading data..." />

<!-- Custom size -->
<t-loading size="48px" />

<!-- Wrap content -->
<t-loading loading="{{isLoading}}">
  <view class="content">
    This content will show after loading
  </view>
</t-loading>
```

---

## ActionSheet

Bottom action sheet.

### Registration

```json
{
  "usingComponents": {
    "t-action-sheet": "tdesign-miniprogram/action-sheet/action-sheet"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `visible` | Boolean | `false` | Control visibility |
| `items` | Array | `[]` | Action items |
| `cancel-text` | String | - | Cancel button text |
| `description` | String | - | Description text |
| `show-cancel` | Boolean | `true` | Show cancel button |
| `theme` | String | `list` | Options: `list`, `grid` |

### Item Structure

```javascript
{
  label: 'Action Name',
  icon: 'icon-name',  // Optional
  color: '#ff0000',   // Optional
  disabled: false     // Optional
}
```

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `selected` | `{selected, index}` | Item selected |
| `cancel` | - | Cancel clicked |
| `close` | - | Sheet closed |

### Examples

```html
<!-- Basic action sheet -->
<t-action-sheet
  visible="{{showAction}}"
  items="{{actions}}"
  cancel-text="Cancel"
  bind:selected="onActionSelect"
  bind:cancel="onActionCancel"
/>

<!-- With description -->
<t-action-sheet
  visible="{{showAction}}"
  description="Please select an action"
  items="{{actions}}"
/>

<!-- Grid theme -->
<t-action-sheet
  visible="{{showShare}}"
  theme="grid"
  items="{{shareItems}}"
/>
```

```javascript
Page({
  data: {
    showAction: false,
    actions: [
      { label: 'Edit' },
      { label: 'Share' },
      { label: 'Delete', color: '#e34d59' }
    ],
    shareItems: [
      { label: 'WeChat', icon: 'logo-wechat' },
      { label: 'Moments', icon: 'share' },
      { label: 'Copy Link', icon: 'link' }
    ]
  },

  onActionSelect(e) {
    const { index } = e.detail;
    this.setData({ showAction: false });
    console.log('Selected:', this.data.actions[index]);
  }
});
```

---

## Message

Message notifications.

### Registration

```json
{
  "usingComponents": {
    "t-message": "tdesign-miniprogram/message/message"
  }
}
```

### Props (via function call)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | String | - | Message content |
| `theme` | String | `info` | Options: `info`, `success`, `warning`, `error` |
| `duration` | Number | `3000` | Display duration (ms) |
| `icon` | Boolean/String | `true` | Show/custom icon |
| `close-btn` | Boolean | `false` | Show close button |
| `offset` | Array | - | Position offset [top, left] |

### API Usage

```javascript
import Message from 'tdesign-miniprogram/message/index';

// Info message
Message.info({
  context: this,
  content: 'This is an info message'
});

// Success message
Message.success({
  context: this,
  content: 'Operation successful!'
});

// Warning message
Message.warning({
  context: this,
  content: 'Please check your input'
});

// Error message
Message.error({
  context: this,
  content: 'Something went wrong'
});

// With close button
Message.info({
  context: this,
  content: 'Closable message',
  closeBtn: true,
  duration: 5000
});
```

### Template

```html
<t-message id="t-message" />
```

---

## Overlay

Background overlay.

### Registration

```json
{
  "usingComponents": {
    "t-overlay": "tdesign-miniprogram/overlay/overlay"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `visible` | Boolean | `false` | Control visibility |
| `background-color` | String | - | Custom background color |
| `duration` | Number | `300` | Animation duration (ms) |
| `prevent-scroll-through` | Boolean | `true` | Prevent scroll |
| `z-index` | Number | `1000` | Stack order |

### Events

| Event | Description |
|-------|-------------|
| `click` | Overlay clicked |

### Examples

```html
<t-overlay visible="{{showOverlay}}" bind:click="hideOverlay">
  <view class="overlay-content" catchtap>
    Content on overlay
  </view>
</t-overlay>
```

---

## SwipeCell

Swipeable cell with action buttons.

### Registration

```json
{
  "usingComponents": {
    "t-swipe-cell": "tdesign-miniprogram/swipe-cell/swipe-cell"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `left` | Array | - | Left action buttons |
| `right` | Array | - | Right action buttons |
| `disabled` | Boolean | `false` | Disable swipe |
| `opened` | Boolean | `false` | Control open state |

### Button Structure

```javascript
{
  text: 'Delete',
  theme: 'danger',  // default, primary, danger
  className: 'custom-class'
}
```

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `click` | `{action}` | Button clicked |
| `open` | - | Cell opened |
| `close` | - | Cell closed |

### Examples

```html
<t-swipe-cell right="{{rightActions}}" bind:click="onSwipeAction">
  <t-cell title="Swipe Left" description="Swipe to reveal actions" />
</t-swipe-cell>
```

```javascript
Page({
  data: {
    rightActions: [
      { text: 'Mark', theme: 'primary' },
      { text: 'Delete', theme: 'danger' }
    ]
  },

  onSwipeAction(e) {
    const { action } = e.detail;
    if (action.text === 'Delete') {
      // Handle delete
    }
  }
});
```
