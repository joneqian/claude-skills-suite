---
name: vant
description: Vant 4 Vue mobile UI component library. Use for building mobile web apps with Vue 3, Vant components, forms, popups, and business components.
---

# Vant UI Skill

Vant 4 is a lightweight, customizable Vue 3 mobile UI component library developed by Youzan. Provides 80+ high-quality components covering various mobile scenarios.

## When to Use This Skill

- Building mobile web applications with Vue 3
- Using Vant UI components (Button, Cell, Form, etc.)
- Implementing mobile forms, popups, navigation
- Configuring Vant theme customization
- Using Vant Composables
- Developing e-commerce mobile apps (address, coupon, product cards)

## Quick Start

```bash
npm i vant
```

```js
import { createApp } from 'vue';
import { Button } from 'vant';
import 'vant/lib/index.css';

const app = createApp();
app.use(Button);
```

## Reference Files

Use `Read` tool to access specific reference files when detailed API information is needed.

### Getting Started (getting-started/)

| File | Description |
|------|-------------|
| home.md | Introduction and features overview |
| quickstart.md | Installation and basic setup guide |
| advanced-usage.md | Component registration, browser adaptation, SSR |
| locale.md | Internationalization configuration |
| faq.md | Frequently asked questions |

### Basic Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| button.md | Button | Trigger actions |
| cell.md | Cell | List item container |
| config-provider.md | ConfigProvider | Global configuration and theming |
| icon.md | Icon | Icon display |
| image.md | Image | Image display with lazy load |
| col.md | Layout (Col/Row) | Flexbox layout system |
| popup.md | Popup | Popup layer container |
| space.md | Space | Spacing between elements |
| style.md | Built-in Styles | CSS utility classes |
| toast.md | Toast | Lightweight feedback |

### Form Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| calendar.md | Calendar | Date selection |
| cascader.md | Cascader | Cascade selection |
| checkbox.md | Checkbox | Multiple selection |
| date-picker.md | DatePicker | Date picker |
| field.md | Field | Input field |
| form.md | Form | Form with validation |
| number-keyboard.md | NumberKeyboard | Virtual number keyboard |
| password-input.md | PasswordInput | Password input with custom keyboard |
| picker.md | Picker | Column selector |
| picker-group.md | PickerGroup | Multiple pickers combination |
| radio.md | Radio | Single selection |
| rate.md | Rate | Rating with stars |
| search.md | Search | Search input |
| slider.md | Slider | Range selection |
| signature.md | Signature | Signature pad |
| stepper.md | Stepper | Quantity input |
| switch.md | Switch | Toggle switch |
| time-picker.md | TimePicker | Time selection |
| uploader.md | Uploader | File upload |

### Feedback Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| action-sheet.md | ActionSheet | Bottom action menu |
| barrage.md | Barrage | Bullet comments |
| dialog.md | Dialog | Modal dialog |
| dropdown-menu.md | DropdownMenu | Dropdown filter menu |
| floating-panel.md | FloatingPanel | Draggable panel |
| floating-bubble.md | FloatingBubble | Floating action button |
| loading.md | Loading | Loading indicator |
| notify.md | Notify | Top notification bar |
| overlay.md | Overlay | Background mask |
| pull-refresh.md | PullRefresh | Pull down to refresh |
| share-sheet.md | ShareSheet | Share options panel |
| swipe-cell.md | SwipeCell | Swipeable cell actions |

### Display Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| badge.md | Badge | Badge indicator |
| circle.md | Circle | Circular progress |
| collapse.md | Collapse | Collapsible content |
| count-down.md | CountDown | Countdown timer |
| divider.md | Divider | Content separator |
| empty.md | Empty | Empty state placeholder |
| highlight.md | Highlight | Text highlighting |
| image-preview.md | ImagePreview | Full screen image viewer |
| lazyload.md | Lazyload | Image lazy loading |
| list.md | List | Infinite scroll list |
| notice-bar.md | NoticeBar | Announcement bar |
| popover.md | Popover | Bubble popup menu |
| progress.md | Progress | Linear progress bar |
| rolling-text.md | RollingText | Rolling number animation |
| skeleton.md | Skeleton | Loading placeholder |
| steps.md | Steps | Step indicator |
| sticky.md | Sticky | Sticky positioning |
| swipe.md | Swipe | Carousel/Slider |
| tag.md | Tag | Label/Tag |
| text-ellipsis.md | TextEllipsis | Text truncation |
| watermark.md | Watermark | Page watermark |

