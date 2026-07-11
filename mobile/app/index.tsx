import { Text } from '@/components/ui/text';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useHealth } from '@/hooks/useHealthCheck';

function HealthProfile() {
  const { data, isPending, isError, error } = useHealth();

  if (isPending) {
    return <Text>Loading...</Text>;
  }

  if (isError) {
    return <Text>{error.message}</Text>;
  }

  return (
    <View>
      <Text>{data?.status}</Text>
      <Text>Backend Connected</Text>
    </View>
  );
}

export default function Home() {
  return (
    <SafeAreaView>
      <HealthProfile />
    </SafeAreaView>
  );
}
