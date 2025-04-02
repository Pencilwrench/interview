## Bulk Task Assignment Feature

Hey team! I've added a new feature that allows assigning multiple tasks to a user at once. This will help make task management more efficient.

### Changes Made
- Added new endpoint `/tasks/bulk-assign/`
- Created serializer for bulk assignment
- Added view to handle the assignment logic
- Updated URL routing

### How to Use
Send a POST request to `/tasks/bulk-assign/` with the following JSON:
```json
{
    "task_ids": [1, 2, 3],
    "user_id": 123
}
```

The endpoint will assign all specified tasks to the given user and return a success message with the updated tasks.

### Testing Done
- Tested manually with Postman
- Verified that tasks get assigned correctly
- Checked that the API returns proper response

### Notes
- This is my first major feature, so any feedback is appreciated!
- Let me know if you need any changes or have questions
- I tried to keep it simple and straightforward
