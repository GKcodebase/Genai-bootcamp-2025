package models

import (
	"database/sql"
	"time"
)

type StudyActivity struct {
	ID              int       `json:"id"`
	StudySessionID  int       `json:"study_session_id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	Name            string    `json:"name"`
	ThumbnailURL    string    `json:"thumbnail_url"`
	Description     string    `json:"description"`
}

type StudySession struct {
	ID              int       `json:"id"`
	GroupID         int       `json:"group_id"`
	CreatedAt       time.Time `json:"created_at"`
	StudyActivityID int       `json:"study_activity_id"`
	GroupName       string    `json:"group_name"`
	StartTime       time.Time `json:"start_time"`
	EndTime         time.Time `json:"end_time"`
	ReviewItemsCount int       `json:"review_items_count"`
}

type StudySessionResponse struct {
	ID               int       `json:"id"`
	ActivityName     string    `json:"activity_name"`
	GroupName        string    `json:"group_name"`
	StartTime        time.Time `json:"start_time"`
	EndTime          time.Time `json:"end_time"`
	ReviewItemsCount int       `json:"review_items_count"`
}

func GetStudyActivity(id int) (*StudyActivity, error) {
	var activity StudyActivity
	err := db.QueryRow(`
		SELECT 
			sa.id, 
			sa.study_session_id,
			sa.group_id,
			sa.created_at,
			COALESCE(sa.name, 'Vocabulary Quiz') as name,
			COALESCE(sa.thumbnail_url, 'https://example.com/thumbnail.jpg') as thumbnail_url,
			COALESCE(sa.description, 'Practice your vocabulary with flashcards') as description
		FROM study_activities sa
		WHERE sa.id = ?`,
		id).Scan(
		&activity.ID,
		&activity.StudySessionID,
		&activity.GroupID,
		&activity.CreatedAt,
		&activity.Name,
		&activity.ThumbnailURL,
		&activity.Description,
	)
	if err == sql.ErrNoRows {
		// For demo purposes, return mock data if not found
		activity = StudyActivity{
			ID:           id,
			Name:         "Vocabulary Quiz",
			ThumbnailURL: "https://example.com/thumbnail.jpg",
			Description:  "Practice your vocabulary with flashcards",
			CreatedAt:    time.Now(),
		}
		return &activity, nil
	}
	if err != nil {
		return nil, err
	}
	return &activity, nil
}

func GetStudyActivitySessions(activityID int, page, perPage int) ([]StudySessionResponse, int, error) {
	offset := (page - 1) * perPage
	var sessions []StudySessionResponse
	var totalItems int

	// Get total count
	err := db.QueryRow(`
		SELECT COUNT(*) 
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		WHERE ss.study_activity_id = ?`,
		activityID).Scan(&totalItems)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated sessions
	rows, err := db.Query(`
		SELECT 
			ss.id,
			COALESCE(sa.name, 'Vocabulary Quiz') as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			DATETIME(ss.created_at, '+10 minutes') as end_time,
			(SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN study_activities sa ON ss.study_activity_id = sa.id
		WHERE ss.study_activity_id = ?
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`,
		activityID, perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	for rows.Next() {
		var s StudySessionResponse
		if err := rows.Scan(
			&s.ID,
			&s.ActivityName,
			&s.GroupName,
			&s.StartTime,
			&s.EndTime,
			&s.ReviewItemsCount,
		); err != nil {
			return nil, 0, err
		}
		sessions = append(sessions, s)
	}

	if err = rows.Err(); err != nil {
		return nil, 0, err
	}

	return sessions, totalItems, nil
}

func GetLastStudySession() (*StudySession, error) {
	var session StudySession
	err := db.QueryRow(`
		SELECT 
			ss.id,
			ss.group_id,
			ss.study_activity_id,
			ss.created_at,
			g.name as group_name,
			ss.created_at as start_time,
			DATETIME(ss.created_at, '+10 minutes') as end_time,
			(SELECT COUNT(*) FROM word_review_items wri WHERE wri.study_session_id = ss.id) as review_items_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		ORDER BY ss.created_at DESC
		LIMIT 1
	`).Scan(
		&session.ID,
		&session.GroupID,
		&session.StudyActivityID,
		&session.CreatedAt,
		&session.GroupName,
		&session.StartTime,
		&session.EndTime,
		&session.ReviewItemsCount,
	)
	if err != nil {
		return nil, err
	}
	return &session, nil
}

func CreateStudyActivity(groupID, studyActivityID int) (int, error) {
	result, err := db.Exec(`
		INSERT INTO study_activities (study_session_id, group_id, created_at)
		VALUES (?, ?, CURRENT_TIMESTAMP)`,
		studyActivityID, groupID)
	if err != nil {
		return 0, err
	}

	id, err := result.LastInsertId()
	if err != nil {
		return 0, err
	}

	return int(id), nil
}
