## Users App Endpoints

### 1. CustomUser Endpoints:

#### - **List Users**
  * **URL:** `/users/`
  * **Method:** `GET`
  * **Description:** Retrieves a list of all custom users.
  * **Response:**
    ```json
    [
      {
        "id": "uuid",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "user_type": "customer|vendor|admin",
        "unique_id": "uuid",
        "phone": "string",
        "country": {
          "id": "integer",
          "name": "string",
          "currency": "string",
          "default_timezone": "string"
        },
         "state": {
          "id": "integer",
          "name": "string",
          "country": "integer",
          "timezone": "integer"
        },
         "city": {
          "id": "integer",
          "state": "integer",
          "name": "string"
        },
        "profile_image": "string (URL or null)",
        "preferred_currency": "string (nullable)",
        "preferred_timezone": {
          "id": "integer",
          "name": "string"
        },
        "age": "integer (nullable)",
        "gender": "M|F|O (nullable)",
        "income_level": "Low|Medium|High (nullable)",
        "housing_status": "Owns House|Owns Apartment|Rents|Other (nullable)",
         "postal_code": "string (nullable)",
        "geolocation": "JSON (nullable)",
        "last_page_visited": "string (URL, nullable)",
        "visit_count": "integer",
        "last_visit": "datetime (nullable)",
        "search_history": "JSON (nullable)",
        "purchase_history": "JSON (nullable)",
        "last_purchase_date": "datetime (nullable)",
        "purchase_count": "integer",
        "total_spent": "decimal",
         "segment": "string (nullable)",
          "lifestyle": "Active|Sedentary|Balanced (nullable)",
        "interests": "JSON (nullable)",
        "marketing_preferences": "JSON (nullable)",
        "behavior_tags": "JSON (nullable)",
        "date_joined": "datetime"
      },
     ...
    ]
    ```

#### - **Get User Detail**
  * **URL:** `/users/<uuid:pk>/`
  * **Method:** `GET`
  * **Description:** Retrieves a single custom user based on its unique ID
  * **Parameters:** `pk`: The unique ID of the user you want to fetch.
  * **Response:**
      ```json
      {
        "id": "uuid",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "user_type": "customer|vendor|admin",
        "unique_id": "uuid",
        "phone": "string",
        "country": {
          "id": "integer",
          "name": "string",
          "currency": "string",
          "default_timezone": "string"
        },
         "state": {
          "id": "integer",
          "name": "string",
          "country": "integer",
          "timezone": "integer"
        },
         "city": {
          "id": "integer",
          "state": "integer",
          "name": "string"
        },
        "profile_image": "string (URL or null)",
        "preferred_currency": "string (nullable)",
        "preferred_timezone": {
          "id": "integer",
          "name": "string"
        },
        "age": "integer (nullable)",
        "gender": "M|F|O (nullable)",
        "income_level": "Low|Medium|High (nullable)",
        "housing_status": "Owns House|Owns Apartment|Rents|Other (nullable)",
         "postal_code": "string (nullable)",
        "geolocation": "JSON (nullable)",
        "last_page_visited": "string (URL, nullable)",
        "visit_count": "integer",
        "last_visit": "datetime (nullable)",
        "search_history": "JSON (nullable)",
        "purchase_history": "JSON (nullable)",
        "last_purchase_date": "datetime (nullable)",
        "purchase_count": "integer",
        "total_spent": "decimal",
         "segment": "string (nullable)",
          "lifestyle": "Active|Sedentary|Balanced (nullable)",
        "interests": "JSON (nullable)",
        "marketing_preferences": "JSON (nullable)",
        "behavior_tags": "JSON (nullable)",
        "date_joined": "datetime"
        }
      ```
  
#### - **Create User**
  *   **URL:** `/users/create/`
  *   **Method:** `POST`
  *   **Description:** Creates a new user.
  *   **Request Body:**
       ```json
            {
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "user_type": "customer|vendor|admin",
                "password": "string",
                "phone": "string (optional)",
                "country": "integer (optional)",
                "state": "integer (optional)",
                "city": "integer (optional)",
                 "profile_image": "string (URL or null)",
                "preferred_currency": "string (optional)",
               "preferred_timezone": "integer (optional)",
                "age": "integer (optional)",
                "gender": "M|F|O (optional)",
                "income_level": "Low|Medium|High (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                 "postal_code": "string (optional)",
                 "geolocation": "JSON (optional)",
                 "last_page_visited": "string (URL, optional)",
                  "visit_count": "integer (optional)",
                  "last_visit": "datetime (optional)",
                  "search_history": "JSON (optional)",
                  "purchase_history": "JSON (optional)",
                 "last_purchase_date": "datetime (optional)",
                  "purchase_count": "integer (optional)",
                  "total_spent": "decimal (optional)",
                  "segment": "string (optional)",
                   "lifestyle": "Active|Sedentary|Balanced (optional)",
                 "interests": "JSON (optional)",
                 "marketing_preferences": "JSON (optional)",
                 "behavior_tags": "JSON (optional)"
            }
        ```
  * **Response:**
        *   Returns a 201 status code on successful creation of the user, together with the created user object.

