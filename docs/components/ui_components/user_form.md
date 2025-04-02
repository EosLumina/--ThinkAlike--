# Design Document: UserForm UI Component

---

## 1. Introduction and Description

The **UserForm** component is a standardized, reusable React component designed to handle user data input across the ThinkAlike platform. It provides a consistent structure for presenting form fields, managing form state, implementing robust data validation (both client-side and server-side feedback), and handling form submissions securely and transparently.

This component is essential for various workflows, including user registration, profile editing, community creation, settings configuration, and potentially interacting with specific features within Modes 1, 2, or 3. It embodies ThinkAlike's principles by ensuring:

*   **Clarity:** Form fields are clearly labeled and presented.
*   **Validation:** Data integrity is maintained through built-in validation, with clear error feedback.
*   **User Empowerment:** Users receive immediate feedback and understand input requirements.
*   **Consistency:** Provides a uniform look and feel for all data input tasks.
*   **Accessibility:** Built with accessibility standards in mind.

It integrates closely with individual input components (like `TextInput`, `SelectDropdown`) and validation feedback components (`DataValidationError`).

---

## 2. UI Components / Elements (Composition)

The `UserForm` component typically orchestrates several other reusable UI components:

*   **Form Fields:** Instances of specific input components like:
    *   `TextInput`
    *   `TextAreaInput`
    *   `SelectDropdown`
    *   `Checkbox` / `RadioGroup`
    *   (Potentially specialized inputs like date pickers, file uploads)

*   **Labels:** Associated with each form field for clarity (often part of the input component itself).
*   **Validation Feedback:** Instances of `DataValidationError` displayed near fields when validation fails.
*   **Submission Button:** An `ActionButton` component to trigger form submission.
*   **General Form Feedback Area:** A space to display overall form submission status (e.g., "Profile Updated Successfully", "Submission Failed: Please check errors below") or general API errors using the `Alert` component.

---

## 3. Core Functionality

*   **State Management:** Manages the state of all input fields within the form (their current values). This is often handled internally using React state hooks or, preferably, delegated to a form management library like `react-hook-form` for efficiency and feature richness.

*   **Client-Side Validation:** Performs validation checks as the user types (on change/blur) or upon submission, based on rules defined (e.g., via a schema prop). Provides immediate feedback using `DataValidationError`.

*   **Submission Handling:**
    *   Prevents submission if client-side validation fails.
    *   Calls a provided `onSubmit` prop function when validation passes, passing the structured form data.
    *   Handles the loading/pending state of the submission button (`ActionButton`).

*   **Backend Error Display:** Receives and displays backend validation errors (passed back via props after an API submission fails) next to the relevant fields or in the general feedback area.

*   **Accessibility:** Ensures proper label association (`htmlFor`), keyboard navigation, and ARIA attributes for form elements.

---

## 4. Data Flow

1. **Initialization:** Form is rendered with optional `initialData`.
2. **User Input:** User interacts with input components (e.g., `TextInput`).
3. **State Update:** Input component’s `onChange` handler updates the `UserForm`’s internal state (or the state managed by `react-hook-form`).
4. **Client-Side Validation (onChange/onBlur):** Validation rules are checked for the changed field. If errors, `DataValidationError` is displayed.
5. **Submission Attempt:** User clicks the submission `ActionButton`.
6. **Client-Side Validation (onSubmit):** All fields are validated. If errors exist, submission is blocked, and errors are displayed.
7. **`onSubmit` Prop Execution:** If client-side validation passes, the `UserForm` calls the `onSubmit(formData)` function provided by the parent component, passing the current form data.
8. **API Call (Parent Component):** The parent component typically handles the actual API submission using the `formData`.
9. **Backend Response Handling (Parent Component):** Parent receives API response.
10. **Feedback / Backend Error Display:**
    *   If API call is successful, parent might display a success message (e.g., using `Alert`) or navigate away.
    *   If API call fails with validation errors, parent passes these errors back to the `UserForm` (e.g., via a `serverErrors` prop), which then displays them using `DataValidationError`. General API errors are shown in the form’s feedback area.

