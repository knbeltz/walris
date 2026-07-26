import { Pressable, View } from 'react-native';

import { Badge } from '@/components/ui/badge';
import { Text } from '@/components/ui/text';
import { cn } from '@/lib/utils';

type TopicOption = {
    value: string;
    label: string;
}

type TopicChipsProps = {
    options: TopicOption[];
    values: string[];
    onValuesChange: (values: string[]) => void;
}

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
        
        onValuesChange(updatedValues)
    }

    return (
        <View className="flex-row flex-wrap gap-2">
            {options.map((option) => {
                const isSelected = values.includes(option.value);

                return (
                    <Pressable
                        key={option.value}
                        role="checkbox"
                        aria-checked={isSelected}
                        onPress={() => handleTopicPress(option.value)}
                    >
                        <Badge
                            variant={isSelected ? 'default' : 'outline'}
                            className={cn(
                                'px-4 py-2',
                                isSelected && 'bg-primary'
                            )}
                        >
                            <Text>{option.label}</Text>
                        </Badge>
                    </Pressable>
                );
            })}
        </View>
    )
}