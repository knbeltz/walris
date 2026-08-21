import { Text } from '@/components/ui/text';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useHealth } from '@/hooks/useHealthCheck';
import { useTodayBriefing } from '@/hooks/useTodayBriefing';
import { Link } from 'expo-router';

// Temporary — Milestone 26 verification only. Remove once Milestone 32 builds the real Home Screen.
function BriefingDebug() {
  const { data, isPending, isError, error } = useTodayBriefing();

  if (isPending) {
    return <Text>Briefing: loading...</Text>;
  }

  if (isError) {
    return <Text>Briefing error: {error.message}</Text>;
  }

  return (
    <View>
      <Text>Briefing date: {data.date}</Text>
      <Text>Headline: {data.content.headline}</Text>
      <Text>Sections: {data.content.sections.length}</Text>
    </View>
  );
}

function HealthProfile() {
  const { data, isPending, isError, error } = useHealth();

  if (isPending) {
    return <Text>Loading...</Text>;
  }

  if (isError) {
    return <Text>{error.message}</Text>;
  }

  return (
    <>
      <View>
        <Text>{data?.status}</Text>
        <Text>Backend Connected</Text>
      </View>

      <Link href="/sign-in">
        <Text>Go to Sign In</Text>
      </Link>

      <Link href="/sign-up">
        <Text>Go to Sign Up</Text>
      </Link>
    </>
  );
}

export default function Home() {
  return (
    <SafeAreaView>
      <HealthProfile />
      <BriefingDebug />
    </SafeAreaView>
  );
}
