# TDesign MiniProgram - Form Components

## Input

Single-line text input field.

### Registration

```json
{
  "usingComponents": {
    "t-input": "tdesign-miniprogram/input/input"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number | - | Input value |
| `type` | String | `text` | Options: `text`, `number`, `password`, `nickname`, `digit`, `idcard` |
| `placeholder` | String | - | Placeholder text |
| `maxlength` | Number | `-1` | Max character limit (-1 = unlimited) |
| `disabled` | Boolean | - | Disable input |
| `clearable` | Boolean/Object | `false` | Show clear button |
| `prefix-icon` | String/Object | - | Leading icon |
| `suffix-icon` | String/Object | - | Trailing icon |
| `suffix` | String | - | Suffix text |
| `label` | String | - | Input label |
| `status` | String | `default` | Options: `default`, `success`, `warning`, `error` |
| `tips` | String | - | Tip text below input |
| `align` | String | `left` | Text alignment: `left`, `center`, `right` |
| `layout` | String | `horizontal` | Options: `horizontal`, `vertical` |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value, cursor}` | Value changed |
| `focus` | `{value}` | Input focused |
| `blur` | `{value}` | Input blurred |
| `enter` | `{value}` | Enter key pressed |
| `clear` | - | Clear button clicked |

### Examples

```html
<!-- Basic input -->
<t-input placeholder="Enter text" value="{{inputValue}}" bind:change="onInputChange" />

<!-- With label -->
<t-input label="Username" placeholder="Enter username" />

<!-- Password type -->
<t-input type="password" label="Password" placeholder="Enter password" />

<!-- With clearable -->
<t-input clearable placeholder="Clearable input" />

<!-- With icons -->
<t-input prefix-icon="search" placeholder="Search..." />
<t-input suffix-icon="browse" type="password" />

<!-- Status states -->
<t-input status="error" tips="Invalid input" />
<t-input status="success" tips="Valid!" />

<!-- Character limit -->
<t-input maxlength="{{20}}" placeholder="Max 20 chars" />
```

---

## Form

Form container with validation support.

### Registration

```json
{
  "usingComponents": {
    "t-form": "tdesign-miniprogram/form/form",
    "t-form-item": "tdesign-miniprogram/form-item/form-item"
  }
}
```

### Form Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `data` | Object | `{}` | Form data object |
| `rules` | Object | - | Validation rules |
| `label-width` | String/Number | `81px` | Label width |
| `label-align` | String | `right` | Label alignment: `left`, `right`, `top` |
| `show-error-message` | Boolean | `true` | Show error messages |
| `reset-type` | String | `empty` | Reset behavior: `empty`, `initial` |

### FormItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | String | - | Field name (must match data key) |
| `label` | String | - | Field label |
| `required-mark` | Boolean | - | Show required asterisk |

### Form Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `submit` | `{fields, errors}` | Form submitted |
| `reset` | - | Form reset |
| `validate` | `{errors}` | Validation complete |

### Form Methods

```javascript
// Get form instance
const form = this.selectComponent('#form');

// Validate all fields
form.validate().then(result => {
  console.log('Valid:', result);
}).catch(errors => {
  console.log('Errors:', errors);
});

// Validate specific fields
form.validate(['username', 'email']);

// Reset form
form.reset();

// Clear validation messages
form.clearValidate();
```

### Built-in Validators

| Type | Description |
|------|-------------|
| `required` | Field is required |
| `email` | Valid email format |
| `telnumber` | Valid phone number |
| `idcard` | Valid ID card number |
| `url` | Valid URL |
| `pattern` | Match regex pattern |
| `min` / `max` | Value range |
| `len` | Exact length |

### Example

```html
<t-form id="form" data="{{formData}}" rules="{{rules}}" bind:submit="onSubmit">
  <t-form-item label="Username" name="username">
    <t-input placeholder="Enter username" />
  </t-form-item>
  <t-form-item label="Email" name="email">
    <t-input placeholder="Enter email" />
  </t-form-item>
  <t-form-item label="Phone" name="phone">
    <t-input type="number" placeholder="Enter phone" />
  </t-form-item>
  <t-button theme="primary" type="submit" block>Submit</t-button>
</t-form>
```

