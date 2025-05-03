import React from 'react';

import {PaperProvider} from 'react-native-paper';
import RootStack from './src/navigation/RooStack';
import {useSnackbar} from './src/hooks/useSnackbar';

import './global.css';

import MaterialCommunityIcons from 'react-native-vector-icons/MaterialCommunityIcons';

const theme = {
  colors: {
    primary: 'rgb(0, 107, 95)',
    onPrimary: 'rgb(255, 255, 255)',
    primaryContainer: 'rgb(113, 248, 228)',
    onPrimaryContainer: 'rgb(0, 32, 28)',
    secondary: 'rgb(0, 95, 175)',
    onSecondary: 'rgb(255, 255, 255)',
    secondaryContainer: 'rgb(212, 227, 255)',
    onSecondaryContainer: 'rgb(0, 28, 58)',
    tertiary: 'rgb(69, 97, 121)',
    onTertiary: 'rgb(255, 255, 255)',
    tertiaryContainer: 'rgb(203, 230, 255)',
    onTertiaryContainer: 'rgb(0, 30, 49)',
    error: 'rgb(186, 26, 26)',
    onError: 'rgb(255, 255, 255)',
    errorContainer: 'rgb(255, 218, 214)',
    onErrorContainer: 'rgb(65, 0, 2)',
    background: 'rgb(250, 253, 251)',
    onBackground: 'rgb(25, 28, 27)',
    surface: 'rgb(250, 253, 251)',
    onSurface: 'rgb(25, 28, 27)',
    surfaceVariant: 'rgb(218, 229, 225)',
    onSurfaceVariant: 'rgb(63, 73, 70)',
    outline: 'rgb(111, 121, 118)',
    outlineVariant: 'rgb(190, 201, 197)',
    shadow: 'rgb(0, 0, 0)',
    scrim: 'rgb(0, 0, 0)',
    inverseSurface: 'rgb(45, 49, 48)',
    inverseOnSurface: 'rgb(239, 241, 239)',
    inversePrimary: 'rgb(79, 219, 200)',
    elevation: {
      level0: 'transparent',
      level1: 'rgb(238, 246, 243)',
      level2: 'rgb(230, 241, 239)',
      level3: 'rgb(223, 237, 234)',
      level4: 'rgb(220, 236, 232)',
      level5: 'rgb(215, 233, 229)',
    },
    surfaceDisabled: 'rgba(25, 28, 27, 0.12)',
    onSurfaceDisabled: 'rgba(25, 28, 27, 0.38)',
    backdrop: 'rgba(41, 50, 48, 0.4)',
  },
};

const App = () => {
  const {SnackbarComponent} = useSnackbar();

  return (
    <PaperProvider
      theme={theme}
      settings={{
        icon: props => <MaterialCommunityIcons {...props} />,
      }}>
      <RootStack />
      <SnackbarComponent />
    </PaperProvider>
  );
};

export default App;
