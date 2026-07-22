import { Text } from '@/components/ui/text';
import { View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useHealth } from '@/hooks/useHealthCheck';
import { Link } from 'expo-router';

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
    </SafeAreaView>
  );
}
