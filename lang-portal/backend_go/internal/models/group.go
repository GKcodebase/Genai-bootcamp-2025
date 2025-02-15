package models

type GroupStats struct {
	TotalWordCount int `json:"total_word_count"`
}

type Group struct {
	ID    int        `json:"id"`
	Name  string     `json:"name"`
	Stats GroupStats `json:"stats"`
}

func GetGroup(id int) (*Group, error) {
	var group Group
	err := db.QueryRow(`
		SELECT g.id, g.name, COUNT(w.id) as total_word_count
		FROM groups g
		LEFT JOIN words_groups wg ON g.id = wg.group_id
		LEFT JOIN words w ON wg.word_id = w.id
		WHERE g.id = ?
		GROUP BY g.id`,
		id).Scan(&group.ID, &group.Name, &group.Stats.TotalWordCount)
	if err != nil {
		return nil, err
	}
	return &group, nil
}

func GetGroups(page, perPage int) ([]Group, int, error) {
	offset := (page - 1) * perPage
	var groups []Group
	var totalItems int

	// Get total count
	err := db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&totalItems)
	if err != nil {
		return nil, 0, err
	}

	// Get paginated groups with word counts
	rows, err := db.Query(`
		SELECT g.id, g.name, COUNT(wg.word_id) as total_word_count
		FROM groups g
		LEFT JOIN words_groups wg ON g.id = wg.group_id
		GROUP BY g.id
		LIMIT ? OFFSET ?`,
		perPage, offset)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	for rows.Next() {
		var g Group
		if err := rows.Scan(&g.ID, &g.Name, &g.Stats.TotalWordCount); err != nil {
			return nil, 0, err
		}
		groups = append(groups, g)
	}

	return groups, totalItems, nil
}
