package service

import (
	"lang-portal/backend_go/internal/models"
)

type DashboardService struct{}

func NewDashboardService() *DashboardService {
	return &DashboardService{}
}

func (s *DashboardService) GetLastStudySession() (*models.StudySession, error) {
	return models.GetLastStudySession()
}

func (s *DashboardService) GetStudyProgress() (*models.StudyProgress, error) {
	return models.GetStudyProgress()
}

func (s *DashboardService) GetQuickStats() (*models.QuickStats, error) {
	return models.GetQuickStats()
}