```javascript
Page({
  data: {
    formData: {
      username: '',
      email: '',
      phone: ''
    },
    rules: {
      username: [
        { required: true, message: 'Username is required' },
        { min: 3, message: 'At least 3 characters' }
      ],
      email: [
        { required: true, message: 'Email is required' },
        { email: true, message: 'Invalid email format' }
      ],
      phone: [
        { telnumber: true, message: 'Invalid phone number' }
      ]
    }
  },
  onSubmit(e) {
    const { fields, errors } = e.detail;
    if (!errors) {
      console.log('Form data:', fields);
    }
  }
});
```

---

## Checkbox

Multiple selection from a group of options.

### Registration

```json
{
  "usingComponents": {
    "t-checkbox": "tdesign-miniprogram/checkbox/checkbox",
    "t-checkbox-group": "tdesign-miniprogram/checkbox-group/checkbox-group"
  }
}
```

### Checkbox Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | Boolean | `false` | Checked state |
| `value` | String/Number/Boolean | - | Checkbox value |
| `label` | String | - | Label text |
| `disabled` | Boolean | `false` | Disable checkbox |
| `icon` | String/Array | - | Icon style: `circle`, `line`, `rectangle` |
| `placement` | String | `left` | Icon position: `left`, `right` |
| `indeterminate` | Boolean | `false` | Half-checked state |

### CheckboxGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | Array | `[]` | Selected values |
| `options` | Array | - | Options array |
| `disabled` | Boolean | `false` | Disable all |
| `max` | Number | - | Max selections |

### Examples

```html
<!-- Basic checkbox group -->
<t-checkbox-group value="{{selected}}" bind:change="onCheckboxChange">
  <t-checkbox value="a" label="Option A" />
  <t-checkbox value="b" label="Option B" />
  <t-checkbox value="c" label="Option C" />
</t-checkbox-group>

<!-- With options array -->
<t-checkbox-group value="{{selected}}" options="{{options}}" bind:change="onCheckboxChange" />

<!-- Max selections -->
<t-checkbox-group value="{{selected}}" max="{{2}}" bind:change="onCheckboxChange">
  <t-checkbox value="1" label="Choice 1" />
  <t-checkbox value="2" label="Choice 2" />
  <t-checkbox value="3" label="Choice 3" />
</t-checkbox-group>
```

---

## Switch

Toggle control for enabling/disabling features.

### Registration

```json
{
  "usingComponents": {
    "t-switch": "tdesign-miniprogram/switch/switch"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String/Number/Boolean | `null` | Current value |
| `custom-value` | Array | `[true, false]` | Custom on/off values |
| `disabled` | Boolean | - | Disable switch |
| `loading` | Boolean | - | Loading state |
| `size` | String | `medium` | Options: `small`, `medium`, `large` |
| `label` | Array | - | On/off labels, e.g., `['ON', 'OFF']` |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Value changed |

### Examples

```html
<t-switch value="{{enabled}}" bind:change="onSwitchChange" />

<!-- With labels -->
<t-switch value="{{enabled}}" label="{{['ON', 'OFF']}}" />

<!-- Custom values -->
<t-switch value="{{status}}" custom-value="{{[1, 0]}}" />

<!-- Different sizes -->
<t-switch size="small" />
<t-switch size="large" />
```

---

## Picker

Selection from preset data options.

### Registration

```json
{
  "usingComponents": {
    "t-picker": "tdesign-miniprogram/picker/picker",
    "t-picker-item": "tdesign-miniprogram/picker-item/picker-item"
  }
}
```

### Picker Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `visible` | Boolean | `false` | Show picker |
| `value` | Array | - | Selected values |
| `title` | String | - | Picker title |
| `auto-close` | Boolean | `true` | Auto close on confirm/cancel |
| `use-popup` | Boolean | `true` | Use popup container |

### PickerItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | Array | - | Options with `{label, value}` |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `confirm` | `{value, label}` | Confirm clicked |
| `cancel` | - | Cancel clicked |
| `change` | `{value, label, column}` | Selection changed |

### Example

```html
<t-cell title="City" description="{{selectedCity}}" arrow bind:click="showPicker" />

<t-picker
  visible="{{pickerVisible}}"
  title="Select City"
  bind:confirm="onPickerConfirm"
  bind:cancel="onPickerCancel"
