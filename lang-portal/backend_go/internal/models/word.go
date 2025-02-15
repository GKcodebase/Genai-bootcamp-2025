package models

import (
	"database/sql"
	"encoding/json"
)

type Word struct {
	ID       int             `json:"id"`
	Japanese string          `json:"japanese"`
	Romaji   string          `json:"romaji"`
	English  string          `json:"english"`
	Parts    json.RawMessage `json:"parts"`
}

type WordStats struct {
	CorrectCount int `json:"correct_count"`
	WrongCount   int `json:"wrong_count"`
}

func GetWords(page, perPage int) ([]Word, int, error) {
	offset := (page - 1) * perPage
	var words []Word
	var totalItems int

	// Get total count
	err := db.QueryRow("SELECT COUNT(*) FROM words").Scan(&totalItems)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated words
	rows, err := db.Query(`
		SELECT id, japanese, romaji, english, parts
		FROM words 
		LIMIT ? OFFSET ?`,
		perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	for rows.Next() {
		var w Word
		if err := rows.Scan(&w.ID, &w.Japanese, &w.Romaji, &w.English, &w.Parts); err != nil {
			return nil, 0, err
		}
		words = append(words, w)
	}

	return words, totalItems, nil
}

func GetWord(id int) (*Word, *WordStats, []Group, error) {
	var word Word
	var stats WordStats
	var groups []Group

	// Get word details
	err := db.QueryRow(`
		SELECT id, japanese, romaji, english, parts
		FROM words 
		WHERE id = ?`,
		id).Scan(&word.ID, &word.Japanese, &word.Romaji, &word.English, &word.Parts)
	if err != nil {
		return nil, nil, nil, err
	}

	// Get word stats
	err = db.QueryRow(`
		SELECT 
			COUNT(CASE WHEN correct = 1 THEN 1 END) as correct_count,
			COUNT(CASE WHEN correct = 0 THEN 1 END) as wrong_count
		FROM word_review_items
		WHERE word_id = ?`,
		id).Scan(&stats.CorrectCount, &stats.WrongCount)
	if err != nil && err != sql.ErrNoRows {
		return nil, nil, nil, err
	}

	// Get groups for the word
	rows, err := db.Query(`
		SELECT g.id, g.name, COUNT(w.id) as total_word_count
		FROM groups g
		JOIN words_groups wg ON g.id = wg.group_id
		JOIN words w ON wg.word_id = w.id
		WHERE wg.word_id = ?
		GROUP BY g.id`,
		id)
	if err != nil {
		return nil, nil, nil, err
	}
	defer rows.Close()

	for rows.Next() {
		var g Group
		if err := rows.Scan(&g.ID, &g.Name, &g.Stats.TotalWordCount); err != nil {
			return nil, nil, nil, err
		}
		groups = append(groups, g)
	}

	return &word, &stats, groups, nil
}
