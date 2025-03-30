CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES Users(id)
);

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY,
    commenter INTEGER REFERENCES Users(id),
    post INTEGER REFERENCES Posts(id),
    comment TEXT
);

CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    reviewer INTEGER REFERENCES Users(id),
    post INTEGER REFERENCES Recipes(id),
    stars INTEGER,
    review TEXT
);
