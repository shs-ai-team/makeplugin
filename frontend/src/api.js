// src/api.js

// Definiere hier die API-URL. Dies ist der einzige Ort, an dem sie gebraucht wird.
const apiUrl = process.env.REACT_APP_API_URL;

/**
 * Generiert ein Plugin durch einen Aufruf an das Backend.
 * @param {string} description - Die Beschreibung des Plugins.
 * @returns {Promise<Blob>} - Eine Promise, die die ZIP-Datei als Blob zurückgibt.
 */
export async function generatePlugin(description) {

    if (!apiUrl) {
        throw new Error("API URL is not configured. Check your .env file.");
    }

    const response = await fetch(`${apiUrl}/generate-plugin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ description: description }),
  });

    // if (!response.ok) {
    //     const error = await response.json();
    //     throw new Error(error.detail || 'Failed to generate plugin');
    // }

    if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'An unknown error occurred');
  }

    return response.blob();
}