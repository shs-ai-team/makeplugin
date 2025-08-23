// /frontend/src/apiService.js

// Retrieve the base URL for the API from environment variables.
// This makes the code portable between development and production environments.
const API_URL = process.env.REACT_APP_API_URL;

/**
 * Handles common fetch logic, including error handling.
 * @param {string} url - The full URL to fetch.
 * @param {object} options - The options object for the fetch call.
 * @returns {Promise<object>} - The JSON response from the API.
 * @throws {Error} - Throws an error if the network response is not ok.
 */
const apiFetch = async (url, options = {}) => {
  const response = await fetch(url, options);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'An unknown error occurred' }));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }
  // For GET requests that might not return a body (like the zip download)
  if (response.headers.get("Content-Type")?.includes("application/zip")) {
      return response;
  }
  return response.json();
};

/**
 * 1. Starts a new chat session.
 * Corresponds to: POST /session
 * @returns {Promise<object>} - An object containing the session_id and initial message.
 */
export const startNewSession = () => {
  return apiFetch(`${API_URL}/session`, {
    method: 'POST',
  });
};

/**
 * 2. Retrieves all messages for a given session.
 * Corresponds to: GET /session/{session_id}
 * @param {string} sessionId - The ID of the session to retrieve.
 * @returns {Promise<object>} - An object containing the session_id and messages array.
 */
export const getSessionMessages = (sessionId) => {
  return apiFetch(`${API_URL}/session/${sessionId}`);
};

/**
 * 3. Sends a user's message to the consultant AI.
 * Corresponds to: POST /session/{session_id}/consultant_response
 * @param {string} sessionId - The ID of the current session.
 * @param {string} userMessage - The message from the user.
 * @returns {Promise<object>} - The consultant's response message object.
 */
export const sendUserMessage = (sessionId, userMessage) => {
  return apiFetch(`${API_URL}/session/${sessionId}/consultant_response`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: userMessage }),
  });
};

/**
 * 4. Polls the backend to check if the plugin is ready.
 * Corresponds to: POST /session/{session_id}/dev_response
 * @param {string} sessionId - The ID of the current session.
 * @returns {Promise<object>} - An object indicating success and containing the developer's message.
 */
export const getDeveloperResponse = (sessionId) => {
  return apiFetch(`${API_URL}/session/${sessionId}/dev_response`, {
    method: 'POST',
  });
};

/**
 * 5. Constructs the URL for downloading the plugin ZIP file.
 * Note: This function doesn't fetch the file, it just provides the URL for an <a> tag.
 * Corresponds to: GET /session/{session_id}/download_zip/{zip_id}
 * @param {string} sessionId - The ID of the current session.
 * @param {number} zipId - The ID of the zip file to download.
 * @returns {string} - The full URL to download the plugin ZIP.
 */
export const getPluginDownloadUrl = (sessionId, zipId) => {
  return `${API_URL}/session/${sessionId}/download_zip/${zipId}`;
};


/**
 * 6. Retrieves all session IDs.
 * Corresponds to: GET /sessions
 * @returns {Promise<string[]>} - An array of session UUIDs.
 */
export const getAllSessions = () => {
  return apiFetch(`${API_URL}/sessions`);
};