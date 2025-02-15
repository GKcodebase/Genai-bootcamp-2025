package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"lang-portal/backend_go/internal/service"
)

var dashboardService = service.NewDashboardService()

func GetLastStudySession(c *gin.Context) {
	session, err := dashboardService.GetLastStudySession()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, session)
}

func GetStudyProgress(c *gin.Context) {
	progress, err := dashboardService.GetStudyProgress()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, progress)
}

func GetQuickStats(c *gin.Context) {
	stats, err := dashboardService.GetQuickStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, stats)
}
