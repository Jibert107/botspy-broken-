CREATE TABLE messages (
	message_id INTEGER PRIMARY KEY AUTOINCREMENT,
	message_username TEXT NOT NULL,
	message_text TEXT NOT NULL,
	message_date DATE NOT NULL
)
