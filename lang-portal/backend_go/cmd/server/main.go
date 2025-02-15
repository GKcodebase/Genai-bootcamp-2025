package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"lang-portal/backend_go/internal/handlers"
	"lang-portal/backend_go/internal/models"
)

func main() {
	// Initialize database
	if err := models.InitDB("words.db"); err != nil {
		log.Fatal(err)
	}

	// Set up Gin router
	r := gin.Default()

	// API routes
	api := r.Group("/api")
	{
		// Dashboard routes
		api.GET("/dashboard/last_study_session", handlers.GetLastStudySession)
		api.GET("/dashboard/study_progress", handlers.GetStudyProgress)
		api.GET("/dashboard/quick-stats", handlers.GetQuickStats)

		// Study activities routes
		api.GET("/study_activities/:id", handlers.GetStudyActivity)
		api.GET("/study_activities/:id/study_sessions", handlers.GetStudyActivitySessions)
		api.POST("/study_activities", handlers.CreateStudyActivity)

		// Words routes
		api.GET("/words", handlers.GetWords)
		api.GET("/words/:id", handlers.GetWord)
	}

	// Run server
	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
