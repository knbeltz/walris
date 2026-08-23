import { View } from 'react-native';

import { Text } from '@/components/ui/text';
import { typography } from '@/theme/typography';

export function DailyBriefingHeader() {
  const now = new Date();
  const hour = now.getHours();

  const greeting =
    hour < 12
      ? 'Good Morning!'
      : hour < 18
        ? 'Good Afternoon!'
        : 'Good Evening!';

  const formattedDate = new Intl.DateTimeFormat(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  }).format(now);

  return (
    <View>
      <Text style={typography.headlineMd}>Walris</Text>

      <Text style={typography.headlineSm}>{greeting}</Text>

      <Text>{formattedDate}</Text>
    </View>
  );
}
