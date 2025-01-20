## Shared App Endpoints

### 1. Product Endpoints:

#### - **List Products**
  * **URL:** `/products/`
  * **Method:** `GET`
  * **Description:** Retrieves a list of all products.
  *  **Response:**
     ```json
        [
            {
                "id": "integer",
                "name": "string",
                "description": "text (optional)",
                "price": "decimal",
                "is_available": "boolean",
                "category": "string (optional)",
               "created_at": "datetime",
                "updated_at": "datetime",
            },
           ...
       ]
     ```
#### - **Get Product Detail**
 *  **URL:** `/products/<int:pk>/`
  * **Method:** `GET`
  * **Description:** Retrieves a single product based on its primary key.
  * **Parameters:** `pk`: The primary key of the product you want to fetch.
  *  **Response:**
        ```json
            {
                "id": "integer",
                "name": "string",
                "description": "text (optional)",
                "price": "decimal",
                "is_available": "boolean",
                "category": "string (optional)",
               "created_at": "datetime",
                "updated_at": "datetime",
            }
        ```
#### - **Create Product**
  *  **URL:** `/products/create/`
    * **Method:** `POST`
    *  **Description:** Creates a new product.
     *  **Request Body:**
         ```json
            {
                "name": "string",
                 "description": "text (optional)",
                "price": "decimal",
                "is_available": "boolean (optional)",
                "category": "string (optional)",
            }
        ```
   * **Response:**
         *   Returns a 201 status code on successful creation of the product, together with the product object.

#### - **Update Product**
 *  **URL:** `/products/<int:pk>/update/`
   *   **Method:** `PUT`
    *  **Description:** Updates an existing product
   *  **Parameters:** `pk`: The primary key of the product you want to update.
     *  **Request Body:**
        ```json
            {
                "name": "string",
                 "description": "text (optional)",
                "price": "decimal",
                "is_available": "boolean (optional)",
                "category": "string (optional)",
            }
        ```
    *  **Response:**
       *   Returns a 200 status code on successful update, together with the updated product object.

#### - **Delete Product**
  *  **URL:** `/products/<int:pk>/delete/`
  *  **Method:** `DELETE`
   * **Description:** Deletes an existing product
     *  **Parameters:** `pk`: The primary key of the product you want to delete.
    *  **Response:**
       *   Returns a 204 status code on successful deletion.

### 2. Table Endpoints:

#### - **List Tables**
  *  **URL:** `/tables/`
  * **Method:** `GET`
  * **Description:** Retrieves a list of all tables.
  *  **Response:**
    ```json
      [
            {
                "id": "integer",
                 "number": "integer",
                "capacity": "integer",
                "vendor": "integer",
                "status": "FREE|OCCUPIED",
            }
           ,
           ...
        ]
    ```

#### - **Get Table Detail**
  * **URL:** `/tables/<int:pk>/`
  *  **Method:** `GET`
    * **Description:** Retrieves a single table using a primary key.
    * **Parameters:** `pk`: The primary key of the table to fetch.
    *  **Response:**
          ```json
            {
                 "id": "integer",
                 "number": "integer",
                "capacity": "integer",
                "vendor": "integer",
                "status": "FREE|OCCUPIED",
            }
        ```
#### - **Create Table**
  *  **URL:** `/tables/create/`
  * **Method:** `POST`
   *   **Description:** Creates a new table
    *   **Request Body:**
        ```json
            {
                "number": "integer",
                 "capacity": "integer",
                 "vendor": "integer",
                 "status": "FREE|OCCUPIED"
            }
        ```
   *   **Response:**
      *   Returns a 201 status code on successful creation of the table, together with the table object.

#### - **Update Table**
  *  **URL:** `/tables/<int:pk>/update/`
  * **Method:** `PUT`
    *  **Description:** Updates an existing table using the given primary key.
     *  **Parameters:** `pk`: The primary key of the table you want to update.
     *  **Request Body:**
         ```json
            {
                "number": "integer",
                 "capacity": "integer",
                "vendor": "integer",
                "status": "FREE|OCCUPIED"
            }
        ```
   *  **Response:**
       *  Returns a 200 status code on successful update, together with the updated table object.

#### - **Delete Table**
  *  **URL:** `/tables/<int:pk>/delete/`
  * **Method:** `DELETE`
  * **Description:** Deletes a table, using the given primary key.
   * **Parameters:** `pk`: The primary key of the table to be deleted.
    * **Response:**
        *  Returns a 204 status code on successful deletion.