>
  <t-picker-item options="{{cities}}" />
</t-picker>
```

```javascript
Page({
  data: {
    pickerVisible: false,
    selectedCity: 'Select',
    cities: [
      { label: 'Beijing', value: 'bj' },
      { label: 'Shanghai', value: 'sh' },
      { label: 'Guangzhou', value: 'gz' }
    ]
  },
  showPicker() {
    this.setData({ pickerVisible: true });
  },
  onPickerConfirm(e) {
    const { label } = e.detail;
    this.setData({ selectedCity: label[0], pickerVisible: false });
  },
  onPickerCancel() {
    this.setData({ pickerVisible: false });
  }
});
```

---

## Upload

Image/file upload component.

### Registration

```json
{
  "usingComponents": {
    "t-upload": "tdesign-miniprogram/upload/upload"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `files` | Array | - | File list |
| `max` | Number | `0` | Max file count (0 = unlimited) |
| `media-type` | Array | `['image', 'video']` | Allowed media types |
| `size-limit` | Number/Object | - | File size limit |
| `disabled` | Boolean | - | Disable upload |
| `draggable` | Boolean/Object | - | Enable drag to reorder |
| `preview` | Boolean | `true` | Enable image preview |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `add` | `{files}` | Files selected |
| `remove` | `{index, file}` | File removed |
| `success` | `{files}` | Upload success |
| `fail` | `{file}` | Upload failed |

### Example

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
    // Upload files to server
    const uploaded = files.map(file => ({
      ...file,
      status: 'loading'
    }));

    this.setData({ files: [...this.data.files, ...uploaded] });

    // Simulate upload
    files.forEach((file, index) => {
      const currentIndex = this.data.files.length - files.length + index;
      setTimeout(() => {
        const updatedFiles = [...this.data.files];
        updatedFiles[currentIndex].status = 'done';
        this.setData({ files: updatedFiles });
      }, 1000);
    });
  },

  onRemove(e) {
    const { index } = e.detail;
    const files = this.data.files.filter((_, i) => i !== index);
    this.setData({ files });
  }
});
```

---

## Search

Search input with action button.

### Registration

```json
{
  "usingComponents": {
    "t-search": "tdesign-miniprogram/search/search"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | String | - | Search value |
| `placeholder` | String | - | Placeholder text |
| `shape` | String | `square` | Options: `square`, `round` |
| `action` | String | - | Action button text |
| `clearable` | Boolean | `true` | Show clear button |
| `disabled` | Boolean | `false` | Disable input |
| `focus` | Boolean | `false` | Auto focus |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Value changed |
| `submit` | `{value}` | Search submitted |
| `action-click` | - | Action button clicked |
| `clear` | - | Clear button clicked |
| `focus` | `{value}` | Input focused |
| `blur` | `{value}` | Input blurred |

### Example

```html
<t-search
  value="{{keyword}}"
  placeholder="Search products"
  action="Cancel"
  bind:change="onSearchChange"
  bind:submit="onSearch"
  bind:action-click="onCancel"
/>
```

---

## Rate

Star rating component.

### Registration

```json
{
  "usingComponents": {
    "t-rate": "tdesign-miniprogram/rate/rate"
  }
}
```

### Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | Number | `0` | Current rating |
| `count` | Number | `5` | Number of stars |
| `allow-half` | Boolean | `false` | Allow half stars |
| `color` | String/Array | `#ED7B2F` | Star color(s) |
| `size` | String | `24px` | Star size |
| `disabled` | Boolean | - | Disable rating |
| `show-text` | Boolean | `false` | Show rating text |
| `texts` | Array | - | Custom texts for each level |
| `gap` | String/Number | `8` | Gap between stars |

### Events

| Event | Parameters | Description |
|-------|-----------|-------------|
| `change` | `{value}` | Rating changed |

### Example

```html
<!-- Basic rating -->
<t-rate value="{{rating}}" bind:change="onRateChange" />

<!-- Half stars -->
<t-rate value="{{rating}}" allow-half />

<!-- With text -->
<t-rate value="{{rating}}" show-text texts="{{['Bad', 'Fair', 'Good', 'Very Good', 'Excellent']}}" />

<!-- Custom count -->
<t-rate value="{{rating}}" count="{{10}}" />
```
