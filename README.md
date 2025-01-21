Djangoreqirement.txt
Build a social media backend where users can post content, follow/unfollow others, and view a feed of posts from users they follow. Users can also hide or block specific users, which impacts the feed visibility.

Requirements:


1. Models:

- User:
Use Django's built-in User model for authentication.
Post:
author (ForeignKey to User): The creator of the post.
content (text): The text of the post (max length: 280 characters).
created_at (DateTime): Timestamp of when the post was created.


- Follower:
follower (ForeignKey to User): The user who follows someone.
following (ForeignKey to User): The user being followed.
Unique Constraint: Prevent duplicate follow relationships.


- UserAction (For Hide and Block):
user (ForeignKey to User): The user performing the action.
target_user (ForeignKey to User): The user being hidden/blocked.
action (ChoiceField): Choices are HIDE or BLOCK.
Unique Constraint: Prevent duplicate actions for the same user-target pair.


2. API Endpoints:

- Authentication:

POST /auth/register/:
Register a new user.
Request Body: { "username": "user1", "password": "password123" }
POST /auth/login/:
Login and retrieve a token.

- Social Media Features:

Post Management:
POST /posts/ (Authenticated users only):
Create a new post.
Request Body: { "content": "This is my first post!" }
GET /posts/:
Retrieve all public posts (paginated).
Query Params:
?author=<username>: Filter posts by a specific user.

- Follow/Unfollow:

POST /users/{username}/follow/ (Authenticated users only):
Follow a specific user.
Validation: Prevent following oneself and prevent duplicate follows.
POST /users/{username}/unfollow/ (Authenticated users only):
Unfollow a specific user.
GET /users/{username}/followers/:
List all followers of a specific user.
GET /users/{username}/following/:
List all users a specific user is following.


- Hide/Block:

POST /users/{username}/action/ (Authenticated users only):
Hide or block a specific user.
Request Body: { "action": "HIDE" } or { "action": "BLOCK" }
Logic:
HIDE: Posts from the target user are excluded from the feed.
BLOCK: Fully restrict interactions (cannot follow/unfollow, view posts, or access profile).
DELETE /users/{username}/action/ (Authenticated users only):
Remove a HIDE or BLOCK action on a user.
GET /users/actions/:
Retrieve a list of users hidden/blocked by the logged-in user.


- Feed:
GET /feed/ (Authenticated users only):
Retrieve posts from users the logged-in user is following, excluding:
Users marked as HIDE.
Users marked as BLOCK.
Posts are sorted by created_at (most recent first).
Paginated response.

3. Deliverables:

- Django REST API:
Fully functional APIs as described above.
Proper use of serializers and viewsets.
JWT-based authentication.

- Database Validations:
Ensure no duplicate follow/hidden/blocked relationships.
Prevent invalid actions (e.g., blocking oneself).

- Feed Logic: Efficiently exclude posts from hidden/blocked users.

- Pagination: Implement pagination for posts and feed APIs.


- Testing: Include a Postman collection or Swagger documentation for easy API testing.



Time Breakdown:
- Setting up models and database relationships: 60 minutes.
- Writing views and serializers for posts, followers, and actions: 90 minutes.
- Implementing feed logic with HIDE and BLOCK: 60 minutes.
- Writing basic validations and testing: 30 minutes.


Evaluation Criteria:
1. Django Proficiency:Correct usage of models, serializers, and views.
2. ORM Knowledge:Efficient querying for feed generation and action handling.
3. API Design: RESTful endpoints with proper naming and structure.
4. Edge Case Handling: Prevent duplicate hides/blocks, self-block, and invalid actions.
5. Speed: How much of the task is completed within the given time.