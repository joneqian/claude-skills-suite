# TDesign MiniProgram - Basic Components

## Button

Action trigger component for initiating operations like "delete" or "purchase".

### Registration

```json
{
  "usingComponents": {
    "t-button": "tdesign-miniprogram/button/button"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `theme` | String | `default` | Options: `default`, `primary`, `danger`, `light` |
| `variant` | String | `base` | Options: `base`, `outline`, `dashed`, `text` |
| `size` | String | `medium` | Options: `extra-small`, `small`, `medium`, `large` |
| `block` | Boolean | `false` | Full width button |
| `disabled` | Boolean | `undefined` | Disable button |
| `loading` | Boolean | `false` | Show loading state |
| `ghost` | Boolean | `false` | Hollow/transparent style |
| `shape` | String | `rectangle` | Options: `rectangle`, `square`, `round`, `circle` |
| `icon` | String/Object | - | Icon configuration |
| `open-type` | String | - | WeChat capabilities (contact, share, launchApp, etc.) |

### Events

| Event | Description |
|-------|-------------|
| `tap` | Triggered when clicked (not loading/disabled) |
| `getuserinfo` | Get user info (requires open-type) |
| `getphonenumber` | Get phone number (requires open-type) |

### Examples

```html
<!-- Basic buttons -->
<t-button theme="primary">Primary</t-button>
<t-button theme="danger">Danger</t-button>

<!-- Variant styles -->
<t-button theme="primary" variant="outline">Outline</t-button>
<t-button theme="primary" variant="text">Text</t-button>

<!-- Sizes -->
<t-button size="small">Small</t-button>
<t-button size="large" block>Large Block</t-button>

<!-- States -->
<t-button loading>Loading</t-button>
<t-button disabled>Disabled</t-button>

<!-- With icon -->
<t-button icon="add" theme="primary">Add</t-button>

<!-- WeChat open types -->
<t-button open-type="share">Share</t-button>
<t-button open-type="contact">Contact</t-button>
```

---

## Cell

Display information across rows with title, description, and optional navigation.

### Registration

```json
{
  "usingComponents": {
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group"
  }
}
```

### Cell Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | String | - | Cell title |
| `description` | String | - | Secondary description |
| `note` | String | - | Right-side note text |
| `arrow` | Boolean/Object | `false` | Show right arrow |
| `left-icon` | String/Object | - | Left icon |
| `image` | String | - | Left image URL |
| `url` | String | - | Navigation link |
| `jump-type` | String | `navigateTo` | Navigation type |
| `hover` | Boolean | - | Enable hover effect |

### CellGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `theme` | String | `default` | Options: `default`, `card` |
| `title` | String | - | Group title |
| `bordered` | Boolean | `false` | Show borders |

### Events

| Event | Description |
|-------|-------------|
| `click` | Triggered on cell click |

### Examples

```html
<t-cell-group title="Settings">
  <t-cell title="Account" arrow />
  <t-cell title="Notifications" description="Enabled" arrow />
  <t-cell title="Privacy" note="Configure" arrow />
</t-cell-group>

<!-- With icons -->
<t-cell-group>
  <t-cell title="Profile" left-icon="user" arrow />
  <t-cell title="Settings" left-icon="setting" arrow />
</t-cell-group>

<!-- Card theme -->
<t-cell-group theme="card" title="Card Style">
  <t-cell title="Item 1" arrow />
  <t-cell title="Item 2" arrow />
</t-cell-group>

<!-- Navigation -->
<t-cell title="About" url="/pages/about/index" arrow />
```

---

## Icon

Display icons from TDesign icon library.

### Registration

```json
{
  "usingComponents": {
    "t-icon": "tdesign-miniprogram/icon/icon"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | String | - | Icon name |
| `size` | String | - | Icon size |
| `color` | String | - | Icon color |
| `prefix` | String | `t` | Icon prefix |

### Examples

```html
<t-icon name="add" />
<t-icon name="close" size="48rpx" color="#ff0000" />
<t-icon name="check-circle-filled" size="64rpx" color="#00aa00" />
```

---

## Divider

Visual separator between content sections.

### Registration

```json
{
  "usingComponents": {
    "t-divider": "tdesign-miniprogram/divider/divider"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | String | - | Text content |
| `align` | String | `center` | Text alignment: `left`, `center`, `right` |
| `dashed` | Boolean | `false` | Dashed line style |
| `layout` | String | `horizontal` | Options: `horizontal`, `vertical` |

### Examples

```html
<t-divider />
<t-divider content="OR" />
<t-divider content="More" align="left" />
<t-divider dashed />
```

---

## Fab (Floating Action Button)

Floating button for primary actions.

### Registration

```json
{
  "usingComponents": {
    "t-fab": "tdesign-miniprogram/fab/fab"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `icon` | String | `add` | Icon name |
| `text` | String | - | Button text |
| `style` | String | - | Custom positioning |
| `button-props` | Object | - | Button component props |

### Examples

```html
<t-fab icon="add" style="right: 32rpx; bottom: 100rpx;" bind:click="onAdd" />
<t-fab icon="chat" text="Chat" bind:click="onChat" />
```

---

## Link

Text links for navigation.

### Registration

```json
{
  "usingComponents": {
    "t-link": "tdesign-miniprogram/link/link"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | String | - | Link text |
| `theme` | String | `default` | Options: `default`, `primary`, `danger`, `warning`, `success` |
| `size` | String | `medium` | Options: `small`, `medium`, `large` |
| `disabled` | Boolean | `false` | Disable link |
| `underline` | Boolean | - | Show underline |
| `prefix-icon` | String/Object | - | Prefix icon |
| `suffix-icon` | String/Object | - | Suffix icon |
| `navigatorProps` | Object | - | wx.navigateTo options |

### Examples

```html
<t-link content="Learn more" theme="primary" />
<t-link content="Terms of Service" underline />
<t-link content="Visit" suffix-icon="jump" />
```
