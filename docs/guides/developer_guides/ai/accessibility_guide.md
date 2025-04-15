# Accessibility Implementation Guide (A11y)

## 1. Introduction

Accessibility (a11y) is fundamental to ThinkAlike's values of **Ethical Humanism** and **Inclusivity**. This guide provides developers practical guidelines for building an accessible React frontend, ensuring usability for people with diverse abilities, including those using assistive technologies.

Our target is **WCAG 2.1 Level AA** compliance. Accessibility must be integral to design, implementation, and testing, not an afterthought.

Refer to [Ethical Guidelines](../core/ethics/ethical_guidelines.md) and the [Testing Plan](./testing_and_validation_plan.md).

---

## 2. Core Principles (POUR)

* **Perceivable:** Content presentation must accommodate different senses (e.g., `alt` text for images, captions). Ensure sufficient color contrast.

* **Operable:** All interactions possible via keyboard; no keyboard traps; adequate time for users; avoid seizure-inducing content.

* **Understandable:** Clear language, predictable navigation, consistent layouts, helpful error feedback.

* **Robust:** Use standard technologies (HTML, ARIA) correctly so assistive technologies can interpret content reliably.

---

## 3. Key Implementation Guidelines (React)

### 3.1 Semantic HTML

* **Use Standard Elements:** Prioritize semantic elements (`<button>`, `<nav>`, `<main>`, `<h1>`-`<h6>`, `<ul>`, `<input>`, `<label>`, etc.) over generic `<div>`s/`<span>`s for interactive or structural content.

* **Logical Structure:** Use headings hierarchically. Structure content with lists, sections, and landmark roles (`<header>`, `<nav>`, `<main>`, `<footer>`).

### 3.2 Keyboard Accessibility

* **Focusability:** All interactive elements must be keyboard focusable (Tab/Shift+Tab). Use `tabindex="0"` *only* when making non-interactive elements (like custom controls built with divs) focusable. Use `tabindex="-1"` to remove from tab order but allow programmatic focus.

* **Visible Focus:** Ensure a clear `:focus` or `:focus-visible` style (do not disable `outline` without a better alternative). Consistent with [Style Guide](./style_guide.md).

* **Logical Order:** Focus should follow visual flow. Manage focus programmatically in modals, menus, or dynamic content changes (`element.focus()`). Avoid keyboard traps.

* **Interaction:** Interactive elements must respond to Enter/Space keys appropriately (e.g., buttons activate, checkboxes toggle).

### 3.3 ARIA (Accessible Rich Internet Applications)

* **Use When Necessary:** Apply ARIA to bridge gaps where native HTML semantics are insufficient (custom widgets, dynamic updates). Incorrect ARIA is worse than no ARIA. **Prefer semantic HTML first.**

* **Key Attributes:**

  * **Roles:** `role="button"`, `menu`, `dialog`, `alert`, `status`, etc., for custom components.

  * **Properties:** `aria-label` (for elements without visible text, like icon buttons), `aria-labelledby` (link to visible label), `aria-describedby` (link to descriptions/errors), `aria-invalid="true"`, `aria-required="true"`.

  * **States:** `aria-expanded`, `aria-selected`, `aria-disabled`, `aria-current`, `aria-hidden="true"`.

  * **Live Regions:** `aria-live="polite"` (non-urgent updates) or `aria-live="assertive"` (urgent updates like errors) for content that changes dynamically.

* **Validation:** Use browser dev tools (Accessibility tab) and linters.

### 3.4 Forms and Labels

* **Explicit Labels:** Every input (`input`, `textarea`, `select`) needs a `<label>` linked via `htmlFor` (React prop for `for`).

* **Grouping:** Use `<fieldset>`/`<legend>` for related radio buttons/checkboxes.

* **Required Fields:** Indicate visually (`*`) and programmatically (`required`, `aria-required="true"`).

* **Error Handling:** Link error messages (`DataValidationError`) to inputs using `aria-describedby`. Errors must be clear and helpful.

### 3.5 Images, Icons, and Media

* **`alt` Text:** Meaningful images need descriptive `alt` text. Decorative images use `alt=""`. Icons used as controls need accessible names (e.g., via `aria-label` on the button).

* **Complex Images/Charts:** Provide text summaries or data tables nearby or via `aria-describedby`.

* **Multimedia:** Videos need accurate captions and preferably transcripts. Audio needs transcripts. Consider audio descriptions for visual content if central to understanding.

### 3.6 Color and Contrast

* **WCAG AA Contrast:** Text/background contrast must meet 4.5:1 (normal text) or 3:1 (large text, UI graphics). Use contrast checkers.

* **Information:** Don't rely *only* on color to convey information (e.g., error states need an icon/text too).

---

## 4. Testing Accessibility

Incorporate accessibility testing throughout the development cycle.

* **Automated Tools:**

  * **Linters:** `eslint-plugin-jsx-a11y` configured in the project.

  * **Testing Libraries:** Integrate `jest-axe` with Jest/React Testing Library tests. Integrate Cypress-axe for E2E tests.

  * **Browser Extensions:** Use axe DevTools, WAVE during manual checks.

* **Manual Keyboard Testing:** Navigate key workflows using only Tab, Shift+Tab, Enter, Space, Arrow Keys. Check focus visibility and order.

* **Screen Reader Testing:** Test primary user flows with major screen readers (NVDA, VoiceOver, JAWS). Verify content is announced logically and controls are operable.

* **User Testing:** Include users with disabilities in UAT sessions when feasible.

---

## 5. Tools & Resources

* **WCAG 2.1:** [w3.org/TR/WCAG21/](https://www.w3.org/TR/WCAG21/)

* **axe-core & Tools:** [deque.com/axe/](https://www.deque.com/axe/)

* **WebAIM:** [webaim.org](https://webaim.org) (Resources, Contrast Checker)

* **MDN Accessibility Docs:** [developer.mozilla.org/en-US../Web/Accessibility](https://developer.mozilla.org/en-US../Web/Accessibility)

* **WAI-ARIA Authoring Practices:** [w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/) (Guidance for custom widgets)

---

Accessibility is an ongoing commitment integral to ThinkAlike's mission. Build inclusively.

---

**Document Details**

* Title: Accessibility Implementation Guide (A11y)

* Type: Developer Guide

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Accessibility Implementation Guide (A11y)

---
