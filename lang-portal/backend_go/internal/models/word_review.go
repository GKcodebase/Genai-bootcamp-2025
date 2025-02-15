package models

import "time"

type WordReviewItem struct {
	WordID          int       `json:"word_id"`
	StudySessionID  int       `json:"study_session_id"`
	Correct         bool      `json:"correct"`
	CreatedAt       time.Time `json:"created_at"`
}

func CreateWordReviewItem(wordID, studySessionID int, correct bool) error {
	_, err := db.Exec(`
		INSERT INTO word_review_items (word_id, study_session_id, correct, created_at)
		VALUES (?, ?, ?, CURRENT_TIMESTAMP)`,
		wordID, studySessionID, correct)
	return err
}

func GetWordReviewStats(wordID int) (int, int, error) {
	var correctCount, wrongCount int
	err := db.QueryRow(`
		SELECT 
			COUNT(CASE WHEN correct = 1 THEN 1 END) as correct_count,
			COUNT(CASE WHEN correct = 0 THEN 1 END) as wrong_count
		FROM word_review_items
		WHERE word_id = ?`,
		wordID).Scan(&correctCount, &wrongCount)
	if err != nil {
		return 0, 0, err
	}
	return correctCount, wrongCount, nil
}
