import { Text } from '@/components/ui/text';
import { View } from 'react-native';
import { useHealth } from '@/hooks/useHealthCheck';
import { useTodayBriefing } from '@/hooks/useTodayBriefing';
import { typography } from '@/theme/typography';
import { Link } from 'expo-router';
import { Screen } from '@/components/ui/screen';
import { DailyBriefingHeader } from '@/components/ui/daily-briefing-header';

// Temporary — Milestone 27 verification only. Remove once real screens apply these tokens.
function TypographyDebug() {
  return (
    <View>
      <Text style={typography.displayLg}>displayLg (Libre Caslon 700)</Text>
      <Text style={typography.displayLgMobile}>displayLgMobile</Text>
      <Text style={typography.headlineMd}>headlineMd</Text>
      <Text style={typography.headlineSm}>headlineSm</Text>
      <Text style={typography.bodyLg}>bodyLg (Inter 400)</Text>
      <Text style={typography.bodyMd}>bodyMd</Text>
      <Text style={typography.caption}>caption (Inter 500)</Text>
      <Text style={typography.dataLabel}>dataLabel (JetBrains Mono 500)</Text>
    </View>
  );
}

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
      <Text>Indicators: {data.indicators.length}</Text>
      {data.indicators.slice(0, 3).map((indicator) => (
        <Text key={indicator.item_key}>
          {indicator.label}: {indicator.points.at(-1)?.value}
        </Text>
      ))}
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
    <Screen>
      <DailyBriefingHeader />
      <HealthProfile />
      <BriefingDebug />
      <TypographyDebug />
    </Screen>
  );
}
