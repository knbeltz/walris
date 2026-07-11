// Milestone 10 — TanStack Query hook for GET /health. Pseudocode/implementation: TBD.

/*

Pseudocode

1. Define the Response Type 

export interface HealthResponse {
    status: string
}

2. Create the API request function 

async function getHealth(): Promise<HealthResponse> {
    const response = await fetch(`${BASE_URL}/health`);

    if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`)
    }

    const data: HealthResponse = await response.json()

    return data;
}

3. Create the custom hook 

import { useQuery } from "@tanstack/react-query";

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
  });
}


# 4. Using the Hook

```tsx
import { useHealth } from "@/hooks/useHealthCheck";

export function HealthProfile() {
  const {
    data,
    isPending,
    isError,
    error,
  } = useHealth();
  
  if (isPending) {
    return <p>Loading...</p>;
  }
  
  if (isError) {
    return <p>{error.message}</p>;
  }
  
  return (
    <section>
      <h2>{data.status}</h2>
      <p>Backend Connected</p>
    </section>
  )
}
```
*/

import { useQuery } from '@tanstack/react-query';

export interface HealthResponse {
  status: string;
}

async function getHealth(): Promise<HealthResponse> {
  const BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL;
  const response = await fetch(`${BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }

  const data: HealthResponse = await response.json();

  return data;
}

export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: getHealth,
  });
}