#### - **Update User**
  *  **URL:** `/users/<uuid:pk>/update/`
    *   **Method:** `PUT`
    *  **Description:** Updates an existing user.
    *  **Parameters:** `pk`: The unique id of the user you want to update.
     *  **Request Body:**
            ```json
            {
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                 "user_type": "customer|vendor|admin",
                "phone": "string (optional)",
                "country": "integer (optional)",
                "state": "integer (optional)",
                 "city": "integer (optional)",
                 "profile_image": "string (URL or null)",
                "preferred_currency": "string (optional)",
                "preferred_timezone": "integer (optional)",
                "age": "integer (optional)",
                "gender": "M|F|O (optional)",
                 "income_level": "Low|Medium|High (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                  "postal_code": "string (optional)",
                 "geolocation": "JSON (optional)",
                "last_page_visited": "string (URL, optional)",
                  "visit_count": "integer (optional)",
                  "last_visit": "datetime (optional)",
                  "search_history": "JSON (optional)",
                 "purchase_history": "JSON (optional)",
                 "last_purchase_date": "datetime (optional)",
                  "purchase_count": "integer (optional)",
                   "total_spent": "decimal (optional)",
                 "segment": "string (optional)",
                   "lifestyle": "Active|Sedentary|Balanced (optional)",
                  "interests": "JSON (optional)",
                   "marketing_preferences": "JSON (optional)",
                 "behavior_tags": "JSON (optional)"
             }
            ```
     *   **Response:**
         *   Returns a 200 status code on successful update, together with the updated user object.

#### - **Delete User**
   *   **URL:** `/users/<uuid:pk>/delete/`
   *  **Method:** `DELETE`
   *  **Description:** Deletes an existing user.
    *  **Parameters:**
        *   `pk`: The unique id of the user you want to delete.
   *  **Response:**
        *   Returns a 204 status code on successful deletion.

### 2. Vendor Endpoints:

#### - **List Vendors**
  * **URL:** `/vendors/`
  * **Method:** `GET`
  * **Description:** Retrieves a list of all vendors.
  * **Response:**
    ```json
       [
            {
                "id": "uuid",
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "user_type": "customer|vendor|admin",
                "company_name": "string",
                "tax_id": "string (optional)",
                "slug": "string",
                "vendor_unique_id": "uuid",
                "contact_person_name": "string (optional)",
                "phone_number": "string (optional)",
                "business_email": "email (optional)",
                "website": "string (URL, optional)",
                "address_line1": "string (optional)",
                "address_line2": "string (optional)",
                "direction": "text (optional)",
                "menu": "string (URL, optional)",
                "cuisine_type": "string (optional)",
                "cuisines": "text (optional)",
                 "opening_hours": "text (optional)",
                "description": "text (optional)",
                "about": "text (optional)",
                "facilities": "text (optional)",
                "atmosphere": "string (optional)",
                "spoken_languages": "string (optional)",
                "payment_options": "string (optional)",
                "special_conditions": "text (optional)",
                "average_rating": "decimal (optional)",
                "review_count": "integer",
                 "created_at": "datetime",
                  "updated_at": "datetime",
                 "is_vendor_superuser": "boolean",
                 "country": {
                     "id": "integer",
                      "name": "string",
                     "currency": "string",
                    "default_timezone": "string"
                 },
                 "state": {
                      "id": "integer",
                      "name": "string",
                     "country": "integer",
                     "timezone": "integer"
                  },
                   "city": {
                         "id": "integer",
                        "state": "integer",
                       "name": "string"
                   },
                "preferred_timezone": {
                      "id": "integer",
                      "name": "string"
                },
               "profile_image": "string (URL or null)",
                "is_active": "boolean",
                 "phone": "string (optional)",
                  "date_joined": "datetime",
                 "income_level": "Low|Medium|High (optional)",
                 "gender": "M|F|O (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                "postal_code": "string (optional)",
              }
            ,
           ...
       ]
    ```