### 3. Menu Endpoints:

#### - **List Menus**
  *  **URL:** `/menus/`
  *  **Method:** `GET`
  *  **Description:** Retrieves a list of all menus.
  *  **Response:**
    ```json
         [
            {
              "vendor": "integer",
              "name": "string",
               "slug": "string",
                 "description": "text (optional)"
            }
              ,
              ...
         ]
    ```

#### - **Get Menu Detail**
  *  **URL:** `/menus/<int:pk>/`
  *  **Method:** `GET`
   *  **Description:** Retrieves a single menu using the primary key.
    *  **Parameters:** `pk`: The primary key of the menu to fetch.
   *  **Response:**
      ```json
           {
               "vendor": "integer",
               "name": "string",
               "slug": "string",
                "description": "text (optional)"
            }
        ```
#### - **Create Menu**
  *  **URL:** `/menus/create/`
   * **Method:** `POST`
    * **Description:** Creates a new menu
     *  **Request Body:**
        ```json
            {
               "vendor": "integer",
                "name": "string",
                "description": "text (optional)"
            }
        ```
   * **Response:**
     *  Returns a 201 status code on successful creation of the menu, together with the menu object.

#### - **Update Menu**
  *  **URL:** `/menus/<int:pk>/update/`
   *  **Method:** `PUT`
    *  **Description:** Updates an existing menu.
    * **Parameters:** `pk`: The primary key of the menu to update.
     *   **Request Body:**
         ```json
            {
               "vendor": "integer",
                "name": "string",
                "description": "text (optional)"
            }
        ```
   * **Response:**
        *  Returns a 200 status code on successful update, together with the updated menu object.

#### - **Delete Menu**
  *  **URL:** `/menus/<int:pk>/delete/`
  * **Method:** `DELETE`
   *  **Description:** Deletes an existing menu
   * **Parameters:** `pk`: The primary key of the menu you want to delete.
   * **Response:**
        * Returns a 204 status code on successful deletion.
### 4. MenuItem Endpoints:

#### - **List Menu Items**
  * **URL:** `/menuitems/`
  * **Method:** `GET`
    * **Description:** Retrieves a list of all menu items.
  *  **Response:**
        ```json
           [
              {
                "id": "integer",
                "menu": "integer",
                 "name": "string",
                "slug": "string",
                "description": "text (optional)",
                "price": "decimal",
                 "category": "string (optional)",
                "image": "string (URL or null)",
                "is_available": "boolean",
                "stock_quantity": "integer (optional)",
                "meta_description": "text (optional)",
                "meta_keywords": "string (optional)",
                 "add_ons":"[integer] (optional)"
               }
               ,
               ...
            ]
         ```

#### - **Get MenuItem Detail**
  *  **URL:** `/menuitems/<int:pk>/`
   * **Method:** `GET`
   *  **Description:** Retrieves a single menu item by its primary key.
   * **Parameters:** `pk`: The primary key of the menu item to fetch.
    * **Response:**
        ```json
          {
              "id": "integer",
                "menu": "integer",
                "name": "string",
                "slug": "string",
                "description": "text (optional)",
                "price": "decimal",
                "category": "string (optional)",
                "image": "string (URL or null)",
                "is_available": "boolean",
                "stock_quantity": "integer (optional)",
                "meta_description": "text (optional)",
                "meta_keywords": "string (optional)",
                 "add_ons":"[integer] (optional)"
            }
         ```
#### - **Create MenuItem**
  *  **URL:** `/menuitems/create/`
   *  **Method:** `POST`
   *  **Description:** Creates a new menu item
   * **Request Body:**
        ```json
           {
                "menu": "integer",
                "name": "string",
                "description": "text (optional)",
                 "price": "decimal",
                "category": "string (optional)",
                 "image": "string (URL or null)",
                "is_available": "boolean (optional)",
                "stock_quantity": "integer (optional)",
                "meta_description": "text (optional)",
                "meta_keywords": "string (optional)",
                "add_ons":"[integer] (optional)"
            }
        ```
    *  **Response:**
        * Returns a 201 status code on successful creation of the menu item, together with the created menu item object.

