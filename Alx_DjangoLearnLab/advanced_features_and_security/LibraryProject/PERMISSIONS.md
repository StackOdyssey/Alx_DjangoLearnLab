# Permissions Setup:
# - Book model defines: can_view, can_create, can_edit, can_delete
# - Groups:
#   - Viewers: can_view
#   - Editors: can_create, can_edit
#   - Admins: all permissions
# - Views use @permission_required to enforce access