#### - **Get Vendor Detail**
  *  **URL:** `/vendors/<uuid:pk>/`
  *  **Method:** `GET`
  *  **Description:** Retrieves a single vendor based on its unique ID
  *  **Parameters:** `pk`: The unique id of the vendor you want to fetch.
  *  **Response:**
        ```json
              {
                "id": "uuid",
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "user_type": "customer|vendor|admin",
                "company_name": "string",
                "tax_id": "string (optional)",
                "slug": "string",
                "vendor_unique_id": "uuid",
                "contact_person_name": "string (optional)",
                "phone_number": "string (optional)",
                "business_email": "email (optional)",
                "website": "string (URL, optional)",
                "address_line1": "string (optional)",
                "address_line2": "string (optional)",
                "direction": "text (optional)",
                "menu": "string (URL, optional)",
                "cuisine_type": "string (optional)",
                "cuisines": "text (optional)",
                 "opening_hours": "text (optional)",
                "description": "text (optional)",
                "about": "text (optional)",
                "facilities": "text (optional)",
                "atmosphere": "string (optional)",
                "spoken_languages": "string (optional)",
                "payment_options": "string (optional)",
                "special_conditions": "text (optional)",
                "average_rating": "decimal (optional)",
                "review_count": "integer",
                 "created_at": "datetime",
                  "updated_at": "datetime",
                 "is_vendor_superuser": "boolean",
                 "country": {
                     "id": "integer",
                      "name": "string",
                     "currency": "string",
                    "default_timezone": "string"
                 },
                 "state": {
                      "id": "integer",
                      "name": "string",
                     "country": "integer",
                     "timezone": "integer"
                  },
                   "city": {
                         "id": "integer",
                        "state": "integer",
                       "name": "string"
                   },
                 "preferred_timezone": {
                      "id": "integer",
                      "name": "string"
                },
                "profile_image": "string (URL or null)",
                "is_active": "boolean",
                 "phone": "string (optional)",
                  "date_joined": "datetime",
                 "income_level": "Low|Medium|High (optional)",
                 "gender": "M|F|O (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                 "postal_code": "string (optional)",
            }
        ```
  
#### - **Create Vendor**
  *   **URL:** `/vendors/create/`
  *  **Method:** `POST`
   *  **Description:** Creates a new vendor.
   *   **Request Body:**
            ```json
           {
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                "password": "string",
                "user_type": "customer|vendor|admin",
                 "company_name": "string",
                "tax_id": "string (optional)",
                "contact_person_name": "string (optional)",
                 "phone_number": "string (optional)",
                "business_email": "email (optional)",
                "website": "string (URL, optional)",
                "address_line1": "string (optional)",
                "address_line2": "string (optional)",
                 "direction": "text (optional)",
                "menu": "string (URL, optional)",
                 "cuisine_type": "string (optional)",
                 "cuisines": "text (optional)",
                "opening_hours": "text (optional)",
                "description": "text (optional)",
                 "about": "text (optional)",
                  "facilities": "text (optional)",
                "atmosphere": "string (optional)",
                "spoken_languages": "string (optional)",
                 "payment_options": "string (optional)",
                "special_conditions": "text (optional)",
                 "average_rating": "decimal (optional)",
                 "review_count": "integer (optional)",
                 "is_vendor_superuser": "boolean (optional)",
                 "country": "integer (optional)",
                "state": "integer (optional)",
                "city": "integer (optional)",
                "preferred_timezone": "integer (optional)",
                 "profile_image": "string (URL or null)",
                "is_active": "boolean (optional)",
                "phone": "string (optional)",
                 "income_level": "Low|Medium|High (optional)",
                 "gender": "M|F|O (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                 "postal_code": "string (optional)",
                 
            }
            ```
    *  **Response:**
       *   Returns a 201 status code on successful creation of the vendor, together with the vendor object.
  