#### - **Update MenuItem**
   *  **URL:** `/menuitems/<int:pk>/update/`
    *   **Method:** `PUT`
    *   **Description:** Updates an existing menu item.
      *  **Parameters:** `pk`: The primary key of the menu item to update.
     * **Request Body:**
        ```json
            {
                "menu": "integer",
                "name": "string",
                "description": "text (optional)",
                "price": "decimal",
                "category": "string (optional)",
                "image": "string (URL or null)",
                 "is_available": "boolean (optional)",
                 "stock_quantity": "integer (optional)",
                 "meta_description": "text (optional)",
                "meta_keywords": "string (optional)",
                "add_ons":"[integer] (optional)"
            }
        ```
    *  **Response:**
         *  Returns a 200 status code on successful update, together with the updated menu item object.

#### - **Delete MenuItem**
   * **URL:** `/menuitems/<int:pk>/delete/`
   * **Method:** `DELETE`
   *   **Description:** Deletes a menu item based on the primary key.
    *  **Parameters:** `pk`: The primary key of the menu item to be deleted
    *  **Response:**
       *  Returns a 204 status code on successful deletion.
### 5. Cart Endpoints
  ####  List all Carts
  *  **URL:** `/carts/`
   * **Method:** `GET`
   *  **Description:** Get a list of all carts
   *  **Response:**
        ```json
        [
           {
              "id": "integer",
                "user": "integer",
                "created_at": "datetime",
                "updated_at":"datetime"
                }
             ,...
          ]
        ```
    
 #### Get Cart Detail
 *  **URL:** `/carts/<int:pk>/`
  *   **Method:** `GET`
  *   **Description:** Get a single cart using a primary key.
  * **Parameters:** `pk` - primary key of the cart
  *  **Response:**
      ```json
         {
              "id": "integer",
                "user": "integer",
                "created_at": "datetime",
                "updated_at":"datetime"
           }
      ```
  #### Create a cart
 *  **URL:** `/carts/create/`
   * **Method:** `POST`
   *   **Description:** Creates a cart using a POST request
     *  **Request Body:**
        ```json
         {
           "user": "integer"
         }
        ```
    *   **Response:**
       * Returns a 201 status code on successful creation of the cart, together with the created cart object.
     
 #### Create a cart item
 *  **URL:** `/carts/<int:cart_id>/cartitems/create/`
   *   **Method:** `POST`
    *  **Description:** Creates a cart item associated with the cart id.
     *  **Parameters:** `cart_id` - The primary key of the cart.
      *  **Request Body:**
         ```json
         {
                "product": "integer",
               "quantity":"integer"
            }
         ```
    *  **Response:**
        * Returns a 201 status code on successful creation of the cart item, together with the created cart object.
      
#### Delete cart item
  * **URL:** `/cartitems/<int:pk>/delete/`
  * **Method:** `DELETE`
   * **Description:** Deletes the cart item from a specific cart.
     * **Parameters:** `pk` - primary key of the cart item.
  *  **Response:**
         * Returns a 204 status code on successful deletion of the cart item.

### 6. Order Endpoints

#### List all orders
  *  **URL:** `/orders/`
   * **Method:** `GET`
   *   **Description:** Get a list of all the orders
   * **Response:**
        ```json
          [
             {
                "id":"integer",
                 "user": "integer",
                 "cart": "integer",
                "total_amount": "decimal",
                  "status": "PENDING|COMPLETED|CANCELLED",
                "created_at": "datetime"
            },
            ...
         ]
        ```

 #### Get Order Detail
 *  **URL:** `/orders/<int:pk>/`
  *  **Method:** `GET`
   * **Description:** Get the details of an order using its primary key.
   * **Parameters:** `pk` - primary key of the order you want to fetch.
   *  **Response:**
       ```json
           {
                "id":"integer",
                 "user": "integer",
                 "cart": "integer",
                "total_amount": "decimal",
                  "status": "PENDING|COMPLETED|CANCELLED",
                "created_at": "datetime"
            }
       ```
#### Create Order
  *  **URL:** `/carts/<int:cart_id>/orders/create/`
   *  **Method:** `POST`
   *  **Description:** Creates an order using a POST request associated with cart id.
    *  **Parameters:** `cart_id` - The primary key of the cart you want to use.
     *  **Request Body:**
            ```json
             {
                "status": "PENDING|COMPLETED|CANCELLED",
              }
            ```
    * **Response:**
      * Returns a 201 status code on successful creation of the order, together with the created order object.

