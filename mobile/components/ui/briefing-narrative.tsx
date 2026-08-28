import { View } from 'react-native';

import { Text } from '@/components/ui/text';
import { typography } from '@/theme/typography';

import type { BriefingContent } from '@/schemas/briefings';

type BriefingNarrativeProps = {
  content: BriefingContent;
};

export function BriefingNarrative({ content }: BriefingNarrativeProps) {
  return (
    <View className="gap-lg">
      <Text style={typography.headlineMd}>{content.headline}</Text>

      <View className="gap-md">
        {content.sections.map((section, index) => (
          <View key={`${section.heading}-${index}`} className="gap-xs">
            <Text style={typography.headlineSm}>{section.heading}</Text>

            <Text style={typography.bodyMd}>{section.body}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}