### Navigation Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| action-bar.md | ActionBar | Bottom action bar (e-commerce) |
| back-top.md | BackTop | Back to top button |
| grid.md | Grid | Grid layout |
| index-bar.md | IndexBar | Alphabetical index |
| nav-bar.md | NavBar | Top navigation bar |
| pagination.md | Pagination | Page navigation |
| sidebar.md | Sidebar | Vertical navigation |
| tab.md | Tab/Tabs | Tab navigation |
| tabbar.md | Tabbar | Bottom tab bar |
| tree-select.md | TreeSelect | Tree category selection |

### Business Components (components/)

| File | Component | Description |
|------|-----------|-------------|
| address-edit.md | AddressEdit | Address form |
| address-list.md | AddressList | Address management list |
| area.md | Area | Province/City/District picker |
| card.md | Card | Product card |
| contact-card.md | ContactCard | Contact display card |
| contact-edit.md | ContactEdit | Contact form |
| contact-list.md | ContactList | Contact management list |
| coupon-list.md | CouponList | Coupon selector |
| submit-bar.md | SubmitBar | Order submit bar |

### Composables (composables/)

| File | Composable | Description |
|------|------------|-------------|
| vant-use-intro.md | Introduction | Composables overview |
| use-click-away.md | useClickAway | Click outside detection |
| use-count-down.md | useCountDown | Countdown timer |
| use-custom-field-value.md | useCustomFieldValue | Custom form field |
| use-event-listener.md | useEventListener | Event listener hook |
| use-page-visibility.md | usePageVisibility | Page visibility detection |
| use-raf.md | useRaf | requestAnimationFrame hook |
| use-rect.md | useRect | Element size measurement |
| use-relation.md | useRelation | Parent-child component relation |
| use-scroll-parent.md | useScrollParent | Scroll container detection |
| use-toggle.md | useToggle | Boolean toggle state |
| use-window-size.md | useWindowSize | Window size tracking |

## Component Quick Reference

### By Category

| Category | Components |
|----------|------------|
| Basic | Button, Cell, ConfigProvider, Icon, Image, Layout, Popup, Space, Style, Toast |
| Form | Calendar, Cascader, Checkbox, DatePicker, Field, Form, NumberKeyboard, PasswordInput, Picker, PickerGroup, Radio, Rate, Search, Slider, Signature, Stepper, Switch, TimePicker, Uploader |
| Feedback | ActionSheet, Barrage, Dialog, DropdownMenu, FloatingPanel, FloatingBubble, Loading, Notify, Overlay, PullRefresh, ShareSheet, SwipeCell |
| Display | Badge, Circle, Collapse, CountDown, Divider, Empty, Highlight, ImagePreview, Lazyload, List, NoticeBar, Popover, Progress, RollingText, Skeleton, Steps, Sticky, Swipe, Tag, TextEllipsis, Watermark |
| Navigation | ActionBar, BackTop, Grid, IndexBar, NavBar, Pagination, Sidebar, Tab, Tabbar, TreeSelect |
| Business | AddressEdit, AddressList, Area, Card, ContactCard, ContactEdit, ContactList, CouponList, SubmitBar |

### Function Components (API calls)

```js
import { showToast, showDialog, showNotify, showImagePreview } from 'vant';

showToast('Message');
showDialog({ title: 'Title', message: 'Content' });
showNotify({ type: 'success', message: 'Success' });
showImagePreview(['url1', 'url2']);
```

## Key Notes

- Vant 4 requires Vue 3 (use `vant@latest-v2` for Vue 2)
- `babel-plugin-import` is no longer supported in Vant 4
- Supports Tree Shaking by default
- Recommended build tools: Rsbuild, Vite

## Resources

- [Official Documentation](https://vant-ui.github.io/vant/)
- [GitHub Repository](https://github.com/vant-ui/vant)
- [Demo Projects](https://github.com/vant-ui/vant-demo)
