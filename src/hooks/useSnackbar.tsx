import { useState, useEffect } from 'react';
import { Snackbar } from 'react-native-paper';
import React from 'react';

type SnackbarColor = 'gray' | 'green' | 'red';

let externalSetState: ((msg: string, color: SnackbarColor) => void) | null = null;

export function useSnackbar() {
  const [visible, setVisible] = useState(false);
  const [message, setMessage] = useState('');
  const [color, setColor] = useState<SnackbarColor>('gray');

  const showSnackbar = (msg: string, color: SnackbarColor = 'gray') => {
    setMessage(msg);
    setColor(color);
    setVisible(true);
  };

  useEffect(() => {
    // Only set once
    if (!externalSetState) {
      externalSetState = showSnackbar;
    }
  }, []);

  const SnackbarComponent: React.FC = () => (
    <Snackbar
      visible={visible}
      onDismiss={() => setVisible(false)}
      duration={3000}
      style={{ backgroundColor: color }}
    >
      {message}
    </Snackbar>
  );

  return {
    showSnackbar,
    SnackbarComponent,
  };
}

export const showGlobalSnackbar = (msg: string, color: SnackbarColor) => {  
  if (externalSetState) {
    externalSetState(msg, color);
  } else {
    console.warn('Snackbar not initialized!');
  }
};
