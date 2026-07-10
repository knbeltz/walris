import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function Home() {
  return (
    <SafeAreaView className="flex-1 items-center justify-center gap-4 bg-background">
      <Text variant="h1">Walris</Text>
      <Text variant="muted">
        Today&apos;s economic briefing, in under five minutes.
      </Text>
      <Button>
        <Text>Get started</Text>
      </Button>
    </SafeAreaView>
  );
}
