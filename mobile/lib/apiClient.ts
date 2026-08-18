export class ApiError extends Error {
  status: number | null;

  constructor(status: number | null, message: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

const apiBaseUrl = process.env.EXPO_PUBLIC_API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error('EXPO_PUBLIC_API_BASE_URL is not configured.');
}

export const API_BASE_URL = apiBaseUrl;

export async function apiFetch(
  path: string,
  getToken?: () => Promise<string | null>,
  options?: RequestInit,
) {
  let token: string | null = null;

  if (getToken) {
    token = await getToken();

    if (!token) {
      throw new ApiError(401, 'You must be signed in.');
    }
  }

  const controller = new AbortController();

  const timeoutId = setTimeout(() => {
    controller.abort();
  }, 10_000);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,

      headers: {
        ...options?.headers,

        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },

      signal: controller.signal,
    });

    if (!response.ok) {
      const body = await response.json().catch(() => null);

      throw new ApiError(
        response.status,
        body?.detail ?? 'API request failed.',
      );
    }

    return response;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError(null, 'The request timed out. Please try again.');
    }

    throw new ApiError(
      null,
      'Unable to connect to the server. Please try again.',
    );
  } finally {
    clearTimeout(timeoutId);
  }
}
