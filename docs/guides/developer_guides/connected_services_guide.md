# Managing Connected Services & Data Sources

---

## 1. Introduction

Welcome to your **Connected Services & Data Sources** center! ThinkAlike allows you to optionally connect certain external service accounts (like Goodreads or Spotify) to potentially enhance your experience by providing supplementary insights for discovering like-minded connections and communities.

This guide explains how this feature works, emphasizing **your complete control** over which services you connect, what data is accessed, and exactly how that data is used within ThinkAlike. Connecting external services is **entirely optional** and designed with your privacy and agency as the top priority, adhering to our [Ethical Guidelines](../../core/ethics/ethical_guidelines.md).

---

## 2. Why Connect External Services?

Connecting services like Goodreads or Spotify can potentially help ThinkAlike:

* **Refine Your Value/Interest Profile:** Data like your reading habits or music tastes can add nuance to your profile, supplementing the insights gained from your Narrative Mode journey and explicit profile entries.

* **Improve Match Discovery (Mode 2):** Identifying shared interests (e.g., favorite authors, artists, genres) derived from connected services can act as an *additional* signal, alongside core value alignment, when suggesting potential connections.

* **Enhance Community Recommendations (Mode 3):** Help suggest relevant communities based on shared cultural tastes or hobbies derived from connected services (e.g., suggesting a book club based on Goodreads data).

* **(Optional) Enrich Your Profile Display:** You can choose to display certain interests derived from connected services (like top genres) on your profile, offering more conversation starters for potential connections.

**Important:** ThinkAlike uses this data ethically and transparently. We only request minimal permissions, and **you control exactly how this data is used** within the platform via specific toggles (see Section 4).

---

## 3. Accessing the "Connected Services" Panel

You can manage your external service connections from your main account settings:

1. Navigate to your **User Profile** or **Settings** area within ThinkAlike.
2. Look for a section or menu item labeled **"Connected Services"**, **"Data Sources"**, or **"Integrations"**.
3. Clicking this will open the dedicated management panel.

---

## 4. Connecting a New Service (Example: Goodreads)

The "Connected Services" panel lists supported third-party platforms.

1. **Find the Service:** Locate the service you wish to connect (e.g., Goodreads). It will show as "Not Connected".
2. **Click "Connect":** Click the "Connect" button next to the service name.
3. **External Authorization:** You will be redirected securely to the external service's website (e.g., Goodreads.com).

    * **Log In:** You may need to log in to your account on that external service if you aren't already.

    * **Review Permissions:** The service will display a screen showing *exactly* what permissions ThinkAlike is requesting (e.g., "Allow ThinkAlike to read your 'read' shelf"). **ThinkAlike only requests minimal, read-only permissions necessary for the feature.** Review these carefully.

    * **Authorize:** If you agree to the permissions, click "Authorize" or "Allow" on the external service's page.

4. **Redirect Back:** You will be redirected back to your ThinkAlike "Connected Services" panel.
5. **Confirmation:** The panel will now show the service (e.g., Goodreads) as "Connected".

---

## 5. Managing Data Usage (Crucial Step!)

Connecting a service **DOES NOT** automatically mean ThinkAlike starts using its data everywhere. You have granular control:

1. **Find the Connected Service:** Locate the service you just connected (e.g., Goodreads) in your "Connected Services" list.
2. **Review Permissions Granted:** The panel will remind you of the permissions you granted on the external site (e.g., "Access Granted: Read 'read' shelf").
3. **Configure Data Usage Toggles:** You will see specific toggles (switches) for how ThinkAlike can use the data from this service. **These default to OFF.** You must actively **turn them ON** to enable specific uses:

    * `[OFF] Use Goodreads data for Match Discovery (Mode 2)?`

    * `[OFF] Use Goodreads data for Community Recommendations (Mode 3)?`

    * `[OFF] Display favorite genres/authors from Goodreads on my Profile?`

4. **Toggle On Desired Uses:** Switch the toggle(s) to ON for the specific ways you want ThinkAlike to utilize the data from that service. Changes are usually saved automatically, or via a "Save Settings" button.
5. **Transparency:** The UI clearly shows which uses are enabled or disabled for each connected service.

---

## 6. Viewing Harvested Data

ThinkAlike promotes transparency. You can see what data has been accessed from your connected services:

1. **Check "Last Synced":** The "Connected Services" panel shows when data was last fetched.
2. **Navigate to Data Explorer:** Click the link provided within the "Connected Services" panel (often labeled "View Harvested Data" or similar) to navigate to your `Data Explorer Panel`.
3. **Filter by Source:** Within the Data Explorer, filter the data points by source (e.g., select "Goodreads") to see the specific information ThinkAlike has retrieved based on your permissions and usage toggles.

---

## 7. Disconnecting a Service

You can disconnect a service and revoke ThinkAlike's access at any time:

1. **Go to "Connected Services":** Navigate to the management panel in your settings.
2. **Find the Service:** Locate the service you wish to disconnect.
3. **Click "Disconnect":** Click the prominent "Disconnect" button next to the service.
4. **Confirm:** You may be asked to confirm your choice.
5. **Action:** Upon confirmation:

    * ThinkAlike will securely delete the stored access/refresh tokens for that service.

    * ThinkAlike will delete the harvested data associated with that service from its active systems.

    * ThinkAlike will attempt to revoke its access grant via the third-party service's API, if supported. (You may also want to manually revoke access via the third-party service's own settings page for full certainty).

6. **Status Update:** The service will now show as "Not Connected" in your panel.

---

## 8. Your Privacy and Control

* Connecting external services is **always optional**.

* You grant permissions directly on the **external service's platform**.

* You control **how** ThinkAlike uses the data via specific **opt-in toggles**.

* You can **disconnect** any service and have associated data deleted at **any time**.

* ThinkAlike uses this data **only** to enhance your experience as described and consented to, never for unrelated advertising or sale to third parties.

Managing your connected services gives you powerful control over how different facets of your digital life can enrich your ThinkAlike experience, always guided by your explicit consent and our commitment to transparency.

---

**Document Details**

* Title: Managing Connected Services & Data Sources

* Type: Developer Guide

* Version: 1.0.0

* Last Updated: 2025-04-05

---

End of Managing Connected Services & Data Sources

---
