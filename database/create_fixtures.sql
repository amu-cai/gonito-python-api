CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    username VARCHAR (50) UNIQUE NOT NULL,
	hashed_password VARCHAR (50) NOT NULL,
	is_admin BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    id serial PRIMARY KEY,
    title VARCHAR (500) UNIQUE NOT NULL,
	type VARCHAR (500) NOT NULL,
	description VARCHAR (500) NOT NULL,
	main_metric VARCHAR (500) NOT NULL,
	best_score VARCHAR (500) NOT NULL,
    deadline VARCHAR (500) NOT NULL,
    award VARCHAR (500) NOT NULL,
    readme VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS submission (
    id serial PRIMARY KEY,
    challenge VARCHAR (500) REFERENCES challenges (title),
	submitter VARCHAR (500) NOT NULL,
	description VARCHAR (500) NOT NULL,
	dev_result VARCHAR (500) NOT NULL,
	test_result VARCHAR (500) NOT NULL,
    timestamp VARCHAR (50) NOT NULL
);
