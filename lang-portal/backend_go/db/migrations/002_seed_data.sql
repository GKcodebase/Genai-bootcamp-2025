-- Insert sample groups
INSERT INTO groups (name) VALUES 
    ('Basic Vocabulary'),
    ('Common Phrases'),
    ('Travel Essentials');

-- Insert sample words
INSERT INTO words (original_text, translated_text, pronunciation, part_of_speech, example_sentence) VALUES
    ('こんにちは', 'Hello', 'Konnichiwa', 'Greeting', 'こんにちは、元気ですか？'),
    ('ありがとう', 'Thank you', 'Arigatou', 'Expression', 'ありがとう、助かりました。'),
    ('お願いします', 'Please', 'Onegaishimasu', 'Expression', 'コーヒーをお願いします。'),
    ('駅', 'Station', 'Eki', 'Noun', '駅はどこですか？'),
    ('水', 'Water', 'Mizu', 'Noun', '水を飲みます。');

-- Associate words with groups
INSERT INTO words_groups (word_id, group_id) VALUES
    (1, 1), -- Hello -> Basic Vocabulary
    (2, 1), -- Thank you -> Basic Vocabulary
    (3, 2), -- Please -> Common Phrases
    (4, 3), -- Station -> Travel Essentials
    (5, 1); -- Water -> Basic Vocabulary

-- Insert sample study activities
INSERT INTO study_activities (name, thumbnail_url, description, group_id) VALUES
    ('Vocabulary Quiz', 'https://example.com/vocab.jpg', 'Test your basic vocabulary knowledge', 1),
    ('Phrase Practice', 'https://example.com/phrases.jpg', 'Practice common Japanese phrases', 2),
    ('Travel Words Review', 'https://example.com/travel.jpg', 'Review essential travel vocabulary', 3);

-- Insert sample study sessions
INSERT INTO study_sessions (group_id, study_activity_id, created_at) VALUES
    (1, 1, datetime('now', '-1 day')),
    (2, 2, datetime('now', '-2 days')),
    (3, 3, datetime('now', '-3 days'));

-- Insert sample word review items
INSERT INTO word_review_items (word_id, study_session_id, correct, created_at) VALUES
    (1, 1, 1, datetime('now', '-1 day')),
    (2, 1, 1, datetime('now', '-1 day')),
    (3, 2, 0, datetime('now', '-2 days')),
    (4, 3, 1, datetime('now', '-3 days')),
    (5, 1, 1, datetime('now', '-1 day'));
