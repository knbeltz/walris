import type { ImperativeRouter } from 'expo-router';

export async function redirectAfterAuth(
  getToken: () => Promise<string | null>,
  router: ImperativeRouter,
) {
  try {
    let token: string | null = null;

    for (let attempt = 0; attempt < 5; attempt++) {
      token = await getToken();

      if (token) {
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, 400));
    }

    if (!token) {
      throw new Error('Your session could not be verified.');
    }
    const response = await fetch(
      `${process.env.EXPO_PUBLIC_API_BASE_URL}/v1/users/me/preferences`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const UserPreferences = await response.json();

    if (UserPreferences.category === null) {
      router.replace('/category');
    } else {
      router.replace('/');
    }
  } catch (error) {
    // We couldn't confirm whether the user has a category set (token race,
    // network error, bad response, etc.) — that's NOT the same as confirming
    // they have none. Falling back to '/category' here would wrongly force
    // real, already-onboarded users back through onboarding on any transient
    // failure. Send them to '/' instead, which has its own real loading/error
    // state and won't touch or reset anything.
    router.replace('/');
    console.error('redirectAfterAuth failed:', error);
  }
}
