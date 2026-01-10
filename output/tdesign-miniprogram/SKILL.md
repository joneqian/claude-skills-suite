---
name: tdesign-miniprogram
description: TDesign Mini Program UI component library by Tencent. Use for building WeChat mini apps with TDesign components, design system, and best practices.
version: 1.0.0
---

# TDesign MiniProgram Skill

TDesign is Tencent's official UI component library for WeChat Mini Programs, providing a comprehensive set of 90+ production-ready components following TDesign's design system.

## When to Use This Skill

This skill should be triggered when:
- Building WeChat Mini Program user interfaces
- Using TDesign Mini Program components
- Implementing forms, navigation, dialogs, and other UI patterns in mini programs
- Looking for TDesign component API references, props, events, and slots
- Debugging or troubleshooting TDesign component issues

## Quick Start

### Installation

```bash
npm i tdesign-miniprogram -S --production
```

**Important:** Follow WeChat's official NPM documentation for mini program NPM support. Minimum base library version: `^2.6.5`

### Component Registration

Register components in `app.json` (global) or page/component `index.json` (local):

```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button",
    "t-input": "tdesign-miniprogram/input/input",
    "t-dialog": "tdesign-miniprogram/dialog/dialog"
  }
}
```

## Component Categories

### Basic Components
| Component | Description | Usage |
|-----------|-------------|-------|
| Button | Action trigger buttons | `t-button` |
| Icon | Icon display | `t-icon` |
| Cell | List item container | `t-cell`, `t-cell-group` |
| Link | Navigation links | `t-link` |
| Fab | Floating action button | `t-fab` |
| Divider | Content separator | `t-divider` |

### Form Components
| Component | Description | Usage |
|-----------|-------------|-------|
| Input | Text input field | `t-input` |
| Textarea | Multi-line text input | `t-textarea` |
| Checkbox | Multiple selection | `t-checkbox`, `t-checkbox-group` |
| Radio | Single selection | `t-radio`, `t-radio-group` |
| Switch | Toggle control | `t-switch` |
| Picker | Selection picker | `t-picker`, `t-picker-item` |
| DateTimePicker | Date/time selection | `t-date-time-picker` |
| Upload | File upload | `t-upload` |
| Search | Search input | `t-search` |
| Rate | Star rating | `t-rate` |
| Slider | Range slider | `t-slider` |
| Stepper | Numeric stepper | `t-stepper` |
| Form | Form container with validation | `t-form`, `t-form-item` |

### Data Display
| Component | Description | Usage |
|-----------|-------------|-------|
| Avatar | User avatar | `t-avatar`, `t-avatar-group` |
| Badge | Notification badge | `t-badge` |
| Image | Image display | `t-image` |
| Swiper | Carousel/slider | `t-swiper`, `t-swiper-nav` |
| Tag | Label tags | `t-tag` |
| Progress | Progress indicator | `t-progress` |
| Skeleton | Loading placeholder | `t-skeleton` |
| Empty | Empty state | `t-empty` |
| CountDown | Countdown timer | `t-count-down` |
| Collapse | Collapsible panel | `t-collapse`, `t-collapse-panel` |

### Feedback Components
| Component | Description | Usage |
|-----------|-------------|-------|
| Dialog | Modal dialog | `t-dialog` |
| Toast | Brief notifications | `t-toast` |
| Popup | Slide-in overlay | `t-popup` |
| Loading | Loading indicator | `t-loading` |
| ActionSheet | Bottom action sheet | `t-action-sheet` |
| Message | Message notifications | `t-message` |
| Drawer | Side drawer | `t-drawer` |
| Overlay | Background overlay | `t-overlay` |
| SwipeCell | Swipeable cell | `t-swipe-cell` |
| PullDownRefresh | Pull to refresh | `t-pull-down-refresh` |

### Navigation Components
| Component | Description | Usage |
|-----------|-------------|-------|
| Navbar | Top navigation bar | `t-navbar` |
| TabBar | Bottom tab bar | `t-tab-bar`, `t-tab-bar-item` |
| Tabs | Tab navigation | `t-tabs`, `t-tab-panel` |
| Steps | Progress steps | `t-steps`, `t-step-item` |
| Indexes | Index navigation | `t-indexes`, `t-indexes-anchor` |
| BackTop | Back to top | `t-back-top` |
| DropdownMenu | Dropdown navigation | `t-dropdown-menu`, `t-dropdown-item` |
| SideBar | Side navigation | `t-side-bar`, `t-side-bar-item` |

## Common Patterns

### Button with Loading State

```html
<t-button theme="primary" loading="{{isLoading}}" bind:tap="handleSubmit">
  Submit
</t-button>
```

```javascript
Page({
  data: { isLoading: false },
  handleSubmit() {
    this.setData({ isLoading: true });
    // API call...
  }
});
```

