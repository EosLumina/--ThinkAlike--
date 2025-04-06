// filepath: C:\--ThinkAlike--\docs\guides\user_guides\connected_services_guide.md
# Managing Connected Services & Data Sources

---

## 1. Introduction

Welcome to your **Connected Services & Data Sources** center! ThinkAlike offers you the **option** to connect certain external service accounts you use (like Goodreads for books or Spotify for music) to potentially enhance your experience on our platform.

Connecting these services can provide ThinkAlike with supplementary insights into your interests and cultural tastes, which *might* help improve the relevance of suggested connections (in Mode 2: Profile Discovery) or communities (in Mode 3: Community Building).

This guide explains how this feature works, putting **you in complete control**. You decide *if* you want to connect any service, *what specific permissions* you grant ThinkAlike on that service, and *exactly how* any retrieved data can be used within ThinkAlike. This feature is designed according to our strict [Ethical Guidelines](../../core/ethics/ethical_guidelines.md), prioritizing your privacy, consent, and data sovereignty.

**Connecting external services is entirely optional.** ThinkAlike's core functionality works effectively based on the information you provide directly within the platform (like your choices in Mode 1 or details in your profile).

---

## 2. How Connecting Services Can Help (Potentially)

By granting ThinkAlike limited, read-only access to data from services you choose to connect, you *may* enable:

*   **Richer Interest Matching:** Identifying shared specific interests (e.g., favourite authors on Goodreads, shared music genres on Spotify) can add another layer to compatibility assessment, alongside core value alignment.
*   **More Relevant Community Suggestions:** Help us suggest communities focused on specific hobbies or cultural areas reflected in your connected services (e.g., a book club, a genre-specific music fan group).
*   **(Optional) Enhanced Profile Display:** You might choose to allow ThinkAlike to display certain insights (like your top genres) on your profile to spark conversations.

**Our Commitment:**
*   We only request **minimal necessary permissions**.
*   We are **transparent** about what data is accessed and how it's used ([DataTraceability](../../components/ui_components/data_traceability.md) will reflect this).
*   **You control** if and how this data is used via simple toggles.
*   We **do not sell** this data or use it for unrelated advertising.
*   You can **disconnect** at any time, and we will delete the associated data.

---

## 3. Finding Your "Connected Services" Panel

Manage your connections easily:

1.  Log in to your ThinkAlike account.
2.  Navigate to your main **Settings** or **Profile Management** area.
3.  Look for the **"Connected Services"** (or similar wording like "Integrations" or "Data Sources") section.

This panel lists all the external services ThinkAlike currently supports integration with.

---

## 4. Connecting a Service (Example: Goodreads)

Let's walk through connecting your Goodreads account:

1.  **Locate Goodreads:** Find "Goodreads" in the list within the "Connected Services" panel. It will show "Not Connected".
2.  **Click "Connect":** Select the "Connect" button next to Goodreads.
3.  **Redirect to Goodreads:** Your browser will be securely redirected to the official Goodreads website. ThinkAlike never sees your Goodreads password.
4.  **Log In & Authorize:**
    *   Log in to your Goodreads account if prompted.
    *   Goodreads will show you exactly what permissions ThinkAlike is requesting (e.g., "Allow ThinkAlike to view your profile information and book shelves"). **Review these permissions carefully.** We only ask for what's needed to understand reading interests.
    *   Click "Authorize" (or similar button) on the Goodreads page if you agree.
5.  **Return to ThinkAlike:** You'll be automatically redirected back to your "Connected Services" panel in ThinkAlike.
6.  **Status Update:** Goodreads should now show as "Connected".

---

## 5. Controlling How Data is Used (Opt-In Required!)

**IMPORTANT:** Simply connecting a service **does not** automatically allow ThinkAlike to use its data for features like matching. You must explicitly opt-in for each specific use case:

1.  **Expand Service Details:** Click on the connected service (e.g., "Goodreads") in your panel to see more details.
2.  **Review Permissions:** You'll see a reminder of the permissions you granted (e.g., "Access Granted: Read book shelves").
3.  **Enable Usage Toggles:** Find the "Data Usage Consent" toggles. **They are OFF by default.** Turn ON the specific ways you want ThinkAlike to use this data:
    *   `[ ] Use Goodreads data for Match Discovery?` *(Allows the matching algorithm to consider shared reading interests)*
    *   `[ ] Use Goodreads data for Community Recommendations?` *(Allows suggesting book clubs or literary groups)*
    *   `[ ] Display reading insights (e.g., top genres) on my Profile?` *(Makes this info visible to others based on your main profile visibility settings)*
4.  **Save (If Necessary):** Changes might save automatically, or you might need to click a "Save Settings" button. The UI will provide confirmation.

You can change these toggles back to OFF at any time.

---

## 6. Checking Accessed Data (Transparency)

Want to see what information ThinkAlike has accessed from a connected service?

1.  In the "Connected Services" panel, find the connected service.
2.  Look for the "Last Synced" timestamp to see when data was last fetched.
3.  Click the link typically labeled **"View Harvested Data in Data Explorer"**.
4.  This will take you to your `Data Explorer Panel`, likely filtered to show only the data points originating from that specific service (e.g., your list of read books from Goodreads).

---

## 7. Disconnecting a Service

You are always in control and can disconnect a service easily:

1.  Go to the "Connected Services" panel.
2.  Find the service you want to disconnect (e.g., Goodreads).
3.  Click the **"Disconnect"** button.
4.  A confirmation pop-up will likely appear asking if you're sure. Confirm your choice.
5.  **What Happens:** ThinkAlike securely deletes the access tokens for that service and removes the harvested data associated with it from our active systems. We also attempt to revoke access directly via the service's API where possible.
6.  **Status:** The service will now show as "Not Connected".

**(Optional Tip):** For complete peace of mind, you can also usually visit the settings page of the external service itself (e.g., Goodreads App Settings) and manually revoke ThinkAlike's access there too.

---

By providing these clear controls and transparent processes, ThinkAlike aims to make third-party data integration an empowering and trustworthy optional feature for enhancing your connection experience.

---
**Document Details**
- Title: Managing Connected Services & Data Sources
- Type: User Guide
- Version: 1.0.0
- Last Updated: 2025-04-05
---
End of Managing Connected Services & Data Sources
---


