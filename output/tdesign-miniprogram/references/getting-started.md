# TDesign MiniProgram - Getting Started

## Overview

TDesign is Tencent's official component library for WeChat Mini Programs, providing a comprehensive UI solution with 90+ production-ready components.

## Installation

### NPM Installation (Recommended)

```bash
npm i tdesign-miniprogram -S --production
```

**Important:** Follow WeChat's [official NPM documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/npm.html) for mini program NPM support.

### Requirements

- Minimum base library version: `^2.6.5`
- WeChat Developer Tools with NPM support enabled

### Build NPM

After installation, in WeChat Developer Tools:
1. Go to Tools > Build npm
2. Wait for build completion
3. Components will be available in `miniprogram_npm/`

## Component Registration

### Global Registration (app.json)

Register frequently used components globally:

```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button",
    "t-input": "tdesign-miniprogram/input/input",
    "t-dialog": "tdesign-miniprogram/dialog/dialog",
    "t-toast": "tdesign-miniprogram/toast/toast",
    "t-navbar": "tdesign-miniprogram/navbar/navbar"
  }
}
```

### Local Registration (page/index.json)

Register page-specific components locally:

```json
{
  "usingComponents": {
    "t-picker": "tdesign-miniprogram/picker/picker",
    "t-picker-item": "tdesign-miniprogram/picker-item/picker-item"
  }
}
```

## Basic Usage

### WXML Template

```html
<view class="container">
  <t-navbar title="My Page" left-arrow bind:go-back="goBack" />

  <t-cell-group>
    <t-cell title="Username" description="{{username}}" arrow />
    <t-cell title="Settings" arrow url="/pages/settings/index" />
  </t-cell-group>

  <t-button theme="primary" block bind:tap="handleSubmit">
    Submit
  </t-button>
</view>
```

### JavaScript

```javascript
Page({
  data: {
    username: 'John Doe'
  },

  goBack() {
    wx.navigateBack();
  },

  handleSubmit() {
    wx.showToast({ title: 'Submitted!' });
  }
});
```

### WXSS Styling

```css
.container {
  padding: 32rpx;
}

/* Override TDesign CSS variables */
page {
  --td-button-primary-bg-color: #1890ff;
}
```

## Development Preview

To view component examples locally:

```bash
git clone https://github.com/Tencent/tdesign-miniprogram.git
cd tdesign-miniprogram
npm install
npm run dev
```

Then open the `_example` directory in WeChat Developer Tools.

## Project Structure Recommendation

```
miniprogram/
├── app.js
├── app.json          # Global component registration
├── app.wxss          # Global styles & CSS variables
├── pages/
│   ├── index/
│   │   ├── index.js
│   │   ├── index.json  # Page-specific components
│   │   ├── index.wxml
│   │   └── index.wxss
│   └── ...
├── components/        # Custom components
└── utils/
```

## Tips

1. **Performance**: Only import components you need to reduce bundle size
2. **Theming**: Use CSS variables for consistent branding
3. **Events**: Use `bind:` prefix for event handlers (e.g., `bind:change`)
4. **Slots**: Many components support slots for custom content
5. **External Classes**: Use `t-class` and related props for styling

## Troubleshooting

### Component Not Found

- Verify component path in `usingComponents`
- Rebuild NPM after installation
- Check for typos in component names

### Styles Not Applied

- Ensure `app.wxss` is loaded
- Check CSS variable names match TDesign specs
- Use `!important` when overriding with external classes

### Events Not Firing

- Use `bind:eventName` syntax (not `bindeventName`)
- Check component documentation for correct event names
- Verify data binding with `{{}}` syntax
