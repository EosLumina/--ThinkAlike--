# Eos Lumina∴ AI Guide: Quick Start Integration

This guide provides simple integration steps to add the Eos Lumina∴ AI Guide to your ThinkAlike project site or documentation.

## Installation

### Method 1: Script Tag (Simplest)

Add this script tag to your HTML page:

```html
<script async src="https://thinkalike-project.com/assets/eos-lumina-guide.js"></script>
<link rel="stylesheet" href="https://thinkalike-project.com/assets/eos-lumina-guide.css">

<script>
  document.addEventListener('DOMContentLoaded', () => {
    window.EosLumina.initialize({
      mountPoint: '#guide-container', // Optional: Where to mount the guide
      initialMessage: 'Welcome to ThinkAlike!', // Optional: Custom welcome message
      enableVoice: true, // Optional: Start with voice enabled
      theme: 'light' // Optional: 'light' or 'dark'
    });
  });
</script>

<!-- Optional: Specify where the guide should appear -->
<div id="guide-container"></div>
```

### Method 2: NPM Installation

For React-based projects:

```bash
npm install @thinkalike/eos-lumina-guide
```

Then in your component:

```jsx
import { EosLuminaGuide } from '@thinkalike/eos-lumina-guide';

function MyComponent() {
  return (
    <div className="my-container">
      <h1>ThinkAlike Documentation</h1>

      {/* Add the guide component */}
      <EosLuminaGuide
        initialMessage="Welcome to ThinkAlike! How can I assist you today?"
        enableVoice={true}
        showTaskRecommendations={true}
      />

      {/* Rest of your content */}
    </div>
  );
}
```

## Configuration Options

### Basic Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `initialMessage` | string | "Welcome..." | First message displayed by the guide |
| `enableVoice` | boolean | true | Whether voice synthesis is initially enabled |
| `theme` | string | 'light' | UI theme: 'light' or 'dark' |
| `showTaskRecommendations` | boolean | true | Show task recommendations panel |
| `minimized` | boolean | false | Start in minimized state |

### Advanced Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `voiceSettings` | object | {...} | Voice characteristics configuration |
| `apiEndpoint` | string | "..." | Custom API endpoint for guide service |
| `contributorProfilePersistence` | string | 'local' | Where to store profile: 'local', 'session', 'server' |
| `gitHubIntegration` | boolean | true | Enable GitHub API integration |

## Customization

### Styling

The guide uses CSS variables that you can override:

```css
:root {
  --eos-primary-color: #f0a500;
  --eos-secondary-color: #4267AC;
  --eos-background: #ffffff;
  --eos-text-color: #333333;
  --eos-accent-glow: rgba(240, 165, 0, 0.2);
  --eos-font-family: 'Manrope', sans-serif;
}

/* Dark theme variables */
[data-theme="dark"] {
  --eos-background: #1a1a2e;
  --eos-text-color: #e6e6e6;
  --eos-accent-glow: rgba(240, 165, 0, 0.15);
}
```

### Custom Voice Settings

You can customize the voice characteristics:

```js
window.EosLumina.initialize({
  // ...other options
  voiceSettings: {
    pitch: 1.1,      // Range: 0.5-1.5
    rate: 0.95,      // Range: 0.8-1.2
    harmony: 0.3,    // Range: 0-1 (ethereal harmonics intensity)
    resonance: 0.4   // Range: 0-1 (spatial quality)
  }
});
```

## Events

You can listen for guide events:

```js
document.addEventListener('eosGuideInitialized', (e) => {
  console.log('Guide is ready:', e.detail);
});

document.addEventListener('eosGuideSpeaking', (e) => {
  console.log('Guide is speaking:', e.detail.text);
});

document.addEventListener('eosGuideTaskRecommended', (e) => {
  console.log('Recommended tasks:', e.detail.tasks);
});
```

## Common Integration Scenarios

### Documentation Site Integration

```html
<div class="docs-sidebar">
  <!-- Navigation -->

  <!-- Add the minimized guide at the bottom of the sidebar -->
  <div id="guide-container" class="sidebar-guide"></div>
</div>

<script>
  window.EosLumina.initialize({
    mountPoint: '#guide-container',
    minimized: true,
    contextAware: true // Will be aware of current documentation page
  });
</script>
```

### GitHub Pages Integration

Add to your Jekyll site's default layout:

```html
{% if site.enable_eos_guide %}
<script async src="{{ site.baseurl }}/assets/js/eos-lumina-guide.js"></script>
<link rel="stylesheet" href="{{ site.baseurl }}/assets/css/eos-lumina-guide.css">

<script>
  document.addEventListener('DOMContentLoaded', () => {
    window.EosLumina.initialize({
      githubRepo: "{{ site.github_username }}/{{ site.github_repo }}",
      theme: "{{ site.theme }}" === 'dark' ? 'dark' : 'light'
    });
  });
</script>
{% endif %}
```

## Accessibility

The guide is built with accessibility in mind:

* All interactive elements are keyboard navigable
* Voice controls can be toggled on/off
* Color contrast meets WCAG 2.1 AA standards
* Screen reader optimized using aria attributes
* Caption system for voice content

## Troubleshooting

### Voice Not Working

* Check if browser supports Web Speech API (Chrome, Edge, Safari)
* Ensure user has granted microphone permissions if using voice input
* Try using the fallback voice server by adding `useFallbackVoice: true`

### Guide Not Loading

* Check browser console for errors
* Verify the script is loading correctly
* Ensure the mount point exists in DOM before initialization
* Try adding `async: false` to force synchronous loading

### Custom Styling Issues

* Inspect element to confirm CSS variables are being applied
* Check for CSS specificity issues in your custom styles
* Make sure the theme attribute is correctly set

## Next Steps

For advanced customization, backend integration, and extension development, see the complete [Eos Lumina∴ Development Guide](./developer_guide.md).
