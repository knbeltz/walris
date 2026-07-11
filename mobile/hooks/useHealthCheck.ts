// Milestone 10 — TanStack Query hook for GET /health. Pseudocode/implementation: TBD.

/*
# TanStack Query GET Hook Reference (TypeScript)

This guide demonstrates the standard pattern for wrapping a GET request in a reusable TanStack Query hook.

---

# 1. Define the Response Type

```ts
export interface User {
  id: string;
  name: string;
  email: string;
}
```

The interface describes the data you expect from your API.

---

# 2. Create the API Request Function

```ts
async function getUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`);
  }

  const data: User = await response.json();

  return data;
}
```

### Responsibilities

- Makes the HTTP request
- Checks for errors
- Throws an Error if the request fails
- Returns typed data

TanStack Query uses:

- the returned value as cached data
- thrown errors for the `isError` state

---

# 3. Create the Custom Hook

```ts
import { useQuery } from "@tanstack/react-query";

export function useUser(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUser(userId),
    enabled: Boolean(userId),
  });
}
```

This hook wraps all of the query logic into one reusable function.

---

# Understanding Each Property

## queryKey

```ts
queryKey: ["user", userId]
```

The query key uniquely identifies cached data.

Example:

```ts
["user", "123"]
```

and

```ts
["user", "456"]
```

are stored separately in the cache.

Changing any part of the query key tells TanStack Query to fetch different data.

### Rule of Thumb

Everything that changes the returned data should be included in the query key.

Examples:

```ts
["users"]

["user", userId]

["posts", page]

["search", searchTerm]

["weather", city]
```

---

## queryFn

```ts
queryFn: () => getUser(userId)
```

This function tells TanStack Query **how** to fetch the data.

Notice the arrow function.

✅ Correct

```ts
queryFn: () => getUser(userId)
```

❌ Incorrect

```ts
queryFn: getUser(userId)
```

The incorrect version immediately calls the function while React is rendering.

TanStack Query expects a function that it can call itself.

---

## enabled

```ts
enabled: Boolean(userId)
```

Sometimes you don't want a request to run immediately.

For example:

```ts
const userId = "";
```

Without `enabled`, TanStack Query would request

```
/api/users/
```

which is probably invalid.

Using

```ts
enabled: Boolean(userId)
```

waits until a valid userId exists.

---

# 4. Using the Hook

```tsx
interface UserProfileProps {
  userId: string;
}

export function UserProfile({ userId }: UserProfileProps) {
  const {
    data: user,
    isPending,
    isError,
    error,
  } = useUser(userId);

  if (isPending) {
    return <p>Loading...</p>;
  }

  if (isError) {
    return <p>{error.message}</p>;
  }

  return (
    <section>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </section>
  );
}
```

---

# Returned Values

The object returned from `useQuery` contains many useful properties.

```ts
const query = useUser(userId);
```

Common ones include:

```ts
query.data

query.error

query.isPending

query.isError

query.isSuccess

query.refetch
```

Most developers destructure the values they need:

```ts
const {
  data,
  isPending,
  isError,
  error,
} = useUser(userId);
```

---

# Typical Folder Structure

```
src/
    features/
        users/
            api/
                get-user.ts

            hooks/
                use-user.ts

            types/
                user.ts
```

---

## user.ts

```ts
export interface User {
  id: string;
  name: string;
  email: string;
}
```

---

## get-user.ts

```ts
import type { User } from "../types/user";

export async function getUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch user");
  }

  return response.json() as Promise<User>;
}
```

---

## use-user.ts

```ts
import { useQuery } from "@tanstack/react-query";
import { getUser } from "../api/get-user";

export function useUser(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => getUser(userId),
    enabled: Boolean(userId),
  });
}
```

---

# Complete Flow

```
Component
    │
    ▼
Custom Hook
    │
    ▼
useQuery()
    │
    ▼
API Function
    │
    ▼
HTTP GET Request
    │
    ▼
JSON Response
    │
    ▼
Typed Data
    │
    ▼
React Component
```

---

# Mental Model

Think of TanStack Query as answering four questions.

### What data am I requesting?

```ts
queryKey: ["user", userId]
```

---

### How do I fetch it?

```ts
queryFn: () => getUser(userId)
```

---

### When should I fetch it?

```ts
enabled: Boolean(userId)
```

---

### How do I use the result?

```ts
const {
    data,
    isPending,
    isError,
    error,
} = useUser(userId);
```

---

# General Template

```ts
async function getSomething(id: string): Promise<ResponseType> {
    const response = await fetch(`/api/...`);

    if (!response.ok) {
        throw new Error("Request failed");
    }

    return response.json() as Promise<ResponseType>;
}

export function useSomething(id: string) {
    return useQuery({
        queryKey: ["something", id],
        queryFn: () => getSomething(id),
        enabled: Boolean(id),
    });
}
```

Whenever you're creating a new GET hook, you'll typically only change:

- The response type
- The API endpoint
- The query key
- The function names

Everything else remains nearly identical.
*/

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

*/