import { Pressable, View } from 'react-native';

import { Card, CardTitle, CardDescription } from '@/components/ui/card';
import { cn } from '@/lib/utils';

type SelectCardOption = {
    value: string;
    label: string;
    description: string;
};

type SelectCardProps = {
    options: SelectCardOption[];
    value: string | null;
    onValueChange: (value: string) => void;
};

function SelectCard({ options, value, onValueChange }: SelectCardProps) {
  return (
    <View role="radiogroup">
      {options.map((option) => {
        const isSelected = option.value === value;

        return (
          <Pressable
            key={option.value}
            role="radio"
            aria-checked={isSelected}
            onPress={() => onValueChange(option.value)}
          >
            <Card
              className={cn(isSelected && 'border-primary bg-accent')}
            >
              <CardTitle>{option.label}</CardTitle>
              <CardDescription>{option.description}</CardDescription>
            </Card>
          </Pressable>
        );
      })}
    </View>
  );
}

export { SelectCard };
export type { SelectCardProps, SelectCardOption };