#### - **Update Vendor**
  *  **URL:** `/vendors/<uuid:pk>/update/`
   *  **Method:** `PUT`
    *  **Description:** Updates an existing vendor
    * **Parameters:** `pk`: The unique id of the vendor you want to update.
     * **Request Body:**
        ```json
           {
                "username": "string",
                "email": "string",
                "first_name": "string",
                "last_name": "string",
                 "user_type": "customer|vendor|admin",
                 "company_name": "string",
                "tax_id": "string (optional)",
                "contact_person_name": "string (optional)",
                 "phone_number": "string (optional)",
                "business_email": "email (optional)",
                "website": "string (URL, optional)",
                "address_line1": "string (optional)",
                "address_line2": "string (optional)",
                 "direction": "text (optional)",
                "menu": "string (URL, optional)",
                 "cuisine_type": "string (optional)",
                 "cuisines": "text (optional)",
                "opening_hours": "text (optional)",
                "description": "text (optional)",
                 "about": "text (optional)",
                  "facilities": "text (optional)",
                "atmosphere": "string (optional)",
                "spoken_languages": "string (optional)",
                 "payment_options": "string (optional)",
                "special_conditions": "text (optional)",
                 "average_rating": "decimal (optional)",
                 "review_count": "integer (optional)",
                  "is_vendor_superuser": "boolean (optional)",
                  "country": "integer (optional)",
                 "state": "integer (optional)",
                 "city": "integer (optional)",
                 "preferred_timezone": "integer (optional)",
                  "profile_image": "string (URL or null)",
                "is_active": "boolean (optional)",
               "phone": "string (optional)",
                 "income_level": "Low|Medium|High (optional)",
                 "gender": "M|F|O (optional)",
                "housing_status": "Owns House|Owns Apartment|Rents|Other (optional)",
                 "postal_code": "string (optional)",
            }
            ```
     *   **Response:**
         *   Returns a 200 status code on successful update, together with the updated vendor object.

#### - **Delete Vendor**
   *   **URL:** `/vendors/<uuid:pk>/delete/`
   *   **Method:** `DELETE`
    *   **Description:** Deletes an existing vendor
    *  **Parameters:**
        *   `pk`: The unique id of the vendor you want to delete.
    *  **Response:**
        *   Returns a 204 status code on successful deletion.

### 3. Other Endpoints

#### 3.1 Country Endpoints:

##### List all countries
 * **URL:** `/countries/`
   * **Method:** `GET`
   * **Description:** Retrieves a list of all countries
   * **Response:**
    ```json
      [
            {
             "id": "integer",
              "name": "string",
             "currency": "string",
            "default_timezone": "string"
             }
            ,...
       ]
    ```

##### Get a single country
 * **URL:** `/countries/<int:pk>/`
   * **Method:** `GET`
   * **Description:** Get a single country using the primary key.
   * **Parameters:** `pk` - primary key of the country
   * **Response:**
        ```json
            {
               "id": "integer",
              "name": "string",
             "currency": "string",
             "default_timezone": "string"
             }
         ```
##### Post a country
 * **URL:** `/countries/create/`
   * **Method:** `POST`
   * **Description:** Create a country using post request.
   * **Request Body:**
    ```json
      {
          "name": "string",
          "currency": "string",
         "default_timezone": "string"
         }
     ```
   * **Response:**
        *   Returns a 201 status code on successful creation of the country, together with the created country object.

##### Put a country
 * **URL:** `/countries/<int:pk>/update/`
    * **Method:** `PUT`
   *  **Description:** Updates a single country using a put request.
     *  **Parameters:** `pk`: The primary key of the country to be updated.
    * **Request Body:**
        ```json
         {
          "name": "string",
          "currency": "string",
         "default_timezone": "string"
         }
        ```
   * **Response:**
       *   Returns a 200 status code on successful update, together with the updated country object.

##### Delete a country
 * **URL:** `/countries/<int:pk>/delete/`
    * **Method:** `DELETE`
   *  **Description:** Deletes a country using a primary key.
     *  **Parameters:** `pk` The primary key of the country to be deleted
    * **Response:**
       *   Returns a 204 status code on successful deletion.

#### 3.2 State Endpoints:

##### List all states
 * **URL:** `/states/`
   * **Method:** `GET`
   * **Description:** Retrieves a list of all states
   * **Response:**
      ```json
      [
           {
             "id": "integer",
             "name": "string",
             "country": "integer",
             "timezone": "integer"
            },
           ...
       ]
       ```

##### Get a single state
 * **URL:** `/states/<int:pk>/`
   * **Method:** `GET`
   * **Description:** Get a single state using the primary key.
   * **Parameters:** `pk` - primary key of the state
   * **Response:**
        ```json
        {
             "id": "integer",
              "name": "string",
             "country": "integer",
             "timezone": "integer"
            }
         ```