#### Update Order
  *  **URL:** `/orders/<int:pk>/update/`
   *  **Method:** `PUT`
    *  **Description:** Updates an existing order using a primary key.
    *  **Parameters:** `pk` - The primary key of the order you want to update
    *  **Request Body:**
        ```json
             {
                "status": "PENDING|COMPLETED|CANCELLED",
              }
        ```
    * **Response:**
      * Returns a 200 status code on successful update of the order, together with the updated order object.

#### Delete Order
  *  **URL:** `/orders/<int:pk>/delete/`
    *  **Method:** `DELETE`
   * **Description:** Deletes a order using the primary key.
   *  **Parameters:** `pk` - The primary key of the order you want to delete.
    * **Response:**
        *  Returns a 204 status code on successful deletion.

#### Create an Order Item
 *  **URL:** `/orders/<int:order_id>/orderitems/create/`
   * **Method:** `POST`
    *   **Description:** Creates an order item related to an order id.
    *  **Parameters:** `order_id` - the primary key of the order.
    * **Request Body:**
        ```json
         {
            "menu_item": "integer",
             "quantity":"integer",
              "special_instructions": "string",
             "price":"decimal"
          }
        ```
   *   **Response:**
        *  Returns a 201 status code on successful creation of the order item, together with the created object.

#### Delete Order item
  *  **URL:** `/orderitems/<int:pk>/delete/`
   * **Method:** `DELETE`
  * **Description:** Deletes the order item using a primary key.
   *  **Parameters:** `pk` - primary key of the order item you want to delete.
   * **Response:**
       * Returns a 204 status code on successful deletion of the order item.
### 7. Tip Endpoints
  #### Create a tip
  * **URL:** `/orders/<int:order_id>/tips/create/`
    *   **Method:** `POST`
    *   **Description:** Creates a tip associated with a specific order.
    *  **Parameters:** `order_id` - primary key of the order
    *  **Request Body:**
        ```json
          {
            "amount":"decimal",
              "payment_method":"CASH|CARD"
           }
        ```
    *   **Response:**
        *  Returns a 201 status code on successful creation of the tip, together with the created object.
        
### 8. Discount Endpoints
    
  #### Create a Discount
  *  **URL:** `/orders/<int:order_id>/discounts/create/`
   *  **Method:** `POST`
    *   **Description:** Creates a discount associated with a specific order.
     * **Parameters:** `order_id` - primary key of the order.
    *  **Request Body:**
          ```json
          {
              "amount":"decimal",
               "reason":"string"
           }
         ```
    *   **Response:**
        *  Returns a 201 status code on successful creation of the discount, together with the created object.
         
### 9. Payment Endpoints
  #### Create a Payment
  *  **URL:** `/orders/<int:order_id>/payments/create/`
   *  **Method:** `POST`
   *   **Description:** Creates a payment associated with a specific order.
   *   **Parameters:** `order_id` - primary key of the order
    *  **Request Body:**
         ```json
         {
                "method":"CASH|CARD|ONLINE",
                 "amount":"decimal",
                 "transaction_id":"string(optional)"
            }
        ```
   *  **Response:**
      * Returns a 201 status code on successful creation of the payment, together with the payment object.

### 10. StaffReport Endpoints

    #### List all Staff Reports
      *  **URL:** `/staffreports/`
       * **Method:** `GET`
      * **Description:** Retrieves a list of all staff reports.
     * **Response:**
        ```json
        [
           {
               "waiter":"integer",
              "start_time":"datetime",
              "end_time":"datetime",
              "total_sales":"decimal",
               "total_tips":"decimal",
              "comments":"string"
           }
           ,...
        ]
        ```

     #### Get Staff Report Detail
     *  **URL:** `/staffreports/<int:pk>/`
    *  **Method:** `GET`
   *   **Description:** Retrieves a single staff report using its primary key.
     *   **Parameters:** `pk` - primary key of the staff report you want to fetch.
      * **Response:**
           ```json
            {
               "waiter":"integer",
              "start_time":"datetime",
              "end_time":"datetime",
              "total_sales":"decimal",
               "total_tips":"decimal",
              "comments":"string"
           }
        ```

     #### Create a staff report
      *  **URL:** `/staffreports/create/`
    *   **Method:** `POST`
   *   **Description:** Creates a staff report using a POST request.
    * **Request Body:**
          ```json
         {
              "start_time":"datetime",
             "end_time":"datetime",
            "comments":"string"
            }
         ```
      * **Response:**
          *  Returns a 201 status code on successful creation of the staff report, together with the created staff report object.

    #### Update a staff report
       *  **URL:** `/staffreports/<int:pk>/update/`
       * **Method:** `PUT`
       *  **Description:** Updates an existing staff report using a primary key.
      *  **Parameters:** `pk` - primary key of the staff report to be updated.
        *  **Request Body:**
          ```json
            {
             "start_time":"datetime",
              "end_time":"datetime",
             "comments":"string"
            }
         ```
       *  **Response:**
          *   Returns a 200 status code on successful update, together with the updated staff report object.

    #### Delete a staff report
     * **URL:** `/staffreports/<int:pk>/delete/`
     * **Method:** `DELETE`
      *  **Description:** Deletes the staff report using its primary key.
     *  **Parameters:** `pk` - primary key of the staff report to be deleted.
      * **Response:**
         * Returns a 204 status code on successful deletion of the staff report.

