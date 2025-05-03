import {View} from 'react-native';
import React from 'react';
import LoaderKit from 'react-native-loader-kit'
import { useTheme } from 'react-native-paper';

const LoadingComponent = () => {
    const theme = useTheme()

  return (
    <View className="w-full h-full items-center justify-center">
      <LoaderKit
        style={{width: 50, height: 50}}
        name={'BallSpinFadeLoader'} // Optional: see list of animations below
        color={theme.colors.primary} // Optional: color can be: 'red', 'green',... or '#ddd', '#ffffff',...
      />
    </View>
  );
};

export default LoadingComponent;
