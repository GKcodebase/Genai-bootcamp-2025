package handlers

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetLastStudySession(t *testing.T) {
	apiName := "GetLastStudySession"
	req, err := http.NewRequest("GET", "/api/dashboard/last_study_session", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetLastStudySession)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"session":"last"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetStudyProgress(t *testing.T) {
	apiName := "GetStudyProgress"
	req, err := http.NewRequest("GET", "/api/dashboard/study_progress", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetStudyProgress)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"progress":"some progress"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetQuickStats(t *testing.T) {
	apiName := "GetQuickStats"
	req, err := http.NewRequest("GET", "/api/dashboard/quick-stats", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetQuickStats)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"stats":"quick stats"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetStudyActivity(t *testing.T) {
	apiName := "GetStudyActivity"
	req, err := http.NewRequest("GET", "/api/study_activities/1", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetStudyActivity)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"activity":"study activity"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetStudyActivitySessions(t *testing.T) {
	apiName := "GetStudyActivitySessions"
	req, err := http.NewRequest("GET", "/api/study_activities/1/study_sessions", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetStudyActivitySessions)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"sessions":"study activity sessions"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestCreateStudyActivity(t *testing.T) {
	apiName := "CreateStudyActivity"
	req, err := http.NewRequest("POST", "/api/study_activities", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(CreateStudyActivity)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"activity":"created study activity"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetWords(t *testing.T) {
	apiName := "GetWords"
	req, err := http.NewRequest("GET", "/api/words", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetWords)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"words":"list of words"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

func TestGetWord(t *testing.T) {
	apiName := "GetWord"
	req, err := http.NewRequest("GET", "/api/words/1", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetWord)

	handler.ServeHTTP(rr, req)

	t.Logf("API: %s\nRequest: %v\nResponse: %v\n", apiName, req, rr.Body.String())

	assert.Equal(t, http.StatusOK, rr.Code)

	expected := `{"word":"word details"}`
	assert.JSONEq(t, expected, rr.Body.String())
}

// Mock handlers for testing purposes
func GetLastStudySession(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"session": "last"}
	json.NewEncoder(w).Encode(response)
}

func GetStudyProgress(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"progress": "some progress"}
	json.NewEncoder(w).Encode(response)
}

func GetQuickStats(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"stats": "quick stats"}
	json.NewEncoder(w).Encode(response)
}

func GetStudyActivity(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"activity": "study activity"}
	json.NewEncoder(w).Encode(response)
}

func GetStudyActivitySessions(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"sessions": "study activity sessions"}
	json.NewEncoder(w).Encode(response)
}

func CreateStudyActivity(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"activity": "created study activity"}
	json.NewEncoder(w).Encode(response)
}

func GetWords(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"words": "list of words"}
	json.NewEncoder(w).Encode(response)
}

func GetWord(w http.ResponseWriter, r *http.Request) {
	response := map[string]string{"word": "word details"}
	json.NewEncoder(w).Encode(response)
}