### 11. ServerSwap Endpoints
  #### Create a server swap
  * **URL:** `/serverswaps/create/`
   *  **Method:** `POST`
    *  **Description:** Creates a server swap using the data in the post body.
     * **Request Body:**
         ```json
        {
            "original_waiter":"integer",
            "new_waiter":"integer",
             "table":"integer(optional)",
            "order":"integer (optional)",
           "reason":"string"
          }
         ```
    *  **Response:**
         *   Returns a 201 status code on successful creation of the server swap, together with the created object.
      
#### List server swaps
*   **URL:** `/serverswaps/`
    *  **Method:** `GET`
    *   **Description:** Get the list of all the server swaps
   * **Response:**
        ```json
           [
             {
               "original_waiter":"integer",
                "new_waiter":"integer",
               "table":"integer(optional)",
               "order":"integer (optional)",
              "swap_time":"datetime",
               "reason":"string"
           },
           ...
        ]
        ```
        
#### Delete Server Swap
  *  **URL:** `/serverswaps/<int:pk>/delete/`
    *  **Method:** `DELETE`
  *  **Description:** Deletes an existing server swap object.
   * **Parameters:** `pk` - Primary key of the server swap to be deleted.
  * **Response:**
        *  Returns a 204 status code on successful deletion.
        
### 12. Promotion Endpoints
   #### Create a promotion
 * **URL:** `/promotions/create/`
    * **Method:** `POST`
   *   **Description:** Creates a new promotion.
    *  **Request Body:**
          ```json
        {
             "recipient":"integer",
             "message":"string",
              "expiry":"datetime(optional)"
            }
         ```
      * **Response:**
        * Returns a 201 status code on successful creation of the promotion, together with the created promotion object.

   #### List all promotions
   * **URL:** `/promotions/`
    * **Method:** `GET`
    *  **Description:** Retrieves a list of all promotions.
   *  **Response:**
       ```json
        [
         {
           "sender":"integer",
          "recipient":"integer",
           "message":"string",
           "created_at":"datetime",
           "is_active":"boolean",
            "expiry":"datetime"
          }
          ,
           ...
         ]
        ```
      
   #### Update a promotion
  *  **URL:** `/promotions/<int:pk>/update/`
    *  **Method:** `PUT`
   *  **Description:** Updates an existing promotion using a primary key.
     * **Parameters:** `pk` - primary key of the promotion to update
     *  **Request Body:**
       ```json
         {
             "recipient":"integer",
           "message":"string",
              "expiry":"datetime(optional)"
          }
         ```
   *   **Response:**
         *  Returns a 200 status code on successful update, together with the updated promotion object.
      
   #### Delete a promotion
  * **URL:** `/promotions/<int:pk>/delete/`
  *  **Method:** `DELETE`
  *   **Description:** Deletes the promotion using a primary key.
   *  **Parameters:** `pk` - Primary key of the promotion you want to delete.
   *   **Response:**
        *   Returns a 204 status code on successful deletion.

### 13. Incentive Endpoints

#### List all Incentives
*  **URL:** `/incentives/`
   * **Method:** `GET`
   *  **Description:** Retrieves a list of all incentives
   *   **Response:**
        ```json
          [
            {
               "waiter":"integer",
              "amount":"decimal",
              "reason":"string",
              "date_given":"date",
              "is_active":"boolean"
             }
             ,...
        ]
        ```
      
  ####  Create a incentive
   *  **URL:** `/incentives/create/`
    * **Method:** `POST`

