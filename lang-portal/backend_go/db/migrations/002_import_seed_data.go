package migrations

import (
	"encoding/json"
	"io/ioutil"
	"path/filepath"
)

type WordSeed struct {
	Kanji   string          `json:"kanji"`
	Romaji  string          `json:"romaji"`
	English string          `json:"english"`
	Parts   json.RawMessage `json:"parts"`
}

type StudyActivitySeed struct {
	Name         string `json:"name"`
	URL          string `json:"url"`
	ThumbnailURL string `json:"thumbnail_url"`
}

func ImportSeedData(db *sql.DB) error {
	// Create default groups
	_, err := db.Exec(`INSERT INTO groups (name) VALUES ('Adjectives'), ('Verbs')`)
	if err != nil {
		return err
	}

	// Read and import adjectives
	adjBytes, err := ioutil.ReadFile(filepath.Join("db", "seeds", "data_adjectives.json"))
	if err != nil {
		return err
	}

	var adjectives []WordSeed
	if err := json.Unmarshal(adjBytes, &adjectives); err != nil {
		return err
	}

	// Import adjectives
	for _, adj := range adjectives {
		result, err := db.Exec(`
			INSERT INTO words (japanese, romaji, english, parts)
			VALUES (?, ?, ?, ?)`,
			adj.Kanji, adj.Romaji, adj.English, adj.Parts)
		if err != nil {
			return err
		}

		wordID, err := result.LastInsertId()
		if err != nil {
			return err
		}

		// Link to Adjectives group
		_, err = db.Exec(`
			INSERT INTO words_groups (word_id, group_id)
			VALUES (?, (SELECT id FROM groups WHERE name = 'Adjectives'))`,
			wordID)
		if err != nil {
			return err
		}
	}

	// Read and import verbs
	verbBytes, err := ioutil.ReadFile(filepath.Join("db", "seeds", "data_verbs.json"))
	if err != nil {
		return err
	}

	var verbs []WordSeed
	if err := json.Unmarshal(verbBytes, &verbs); err != nil {
		return err
	}

	// Import verbs
	for _, verb := range verbs {
		result, err := db.Exec(`
			INSERT INTO words (japanese, romaji, english, parts)
			VALUES (?, ?, ?, ?)`,
			verb.Kanji, verb.Romaji, verb.English, verb.Parts)
		if err != nil {
			return err
		}

		wordID, err := result.LastInsertId()
		if err != nil {
			return err
		}

		// Link to Verbs group
		_, err = db.Exec(`
			INSERT INTO words_groups (word_id, group_id)
			VALUES (?, (SELECT id FROM groups WHERE name = 'Verbs'))`,
			wordID)
		if err != nil {
			return err
		}
	}

	// Read and import study activities
	activityBytes, err := ioutil.ReadFile(filepath.Join("db", "seeds", "study_activities.json"))
	if err != nil {
		return err
	}

	var activities []StudyActivitySeed
	if err := json.Unmarshal(activityBytes, &activities); err != nil {
		return err
	}

	// Import study activities
	for _, activity := range activities {
		_, err := db.Exec(`
			INSERT INTO study_activities (name, thumbnail_url)
			VALUES (?, ?)`,
			activity.Name, activity.ThumbnailURL)
		if err != nil {
			return err
		}
	}

	return nil
}
