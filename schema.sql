CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	administrator BOOLEAN,
	username TEXT,
	pwhash TEXT
);

CREATE TABLE IF NOT EXISTS forums (
	id SERIAL PRIMARY KEY,
	hide BOOLEAN,
	topic TEXT
);

CREATE TABLE IF NOT EXISTS threads (
	id SERIAL PRIMARY KEY,
	forum_id INTEGER REFERENCES forums ON DELETE CASCADE,
	created_by INTEGER REFERENCES users,
	title TEXT,
	created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
	id SERIAL PRIMARY KEY,
	thread_id INTEGER REFERENCES threads ON DELETE CASCADE,
	user_id INTEGER REFERENCES users,
	content TEXT,
	sent_at TIMESTAMP
);