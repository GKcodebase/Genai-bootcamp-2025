package main

import (
	"lang-portal/backend_go/internal/handlers"
	"lang-portal/backend_go/internal/models"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize database
	if err := models.InitDB("lang_learning.db"); err != nil {
		panic(err)
	}

	// Initialize router
	r := gin.Default()

	// Enable CORS
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, Authorization")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	})

	// Dashboard routes
	r.GET("/api/dashboard/last_study_session", handlers.GetLastStudySession)
	r.GET("/api/dashboard/study_progress", handlers.GetStudyProgress)
	r.GET("/api/dashboard/quick-stats", handlers.GetQuickStats)

	// Study activities routes
	r.GET("/api/study_activities/:id", handlers.GetStudyActivity)
	r.GET("/api/study_activities/:id/study_sessions", handlers.GetStudyActivitySessions)
	r.POST("/api/study_activities", handlers.CreateStudyActivity)

	// Words routes
	r.GET("/api/words", handlers.GetWords)
	r.GET("/api/words/:id", handlers.GetWord)

	// Run server
	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
