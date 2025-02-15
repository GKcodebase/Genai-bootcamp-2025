package handlers

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/backend_go/internal/service"
)

var wordService = service.NewWordService()

func GetWords(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	perPage := 100 // As per specification

	words, totalItems, err := wordService.GetWords(page, perPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	totalPages := (totalItems + perPage - 1) / perPage

	c.JSON(http.StatusOK, gin.H{
		"items": words,
		"pagination": gin.H{
			"current_page":    page,
			"total_pages":     totalPages,
			"total_items":     totalItems,
			"items_per_page":  perPage,
		},
	})
}

func GetWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid word ID"})
		return
	}

	word, stats, groups, err := wordService.GetWord(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"id":              word.ID,
		"original_text":   word.OriginalText,
		"translated_text": word.TranslatedText,
		"pronunciation":   word.Pronunciation,
		"part_of_speech": word.PartOfSpeech,
		"example":        word.ExampleSentence,
		"stats":          stats,
		"groups":         groups,
	})
}
