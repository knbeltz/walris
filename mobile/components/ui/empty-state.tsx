import { View } from 'react-native';
import { Text } from '@/components/ui/text';
import { typography } from '@/theme/typography';

type EmptyStateProps = {
  title: string;
  description?: string;
};

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <View>
      <Text style={typography.bodyLg}>{title}</Text>

      {description ? (
        <Text style={typography.bodyMd}>{description}</Text>
      ) : null}
    </View>
  );
}
