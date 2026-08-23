import type { ReactNode } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ScrollView, View } from 'react-native';

type ScreenProps = {
  children: ReactNode;
  scroll?: boolean;
};

export function Screen({ children, scroll = false }: ScreenProps) {
  return (
    <SafeAreaView className="flex-1">
      {scroll ? (
        <ScrollView className="flex-1">
          <View className="px-md">{children}</View>
        </ScrollView>
      ) : (
        <View className="flex-1 px-md">{children}</View>
      )}
    </SafeAreaView>
  );
}
