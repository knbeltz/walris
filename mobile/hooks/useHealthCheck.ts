import { useQuery } from '@tanstack/react-query';
import { apiFetch, ApiError } from '@/lib/apiClient';


export interface HealthResponse {
  status: string;
}

async function getHealth(): Promise<HealthResponse> {
  const response = await apiFetch('/health');

  const data: HealthResponse = await response.json();

  return data;
}

export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  });
}
