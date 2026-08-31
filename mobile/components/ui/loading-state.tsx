import { ActivityIndicator, View } from 'react-native';
import { Text } from '@/components/ui/text';
import { typography } from '@/theme/typography';

type LoadingStateProps = {
  message?: string;
};

export function LoadingState({ message }: LoadingStateProps) {
  return (
    <View>
      <ActivityIndicator />

      {message ? <Text style={typography.bodyMd}>{message}</Text> : null}
    </View>
  );
}