### Form with Validation

```html
<t-form id="form" data="{{formData}}" rules="{{rules}}" bind:submit="onSubmit">
  <t-form-item label="Username" name="username">
    <t-input placeholder="Enter username" value="{{formData.username}}" />
  </t-form-item>
  <t-form-item label="Email" name="email">
    <t-input placeholder="Enter email" value="{{formData.email}}" />
  </t-form-item>
  <t-button theme="primary" type="submit">Submit</t-button>
</t-form>
```

```javascript
Page({
  data: {
    formData: { username: '', email: '' },
    rules: {
      username: [{ required: true, message: 'Username is required' }],
      email: [{ required: true }, { email: true, message: 'Invalid email' }]
    }
  },
  onSubmit(e) {
    console.log('Form validated:', e.detail);
  }
});
```

### Dialog Confirmation

```html
<t-dialog
  visible="{{showDialog}}"
  title="Confirm"
  content="Are you sure you want to proceed?"
  confirm-btn="Yes"
  cancel-btn="No"
  bind:confirm="onConfirm"
  bind:cancel="onCancel"
/>
```

### Tab Navigation

```html
<t-tabs value="{{activeTab}}" bind:change="onTabChange">
  <t-tab-panel label="Home" value="0">Home content</t-tab-panel>
  <t-tab-panel label="Profile" value="1">Profile content</t-tab-panel>
  <t-tab-panel label="Settings" value="2">Settings content</t-tab-panel>
</t-tabs>
```

### Image with Error Handling

```html
<t-image
  src="{{imageUrl}}"
  mode="aspectFill"
  shape="round"
  width="200"
  height="200"
  error="default"
  loading="default"
  bind:error="onImageError"
/>
```

### Search with Results

```html
<t-search
  value="{{searchValue}}"
  placeholder="Search products"
  action="Cancel"
  bind:change="onSearchChange"
  bind:submit="onSearch"
  bind:action-click="onCancel"
/>
```

### Upload Images

```html
<t-upload
  files="{{files}}"
  max="{{9}}"
  media-type="{{['image']}}"
  bind:add="onAdd"
  bind:remove="onRemove"
/>
```

```javascript
Page({
  data: { files: [] },
  onAdd(e) {
    const { files } = e.detail;
    this.setData({ files: [...this.data.files, ...files] });
  },
  onRemove(e) {
    const { index } = e.detail;
    const files = this.data.files.filter((_, i) => i !== index);
    this.setData({ files });
  }
});
```

### Toast Notifications

```html
<t-toast id="toast" />
```

```javascript
import Toast from 'tdesign-miniprogram/toast/index';

Page({
  showSuccess() {
    Toast({ context: this, selector: '#toast', message: 'Success!', theme: 'success' });
  },
  showError() {
    Toast({ context: this, selector: '#toast', message: 'Error occurred', theme: 'error' });
  }
});
```

### Picker Selection

```html
<t-picker
  visible="{{pickerVisible}}"
  title="Select City"
  bind:confirm="onPickerConfirm"
  bind:cancel="onPickerCancel"
>
  <t-picker-item options="{{cities}}" />
</t-picker>
```

## CSS Variables Customization

TDesign components support extensive CSS variable customization:

```css
/* Override in app.wxss or page.wxss */
page {
  --td-button-primary-bg-color: #1890ff;
  --td-button-primary-border-color: #1890ff;
  --td-input-border-color: #d9d9d9;
  --td-dialog-confirm-btn-color: #1890ff;
}
```

## External Classes

Most components support external CSS classes for custom styling:

```html
<t-button t-class="custom-button" t-class-icon="custom-icon">
  Custom Button
</t-button>
```

```css
.custom-button {
  border-radius: 20rpx !important;
}
```

## Reference Files

This skill includes detailed documentation in `references/`:

- **getting-started.md** - Installation, setup, and quick start guide
- **basic-components.md** - Button, Icon, Cell, Link, Fab, Divider
- **form-components.md** - Input, Checkbox, Radio, Switch, Picker, Upload, Form
- **data-display.md** - Avatar, Image, Swiper, Tag, Progress, Skeleton
- **feedback-components.md** - Dialog, Toast, Popup, Loading, ActionSheet
- **navigation.md** - Navbar, TabBar, Tabs, Steps, Indexes

## Resources

- [TDesign Official Website](https://tdesign.tencent.com/miniprogram/overview)
- [GitHub Repository](https://github.com/Tencent/tdesign-miniprogram)
- [NPM Package](https://www.npmjs.com/package/tdesign-miniprogram)

## Notes

- Always use NPM installation for dependency management
- Ensure WeChat base library version >= 2.6.5
- Components are modular - only import what you need
- CSS variables provide extensive theming capabilities
- External classes allow component-level style overrides
