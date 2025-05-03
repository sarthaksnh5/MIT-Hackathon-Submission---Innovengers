import React from 'react';
import { TextInput, TextInputProps } from 'react-native-paper';

type IconConfig = {
  icon: string;
  onPress?: () => void;
};

interface InputComponentProps extends Omit<TextInputProps, 'left' | 'right'> {
  inputClassName?: string;
  left?: IconConfig;
  right?: IconConfig;
}

const InputComponent: React.FC<InputComponentProps> = ({
  inputClassName,
  left,
  right,
  ...rest
}) => {
  const leftIcon =
    left?.icon ? <TextInput.Icon icon={left.icon} onPress={left.onPress} /> : undefined;

  const rightIcon =
    right?.icon ? <TextInput.Icon icon={right.icon} onPress={right.onPress} /> : undefined;

  return (
    <TextInput
      mode="outlined"
      className={inputClassName}
      {...rest}
      left={leftIcon}
      right={rightIcon}
    />
  );
};

export default InputComponent;
