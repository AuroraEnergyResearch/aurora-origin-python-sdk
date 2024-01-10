get_workbook_status = """
query ($sessionId: String!, $requestId: String) {
  getSession(sessionId: $sessionId) {
    getWorkbookStatus(requestId: $requestId) {
      generationStatus
      generationErrors
      downloadURL
      requestId
    }
  }
}
"""
