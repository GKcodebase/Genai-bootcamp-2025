
-- Insert study activities
INSERT INTO study_activities (id, name, url, thumbnail_url) VALUES
(1, 'Vocabulary Quiz', '/quiz', '/images/quiz.png'),
(2, 'Flashcards', '/flashcards', '/images/flashcards.png'),
(3, 'Writing Practice', '/writing', '/images/writing.png');

-- Insert groups
INSERT INTO groups (id, name, words_count) VALUES
(1, 'Basic Greetings', 3),
(2, 'Numbers', 10),
(3, 'Colors', 8),
(4, 'Days of Week', 7);

-- Insert words
-- INSERT INTO words (id, kanji, romaji, english, parts) VALUES
-- (1, 'こんにちは', 'konnichiwa', 'hello', '[{"kanji":"こん","romaji":["kon"]},{"kanji":"にち","romaji":["nichi"]},{"kanji":"は","romaji":["wa"]}]'),
-- (2, 'さようなら', 'sayounara', 'goodbye', '[{"kanji":"さよう","romaji":["sayou"]},{"kanji":"なら","romaji":["nara"]}]'),
-- (3, 'ありがとう', 'arigatou', 'thank you', '[{"kanji":"あり","romaji":["ari"]},{"kanji":"がとう","romaji":["gatou"]}]'),
-- (4, '赤', 'aka', 'red', '[{"kanji":"赤","romaji":["aka"]}]'),
-- (5, '青', 'ao', 'blue', '[{"kanji":"青","romaji":["ao"]}]');

-- Link words to groups (word_groups join table)
INSERT INTO word_groups (word_id, group_id) VALUES
(1, 1), -- こんにちは -> Basic Greetings
(2, 1), -- さようなら -> Basic Greetings
(3, 1), -- ありがとう -> Basic Greetings
(4, 3), -- 赤 -> Colors
(5, 3); -- 青 -> Colors

-- Insert study sessions
INSERT INTO study_sessions (id, group_id, study_activity_id, created_at) VALUES
(1, 1, 1, datetime('now')),
(2, 3, 2, datetime('now', '-1 day')),
(3, 1, 3, datetime('now', '-2 days'));

-- Insert word review items
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
(1, 1, true, datetime('now')),
(2, 1, false, datetime('now')),
(3, 1, true, datetime('now')),
(4, 2, true, datetime('now', '-1 day')),
(5, 2, true, datetime('now', '-1 day'));
