# Product Requirements (PRD)

## Context
This document outlines the product and engineering requirements for a **Smart Link Shortener** service. The service's primary function is to accept a long URL and generate a unique, shortened version. When a user accesses the short link, they are redirected to the original URL, and this interaction (a "click") is tracked. The system is designed to be extensible, with a data model that supports both immediate, simple analytics and future, more complex analytical features. All functionality will be exposed via a RESTful API, and a simple frontend will be developed to interact with it.

## Data Model for Reference

The data model consists of two core tables: `links` and `visits`.

### Table: `links`

| Column Name | Data Type (SQLite) | Constraints / Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`. The unique identifier for each link record. |
| `original_url` | `TEXT` | `NOT NULL, UNIQUE`. The original, long URL. |
| `short_code` | `TEXT` | `NOT NULL, UNIQUE`. The unique code for the shortened URL. |
| `created_at` | `DATETIME` | `NOT NULL, DEFAULT CURRENT_TIMESTAMP`. Timestamp of creation. |
| `last_visited_at` | `DATETIME` | `NULL`. Timestamp of the most recent click. |
| `click_count` | `INTEGER` | `NOT NULL, DEFAULT 0`. A counter for the total number of clicks. |

### Table: `visits`

| Column Name | Data Type (SQLite) | Constraints / Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT`. The unique identifier for each visit. |
| `link_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(links.id)`. Reference to the visited link. |
| `visited_at` | `DATETIME` | `NOT NULL, DEFAULT CURRENT_TIMESTAMP`. Timestamp of the click. |

---
---

## Feature 1: Create a Short Link

This feature allows a user to submit a long URL and receive a shortened version. The system must handle new submissions and URLs that have been submitted previously.

### **1.1: API for Link Creation**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to accept a `POST` request containing an `original_url`, so that I can generate a unique `short_code`, save the link to the database, and return the new link object.
* **Acceptance Criteria:**
    * **Given** the service receives a `POST` request to `/api/v1/links` with a JSON body containing a unique `original_url`.
    * **When** the request is processed.
    * **Then** the service should generate a new, unique `short_code`.
    * **And** a new record should be inserted into the `links` table with the `original_url` and the new `short_code`.
    * **And** the service should respond with a `201 Created` status and a JSON body of the newly created link object.
    * ---
    * **Given** the service receives a `POST` request to `/api/v1/links` with an `original_url` that already exists in the `links` table.
    * **When** the request is processed.
    * **Then** the service should not create a new record.
    * **And** it should retrieve the existing record.
    * **And** respond with a `200 OK` status and a JSON body of the existing link object.
* **Architecture Design Notes:**
    * Implement the `POST /api/v1/links` endpoint in a framework like FastAPI.
    * The logic must first query the `links` table to see if the `original_url` exists, leveraging the `UNIQUE` constraint and index for performance.
    * If it exists, return the existing record.
    * If it does not exist, the application logic must generate a unique `short_code`. A common strategy is to use a base62 encoding of the auto-incrementing `id` or a sufficiently random hash. The logic must ensure uniqueness before insertion.
    * Insert the new record and return it to the client.

### **1.2: Submit a Long URL for Shortening**

* **Story Type:** Frontend
* **Story:** As a user, I want to paste a long URL into an input field and click a "Shorten" button, so that I can receive a short, easy-to-share link.
* **Design / UX Considerations:**
    * The UI should have a prominent, clear input field for the `original_url`.
    * A "Shorten" or "Create Link" button should trigger the action.
    * After submission, the resulting short link should be displayed clearly, with a "Copy to Clipboard" button for convenience.
    * Display a loading indicator while the API call is in progress.
    * Handle and display API errors gracefully (e.g., "Invalid URL format").
* **Acceptance Criteria:**
    * **Given** a user is on the main page
    * **When** they enter a valid URL (e.g., `https://www.google.com`) into the input field and click "Shorten"
    * **Then** the page should display the newly generated short link (e.g., `http://your.domain/aB3xY7`).
    * **And** a "Copy" button should appear next to the short link.
* **Architecture Design Notes:**
    * The frontend will be built using a modern JavaScript framework (e.g., React, Vue).
    * The "Shorten" button will trigger an asynchronous `POST` request to the `/api/v1/links` endpoint.
    * The request body will be a JSON object: `{ "original_url": "..." }`.
    * The component will update its state with the returned link object from the API to display the `short_code`.
* **Dependencies:** Story 1.1 (Backend: API for Link Creation) must be completed.

---
---

## Feature 2: Redirect Short Link

This feature is the core purpose of the service: redirecting a user from the short link to its original destination URL.

