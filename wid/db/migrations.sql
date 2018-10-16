CREATE DATABASE widdev;

\c widdev

CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	password_digest VARCHAR(255) NOT NULL
);

CREATE TABLE activities(
	id SERIAL PRIMARY KEY,
	name VARCHAR(255),
	description VARCHAR(255)
);

CREATE TABLE engagements(
	id SERIAL PRIMARY KEY,
	activity_id INT REFERENCES activities(id),
	start_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
	end_time TIMESTAMP WITH TIME ZONE,
	rating INT,
	notes VARCHAR(255)
);