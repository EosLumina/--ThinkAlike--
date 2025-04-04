# Style Guide

This document outlines the visual style and branding guidelines for the ThinkAlike platform. We aim for a "Zenith of Excellence" aesthetic: clean, modern, professional, high-tech, and futuristic, while conveying trust, transparency, and ethical excellence.

## Color Palette

| Color                       | HEX Code    | Usage                                                                                                                               |
| ---------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Primary Colors:**           |             |                                                                                                                                    |
| Amber/Honey Yellow (Neutral) | `#FFC300`     | AI indicator (idle state), base color for some UI elements, subtle highlights.                                                    |
| Deep Mandarine Orange (Active)         | `#F86B03`     | AI indicator (active/processing state), data visualization, progress indicators.                                               |
| Neon Orange (Highlight)     | `#FF8C00`     | Calls to action, important notifications, errors, interactive elements. Use sparingly.                                          |
| Deep Ruby (Connection)       | `#800000`     | Indicates a successful, real-world connection established between users.                                                          |
| Ruby Highlight (Optional)   | `#e60000`    | *Use very sparingly*. For visual highlights *only* (not for text).                                                                 |
| Ruby Shadow                 |  `#3f0000`     | Optional, for subtle gradients and outlines.                                                                              |
| **Secondary Colors:**        |             |                                                                                                                                    |
| Dark Blue (Waveform/Accents)| `#001F3F`     | Sinusoidal waveform on the AI indicator, subtle UI accents.                                                                       |
| Electric Blue (Accent)      | `#00FFFF`     |  **Use sparingly.** Highlights, AI communication/information, specific data types, hover/active states, loading indicators. *Never for body text.* |
| **Neutral Colors:**          |             |                                                                                                                                    |
| Black (Background)          | `#000000`     | Main background color.                                                                                                           |
| Dark Gray (Text)            | `#333333`     | Body text.                                                                                                                      |
| Medium Gray (UI Elements)   | `#666666`     | UI elements, separators, less prominent text.                                                                                    |
| Light Gray (Subtle)         | `#CCCCCC`     | Subtle backgrounds, hover states, inactive elements.                                                                              |
| White (Text/Highlights)     | `#FFFFFF`     | High-contrast text, highlights against dark backgrounds.                                                                           |

## Typography

*   **Primary Font (Headings):** [Montserrat](https://fonts.google.com/specimen/Montserrat) (Google Fonts) - Used for headings and prominent text. Weights: 400 (Regular), 700 (Bold).
*   **Secondary Font (Body Text):** [Open Sans](https://fonts.google.com/specimen/Open+Sans) (Google Fonts) - Used for body text and less prominent UI elements. Weight: 400 (Regular).

**Implementation (HTML - in `frontend/public/index.html`):**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
```

**Implementation (CSS - in `frontend/src/App.css`):**

```css
body {
  font-family: 'Open Sans', sans-serif; /* Corrected to Open Sans */
}

h1, h2, h3 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 700;
}
```

## Imagery

- Use authentic, diverse, and high-quality images that reflect real human connections.
- Avoid generic stock photography.
- Images should be optimistic, empowering, and aligned with the project's core values.
- All images must include detailed alt descriptions.

## UI Components

**Nodes Map:** UI elements should be visually represented as interconnected nodes, with lines indicating relationships and data flow. (See example images in `docs/assets/images/` - You'll need to add the correct relative paths after uploading the images.)

- Colors: Nodes and data connections should use the core color palette defined above. The electric blue (`#00FFFF`) can be used to represent a specific category of data or to highlight active/selected nodes.

**AI Agent Indicator:** A circular shape with a dynamic, multi-hued orange/red light at its center against a black background.

- **Pulsating Light:** The central light pulsates with a period of 1.5 seconds (adjustable), smoothly transitioning between `#FFC300` (brighter yellow-orange) and `#F86B03` (deeper orange). The intensity change should follow an ease-in-out timing function.
- **Blue Variant:** The blue color (`#001F3F`) can be used to indicate a different state of the AI agent (e.g., providing information, communicating with the user). The waveform color can change from blue, to orange and finally to ruby red, to represent the transition from AI interaction to real world connection.
- **Sinusoidal Waveform:** A sinusoidal waveform with a wavelength of 20 pixels (adjustable) and an amplitude of 5 pixels (adjustable) travels across the circle from left to right over a duration of 1 second (adjustable). The waveform color is `#001F3F` (dark blue).
- **Triangle Indicator:** A subtle, triangle shape using color `#800000`. The triangle should be within the circle, and should become clearly visible (increasing in opacity or brightness) when a direct, real-world connection is established between two users. The change must be smooth.

### Animation Parameters:

**Pulsating Light**
- `period: 1.5s (adjustable)`
- `colorStart: #FFC300`
- `colorEnd: #F86B03`
- `easing: ease-in-out`

**Sinusoidal Waveform**
- `wavelength: 20px (adjustable)`
- `amplitude: 5px (adjustable)`
- `duration: 1s (adjustable)`
- `color: #001F3F`

**Triangle Indicator**
- `color: #800000`
- `animation: smooth transition`

## Data Table

(See example image in `docs/assets/images/` - You'll need to add the correct relative path after uploading the image.)

- Clear column headers.
- Alternating row colors (light gray and a slightly darker shade).
- Sufficient spacing between rows and columns.
- Use Open Sans font for body text and Montserrat for headers.

## Collective Empowerment

ThinkAlike is committed to empowering not just individuals, but also groups of users. This means providing tools for:

- **Shared Data Visualization:** Groups should be able to see how their collective data is being used, similar to the individual DataTraceability component, but at a group level. (See mockup: [link to mockup image - to be created])
- **Collaborative Settings:** Groups should have mechanisms to collectively define their privacy settings, data sharing preferences, and AI interaction parameters. This could involve voting mechanisms or consensus-building tools.
- **Collective Action:** The platform should facilitate collective action and decision-making, enabling groups to work together towards shared goals.