### **2.1: Handle Redirection and Track Visit**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to receive a request for a `short_code`, so that I can log the visit, update analytics, and redirect the user to the corresponding `original_url`.
* **Acceptance Criteria:**
    * **Given** a valid `short_code` exists in the `links` table.
    * **When** the service receives a `GET` request to `/{short_code}` (e.g., `http://your.domain/aB3xY7`).
    * **Then** the `click_count` on the corresponding `links` record should be incremented by 1.
    * **And** the `last_visited_at` timestamp on the `links` record should be updated to the current time.
    * **And** a new record should be inserted into the `visits` table with the correct `link_id`.
    * **And** the service should respond with an HTTP `302 Found` redirect to the `original_url`.
* **Architecture Design Notes:**
    * This endpoint is not part of the `/api/v1` namespace. It should be configured at the application's root path to capture requests like `GET /aB3xY7`.
    * The logic must perform the following actions, ideally within a single database transaction to ensure data integrity:
        1.  Look up the `short_code` in the `links` table. If not found, trigger the logic in Story 2.2.
        2.  Retrieve the `link.id` and `link.original_url`.
        3.  Execute an `UPDATE` statement on the `links` table to increment `click_count` and set `last_visited_at`.
        4.  Execute an `INSERT` statement into the `visits` table with the `link.id`.
        5.  Return an HTTP 302 Redirect response with the `Location` header set to the `original_url`.
* **Related Stories:** The logic for creating a visit log entry is formally defined in Story 3.1 but is executed as part of this flow.

### **2.2: Handle Non-Existent Short Link**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to handle requests for `short_code`s that do not exist, so that the user receives an appropriate error.
* **Acceptance Criteria:**
    * **Given** a `short_code` does not exist in the `links` table.
    * **When** the service receives a `GET` request to `/{short_code}`.
    * **Then** the service should respond with an HTTP `404 Not Found` status code.
* **Architecture Design Notes:**
    * This is the failure path for the lookup logic described in Story 2.1.
    * The response body for the 404 error should be minimal or a simple JSON object like `{ "detail": "Not Found" }`.

---
---

## Feature 3: View Link Analytics

This feature allows a user to see basic analytics for a given short link and provides the backend mechanism for logging those analytics.

### **3.1: API for Creating a Visit Log**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to accept a `POST` request with a `link_id`, so that I can create a new entry in the `visits` table to log a click event.
* **Acceptance Criteria:**
    * **Given** the service receives a `POST` request to `/api/v1/visits` with a JSON body containing a valid `link_id`.
    * **When** the request is processed.
    * **Then** a new record should be inserted into the `visits` table with the provided `link_id` and the `CURRENT_TIMESTAMP`.
    * **And** the service should respond with a `201 Created` status and a JSON body of the newly created visit object.
* **Architecture Design Notes:**
    * This endpoint is designed to be called internally, primarily by the redirection logic in Story 2.1. While exposed via the API, its main consumer is the service itself.
    * The endpoint should validate that the provided `link_id` exists in the `links` table to maintain referential integrity.

### **3.2: Display Analytics for a Short Link**

* **Story Type:** Frontend
* **Story:** As a user, I want to enter a short code into a form, so that I can view its total click count and the last time it was visited.
* **Design / UX Considerations:**
    * Create a separate "Analytics" page or section.
    * Include an input field for the `short_code` and a "View Stats" button.
    * Display the results clearly, for example: "Total Clicks: 150", "Last Visited: 2025-06-15 10:30:00 UTC".
    * If the short code is not found, display a "Link not found" message.
* **Acceptance Criteria:**
    * **Given** a user is on the Analytics page.
    * **When** they enter a valid, existing `short_code` and click "View Stats".
    * **Then** the page should display the `click_count` and `last_visited_at` data for that link.
    * ---
    * **Given** a user is on the Analytics page.
    * **When** they enter a `short_code` that does not exist and click "View Stats".
    * **Then** the page should display an appropriate "Not Found" message.
* **Architecture Design Notes:**
    * This feature requires a way to get a link's data by its `short_code`. Since the provided API endpoints use `{id}`, the frontend will first need to get the list of all links and find the one with the matching `short_code`.
    * On button click, the component will fetch data from `GET /api/v1/links`.
    * It will then filter the returned array to find the object where `link.short_code` matches the user's input.
    * If found, it will display the `click_count` and `last_visited_at` properties. If not found, it will display an error.
* **Dependencies:** Story 4.1 (Backend: API for Listing All Links) must be completed.

---
---

## Feature 4: Admin Link Management

This feature provides administrative capabilities to view, update, and delete all links in the system.

### **4.1: API for Listing All Links**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to provide an endpoint that returns a list of all link objects, so that an admin interface can display them.
* **Acceptance Criteria:**
    * **Given** there are records in the `links` table.
    * **When** the service receives a `GET` request to `/api/v1/links`.
    * **Then** the service should respond with a `200 OK` status and a JSON array of all link objects.
