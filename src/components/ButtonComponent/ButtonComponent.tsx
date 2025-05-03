// components/ButtonComponent.tsx
import React from 'react';
import {Button, ButtonProps} from 'react-native-paper';

interface ButtonComponentProps extends ButtonProps {
  children: React.ReactNode;
  className?: string;
}

const ButtonComponent: React.FC<ButtonComponentProps> = ({
  children,
  className,
  mode = 'contained',
  ...props
}) => {
  return (
    <Button
      {...props}
      className={className}
      labelStyle={{fontFamily: 'Nunito', textTransform: 'uppercase'}}
      mode={mode}>
      {children}
    </Button>
  );
};

export default ButtonComponent;
