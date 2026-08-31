import { Text } from '@/components/ui/text';
import { Pressable, RefreshControl, View } from 'react-native';
import { useTodayBriefing } from '@/hooks/useTodayBriefing';
import { Link } from 'expo-router';
import { Screen } from '@/components/ui/screen';
import { DailyBriefingHeader } from '@/components/ui/daily-briefing-header';
import { NewsCard } from '@/components/ui/news-card';
import { BriefingNarrative } from '@/components/ui/briefing-narrative';
import { useAuth } from '@clerk/expo';
import { LoadingState } from '@/components/ui/loading-state';
import { ErrorState } from '@/components/ui/error-state';
import { EmptyState } from '@/components/ui/empty-state';

function SignInPrompt() {
  return (
    <View>
      <Link href="/sign-in">
        <Text>Go to Sign In</Text>
      </Link>

      <Link href="/sign-up">
        <Text>Go to Sign Up</Text>
      </Link>
    </View>
  );
}

function SignOut() {
  const { signOut } = useAuth();

  return (
    <Pressable onPress={() => signOut()}>
      <Text>Sign Out</Text>
    </Pressable>
  );
}

function TodayBriefing() {
  const { data, isPending, isError, refetch } = useTodayBriefing();

  if (isPending) {
    return <LoadingState message="Loading your briefing..." />;
  }

  if (isError) {
    return <ErrorState onRetry={refetch} />;
  }

  if (data.content.sections.length === 0) {
    return (
      <EmptyState
        title="Today's briefing is not available yet."
        description="Check back shortly."
      />
    );
  }

  return (
    <View>
      <BriefingNarrative content={data.content} />
      {data.news.map((newsItem) => (
        <NewsCard key={newsItem.url} news={newsItem} />
      ))}
    </View>
  );
}

export default function Home() {
  const { isLoaded, isSignedIn } = useAuth();
  const { refetch, isRefetching } = useTodayBriefing();

  return (
    <Screen
      scroll
      refreshControl={
        <RefreshControl refreshing={isRefetching} onRefresh={refetch} />
      }
    >
      <DailyBriefingHeader />
      {isLoaded && !isSignedIn && <SignInPrompt />}
      {isLoaded && isSignedIn && <TodayBriefing />}
      {isLoaded && isSignedIn && <SignOut />}
    </Screen>
  );
}
