import { Text } from '@/components/ui/text';
import { Pressable, RefreshControl, View } from 'react-native';
import { useTodayBriefing } from '@/hooks/useTodayBriefing';
import { Link } from 'expo-router';
import { Screen } from '@/components/ui/screen';
import { DailyBriefingHeader } from '@/components/ui/daily-briefing-header';
import { NewsCard } from '@/components/ui/news-card';
import { BriefingNarrative } from '@/components/ui/briefing-narrative';
import { useAuth } from '@clerk/expo';

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
  const { data, isPending, isError, error } = useTodayBriefing();

  if (isPending) {
    return <Text>Loading...</Text>;
  }

  if (isError) {
    return <Text>{error.message}</Text>;
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
