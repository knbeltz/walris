import type { ReactElement, ReactNode } from 'react';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ScrollView, View } from 'react-native';
import type { RefreshControlProps } from 'react-native';

type ScreenProps = {
  children: ReactNode;
  scroll?: boolean;
  refreshControl?: ReactElement<RefreshControlProps>;
};

export function Screen({
  children,
  scroll = false,
  refreshControl,
}: ScreenProps) {
  return (
    <SafeAreaView className="flex-1">
      {scroll ? (
        <ScrollView className="flex-1" refreshControl={refreshControl}>
          <View className="px-md">{children}</View>
        </ScrollView>
      ) : (
        <View className="flex-1 px-md">{children}</View>
      )}
    </SafeAreaView>
  );
}
