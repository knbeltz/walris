import { useQuery } from '@tanstack/react-query';
import { useAuth } from '@clerk/expo';

import { apiFetch } from '@/lib/apiClient';
import { UserBriefingResponseSchema } from '@/schemas/briefings';

export function useTodayBriefing() {
  const { getToken, isLoaded, isSignedIn } = useAuth();

  return useQuery({
    queryKey: ['briefing', 'today'],

    queryFn: async () => {
      const response = await apiFetch('/v1/users/me/briefing', getToken, {
        method: 'GET',
      });

      const data = await response.json();

      return UserBriefingResponseSchema.parse(data);
    },

    enabled: isLoaded && isSignedIn,
  });
}
