// components/TextComponent.tsx
import React from 'react';
import { Text, TextProps } from 'react-native-paper';

interface TextComponentProps extends TextProps<any> {
  children: React.ReactNode;
  className?: string;
}

const TextComponent: React.FC<TextComponentProps> = ({ children, className, ...props }) => {
  return (
    // eslint-disable-next-line react-native/no-inline-styles
    <Text {...props} className={className} >
      {children}
    </Text>
  );
};

export default TextComponent;