## Shared App Endpoints (Continued)

### 13. Incentive Endpoints:

#### - **List Incentives**
  *   **URL:** `/incentives/`
  *  **Method:** `GET`
   * **Description:** Retrieves a list of all incentives.
  * **Response:**
       ```json
          [
            {
               "waiter":"integer",
              "amount":"decimal",
              "reason":"string",
              "date_given":"date",
              "is_active":"boolean"
             }
             ,...
        ]
        ```

#### - **Create Incentive**
  *   **URL:** `/incentives/create/`
  *   **Method:** `POST`
  *  **Description:** Creates a new incentive using a POST request.
    *  **Request Body:**
         ```json
          {
              "amount":"decimal",
              "reason":"string"
          }
         ```
  *   **Response:**
        *  Returns a 201 status code on successful creation of the incentive, together with the created object.

#### - **Update Incentive**
  *  **URL:** `/incentives/<int:pk>/update/`
   * **Method:** `PUT`
    * **Description:** Updates an existing incentive using a primary key.
   *  **Parameters:** `pk` - primary key of the incentive to be updated.
    *  **Request Body:**
       ```json
        {
              "amount":"decimal",
              "reason":"string"
          }
        ```
   *   **Response:**
        * Returns a 200 status code on successful update, together with the updated incentive object.

#### - **Delete Incentive**
  *  **URL:** `/incentives/<int:pk>/delete/`
   * **Method:** `DELETE`
   *  **Description:** Deletes an existing incentive using the primary key.
   *  **Parameters:** `pk` - primary key of the incentive you want to delete.
  *  **Response:**
       *  Returns a 204 status code on successful deletion.

### 14. Badge Endpoints:
 #### List All Badges
 *  **URL:** `/badges/`
    *  **Method:** `GET`
    *  **Description:** Get a list of all badges
     *  **Response:**
        ```json
           [
                {
                "name":"string",
                "description":"text",
                "image":"string (optional)",
                "badge_type":"SALES|SERVICE|LOYALTY|SPECIAL",
                "criteria":"text",
                 "expiration_period":"duration (optional)"
               }
               ,...
            ]
         ```
         
#### Get single Badge
 *  **URL:** `/badges/<int:pk>/`
   *  **Method:** `GET`
    * **Description:** Get a single badge using primary key.
   *  **Parameters:** `pk` - primary key of the badge you want to fetch.
    *  **Response:**
        ```json
             {
                "name":"string",
                "description":"text",
                "image":"string (optional)",
                "badge_type":"SALES|SERVICE|LOYALTY|SPECIAL",
                "criteria":"text",
                 "expiration_period":"duration (optional)"
               }
         ```
         
  #### Create a Badge
   * **URL:** `/badges/create/`
   *  **Method:** `POST`
   *   **Description:** Create a new Badge using POST request.
    *   **Request Body:**
           ```json
            {
                "name":"string",
                "description":"text",
                "image":"string (optional)",
                "badge_type":"SALES|SERVICE|LOYALTY|SPECIAL",
                "criteria":"text",
                 "expiration_period":"duration (optional)"
                }
           ```
    *  **Response:**
        *   Returns a 201 status code on successful creation of the badge, together with the created badge object.

  #### Update a Badge
    * **URL:** `/badges/<int:pk>/update/`
    * **Method:** `PUT`
    *  **Description:** Updates an existing badge using primary key
    *  **Parameters:** `pk` - primary key of the badge you want to update
     * **Request Body:**
            ```json
            {
                "name":"string",
                "description":"text",
                "image":"string (optional)",
                "badge_type":"SALES|SERVICE|LOYALTY|SPECIAL",
                "criteria":"text",
                 "expiration_period":"duration (optional)"
                }
            ```
     *  **Response:**
        *  Returns a 200 status code on successful update, together with the updated badge object.

    #### Delete a Badge
      *  **URL:** `/badges/<int:pk>/delete/`
     *  **Method:** `DELETE`
    * **Description:** Delete an existing badge using its primary key.
     * **Parameters:** `pk` - Primary key of the badge you want to delete.
    * **Response:**
        * Returns a 204 status code on successful deletion of the badge.

### 15. WaiterBadge Endpoints:

