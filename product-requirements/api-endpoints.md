## API Endpoints

All endpoints should follow RESTful conventions. Below is a complete list of endpoints for the `links` and `visits` resources.

-----

### Links Endpoints

These endpoints manage the core functionality of creating, retrieving, updating, and deleting shortened links.

#### **Endpoint:** `/api/v1/links`

  * **POST request:**
    Creates a new link object. The request body must contain the `original_url`. The `short_code` can be provided, but if omitted, the service should generate a unique one. This endpoint returns the newly created link object from the database.

      * **Example Request Body:**
        ```json
        {
          "original_url": "https://www.verylonganddetailedurlthatneedstobeshortened.com/articles/2025/some-interesting-topic"
        }
        ```

  * **GET request:**
    Returns a list of all link objects stored in the database.


#### **Endpoint:** `/api/v1/links/{id}`

  * **GET request:**
    Returns the link object for the given `id`.

  * **PUT request:**
    Updates the link object for the given `id`. This is typically used to change the `original_url` a `short_code` points to. It returns the updated object.

      * **Example Request Body:**
        ```json
        {
          "original_url": "https://www.newdestinationurl.com/updated-page"
        }
        ```

  * **DELETE request:**
    Deletes the link object for the given `id` and returns a success message with a status code of 200.

-----

### Visits Endpoints

These endpoints are for logging and retrieving visit data. As `visits` represent a historical log, they are immutable by design; therefore, `PUT` and `DELETE` operations are not permitted.

#### **Endpoint:** `/api/v1/visits`

  * **POST request:**
    Creates a new visit log entry. This endpoint would be called internally every time a shortened link is successfully resolved and visited. It returns the newly created visit object.

      * **Example Request Body:**
        ```json
        {
          "link_id": 123
        }
        ```

  * **GET request:**
    Returns a list of all visit objects. For performance reasons in a production environment, this should be paginated.


#### **Endpoint:** `/api/v1/visits/{id}`

  * **GET request:**
    Returns the specific visit object for the given `id`.