import { Linking, Pressable, View } from 'react-native';
import { Text } from '@/components/ui/text';
import { typography } from '@/theme/typography';

import type { NewsItem } from '@/schemas/briefings';

type NewsCardProps = {
  news: NewsItem;
};

export function NewsCard({ news }: NewsCardProps) {
  const handlePress = async () => {
    await Linking.openURL(news.url);
  };

  const formattedPublishedAt = new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(news.published_at));

  return (
    <Pressable
      onPress={handlePress}
      className="rounded-md border border-border p-4"
    >
      <View className="gap-3">
        <View className="gap-2">
          <Text style={typography.headlineSm}>{news.headline}</Text>

          <Text style={typography.bodyMd}>{news.summary}</Text>
        </View>

        <View className="flex-row items-center gap-2">
          <Text style={typography.dataLabel}>{news.source}</Text>

          <Text style={typography.dataLabel}>•</Text>

          <Text style={typography.dataLabel}>{formattedPublishedAt}</Text>
        </View>
      </View>
    </Pressable>
  );
}
