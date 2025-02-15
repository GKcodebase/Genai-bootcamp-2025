package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"

	_ "modernc.org/sqlite"
)

type Word struct {
	OriginalText     string `json:"japanese"`
	TranslatedText   string `json:"english"`
	Pronunciation    string `json:"romaji"`
	PartOfSpeech    string `json:"type"`
	ExampleSentence string `json:"example,omitempty"`
}

type StudyActivity struct {
	Name         string `json:"name"`
	ThumbnailURL string `json:"thumbnail_url"`
	Description  string `json:"description"`
	GroupID      int    `json:"group_id"`
}

func main() {
	db, err := sql.Open("sqlite", "lang_learning.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Create Adjectives group
	result, err := db.Exec("INSERT INTO groups (name) VALUES (?)", "Adjectives")
	if err != nil {
		log.Fatal(err)
	}
	adjectivesGroupID, _ := result.LastInsertId()

	// Create Verbs group
	result, err = db.Exec("INSERT INTO groups (name) VALUES (?)", "Verbs")
	if err != nil {
		log.Fatal(err)
	}
	verbsGroupID, _ := result.LastInsertId()

	// Import adjectives
	importWords(db, "data_adjectives.json", int(adjectivesGroupID))

	// Import verbs
	importWords(db, "data_verbs.json", int(verbsGroupID))

	// Import study activities
	importStudyActivities(db)
}

func importWords(db *sql.DB, filename string, groupID int) {
	data, err := ioutil.ReadFile(filepath.Join("db", "seeds", filename))
	if err != nil {
		log.Fatal(err)
	}

	var words []Word
	if err := json.Unmarshal(data, &words); err != nil {
		log.Fatal(err)
	}

	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
	}

	stmt, err := tx.Prepare(`
		INSERT INTO words (original_text, translated_text, pronunciation, part_of_speech, example_sentence)
		VALUES (?, ?, ?, ?, ?)
	`)
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	groupStmt, err := tx.Prepare(`
		INSERT INTO words_groups (word_id, group_id)
		VALUES (?, ?)
	`)
	if err != nil {
		log.Fatal(err)
	}
	defer groupStmt.Close()

	for _, word := range words {
		result, err := stmt.Exec(
			word.OriginalText,
			word.TranslatedText,
			word.Pronunciation,
			word.PartOfSpeech,
			word.ExampleSentence,
		)
		if err != nil {
			tx.Rollback()
			log.Fatal(err)
		}

		wordID, _ := result.LastInsertId()
		_, err = groupStmt.Exec(wordID, groupID)
		if err != nil {
			tx.Rollback()
			log.Fatal(err)
		}
	}

	if err := tx.Commit(); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Imported %d words from %s\n", len(words), filename)
}

func importStudyActivities(db *sql.DB) {
	data, err := ioutil.ReadFile(filepath.Join("db", "seeds", "study_activities.json"))
	if err != nil {
		log.Fatal(err)
	}

	var activities []StudyActivity
	if err := json.Unmarshal(data, &activities); err != nil {
		log.Fatal(err)
	}

	stmt, err := db.Prepare(`
		INSERT INTO study_activities (name, thumbnail_url, description, group_id)
		VALUES (?, ?, ?, ?)
	`)
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	for _, activity := range activities {
		_, err := stmt.Exec(
			activity.Name,
			activity.ThumbnailURL,
			activity.Description,
			activity.GroupID,
		)
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Printf("Imported %d study activities\n", len(activities))
}