* **Architecture Design Notes:**
    * Implement the `GET /api/v1/links` endpoint.
    * The implementation should perform a `SELECT * FROM links`.
    * For production systems, this endpoint should be paginated to avoid performance issues with large datasets.

### **4.2: View All Created Links**

* **Story Type:** Frontend
* **Story:** As an admin, I want to view a list of all the links in the system, so that I can have an overview of all short links, their destinations, and creation dates.
* **Design / UX Considerations:**
    * Display the links in a clear, tabular format.
    * Columns should include: `id`, `original_url`, `short_code`, and `created_at`.
    * Include controls for editing and deleting each link in its row (for Stories 4.4 and 4.6).
* **Acceptance Criteria:**
    * **Given** I am on the admin "Manage Links" page.
    * **When** the page loads.
    * **Then** a table is displayed containing all the link records from the database.
* **Architecture Design Notes:**
    * The page component will make a `GET` request to `/api/v1/links` when it mounts.
    * The returned array of link objects will be stored in the component's state and rendered in a table.
* **Dependencies:** Story 4.1 (Backend: API for Listing All Links).

### **4.3: API for Updating a Link**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to accept a `PUT` request with an `original_url`, so that I can update the destination for a specific link `id`.
* **Acceptance Criteria:**
    * **Given** a link record exists for a given `id`.
    * **When** the service receives a `PUT` request to `/api/v1/links/{id}` with a JSON body containing a new `original_url`.
    * **Then** the `original_url` for that record in the `links` table should be updated.
    * **And** the service should respond with a `200 OK` status and a JSON body of the updated link object.
* **Architecture Design Notes:**
    * Implement the `PUT /api/v1/links/{id}` endpoint.
    * The logic should find the link by its `id` and execute an `UPDATE` statement.
    * Return the full, updated object after the update is complete.

### **4.4: Update a Link's Destination URL**

* **Story Type:** Frontend
* **Story:** As an admin, I want to be able to change the `original_url` that a `short_code` points to, so that I can correct errors or update outdated links.
* **Design / UX Considerations:**
    * In the link list table (from Story 4.2), each row should have an "Edit" button.
    * Clicking "Edit" could either open a modal or turn the `original_url` cell into an editable input field with "Save" and "Cancel" buttons.
* **Acceptance Criteria:**
    * **Given** I am viewing the list of all links.
    * **When** I click "Edit" on a specific link, change its `original_url`, and click "Save".
    * **Then** a `PUT` request is sent to `/api/v1/links/{id}` with the new URL.
    * **And** the table display updates to show the new `original_url`.
* **Architecture Design Notes:**
    * The "Save" action triggers a `PUT` request to `/api/v1/links/{id}`, where `{id}` is the ID of the link being edited.
    * The request body will be `{ "original_url": "https://new-url.com" }`.
    * Upon a successful response, the frontend should either refetch the entire list or update the local state for that specific item.
* **Dependencies:** Story 4.3 (Backend: API for Updating a Link).

### **4.5: API for Deleting a Link**

* **Story Type:** Backend API
* **Story:** As the backend service, I want to accept a `DELETE` request for a specific link `id`, so that I can remove it from the database.
* **Acceptance Criteria:**
    * **Given** a link record exists for a given `id`.
    * **When** the service receives a `DELETE` request to `/api/v1/links/{id}`.
    * **Then** the corresponding record should be deleted from the `links` table.
    * **And** the service should respond with a `200 OK` status and a success message.
* **Architecture Design Notes:**
    * Implement the `DELETE /api/v1/links/{id}` endpoint.
    * The logic should find the link by its `id` and execute a `DELETE` statement.
    * Note: Consider the database's foreign key constraint. Deleting a link might require a `CASCADE` delete on related `visits` records, or it might fail if visits exist, depending on the chosen strategy. The schema should define `ON DELETE CASCADE` for the `visits.link_id` foreign key.

### **4.6: Delete a Link**

* **Story Type:** Frontend
* **Story:** As an admin, I want to be able to permanently delete a short link, so that it can no longer be used.
* **Design / UX Considerations:**
    * Each row in the link list table should have a "Delete" button.
    * Clicking "Delete" must trigger a confirmation dialog (e.g., "Are you sure you want to delete this link?") to prevent accidental deletion.
* **Acceptance Criteria:**
    * **Given** I am viewing the list of all links.
    * **When** I click the "Delete" button for a specific link and confirm the action.
    * **Then** a `DELETE` request is sent to `/api/v1/links/{id}`.
    * **And** the link's row is removed from the table on the UI.
* **Architecture Design Notes:**
    * The "Confirm" action in the dialog triggers a `DELETE` request to `/api/v1/links/{id}`.
    * Upon successful deletion, the frontend state should be updated to remove the item from the list, causing the UI to re-render.
* **Dependencies:** Story 4.5 (Backend: API for Deleting a Link).