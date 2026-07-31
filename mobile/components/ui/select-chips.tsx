import { Pressable, View } from 'react-native';

import { Text } from '@/components/ui/text';

type TopicOption = {
  value: string;
  label: string;
};

type TopicChipsProps = {
  options: TopicOption[];
  values: string[];
  onValuesChange: (values: string[]) => void;
};

// const options = [
//     {value: 'inflation', label: 'Inflation'},
//     {value: 'employment_labor', label: 'Employment and Labor'},
//     {value: 'economic_growth', label: 'Economic Growth'},
//     {value: 'housing', label: 'Housing'},
//     {value: 'consumer_cost', label: 'Consumer Costs'},
//     {value: 'major_market_indicies', label: 'Major Market Indicies'},
//     {value: 'industry_sector_performance', label: 'Industry Sector Performance'},
//     {value: 'company_spotlights', label: 'Company Spotlights'}
// ]

export function TopicChips({
  options,
  values,
  onValuesChange,
}: TopicChipsProps) {
  const handleTopicPress = (topicValue: string) => {
    const isSelected = values.includes(topicValue);

    const updatedValues = isSelected
      ? values.filter((value) => value !== topicValue)
      : [...values, topicValue];

    onValuesChange(updatedValues);
  };

  return (
  <View className="flex-row flex-wrap gap-2">
    {options.map((option) => {
      const isSelected = values.includes(option.value);

      return (
        <Pressable
          key={option.value}
          onPress={() => handleTopicPress(option.value)}
          accessibilityRole="checkbox"
          accessibilityLabel={option.label}
          accessibilityState={{ checked: isSelected }}
          style={{
            borderRadius: 999,
            borderWidth: 1,
            paddingHorizontal: 16,
            paddingVertical: 10,
            backgroundColor: isSelected ? 'black' : 'white',
            borderColor: isSelected ? 'black' : '#d1d5db',
          }}
        >
          <Text
            style={{
              color: isSelected ? 'white' : 'black',
            }}
          >
            {option.label}
          </Text>
        </Pressable>
      );
    })}
  </View>
);
}
