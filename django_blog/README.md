Overview

This Django authentication system provides user registration, login, logout, and profile management functionality. It combines Django’s built-in authentication views with custom forms and views to support an extended user profile, including optional fields such as profile picture and bio.

Features

User Registration (custom form extending UserCreationForm)

User Login & Logout (Django built-in authentication views)

Profile Management (editable email)

Secure password handling (Django hashing)

CSRF protection on all forms

Automatic profile creation using Django signals

Overview
The blog app provides CRUD (Create, Read, Update, Delete) functionality for managing blog posts. Posts are stored in the database and can be managed through both the Django admin panel and custom views/templates.

Purpose
Enable users to engage by commenting on blog posts. Authenticated users can add, edit, and delete their own comments. All visitors can read comments.
How it works
- Comments are linked to posts via Comment.post and to users via Comment.author.
- Post detail page shows:
- All comments for the post (newest first).
- Inline form for adding a comment (for logged-in users).
- Edit/Delete controls only for the comment’s author.
Permissions
- Add comment: authenticated users only.
- Edit/Delete: only the comment author.
- Visibility: all comments visible on the post detail page.
URLs
- Post list: /post/
- Post detail: /post/<pk>/
- New post: /post/new/
- Update post: /post/<pk>/update/
- Delete post: /post/<pk>/delete/
- Add comment: /post/<post_pk>/comments/new/
- Edit comment: /comments/<pk>/edit/
- Delete comment: /comments/<pk>/delete/
Testing checklist
- As a logged-out user, you can read comments but see a prompt to log in to comment.
- As a logged-in user, you can add a comment; it appears immediately under the post.
- Only the comment author sees Edit/Delete for their comments.
- Editing updates the content and timestamp; deletion removes the comment and redirects back to the post.
- URL names work in templates with {% url %} tags.
Testing and documentation
- Create tags: In the post form, enter comma-separated tags. After saving, tags appear under the post title and link to the tag view.
- Edit tags: Open a post in edit mode, change the tag list; tags are created if new and removed if omitted.
- Search: Use the search bar; results include matches in title, content, or tag names.
- Permissions: Only authors can edit/delete posts; anyone can view and search; tags are public.
- Quick checks:
- Tags route: /tags/<tag_name>/ shows posts filtered by tag.
- Search route: /search/?q=django returns posts with “django” in title, content, or tags.
- Case-insensitivity: Tags stored as lowercase; searching is case-insensitive.
- Notes for maintainability:
- Normalization: Storing tags in lowercase avoids duplicates (“Django” vs “django”).
- Indexing (optional): Add indexes on Post.title and Tag.name for larger datasets.
- Taggit option: If you later adopt django-taggit, replace the Tag model and form logic with TaggableManager and taggit forms.