```mermaid
graph LR
    A[User Interaction (Input Field)] --> B{UserForm State Management};
    B -- Updates --> C[Input Component Value];
    B -- Triggers Validation --> D{Client-Side Validation Logic};
    D -- Validation Result --> B;
    D -- Errors? --> E(DataValidationError Display);
    F[User Interaction (Submit Button)] --> G{onSubmit Validation};
    G -- Validation OK? --> H(Call onSubmit Prop);
    G -- Validation Failed? --> E;
    H --> I[API Call (Parent Component)];
    I -- Success --> J[Display Success / Navigate];
    I -- Failure --> K[Return Errors to UserForm];
    K --> E;
```

---

## 5. Code Implementation Notes

**Framework:** React.
**Form Management Library (Recommended):** Use `react-hook-form` or Formik. These libraries handle state management, validation, and submission logic efficiently. Using a library is generally preferred over custom state management for complex forms.

### Props

*   **onSubmit**: (Function, Required) Callback function executed on successful validation and submission. Receives form data object as an argument. Async-compatible.
*   **initialData**: (Object, Optional) Pre-populates form fields.
*   **validationSchema**: (Object, Optional) Schema defining validation rules (e.g., Yup schema for `react-hook-form` or a custom format).
*   **serverErrors**: (Object, Optional) An object mapping field names to backend error messages (e.g., `{ email: "Email already exists." }`).
*   **isLoading**: (Boolean, Optional) Controls the loading state of the submission button. Passed down to `ActionButton`.
*   **children**: (ReactNode, Required) The actual form field components (`TextInput`, `SelectDropdown`, etc.) are passed as children.
*   **className**: (String, Optional) Additional CSS class.

### Implementation Strategy (with `react-hook-form`)

1. Use the `useForm` hook from `react-hook-form`.
2. Pass `register` function from `useForm` to each child input component to manage state and validation.
3. Use `handleSubmit` from `useForm` to wrap the `onSubmit` prop so that client-side validation occurs automatically.
4. Use `formState.errors` to display client-side errors.
5. Use `setError` from `useForm` to manually set errors received from the `serverErrors` prop.

```javascript
// filepath: c:\ThinkAlike\docs\components\ui_components\user_form.md
import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
// import { yupResolver } from '@hookform/resolvers/yup'; // Example resolver
// import * as yup from 'yup'; // Example validation library

import ActionButton from './ActionButton';
import DataValidationError from './DataValidationError';
import Alert from './Alert'; // For general feedback

// Example schema (using yup)
// const schema = yup.object().shape({
//   username: yup.string().required('Username is required').min(3),
//   email: yup.string().email('Invalid email format').required('Email is required'),
// });

function UserForm({
  onSubmit,
  initialData = {},
  validationSchema, // Optionally pass the yup schema here
  serverErrors,
  isLoading,
  children,
  className,
  submitButtonText = 'Submit'
}) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
    reset
  } = useForm({
    defaultValues: initialData,
    // resolver: yupResolver(validationSchema), // Integrate schema validation if needed
  });

  // Effect to set server errors when they change
  useEffect(() => {
    if (serverErrors) {
      Object.entries(serverErrors).forEach(([fieldName, message]) => {
        setError(fieldName, { type: 'server', message });
      });
    }
  }, [serverErrors, setError]);

  // Reset form if initialData changes
  useEffect(() => {
    reset(initialData);
  }, [initialData, reset]);

  // Wrap each child to pass register() and error info (if child has a name)
  const enhancedChildren = React.Children.map(children, (child) => {
    if (React.isValidElement(child) && child.props.name) {
      return React.cloneElement(child, {
        ...child.props,
        register,
        error: errors[child.props.name],
      });
    }
    return child;
  });

  // Find a general server error if provided
  const generalServerError = serverErrors?.general || serverErrors?.detail;

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className={`user-form ${className || ''}`}
      noValidate
    >
      {generalServerError && (
        <Alert type="error" message={generalServerError} />
      )}

      {enhancedChildren}

      {/* Render errors NOT associated with a specific named field */}
      {Object.entries(errors)
        .filter(
          ([fieldName]) =>
            !React.Children.toArray(children).some(
              (childElement) =>
                React.isValidElement(childElement) &&
                childElement.props.name === fieldName
            )
        )
        .map(([fieldName, error]) => (
          <DataValidationError key={fieldName} message={error.message} />
        ))}

      <ActionButton type="submit" isLoading={isLoading} disabled={isLoading}>
        {submitButtonText}
      </ActionButton>
    </form>
  );
}

export default UserForm;
```

