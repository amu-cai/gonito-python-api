CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    email VARCHAR (50) UNIQUE NOT NULL,
    username VARCHAR (50) UNIQUE NOT NULL,
	hashed_password VARCHAR NOT NULL,
	is_admin BOOLEAN NOT NULL,
	is_author BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    id serial PRIMARY KEY,
    author VARCHAR (50) REFERENCES users (username),
    source VARCHAR (5000) NOT NULL,
    title VARCHAR (500) UNIQUE NOT NULL,
	type VARCHAR (100) NOT NULL,
	description VARCHAR (5000) NOT NULL,
	main_metric VARCHAR (100) NOT NULL,
    main_metric_parameters VARCHAR (5000),
	best_score FLOAT (50) NOT NULL,
    deadline VARCHAR (500) NOT NULL,
    award VARCHAR (500) NOT NULL,
    readme VARCHAR NOT NULL,
    deleted BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS submission (
    id serial PRIMARY KEY,
    challenge VARCHAR (500) REFERENCES challenges (title),
	submitter VARCHAR (50) REFERENCES users (username),
	description VARCHAR (500) NOT NULL,
	dev_result FLOAT (50) NOT NULL,
	test_result FLOAT (50) NOT NULL,
    timestamp VARCHAR (50) NOT NULL,
    deleted BOOLEAN
);