####  List All Waiter Badges
 * **URL:** `/waiterbadges/`
  *  **Method:** `GET`
  * **Description:** List all of the waiter badges
  *   **Response:**
        ```json
        [
           {
              "waiter":"integer",
             "badge":"integer",
             "date_awarded":"date",
              "expiration_date":"date (optional)"
            },
            ...
         ]
        ```

#### Create Waiter Badge
 *  **URL:** `/waiterbadges/create/`
    * **Method:** `POST`
   *  **Description:** Create a waiter badge.
     *  **Request Body:**
        ```json
        {
           "badge":"integer"
          }
         ```
    * **Response:**
         *   Returns a 201 status code on successful creation of the waiter badge, together with the created object.

#### Delete Waiter Badge
 * **URL:** `/waiterbadges/<int:pk>/delete/`
   *  **Method:** `DELETE`
  *   **Description:** Delete a waiter badge.
     *  **Parameters:** `pk`: The primary key of the waiter badge to be deleted.
   *   **Response:**
        *   Returns a 204 status code on successful deletion.

### 16. Tax Endpoints

   #### Create Tax
   *   **URL:** `/orders/<int:order_id>/taxes/create/`
    *   **Method:** `POST`
   *   **Description:** Creates a tax entry associated with an order.
    * **Parameters:** `order_id` - primary key of the order.
     *  **Request Body:**
        ```json
        {
           "name":"string",
          "amount":"decimal",
           "is_percentage":"boolean"
          }
       ```
   *  **Response:**
       *   Returns a 201 status code on successful creation of the tax, together with the created object.

### 17. Review Endpoints

#### Create Review
  * **URL:** `/orders/<int:order_id>/reviews/create/`
    *   **Method:** `POST`
    *  **Description:** Creates a review for a user associated with an order.
   *  **Parameters:** `order_id` - primary key of the order
     *  **Request Body:**
       ```json
        {
            "rating":"integer",
            "comment":"string"
          }
         ```
    *  **Response:**
      * Returns a 201 status code on successful creation of the review, together with the created object.
       
### 18. Takeout Endpoints
    
  #### Create Takeout
  * **URL:** `/orders/<int:order_id>/takeouts/create/`
    *   **Method:** `POST`
   *  **Description:** Create a takeout object associated with an order.
     *  **Parameters:** `order_id` - primary key of the order.
   *   **Request Body:**
         ```json
            {
             "pickup_time": "datetime",
               "delivery_option": "PICKUP|DELIVERY",
              "delivery_address": "string (optional)"
            }
         ```
    *  **Response:**
         *   Returns a 201 status code on successful creation of the takeout, together with the created object.

### 19 Role Endpoints
    #### List All Roles
      *  **URL:** `/roles/`
        * **Method:** `GET`
    *  **Description:** Get a list of all roles.
     *  **Response:**
        ```json
        [
           {
              "id": "integer",
              "name": "string",
              "description": "string (optional)",
               "vendor":"integer"
           }
           ,...
        ]
       ```
       
  #### Get Single Role Detail
    *  **URL:** `/roles/<int:pk>/`
     * **Method:** `GET`
     *  **Description:** Retrieves a single role using its primary key.
     * **Parameters:** `pk` - Primary key of the role to be fetched.
     *  **Response:**
        ```json
          {
             "id": "integer",
              "name": "string",
             "description": "string (optional)",
               "vendor":"integer"
          }
         ```
         
    #### Create a role
      *  **URL:** `/roles/create/`
      *  **Method:** `POST`
      * **Description:** Creates a role using the posted data.
        * **Request Body:**
            ```json
            {
                "name": "string",
                "description": "string (optional)",
               "vendor":"integer"
             }
           ```
     * **Response:**
         * Returns a 201 status code on successful creation of the role, together with the created object.
     
    #### Update a role
     *  **URL:** `/roles/<int:pk>/update/`
     *  **Method:** `PUT`
     *  **Description:** Updates a role using the posted data
     *   **Parameters:** `pk` - primary key of the role to be updated
      * **Request Body:**
           ```json
           {
                 "name": "string",
                "description": "string (optional)",
                  "vendor":"integer"
             }
         ```
     *   **Response:**
         *  Returns a 200 status code on successful update, together with the updated role object.

    #### Delete a role
      *  **URL:** `/roles/<int:pk>/delete/`
     * **Method:** `DELETE`
      *  **Description:** Deletes a role using the primary key.
      * **Parameters:** `pk` - primary key of the role to be deleted.
      *  **Response:**
        * Returns a 204 status code on successful deletion.