---

## 6. Validation Integration

**Client-Side:** Define rules using a schema (`validationSchema` prop, e.g., Yup) or directly within the form component. Use `react-hook-form`'s resolver integration or built-in validation. Errors are displayed immediately using `DataValidationError`.

**Server-Side:** Backend API validates submitted data. If errors occur, the API response should include a structured error object (e.g., `{ "field_name": "Error message", "email": "Invalid format." }`). The parent component passes this object to `UserForm` via the `serverErrors` prop. `UserForm` uses the `setError` function (from `react-hook-form`) to display these errors next to the corresponding fields.

---

## 7. Ethical Considerations

**Data Minimization:** Forms should only include fields that are strictly necessary for the intended action, avoiding collection of superfluous data. Labels and help text should clarify why data is needed.

**Clear Labeling:** All fields must have clear, unambiguous labels. Use placeholder text judiciously; it should not replace labels.

**Transparent Error Messaging:** Validation errors (client and server) must be clear, constructive, and tell the user how to fix the problem, not just that there is one. Avoid overly technical jargon.

**Consent:** For forms collecting sensitive data or data for non-essential purposes, include clear consent mechanisms (e.g., Checkbox linked to privacy policy) as part of the form structure.

---

## 8. Testing Instructions

**Rendering:** Verify the form renders correctly with all child input components and the submit button, using `initialData` if provided.

**State Updates:** Interact with input fields and verify the form's internal state updates correctly.

**Client-Side Validation:**

* Test valid input: Ensure no errors are shown.
* Test invalid input (required fields, format errors, min/max length): Verify correct error messages appear next to the relevant fields using `DataValidationError` upon blur/change or submit.
* Test form submission blocking when validation fails.

**Submission Handling:**

* Test successful submission: Provide valid data, click submit. Verify the `onSubmit` prop is called with the correct `formData`. Verify loading state on the `ActionButton`.
* Test submission failure (Backend Validation): Mock an API response with `serverErrors`. Verify these errors are passed back via props and displayed correctly next to the relevant fields.

**Accessibility:** Test keyboard navigation through all form fields and the submit button. Verify correct label association (`htmlFor`). Test ARIA attributes (`aria-invalid`, `aria-describedby`) are set correctly when errors are present. Test with screen readers.

**Reset/Initial Data:** Verify the form populates correctly with `initialData` and resets properly if `initialData` changes.

---

## 9. UI Mockup Placeholder

Refer to the project's central design repository for visual mockups of standard form layouts.

[Placeholder: Link or embed visual mockup of a typical UserForm layout, showing input fields, labels, validation errors, and submit button here]

---

## 10. Dependencies & Integration

**Depends On:**

* Reusable input components (`TextInput`, `SelectDropdown`, etc.).
* `DataValidationError` component.
* `ActionButton` component.
* `Alert` component (optional, for general feedback).
* Form management library (`react-hook-form` recommended).
* Validation library (`yup` recommended if using resolver).
* ThinkAlike Style Guide (styling).

**Integrates With:**

* Parent components that manage data fetching and API submission logic.
* API services.

---

## 11. Future Enhancements

* Support for multi-step forms/wizards.
* Conditional logic for showing/hiding fields based on other field values.
* Integration with asynchronous validation rules.
* Saving form drafts locally.
* More sophisticated layout options (e.g., grid-based field arrangement).
