package models

type StudyProgress struct {
	TotalWordsStudied    int `json:"total_words_studied"`
	TotalAvailableWords  int `json:"total_available_words"`
}

type QuickStats struct {
	TotalWords      int `json:"total_words"`
	WordsStudied    int `json:"words_studied"`
	StudyActivities int `json:"study_activities"`
}

func GetStudyProgress() (*StudyProgress, error) {
	var progress StudyProgress
	err := db.QueryRow(`
		SELECT 
			(SELECT COUNT(DISTINCT word_id) FROM word_review_items) as total_words_studied,
			(SELECT COUNT(*) FROM words) as total_available_words
	`).Scan(&progress.TotalWordsStudied, &progress.TotalAvailableWords)
	if err != nil {
		return nil, err
	}
	return &progress, nil
}

func GetQuickStats() (*QuickStats, error) {
	var stats QuickStats
	err := db.QueryRow(`
		SELECT 
			(SELECT COUNT(*) FROM words) as total_words,
			(SELECT COUNT(DISTINCT word_id) FROM word_review_items) as words_studied,
			(SELECT COUNT(*) FROM study_activities) as study_activities
	`).Scan(&stats.TotalWords, &stats.WordsStudied, &stats.StudyActivities)
	if err != nil {
		return nil, err
	}
	return &stats, nil
}
