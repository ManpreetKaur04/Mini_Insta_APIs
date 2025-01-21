# Social Media Backend

A social media backend where users can post content, follow/unfollow others, and view a feed of posts from users they follow. Users can also hide or block specific users, which impacts feed visibility.

## Requirements

### 1. Models

#### User
- Use Django's built-in User model for authentication.

#### Post
- `author` (ForeignKey to User): The creator of the post.
- `content` (TextField): The text of the post (max length: 280 characters).
- `created_at` (DateTimeField): Timestamp of when the post was created.

#### Follower
- `follower` (ForeignKey to User): The user who follows someone.
- `following` (ForeignKey to User): The user being followed.
- **Unique Constraint**: Prevent duplicate follow relationships.

#### UserAction (For Hide and Block)
- `user` (ForeignKey to User): The user performing the action.
- `target_user` (ForeignKey to User): The user being hidden/blocked.
- `action` (ChoiceField): Choices are HIDE or BLOCK.
- **Unique Constraint**: Prevent duplicate actions for the same user-target pair.

### 2. API Endpoints

#### Authentication

- **POST /auth/register/**: Register a new user.
  - Request Body: 
    ```json
    { "username": "user1", "password": "password123" }
    ```

- **POST /auth/login/**: Login and retrieve a token.

#### Social Media Features

##### Post Management

- **POST /posts/** (Authenticated users only): Create a new post.
  - Request Body:
    ```json
    { "content": "This is my first post!" }
    ```

- **GET /posts/**: Retrieve all public posts (paginated).
  - Query Params:
    - `?author=<username>`: Filter posts by a specific user.

##### Follow/Unfollow

- **POST /users/{username}/follow/** (Authenticated users only): Follow a specific user.
  - Validation: Prevent following oneself and prevent duplicate follows.

- **POST /users/{username}/unfollow/** (Authenticated users only): Unfollow a specific user.

- **GET /users/{username}/followers/**: List all followers of a specific user.

- **GET /users/{username}/following/**: List all users a specific user is following.

##### Hide/Block

- **POST /users/{username}/action/** (Authenticated users only): Hide or block a specific user.
  - Request Body:
    ```json
    { "action": "HIDE" } 
    ```
    or
    ```json
    { "action": "BLOCK" }
    ```

  - Logic:
    - **HIDE**: Posts from the target user are excluded from the feed.
    - **BLOCK**: Fully restrict interactions (cannot follow/unfollow, view posts, or access profile).

- **DELETE /users/{username}/action/** (Authenticated users only): Remove a HIDE or BLOCK action on a user.

- **GET /users/actions/**: Retrieve a list of users hidden/blocked by the logged-in user.

##### Feed

- **GET /feed/** (Authenticated users only): Retrieve posts from users the logged-in user is following, excluding:
  - Users marked as HIDE.
  - Users marked as BLOCK.
  - Posts are sorted by `created_at` (most recent first).
  - Paginated response.


