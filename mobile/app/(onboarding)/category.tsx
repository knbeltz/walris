import { useState } from 'react';
import { ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@clerk/expo';

import { SelectCard } from '@/components/ui/select-card';
import type { SelectCardOption } from '@/components/ui/select-card';
import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';

const categories: SelectCardOption[] = [
  {
    value: 'investor',
    label: 'Investor',
    description: "Get a daily read on where the economy is headed and what it means for markets and your portfolio. Includes index performance, sector movers, and the data behind them.",
  },

  {
    value: 'small_business_owner',
    label: 'Small Business Owners / Entrepreneur',
    description: "Track the conditions that affect your business: costs, consumer demand, hiring, and financing to know what's getting easier or harder.",
  },

  {
    value: 'consumer',
    label: 'Consumer',
    description: "Understand what's happening to your cost of living, income, and purchasing power, in plain terms.",
  },

  {
    value: 'student',
    label: 'Student',
    description: 'See what the economy means for your living costs, student loans, and job prospects after graduation.',
  },

  {
    value: 'home',
    label: 'Home Owner / Home Buyer',
    description: 'Stay on top of mortgage rates, home prices, and housing supply to know whether now favors buying, selling, or waiting.',
  },

  {
    value: 'job_seeker',
    label: 'Job Seeker',
    description: 'Know whether hiring is heating up or cooling down, where opportunities are emerging, and how much leverage workers have right now',
  },

  {
    value: 'everything',
    label: '"I want everything"',
    description: 'Get the full picture — inflation, jobs, housing, business activity, interest rates, and markets, all in one daily briefing.',
  },

];

export default function CategorySelectionScreen() {
    // Store the value of the category currently selected by the user.

    const { getToken } = useAuth();

    const router = useRouter();

    // The initial value is null because no category has been selected yet/
    const [selectedCategory, setSelectedCategory] =
        useState<string | null>(null);

    const [errorMessage, setErrorMessage] = useState('');

    const handleContinue = async () => {
        // Clear an error left over from a previous attempt. 
        setErrorMessage('');
        
        if (!selectedCategory) {
            setErrorMessage('Please select a category.');
            return;
        }

        if (!process.env.EXPO_PUBLIC_API_BASE_URL) {
            setErrorMessage('The API URL is not configured.')
        }

        try {
            // Request the JWT for the currently active Clerk session.
            const token = await getToken();

            if (!token) {
                throw new Error('You must be signed in to continue.')
            }

        const response = await fetch(
            `${process.env.EXPO_PUBLIC_API_BASE_URL}/v1/users/me/preferences`,
            {
                method: 'Put',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: selectedCategory,
                    additional_topics: []
                }),
            },
        );

        
        if (!response.ok) {
            const errorBody = await response.json().catch(() => null);

            throw new Error(
                errorBody?.detail ?? 'Failed to save your preferences.',
            );
        }

        router.push('/topics');
    }   catch (error: unknown) {
        console.error('Preference submission failed:', error);

        if (error instanceof Error) {
            setErrorMessage(error.message);
        } else {
            setErrorMessage('An unexpected error occured.');
        }
        }
    }

    return(
        <ScrollView>
            <SelectCard
                // The full list of categories the user can choose from.
                options={categories}

                // The category that is currently selected.
                // SelectCard uses this value to determine which card should appear selected.
                value={selectedCategory}

                // SelectCard calls this function whenever the user presses one of the category cards.

                // The selected option's value becomes the new state value.
                onValueChange={setSelectedCategory}
            />

            {errorMessage ? <Text>{errorMessage}</Text> : null}

            <Button
                onPress={handleContinue}
                disabled={!selectedCategory}
            >
                <Text>Continue</Text>
            </Button>
        </ScrollView>
    );
}