package service

import (
	"lang-portal/backend_go/internal/models"
)

type WordService struct{}

func NewWordService() *WordService {
	return &WordService{}
}

func (s *WordService) GetWords(page, perPage int) ([]models.Word, int, error) {
	return models.GetWords(page, perPage)
}

func (s *WordService) GetWord(id int) (*models.Word, *models.WordStats, []models.Group, error) {
	return models.GetWord(id)
}
