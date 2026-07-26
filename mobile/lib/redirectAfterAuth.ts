import type { Router } from 'expo-router';

async function redirectAfterAuth(
    getToken: () => Promise<string | null>, 
    router: Router
) {
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

    // Need a conditional to determine where to route depending on if categories could be fetched. 

}