##### Post a state
 * **URL:** `/states/create/`
   * **Method:** `POST`
   * **Description:** Create a state using post request.
   * **Request Body:**
    ```json
        {
            "name": "string",
           "country": "integer",
           "timezone": "integer"
            }
        ```
    *   **Response:**
       *   Returns a 201 status code on successful creation of the state, together with the created state object.

##### Put a state
 * **URL:** `/states/<int:pk>/update/`
    * **Method:** `PUT`
     *  **Description:** Updates a single state using a put request.
      *  **Parameters:** `pk`: The primary key of the state to be updated.
     *  **Request Body:**
         ```json
         {
            "name": "string",
           "country": "integer",
           "timezone": "integer"
          }
         ```
    *   **Response:**
        *   Returns a 200 status code on successful update, together with the updated state object.

##### Delete a state
 * **URL:** `/states/<int:pk>/delete/`
    * **Method:** `DELETE`
    *  **Description:** Deletes a state using a primary key.
     *  **Parameters:** `pk` The primary key of the state to be deleted
    *  **Response:**
        *   Returns a 204 status code on successful deletion.
#### 3.3 City Endpoints:

##### List all cities
 * **URL:** `/cities/`
   * **Method:** `GET`
   * **Description:** Retrieves a list of all cities
   * **Response:**
    ```json
       [
            {
               "id": "integer",
                "state": "integer",
                "name": "string"
             },
             ...
        ]
       ```

##### Get a single city
 * **URL:** `/cities/<int:pk>/`
   * **Method:** `GET`
    * **Description:** Get a single city using the primary key.
   *  **Parameters:** `pk` - primary key of the city
    * **Response:**
        ```json
            {
             "id": "integer",
                "state": "integer",
                "name": "string"
             }
         ```
##### Post a city
 * **URL:** `/cities/create/`
   *  **Method:** `POST`
   *  **Description:** Create a city using post request.
    *  **Request Body:**
        ```json
        {
            "state": "integer",
            "name": "string"
         }
        ```
   *  **Response:**
        *  Returns a 201 status code on successful creation of the city, together with the created city object.

##### Put a city
 * **URL:** `/cities/<int:pk>/update/`
    *  **Method:** `PUT`
    *  **Description:** Updates a single city using a put request.
     * **Parameters:** `pk`: The primary key of the city to be updated.
    *  **Request Body:**
         ```json
        {
            "state": "integer",
            "name": "string"
         }
        ```
    *   **Response:**
         *   Returns a 200 status code on successful update, together with the updated city object.

##### Delete a city
 * **URL:** `/cities/<int:pk>/delete/`
    *   **Method:** `DELETE`
   *  **Description:** Deletes a city using a primary key.
     * **Parameters:** `pk`: The primary key of the city to be deleted
    *  **Response:**
       *   Returns a 204 status code on successful deletion.
       
#### 3.4 Timezones Endpoints:

##### List all timezones
 * **URL:** `/timezones/`
   * **Method:** `GET`
    * **Description:** Retrieves a list of all timezones.
   * **Response:**
    ```json
    [
        {
            "id": "integer",
             "name": "string",
        }
         ,...
      ]
    ```

##### Get a single timezone
 * **URL:** `/timezones/<int:pk>/`
   * **Method:** `GET`
    * **Description:** Get a single timezone using the primary key.
     *  **Parameters:** `pk` - primary key of the timezone.
     *  **Response:**
        ```json
        {
            "id": "integer",
              "name": "string"
            }
         ```

##### Post a timezone
 * **URL:** `/timezones/create/`
   * **Method:** `POST`
  *  **Description:** Create a timezone using post request.
    *   **Request Body:**
        ```json
            {
              "name": "string"
             }
         ```
    *  **Response:**
        *  Returns a 201 status code on successful creation of the timezone, together with the created timezone object.

##### Put a timezone
 * **URL:** `/timezones/<int:pk>/update/`
    *  **Method:** `PUT`
    * **Description:** Updates a single timezone using a put request.
    *  **Parameters:** `pk`: The primary key of the timezone to be updated.
    *   **Request Body:**
          ```json
        {
              "name": "string"
         }
         ```
    * **Response:**
        *  Returns a 200 status code on successful update, together with the updated timezone object.

##### Delete a timezone
 * **URL:** `/timezones/<int:pk>/delete/`
    *  **Method:** `DELETE`
    * **Description:** Deletes a timezone using a primary key.
     * **Parameters:** `pk` The primary key of the timezone to be deleted
    *  **Response:**
        * Returns a 204 status code on successful deletion.