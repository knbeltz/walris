import { useEffect, useRef, useState } from 'react';
import { ScrollView } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuth } from '@clerk/expo';

import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';
import { TopicChips } from '@/components/ui/select-chips';
import { getErrorMessage } from '@/lib/utils';
import { apiFetch } from '@/lib/apiClient';
import { UserPreferencesSchema } from '@/schemas/preferences';

type UserPreferences = {
  category: string | null;
  additional_topics: string[];
};

const topics = [
  { value: 'inflation', label: 'Inflation' },
  { value: 'employment_labor', label: 'Employment and Labor' },
  { value: 'economic_growth', label: 'Economic Growth' },
  { value: 'housing', label: 'Housing' },
  {
    value: 'interest_rates_monetary_policy',
    label: 'Interest Rates & Monetary Policy',
  },
  { value: 'consumer_cost', label: 'Consumer Costs' },
  { value: 'major_market_indicies', label: 'Major Market Indicies' },
  {
    value: 'industry_sector_performance',
    label: 'Industry Sector Performance',
  },
  { value: 'company_spotlights', label: 'Company Spotlights' },
];

export default function TopicsScreen() {
  const { getToken, isLoaded, isSignedIn } = useAuth();
  const router = useRouter();
  const hasFetchedPreferences = useRef(false);

  const [savedPreferences, setSavedPreferences] =
    useState<UserPreferences | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Store what fetches returns based on category and selected topics
  const [category, setCategory] = useState<string | null>(null);
  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);

  const [fetchError, setFetchError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoaded || !isSignedIn) {
      return;
    }

    if (hasFetchedPreferences.current) {
      return;
    }

    hasFetchedPreferences.current = true;

    const fetchPreferences = async () => {
      try {
        const response = await apiFetch('/v1/users/me/preferences', getToken, {
          method: 'GET',
        });

        const data: UserPreferences = await response.json();

        UserPreferencesSchema.parse(data);

        

        setCategory(data.category);
        setSelectedTopics(data.additional_topics ?? []);
        setSavedPreferences(data);
      } catch (error: unknown) {
        console.error('Error fetching preferences:', error);
        setFetchError(getErrorMessage(error));
        hasFetchedPreferences.current = false;
      } finally {
        setIsLoading(false);
      }
    };

    void fetchPreferences();
  }, [getToken, isLoaded, isSignedIn]);

  const handleContinue = async () => {
    if (!category) {
      setSubmitError('A category is required before continuing.');
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const response = await apiFetch('/v1/users/me/preferences', getToken, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          category,
          additional_topics: selectedTopics,
        }),
      });
      
      const data: UserPreferences = await response.json();

      UserPreferencesSchema.parse(data);


      setSavedPreferences(data);
      setCategory(data.category);
      setSelectedTopics(data.additional_topics);

      router.replace('/');
    } catch (error: unknown) {
      console.error('Error submitting preferences:', error);
      setSubmitError(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (fetchError) {
    return <Text>{fetchError}</Text>;
  }

  if (savedPreferences === null) {
    return <Text>Preferences could not be loaded.</Text>;
  }

  return (
    <ScrollView>
      <Text>Choose additional topics</Text>

      <TopicChips
        options={topics}
        values={selectedTopics}
        onValuesChange={setSelectedTopics}
      />

      {submitError ? <Text>{submitError}</Text> : null}

      <Button onPress={handleContinue} disabled={isSubmitting}>
        <Text>{isSubmitting ? 'Saving...' : 'Continue'}</Text>
      </Button>
    </ScrollView>
  );
}
