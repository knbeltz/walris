import { View } from 'react-native';
import { Text } from '@/components/ui/text';
import { Button } from '@/components/ui/button';
import { typography } from '@/theme/typography';

type ErrorStateProps = {
  title?: string;
  description?: string;
  onRetry: () => void;
};

export function ErrorState({
  title = "We couldn't load today's briefing.",
  description = 'Please try again.',
  onRetry,
}: ErrorStateProps) {
  return (
    <View>
      <Text style={typography.bodyLg}>{title}</Text>
      <Text style={typography.bodyMd}>{description}</Text>

      <Button onPress={onRetry}>
        <Text>Try Again</Text>
      </Button>
    </View>
  );
}
