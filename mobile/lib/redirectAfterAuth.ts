import type { Router } from 'expo-router';

export async function redirectAfterAuth(
    getToken: () => Promise<string | null>, 
    router: Router
) {
    try {

        const token = await getToken();

        if (!token) {
            throw new Error('Your session could not be verified');
    }
         const response = await fetch(
        `${process.env.EXPO_PUBLIC_API_BASE_URL}/v1/users/me/preferences`,
        {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${token}`,
            },
        }
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
        router.replace('/category');
        console.error('redirectAfterAuth failed:', error);
    }
}
